URLs for Docker Hub images:

1. SA-Frontend: https://hub.docker.com/r/quentincmu/sentiment-analysis-frontend
2. SA-WebApp: https://hub.docker.com/r/quentincmu/sentiment-analysis-webapp
3. SA-Logic: https://hub.docker.com/r/quentincmu/sentiment-analysis-logic

Steps for get the application to work on Google Kubernetes Engine:
1. Create Docker images and push to DockerHub.
2. In Cloud Shell, pull the images.
3. Tag the images with Google proper way
4. Push the images to the Google Container Registry
5. In Kubernetes Engine, deploy sa-frontend, sa-webapp and sa-logic to the cluster.
6. Expose sa-frontend and sa-webapp services to external traffic.
7. Expose sa-logic service to internal traffic.
8. Set up the correct ports in YAML files for sa-frontend, sa-webapp and sa-logic for the proper communication.
