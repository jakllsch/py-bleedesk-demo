#!/usr/bin/env python3
import pygatt
import struct
import sys
import getopt

"""
for BLE dongle compatible with Jiecang JCP35N-BLT
"""

def data_handler_cb(handle, value):
    """
        Indication and notification come asynchronously, we use this function to
        handle them either one at the time as they come.
    :param handle:
    :param value:
    :return:
    """
    print("Handle: {}".format(handle))
    print("Data: {}".format(value.hex()))

    # Sometimes we get values of 33 bytes, but the gatttool backend splits them
    # into 16 byte max chunks?  The deskStatus() response in particular which
    # has 5 records, and I really only want to see the last 9 byte record of it.

    if len(value) is 9:
        height = struct.unpack('>h', value[4:6])[0]
        print("Height: {}".format(height))


def deskUp(device):
    device.char_write('0000ff01-0000-1000-8000-00805f9b34fb', bytearray([0xf1, 0xf1, 0x01, 0x00, 0x01, 0x7e]), wait_for_response=False)

def deskDown(device):
    device.char_write('0000ff01-0000-1000-8000-00805f9b34fb', bytearray([0xf1, 0xf1, 0x02, 0x00, 0x02, 0x7e]), wait_for_response=False)

def deskStop(device):
    device.char_write('0000ff01-0000-1000-8000-00805f9b34fb', bytearray([0xf1, 0xf1, 0x2b, 0x00, 0x2b, 0x7e]), wait_for_response=False)

def memorySave1(device):
    device.char_write('0000ff01-0000-1000-8000-00805f9b34fb', bytearray([0xf1, 0xf1, 0x03, 0x00, 0x03, 0x7e]), wait_for_response=False)

def memorySave2(device):
    device.char_write('0000ff01-0000-1000-8000-00805f9b34fb', bytearray([0xf1, 0xf1, 0x04, 0x00, 0x04, 0x7e]), wait_for_response=False)

def memoryRecall1(device):
    device.char_write('0000ff01-0000-1000-8000-00805f9b34fb', bytearray([0xf1, 0xf1, 0x05, 0x00, 0x05, 0x7e]), wait_for_response=False)

def memoryRecall2(device):
    device.char_write('0000ff01-0000-1000-8000-00805f9b34fb', bytearray([0xf1, 0xf1, 0x06, 0x00, 0x06, 0x7e]), wait_for_response=False)

def deskStatus(device):
    device.char_write('0000ff01-0000-1000-8000-00805f9b34fb', bytearray([0xf1, 0xf1, 0x07, 0x00, 0x07, 0x7e]), wait_for_response=False)

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "a:", ["address="])
        except (getopt.error, msg):
            raise Usage(msg)
        for o, a in opts:
            if o in ("-a", "--address"):
                address = a
            else:
                assert False, "unhandled option"
    except (Usage, err):
            return 2
    adapter = pygatt.GATTToolBackend(search_window_size=2048)
    try:
        adapter.start(reset_on_start=False)
        device = adapter.connect(address)
        device.bond()
        #print(device.discover_characteristics())
        device.subscribe('0000ff02-0000-1000-8000-00805f9b34fb', callback=data_handler_cb, indication=True, wait_for_response=False)
        deskStatus(device)
        deskStatus(device)
        input("Press enter to stop program...\n")
    finally:
        adapter.stop()
    print("Data: {}".format(height))
    return 0

if __name__ == '__main__':
    exit(main())
