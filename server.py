import socket
import sys
import asyncio
import websockets

HEADERSIZE = 10

def create_socket():
    """
    Creates a socket.
    """
    try:
        global host
        global port
        global s
        host = ""
        port = 9999
        s = socket.socket()

    except socket.error as msg:
        print("Socket creation error: " + str(msg))


def bind_socket():
    """
    Binds the socket and listens for connections.
    """
    try:
        global host
        global port
        global s
        print("Binding the Port: " + str(port))
        s.bind((host, port))
        s.listen(5)

    except socket.error as msg:
        print("Socket Binding error" + str(msg) + "\n" + "Retrying...")
        bind_socket()


def socket_accept():
    """
    Accepts the conection with the client. 'Conn' is the connection object and 
    'address' is a list with the IP as string and the port as integer.
    """
    conn, address = s.accept()
    print("Connection has been established! |" + " IP " + address[0] + " | Port" + str(address[1]))
    send_commands(conn)
    # Close connection
    conn.close()


def send_commands(conn):
	"""
	Interchange messages with the client. The data sent is in byte format, so we have to 
	encode/decode into bytes.
	"""
	global tcp_response
	global ws_message
	# Infinite loop for persistance
	while True:
		msg = input()                                           # Input message
		if msg == 'quit':                                       # Exit command
			conn.close()
			s.close()
			sys.exit()
		if len(str.encode(msg)) > 0:
			send_message(msg, conn)                             
			tcp_response = receive_message(conn)
			print(tcp_response)
			asyncio.get_event_loop().run_until_complete(message())    
			send_message(ws_message, conn)   

def send_message(msg, conn):
    """
    Sends a message with a header of fixed length 10 containing the length of the message
    and the actual message. Returns nothing.
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


def main():
    create_socket()
    bind_socket()
    socket_accept()
    
async def message():
	global ws_message
	## Conect to the server
	async with websockets.connect("ws://localhost:8765") as websocket:
		await websocket.send(tcp_response)
		print("WS sending confirmation...")
		ws_message = await websocket.recv()
		print(f"> {ws_message}")


# __INIT__
main()








