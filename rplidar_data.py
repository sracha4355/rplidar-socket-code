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
def deserialize_points(bytes, offset=0):
    u16 = struct.unpack('<H', bytes[offset: offset + 2])[0]
    u32 = struct.unpack('<I', bytes[offset + 2: offset + 6])[0]
    u8 =  struct.unpack('<B', bytes[offset + 6: offset + 7])[0]
    return [u16 * (90/16384), u32/4, u8 >> 2] # angle, distance, quality flasg

def producer_network_IO(socket):
    point_size = 7
    total_bytes = MAX_POINTS * point_size
    print(f'Networking IO thread started')
    while True:
        queue_lock.acquire() # lock the queue for writing
        rplidar_data = []
        bytes_left_to_read = total_bytes
        while bytes_left_to_read > 0:
            try:
                data = socket.recv(point_size)
                #print(f'bytes left: {bytes_left_to_read} data: {data}')
                angle, distance, quality = deserialize_points(data)
                if(angle < 359):
                    print(f'serialized_point: [{angle}, {distance}, {quality}]')
                    rplidar_data.append([angle, distance])
            except Exception as e:
                print('in here')
                print(f'ERROR: {e}')
                queue_lock.release()
                return
            bytes_left_to_read -= point_size
        print('exited inner loop')
        queue_lock.release() # lock the queue so plotting threading can read it
        time.sleep(0.005)
        print('lock released')
    print(f'Networking IO thread ended')

###### plotting code #######
def plotting_thread():
    print(f'Plotting thread started')
    ### setup the plot
    fig, ax = plt.subplots()
    points = ax.scatter([], [], marker='o')
    ani = animation.FuncAnimation(fig, update, frames=range(11), fargs=(points, ax), blit=True, interval=200)
    clear_ani = animation.FuncAnimation(fig, clear_plot, frames=[10], fargs=(fig, ax))    
    print('made it here')
    plt.show()

def update(frame, points, ax):
    print(f'FRAME {frame}')
    queue_lock.acquire() ### only read the data once all the data from rasp-pi is in
    print('lock aq for plotting')
    rpd_copy = copy.deepcopy(rplidar_data)
    print(f'copy:', rpd_copy)
    print('lock released for plotting')

    queue_lock.release()
    ax.set_xlim(0,360)
    ax.set_ylim(0, 20000)
    points.set_offsets(rpd_copy)
    return points, ax,

def clear_plot(fig, ax):
    print(f'Clearing Plot')
    ax.cla()
    fig.canvas.draw()  # Optional: Explicitly redraw the figure after clearing

############################

if __name__ == "__main__":
    IP_ADDR, PORT = '10.200.61.12', 6674
    fd = None
    try:
        sock = connect(IP_ADDR, PORT)
    except Exception as e:
        print(f'ERROR: {fd}')
        sys.exit(1)

    print(f'CONNECTION socket fd: {fd}')
    network_IO = threading.Thread(target=producer_network_IO, args=(sock,))
    network_IO.start()
    time.sleep(5)

    print('going into plotting thread')
    plotting_thread()
    '''
    plotting.start()

    network_IO.join()
    plotting.join()
    '''

    sock.close();




    

