# Name: Luong Nguyen
# StarID: vv2796uo

from socket import *
import sys
import datetime
import hashlib

HOST = gethostbyname(gethostname())
PORT = 5555

fileName = sys.argv[1]    # Text File or just plain text

if fileName.endswith('txt'):
    f = open(fileName)
    outputData = f.read()
    # Calculating the checksum
    checksum = hashlib.md5(open(fileName, 'rb').read())
else:
    outputData = fileName
    checksum = hashlib.md5(outputData.encode())

# Establish UDP connection
clientSocket = socket(AF_INET, SOCK_DGRAM)
try:
    # Sending the text to the server
    clientSocket.sendto(outputData.encode(), (HOST, PORT))
    today = datetime.datetime.now()  # Get the time when the message was sent

    # Sending the client checksum
    clientSocket.sendto(checksum.hexdigest().encode(), (HOST, PORT))
    print(f"Checksum sent: {checksum.hexdigest()}")

    # Get the checksum from the server and print it out
    today1, address = clientSocket.recvfrom(1024)
    # Calculating the RTT
    today2 = datetime.datetime.now()
    RTT = today2 - today
    confirmation, address = clientSocket.recvfrom(1024)

    print(f"Server received the message at: {today1.decode()}")
    print(str((today2 - today).microseconds)+'ms')
    print(f"Server confirmed that: {confirmation.decode()}")
except IOError:
    print("ERROR")
    confirmation, address = clientSocket.recvfrom(1024)
    print(f"Server confirmed that: {confirmation.decode()}")
