import threading
import time
import socket
import struct
import sys
import copy

import matplotlib.pyplot as plt
import matplotlib.animation as animation


MAX_POINTS = 8192
rplidar_data = []
queue_lock = threading.Lock()

###
### returns file descriptor of socket
###
def connect(IP_ADDR, PORT) -> int:
    cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        cli_sock.connect((IP_ADDR, PORT))
    except Exception as e:
        print(f'ERROR: {e}')
    return cli_sock

def close(socket):
    socket.close()

### offset


def producer_network_IO(socket):
    total_bytes = MAX_POINTS * 7
    all_data = []
    try:
        while total_bytes > 0:
            data = socket.recv(7)  
            print(f'data recv this iteration: {data}')
            total_bytes -= len(data) 
            angle, distance, quality = deserialize_points(data)
            all_data.append([angle, distance, quality])
        '''
        for data in (all_data):
            print(data)
        '''
        return all_data
    except Exception as e:
        print(f'[producer_network_IO] ERROR: {e}')
        raise Exception("rplidar data could not be retrieved")

def deserialize_points(bytes, offset=0):
    u16 = struct.unpack('<H', bytes[offset: offset + 2])[0]
    u32 = struct.unpack('<I', bytes[offset + 2: offset + 6])[0]
    u8 =  struct.unpack('<B', bytes[offset + 6: offset + 7])[0]
    return u16 * (90/16384), u32/4, u8 >> 2 # angle, distance, quality flasg

def read_rpdata_into_file(data, filename):
    with open(filename, 'w') as file:
        for angle, distance, quality in data:        
            file.write(f'{angle} {distance} {quality}\n')
        
if __name__ == "__main__":
    IP_ADDR, PORT = '10.200.61.12', 6676
    fd = None
    try:
        sock = connect(IP_ADDR, PORT)
    except Exception as e:
        print(f'ERROR: {fd}')
        sys.exit(1)

    print(f'CONNECTION socket fd: {fd}')
    try:
        data = producer_network_IO(sock)
        read_rpdata_into_file(data, 'RP.txt')
    except Exception as e:
        print(f'[main] ERROR: {e}')


    sock.close();




    

