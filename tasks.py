import invoke


@invoke.task
def setup(c):
    c.run("docker run -v $(pwd)/data/grafana:/dir alpine chown 472:472 /dir -R")
    c.run("docker-compose restart")

