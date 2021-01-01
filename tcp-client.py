import socket
import os
import subprocess

# The client will try and connect to the server, receive a message
# and send a response back to the server.

HEADERSIZE = 10

def send_message(msg, conn):
    """
    Sends a message with a header of fixed length 10 and the actual message.
    Returns nothing.
    """
    msg = f'{len(msg):<{HEADERSIZE}}' + msg             # Header + message
    conn.send(bytes(msg, "utf-8"))                      # Send message

def receive_message(conn):
    """
    Receives a message and returns it.
    """
    fullMsg = ''
    newMsg = True
    while True:
        msg = conn.recv(16)
        ## When its a new message
        if newMsg:
            msgLen = int(msg[:HEADERSIZE])
            newMsg = False
        fullMsg += msg.decode("utf-8")
        ## When the full message is recived
        if len(fullMsg)-HEADERSIZE == msgLen:
            return(fullMsg[HEADERSIZE:])


s = socket.socket()                                             # Create the socket object
host = socket.gethostname()
port = 9999
s.connect((host, port))                                         # Connect to the server

while True:
    print(receive_message(s))                                   # Receive message
    msg = input()                                               # Input
    send_message(msg, s)                                        # Send message to the server
    print(f"From WS Server: {receive_message(s)}")                                   # Receive message
