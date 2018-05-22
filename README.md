# Collect Container Log via API

Sample demo to collect container log via Docker API.
using Python with Docker library, you will need to do `pip install docker-py`

To demonstrate this, you need to have the target IP listening on port 1514
for example you can do `netcat TARGET_IP 1514`

## References:
API ref: https://docs.docker.com/engine/api/v1.37/#operation
1. GET /containers/json, to detect the containers that are running (https://docs.docker.com/engine/api/v1.37/#operation/ContainerList)
2. POST /containers/{id}/attach, to fetch the logs from each container (https://docs.docker.com/engine/api/v1.37/#operation/ContainerAttach)
