# Name: Luong Nguyen
# StarID: vv2796uo

import sys
from socket import *
import datetime
import hashlib

# Set up the socket for UDP connection
HOST = gethostbyname(gethostname())
PORT = 5555
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind((HOST, PORT))

while True:
    print('\n\rWaiting')
    print(f"Listening on port {PORT}")
    # Receive the message first, create a timestamp and then receive the checksum
    message, address = serverSocket.recvfrom(1024)
    today = datetime.datetime.today()

    print(f"Received time: {today}")
    print(f"Received message: {message.decode()}")

    # Create a local checksum to compare later
    calChecksum = hashlib.md5(message).hexdigest()

    recChecksum, address = serverSocket.recvfrom(1024) # The checksum received from client

    print(f"Received checksum: {recChecksum.decode()}")
    print(f"Calculated checksum: {calChecksum}")

    # Comparing two checksum
    if calChecksum == recChecksum.decode():
        serverSocket.sendto(str(today).encode(), address)
        serverSocket.sendto("The checksum matches!".encode(), address)
    else:
        print("Checksums don't match!!!")
        serverSocket.sendto("The checksum doesn't match".encode(), address)