#!/usr/bin/env python3
# Software License Agreement (BSD License)
#
# Copyright (c) 2023, UFACTORY, Inc.
# All rights reserved.
#
# Author: Vinman <vinman.wen@ufactory.cc> <vinman.cub@gmail.com>

"""
Description: read report data example
    1. requires firmware 2.1.0 and above support
"""

import os
import sys
import time
import datetime
import csv
import socket
import json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))

from xarm.core.comm import SocketPort
from xarm.core.utils import convert


#######################################################
"""
Just for test example
"""
if len(sys.argv) >= 2:
    ip = sys.argv[1]
else:
    try:
        from configparser import ConfigParser
        parser = ConfigParser()
        parser.read('../robot.conf')
        ip = parser.get('xArm', 'ip')
    except:
        ip = input('Please input the xArm ip address:')
        if not ip:
            print('input error, exit')
            sys.exit(1)
########################################################

# Setup for the socket client
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

sock = SocketPort(ip, 30001)


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

while sock.connected:
    try:
        data = sock.read(timeout=1)
        if data == -1:
            time.sleep(0.1)
            continue
        angles = convert.bytes_to_fp32s(data[7:35], 7)
        print('angles: {}'.format(angles))
        # Convert angles to JSON and send
        message = json.dumps(angles)
        client_socket.sendall(message.encode('utf-8'))
    except Exception as e:
        print(f"An error occurred: {e}")
        break

client_socket.close()

'''while sock.connected:
    data = sock.read(timeout=1)
    if data == -1:
        time.sleep(0.1)
        continue
    total = convert.bytes_to_u32(data[0:4])
    angles = convert.bytes_to_fp32s(data[7:35], 7)
    poses = convert.bytes_to_fp32s(data[35:59], 6)
    print('total={}, now={}'.format(total, datetime.datetime.now()))
    print('angles: {}'.format(angles))
    print('poses: {}'.format(poses))'''






# asynchronous code
'''with open('xarm_data4.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    while sock.connected:
        try:
            data = sock.read(timeout=1)
            if data == -1:
                time.sleep(0.1)
                continue
            total = convert.bytes_to_u32(data[0:4])
            angles = convert.bytes_to_fp32s(data[7:35], 7)
            timestamp = datetime.datetime.now()
            writer.writerow([timestamp, *angles])
            file.flush()  # Flush data to file
        except Exception as e:
            print(f"An error occurred: {e}")
            break'''
