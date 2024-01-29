# DockerCompose DNSRR load-balancing

Testing docker compose [dnsrr](https://docs.docker.com/compose/compose-file/deploy/#endpoint_mode) load balancing with [nginx](https://www.nginx.com/) + [FastAPI](https://fastapi.tiangolo.com/).

## Quickstart
```shell
docker compose up # and victory awaits at http://localhost:8080
```

## Limitations
- Cannot dynamically scale services, as nginx upstreams are configured at startup via a DNS request.
