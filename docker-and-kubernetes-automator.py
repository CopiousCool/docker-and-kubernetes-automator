import docker
from kubernetes import client, config

# Docker client setup
docker_client = docker.from_env()

# Kubernetes client setup
config.load_kube_config()
kubernetes_client = client.CoreV1Api()

# List all running Docker containers
def list_containers():
    containers = docker_client.containers.list()
    for container in containers:
        print(container.name)

# List all Docker images
def list_images():
    images = docker_client.images.list()
    for image in images:
        print(image.tags)

# Check the health and uptime of a Docker container
def container_health(container_name):
    container = docker_client.containers.get(container_name)
    health = container.attrs['State']['Health']
    uptime = container.attrs['State']['StartedAt']
    print(f"{container_name} is {health['Status']}, uptime: {uptime}")

# Check if any Docker images are out of date
def check_outdated_images():
    images = docker_client.images.list()
    for image in images:
        if len(image.history()) > 1:
            latest_id = image.history()[0]['Id']
            older_id = image.history()[1]['Id']
            if latest_id != older_id:
                print(f"{image.tags[0]} is outdated")

# List all Kubernetes pods in the default namespace
def list_pods():
    pods = kubernetes_client.list_namespaced_pod(namespace="default")
    for pod in pods.items:
        print(pod.metadata.name)

# List all Kubernetes deployments in the default namespace
def list_deployments():
    deployments = kubernetes_client.list_namespaced_deployment(namespace="default")
    for deployment in deployments.items:
        print(deployment.metadata.name)

# Create a Kubernetes deployment
def create_deployment(deployment_name, container_image):
    deployment_manifest = {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {
            "name": deployment_name,
        },
        "spec": {
            "replicas": 1,
            "selector": {
                "matchLabels": {
                    "app": deployment_name,
                }
            },
            "template": {
                "metadata": {
                    "labels": {
                        "app": deployment_name,
                    }
                },
                "spec": {
                    "containers": [
                        {
                            "name": deployment_name,
                            "image": container_image,
                            "ports": [
                                {
                                    "containerPort": 80,
                                }
                            ],
                        }
                    ],
                }
            }
        }
    }
    kubernetes_client.create_namespaced_deployment(namespace="default", body=deployment_manifest)

# Delete a Kubernetes deployment
def delete_deployment(deployment_name):
    kubernetes_client.delete_namespaced_deployment(namespace="default", name=deployment_name)

# Example usage
if __name__ == '__main__':
    list_containers()
    list_images()
    container_health('my_container')
    check_outdated_images()
    list_pods()
    list_deployments()
    create_deployment('my_deployment', 'nginx:latest')
    delete_deployment('my_deployment')
