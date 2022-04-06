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
    if mensaje  == DISCONNECT_MESSAGE or mensaje == "2": #algo no funciona....
        send(mensaje)
        print(clientSocket.recv(2048).decode())

        break
    send(mensaje)
    listen(clientSocket)

    #print(clientSocket.recv(2048).decode())
    #print(clientSocket.recv(2048).decode())
    

    






"""
    while True:
        try:
            print(clientSocket.recv(2048).decode())
        except TimeoutError:
            break




    flag = True
    while flag:
        print("estoy intentando recibir...")
        respuesta = clientSocket.recv(2048).decode()
        if respuesta.strip() == END_OF_RESPONSE:
            print("WTF")
            flag = False
        else:
            print(respuesta)




    n_respuestas = int(clientSocket.recv(2048).decode())
    print(f"numero de mensajes proximos: {n_respuestas} ")
    for i in range(n_respuestas):
        print("estoy intentando recibir...")
        print(clientSocket.recv(2048).decode())
        """

    
    








"""
while True:
    

    toSend = input('Mensaje: ')
    clientSocket.send(toSend.encode())

    response = clientSocket.recv(1024).decode()
    print("respuesta del servidor", response)

clientSocket.close() 
"""