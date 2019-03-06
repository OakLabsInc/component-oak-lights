import concurrent.futures
import grpc
import os
import serial
import serial.tools.list_ports
import signal
import time
import webcolors

import oak_lights_pb2
import oak_lights_pb2_grpc

PORT = os.getenv('PORT')


def main():
    signal.signal(signal.SIGTERM, signal_handler)

    address = '0.0.0.0:%s' % PORT
    server = make_server(address)

    try:
        server.start()
        print('oak-lights component serving on %s' % address)
        while True:
            time.sleep(60 * 60 * 24)
    except (KeyboardInterrupt, QuitException):
        server.stop(5).wait()


class QuitException(BaseException):
    pass


def signal_handler(sig_num, frame):
    raise QuitException


def make_server(address):
    controllers = find_oak_lights_devices()
    if not controllers:
        print('WARNING! No Oak Lights controllers found.'
              ' This server must be restarted after any are connected.')
    else:
        print('Found Oak Lights controllers: %s', controllers)

    server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=10))
    oak_lights_pb2_grpc.add_OakLightsServicer_to_server(
        OakLightsServicer(controllers), server)
    server.add_insecure_port(address)
    return server


class OakLightsServicer(oak_lights_pb2_grpc.OakLightsServicer):

    def __init__(self, device_path_by_id):
        super().__init__()
        self.controllers = device_path_by_id

    def Info(self, request, context):
        controllers = [
            {'controller_id': id_} for id_ in self.controllers.keys()
        ]
        return oak_lights_pb2.OakLightsInformation(controllers=controllers)

    def ChangeColor(self, request, context):
        if not request.controller_id:
            raise Exception('controller_id must be specified')
        path = self.controllers.get(request.controller_id)
        if path is None:
            raise Exception('Oak Lights controller with id %r not found'
                            % request.controller_id)
        device = OakLights(path)
        if request.WhichOneof('color') == 'rgb':
            r, g, b = request.rgb.r, request.rgb.g, request.rgb.b
        else:
            r, g, b = webcolors.hex_to_rgb(request.hex)
        device.write(r, g, b, request.white, request.duration)
        # TODO block until complete?
        return oak_lights_pb2.Empty()


class OakLights(object):

    def __init__(self, path):
        self.path = path
        self.device_id = path.rsplit('/')[-1]
        self.device = serial.Serial(port=path, baudrate=115200)

    def write(self, r, g, b, w, d):
        if not all(0 <= x < 256 for x in (r, g, b, w)) or d < 0:
            raise Exception('Invalid parameters for Oak Light device')
        cmd = b'%d,%d,%d,%d,%d\n' % (r, g, b, w, d)
        try:
            self.device.write(cmd)
        except serial.SerialTimeoutException:
            raise Exception('Timed out sending command to device')


def find_oak_lights_devices():
    devices = {}
    for device in serial.tools.list_ports.comports():
        if (device.manufacturer, device.product) == ('OAK', 'LIGHT'):
            devices[device.serial_number] = device.device
    return devices


if __name__ == '__main__':
    main()
