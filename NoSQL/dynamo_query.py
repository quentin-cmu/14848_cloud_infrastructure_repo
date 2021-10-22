import boto3

# Create an S3 instance object
s3 = boto3.resource('s3',
                    aws_access_key_id='HiddenId',
                    aws_secret_access_key='HiddenKey'
                    )

# Create a bucket
try:
    s3.create_bucket(Bucket='cloud-infra-cmu', CreateBucketConfiguration={
        'LocationConstraint': 'us-west-2'})
except Exception as e:
    print(e)

# Make the bucket publicly readable
bucket = s3.Bucket("cloud-infra-cmu")
bucket.Acl().put(ACL='public-read')

# upload a new object into the bucket
# body = open('./path-to-a-file/exp1.csv','rb')
#
# o = s3.Object('cloud-infra-cmu', 'test').put(Body=body )
#
# s3.Object('cloud-infra-cmu', 'test').Acl().put(ACL='public-read')

# Create DynamoDB table
dyndb = boto3.resource('dynamodb',
                       region_name='us-west-2',
                       aws_access_key_id='HiddenId',
                       aws_secret_access_key='HiddenKey')

try:
    table = dyndb.create_table(
        TableName='DataTable-cloud-infra-cmu-1',
        KeySchema=[
            {
                'AttributeName': 'PartitionKey',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'RowKey',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'PartitionKey',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'RowKey',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
except Exception as e:
    print(e)
    # if there is an exception, the table may already exist.
    table = dyndb.Table("DataTable-cloud-infra-cmu-1")

# wait for the table to be created
table.meta.client.get_waiter('table_exists').wait(TableName='DataTable-cloud-infra-cmu-1')
print(table.item_count)

# Reading the CSV file, uploading the blobs and creating the table
import csv

with open('./path-to-a-file/experiments.csv', 'r') as csvfile:
    csvf = csv.reader(csvfile, delimiter=',', quotechar='|')
    headers = next(csvf)  # Skip the header in the first line
    for item in csvf:
        print(item)
        body = open('./path-to-a-file/' + item[4], 'rb')
        s3.Object('cloud-infra-cmu', item[4]).put(Body=body)
        md = s3.Object('cloud-infra-cmu', item[4]).Acl().put(ACL='public-read')

        url = " https://s3-us-west-2.amazonaws.com/cloud-infra-cmu/" + item[4]
        metadata_item = {'PartitionKey': item[0], 'RowKey': item[1],
                         'Conductivity': item[2], 'Concentration': item[3], 'url': url}
        try:
            table.put_item(Item=metadata_item)
        except:
            print("item may already be there or another failure")

# Search for an item

# The query used to pull the data from Dynamo DB
try:
    response = table.get_item(
        Key={
            'PartitionKey': '1',
            'RowKey': '-1'
        }
    )
    # print the result of the above query
    item = response['Item']
    print()
    print("The data from DynamoDB is shown below:")
    print(item)

    # The response of the above query
    print()
    print("The response from DynamoDB:")
    print(response)
except Exception as e:
    print()
    print("Couldn't find the item!")
