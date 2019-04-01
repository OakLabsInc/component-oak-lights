# Oak Lights Controller
[![Dockerhub](https://img.shields.io/static/v1.svg?label=Docker%20Hub&message=latest&color=green)](https://hub.docker.com/r/oaklabs/component-oak-lights)

Requirements for use:
* `PORT` env var set to port that gRPC server should listen on, defaults to `9100`
* `/dev/ttyACM*` devices that correspond to Oak Lights controllers mounted


## Dev Notes

To run the unit tests, make sure at least one oak-lighting controller
is plugged in and the above udev rule has fired. Then use this
command:

```
docker-compose run server python -m pytest
```
