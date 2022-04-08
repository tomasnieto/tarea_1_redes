from re import T
import socket as skt

END_OF_RESPONSE = "FIN"
DISCONNECT_MESSAGE = "DISCONNECT"
HEADER = 1024
address = 'localhost'
serverPort = 5001
clientSocket = skt.socket(skt.AF_INET, skt.SOCK_STREAM)
clientSocket.connect((address, serverPort))

clientSocket.settimeout(1)


def send(msg):
    message = msg.encode()
    msg_length = len(message)
    send_length = str(msg_length).encode()
    send_length += b' ' * (HEADER - len(send_length))
    clientSocket.send(send_length)
    clientSocket.send(message)
    return

def listen(clientSocket):
    while True:
        try:
            print(clientSocket.recv(2048).decode().strip())
        except TimeoutError:
            return


listen(clientSocket)
while True:
    mensaje = input("mensaje: ")
    if mensaje  == DISCONNECT_MESSAGE or mensaje == "2": 
        send(mensaje)
        print(clientSocket.recv(2048).decode())

        break
    send(mensaje)
    listen(clientSocket)

 