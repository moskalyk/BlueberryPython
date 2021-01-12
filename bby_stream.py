# -*- coding: utf-8 -*-
"""
cayden, Blueberry
hbldh <henrik.blidh@gmail.com>, BLEAK
"""

import sys
import logging
import asyncio
import platform
import bitstring
import argparse
import time

from bleak import BleakClient 
from bleak import _logger as logger

#Blueberry glasses GATT server characteristics information
bbxService={"name": 'fnirs service',
            "uuid": '0f0e0d0c-0b0a-0908-0706-050403020100' }
bbxchars={
          "commandCharacteristic": {
              "name": 'write characteristic',
                  "uuid": '1f1e1d1c-1b1a-1918-1716-151413121110',
                  "handles": [None],
                    },
            "shortFnirsCharacteristic": {
                    "name": 'short_path',
                        "uuid": '2f2e2d2c-2b2a-2928-2726-252423222120',
                        "handles": [20, 27],
                          },
            "longFnirsCharacteristic": {
                    "name": 'long_path',
                        "uuid": '3f3e3d3c-3b3a-3938-3736-353433323130',
                        "handles": [23, 31],
                          }

            }
SHORT_PATH_CHAR_UUID = bbxchars["shortFnirsCharacteristic"]["uuid"]
LONG_PATH_CHAR_UUID = bbxchars["longFnirsCharacteristic"]["uuid"]

stream = True
save = False
debug = False
save_file = None

#unpack fNIRS byte string
def unpack_fnirs(sender, packet):
    global bbxchars
    path = " "
    #figure out which characteristic sent it (using the handle, why do we have UUID AND handle?)
    for char in bbxchars:
        if sender in bbxchars[char]["handles"]:
            path = bbxchars[char]["name"]
            break
        elif type(sender) == str and sender.lower() == bbxchars[char]["uuid"]:
            path = bbxchars[char]["name"]
            break
    #unpack packet
    aa = bitstring.Bits(bytes=packet)
    pattern = "uintbe:8,uintbe:8,intbe:32,intbe:32,intbe:32,intbe:8,intbe:8"
    res = aa.unpack(pattern)
    packet_index = res[1]
    channel1 = res[2] #740
    channel2 = res[3] #880
    channel3 = res[4] #850
    return packet_index, path, channel1, channel2, channel3

def notification_handler(sender, data):
    global save, debug
    """Simple notification handler which prints the data received."""
    idx, path, c1, c2, c3 = unpack_fnirs(sender, data)

    if save:
        save_file.write("{},{},{},{},{},{}\n".format(time.time(), idx, path, c1, c2, c3))

    if debug:
        print("Blueberry: {}, path: {}, index: {}, C1: {}, C2: {}, C3: {}".format(sender, path, idx, c1, c2, c3))

async def run(address, debug=False):
    global stream
    if debug:
        l = logging.getLogger("asyncio")
        l.setLevel(logging.DEBUG)
        h = logging.StreamHandler(sys.stdout)
        h.setLevel(logging.DEBUG)
        l.addHandler(h)
        logger.addHandler(h)

    print("Trying to connect...")
    async with BleakClient(address) as client:
        x = await client.is_connected()
        logger.info("Connected to: {0}".format(x))

        await client.start_notify(SHORT_PATH_CHAR_UUID, notification_handler)
        await client.start_notify(LONG_PATH_CHAR_UUID, notification_handler)
        while stream:
            await asyncio.sleep(0.1)
        await client.stop_notify(CHARACTERISTIC_UUID)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-a","--address", help="MAC address of the blueberry")
    parser.add_argument("-s","--save", help="If present, save", action='store_true')
    parser.add_argument("-f","--filename", help="Name of file to save to", type=str)
    parser.add_argument("-d", "--debug", help="debug", action='store_true')
    args = parser.parse_args()

    #get address
    mac = args.address

    #should we debug?
    if args.debug:
        debug = True

    #if we should save, and make the save file
    if args.save:
        save = True
        if not args.filename or args.filename == "":
            save_file = open("{}.csv".format(time.time()), "w+")
        else:
            save_file = open(args.filename, "w+")
        save_file.write("timestamp,idx,path,c1,c2,c3\n")

    #translate address to be multi-platform
    address = (
        mac # <--- Change to your device's address here if you are using Windows or Linux
        if platform.system() != "Darwin"
        else mac # <--- Change to your device's address here if you are using macOS
    )

    #start main loop
    loop = asyncio.get_event_loop()
    # loop.set_debug(True)
    loop.run_until_complete(run(address, debug=True))

