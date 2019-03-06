# Oak Lights Controller

Requirements for use:
* `PORT` env var set to port that gRPC server should listen on
* `/dev/ttyACM*` devices that correspond to Oak Lights controllers mounted


## Dev Notes

To run the unit tests, make sure at least one oak-lighting controller
is plugged in and the above udev rule has fired. Then use this
command:

```
docker-compose run server python -m pytest
```
