import sys

for line in sys.stdin:
    line = line.strip()
    temperature = int(line[87:92])
    quality = int(line[92:93])  # The quality flag
    quality_set = {0, 1, 4, 5, 9}  # quality flag allowed for a record
    if ((temperature != 9999) and (quality in quality_set)):
        print('%s\t%d' % (line[15:23], int(line[87:92])))
