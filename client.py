import socket
import cv2
import pickle
import struct
import imutils

#Socket creation:

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_ip = '192.168.56.1' # paste your HOST IP
port = 1234

#Socket connect:

client_socket.connect((host_ip,port))  # tuple
data = b"" # Initialise data variable as a string , b - bytes
# Payload size is defined with "Q" i.e.,unsigned long long integer that takes 8 bytes
payload_size = struct.calcsize("Q")

#Socket receive:

while True:
    while len(data) < payload_size:
        packet = client_socket.recv(4*1024) # 4K
        if not packet: break
        data+=packet
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q",packed_msg_size)[0]
    
    while len(data) < msg_size:
        data += client_socket.recv(4*1024)
    frame_data = data[:msg_size]
    data  = data[msg_size:]
    frame = pickle.loads(frame_data)
    cv2.imshow("RECEIVING VIDEO",frame)
    key = cv2.waitKey(10) 
    if key  == 13:
        break
client_socket.close()
