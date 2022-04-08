from random import randint
import socket as skt
from time import sleep
from juego import insertar, ver_tablero, verificar_estado


tablero = [[' ', ' ', ' '],[ ' ', ' ', ' '], [' ', ' ', ' ']]

MENSAJES_POR_ENVIAR = "2"
REQUEST = "disponible"
END_OF_RESPONSE = "FIN"
DISCONNECT_MESSAGE = "DISCONNECT"
BOARD_CLEAR = "reinicio"
address = 'localhost'
HEADER = 1024
serverPort = 5000
serverSocket = skt.socket(skt.AF_INET, skt.SOCK_DGRAM)

clientPort = 5001

clientSocket = skt.socket(skt.AF_INET, skt.SOCK_STREAM) #skt.AF_INET indica la direccion ipv4 y skt.SOCK_STREAM para el tipo de conexion tcp
clientSocket.bind(('', clientPort))
#clientSocket.listen(1)

def eleccion_menu_inicio(conn):
    conn.send("-------- Bienvenido al Juego --------\n".encode())
    conn.send("- Seleccione una opcion\n".encode())
    conn.send("1-Jugar\n".encode())
    conn.send("2-Salir\n".encode())
    msg_length = conn.recv(HEADER).decode()
    if msg_length:
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode()
    return(msg)

def protocolo_cierre(conn,serverSocket):
    
    serverSocket.sendto("DISCONNECT".encode(), (address, serverPort))
    puerto_aleatorio = randint(8000,65535)
    msg, addr = serverSocket.recvfrom(puerto_aleatorio)

    msg_aux = msg.decode()
    print("Servidor gato dice: ", msg_aux)
    print("Cerrando servidor intermedio... ")
    
    conn.send(f"Servidor gato dice: {msg_aux}\n".encode())
    conn.send(f"Cerrando servidor intermedio... ".encode())
    
    return

def enviar_tablero(conn,tablero):
    conn.send(". 0   1   2   (x)\n".encode())
    conn.send(f"0 {tablero[0][0]} | {tablero[1][0]} | {tablero[2][0]}\n".encode())
    conn.send(f" ---+---+---\n".encode())
    conn.send(f"1 {tablero[0][1]} | {tablero[1][1]} | {tablero[2][1]}\n".encode())
    conn.send(f" ---+---+---\n".encode())
    conn.send(f"2 {tablero[0][2]} | {tablero[1][2]} | {tablero[2][2]}\n".encode())
    conn.send("(y)\n".encode())
    return


def protocolo_reinicio_juego(serverSocket,tablero,menu_inicio,evento_especial_1,evento_especial_2):
    tablero = [[' ', ' ', ' '],[ ' ', ' ', ' '], [' ', ' ', ' ']] 
    serverSocket.sendto(BOARD_CLEAR.encode(), (address, serverPort))
    menu_inicio = True
    evento_especial_1 = False
    evento_especial_2 = False
    return(tablero,menu_inicio,evento_especial_1,evento_especial_2)



def handle_client(conn, addr, serverSocket, serverPort, tablero):
    
    connected = True
    evento_especial_1 = False #gana el cliente
    evento_especial_2 = False #gana el bot
    evento_especial_3 = False #empate entre cliente y bot
    menu_inicio = True
    jugadas = 0
    while connected:
       
        if menu_inicio:
            print("menu de inicio")
            respuesta_menu = eleccion_menu_inicio(conn)
            if int(respuesta_menu) == 2:
                print("protocolo de cierre de menu de inicio")
                protocolo_cierre(conn,serverSocket)
                connected = False
                conn.close()
                serverSocket.close()
                return
            elif int(respuesta_menu) == 1:
                print("opcion para jugar")
                print("accediendo disponibilidad del servidor gato...")
                #preguntar al servidor gato si esta disponible
                serverSocket.sendto(REQUEST.encode(), (address, serverPort))
                msg, addr = serverSocket.recvfrom(serverPort)
                msg_aux = int(msg.decode())
                if msg_aux == 1:#no esta disponible
                    print("servidor gato no disponible")
                    conn.send("servidor gato no disponible por el momento... intente denuevo\n".encode())
                    continue
                print("servidor gato disponible")
                conn.send("servidor gato disponible para jugar\n".encode())
                #-------------------------
                enviar_tablero(conn,tablero)
                menu_inicio = False
                continue
            else:
                print("opcion invalida")
                conn.send("Opcion invalida, ingrese denuevo".encode())

        else:
            print("juego en marcha")
            #TODO: Checkear disponibilidad del servidor gato
            conn.send("Ingrese coordenadas, separadas con ',': ".encode())
            msg_length = conn.recv(HEADER).decode()
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode()

                #protocolo de cierre
                if msg == DISCONNECT_MESSAGE:
                    protocolo_cierre(conn,serverSocket)
                    connected = False
                    conn.close()
                    serverSocket.close()
                    return
                    
                #--------------------
                print('Coordenadas del cliente: ', msg)
                #logica del juego cliente
                move = str(msg).strip().split(",")
                if len(move) != 2:
                    print("mensaje invalido")
                    conn.send("jugada invalida, juegas denuevo".encode())
                    continue
                input1,input2 = move
                res=insertar(int(input1),int(input2),0,tablero,jugadas)
                if res=="Jugada invalida,No puede poner el elemento alli" or res=="Posicion fuera de rango":
                    print("Jugada invalida reintentelo")
                    conn.send("Jugada invalida, juegas denuevo.\n".encode())
                    enviar_tablero(conn,tablero)
                    continue #no deja jugar al servidor gato
                    #ENVIAR MSG A "a.py" para que vuelva a ingresar un valor... No dejar q el bot juegue LISTO
                else:
                    print(res)
                    jugadas += 1
                    if jugadas == 9:#empate
                        evento_especial_3 = True
                #TODO: variable "jugadas" no se actualiza con insertar() por algun motivo
                
                

                if verificar_estado(tablero)[0]!="neutral":
                    if verificar_estado(tablero)[1]=="X":
                        print("¡Felicidades, has ganado!")
                        evento_especial_1 = True
                        enviar_tablero(conn,tablero)
                        #tablero = [[' ', ' ', ' '],[ ' ', ' ', ' '], [' ', ' ', ' ']] 
                        #TODO: arreglar, tablero se ve sobreescrito por el bot despues de reiniciar LISTO
                #------------------------

                if (not evento_especial_1) and (not evento_especial_3):
                    serverSocket.sendto(msg.encode(), (address, serverPort))
                    print("esperando jugada del servidor")

                    puerto_aleatorio = randint(8000,65535)
                    msg, addr = serverSocket.recvfrom(puerto_aleatorio)

                    msg_aux = msg.decode()
                    print("jugada del servidor", msg_aux)

                    #logica del juego BOT
                    move = str(msg_aux).strip().split(",")
                    input1,input2 = move
                    print(insertar(int(input1),int(input2),1,tablero,jugadas))
                    jugadas += 1
                    if jugadas == 9:#empate
                        evento_especial_3 = True
                        
                    if verificar_estado(tablero)[0]!="neutral":
                        if verificar_estado(tablero)[1]=="O":
                            enviar_tablero(conn,tablero)
                            print("Lamentablemente has perdido contra el BOT")
                            #tablero = [[' ', ' ', ' '],[ ' ', ' ', ' '], [' ', ' ', ' ']] 
                            evento_especial_2 = 2
                            #TODO: decirle al servidor gato que reinicie su propio tablero y que no juege LISTO
                    #--------------------
                
                #enviar informacion al cliente:

                #conn.send(MENSAJES_POR_ENVIAR.encode())
                
                #conn.send(msg)
                if evento_especial_1 or evento_especial_2:
                    
                    final = "¡Felicidades, has ganado!"*(evento_especial_1) + "Lamentablemente has perdido contra el BOT"*(evento_especial_2)
                    conn.send(final.encode())
                    protocolo_reinicio_juego(serverSocket,tablero,menu_inicio,evento_especial_1,evento_especial_2)
                    tablero = [[' ', ' ', ' '],[ ' ', ' ', ' '], [' ', ' ', ' ']]
                    evento_especial_1 = False
                    evento_especial_2 = False
                    evento_especial_3 = False
                    menu_inicio = True
                    jugadas = 0

                elif evento_especial_3:
                    final = "empate, nadie gana!"
                    conn.send(final.encode())
                    protocolo_reinicio_juego(serverSocket,tablero,menu_inicio,evento_especial_1,evento_especial_2)
                    tablero = [[' ', ' ', ' '],[ ' ', ' ', ' '], [' ', ' ', ' ']]
                    evento_especial_1 = False
                    evento_especial_2 = False
                    evento_especial_3 = False
                    menu_inicio = True
                    jugadas = 0
                    
                else:
                    enviar_tablero(conn,tablero) #siete envios

                #conn.send(END_OF_RESPONSE.encode())#ultimo mensaje que se manda al cliente en cada iteracion
                #termino del envio de informacion al cliente

    conn.close()
    serverSocket.close()
    return

def start():
    clientSocket.listen(1)
    playerSocket, playerAddr = clientSocket.accept()
    handle_client(playerSocket, playerAddr, serverSocket, serverPort, tablero)


    return

start()

