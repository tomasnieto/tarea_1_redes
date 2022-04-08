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
    conn.send("\n-------- Bienvenido al Juego --------\n".encode())
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




def handle_evento_especial(e_e_1, e_e_2, e_e_3, conn, serverSocket, tablero, menu_inicio, jugadas):
    #print("handle envento especial")
    final = "¡Felicidades, has ganado!"*(e_e_1) + "Lamentablemente has perdido contra el BOT"*(e_e_2) + "empate, nadie gana!"*(e_e_3)
    conn.send(final.encode())
    serverSocket.sendto(BOARD_CLEAR.encode(), (address, serverPort))
    tablero = [[' ', ' ', ' '],[ ' ', ' ', ' '], [' ', ' ', ' ']]
    e_e_1 = False
    e_e_2 = False
    e_e_3 = False
    menu_inicio = True
    jugadas = 0

    return(e_e_1, e_e_2, e_e_3, tablero, menu_inicio, jugadas)



def handle_client(conn, addr, serverSocket, serverPort, tablero):
    
    connected = True
    evento_especial_1 = False #gana el cliente
    evento_especial_2 = False #gana el bot
    evento_especial_3 = False #empate entre cliente y bot
    menu_inicio = True
    jugadas = 0
    while connected:
       
        if menu_inicio:
            #menu de inicio, cliente puede jugar(1) o salir(2)
            print("menu de inicio")
            respuesta_menu = eleccion_menu_inicio(conn)
            if int(respuesta_menu) == 2:#cliente cierra conexion
                print("protocolo de cierre de menu de inicio")
                protocolo_cierre(conn,serverSocket)
                connected = False
                conn.close()
                serverSocket.close()
                return
            elif int(respuesta_menu) == 1:#cliente quiere jugar
                #print("opcion para jugar")
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
                menu_inicio = False #juego empieza
                continue
            else:
                #print("opcion invalida")
                conn.send("Opcion invalida, ingrese denuevo".encode())

        else:
            #print("juego en marcha")
            #recibir input del cliente
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
                #desempaquetar input del cliente para leerlo
                move = str(msg).strip().split(",")
                if len(move) != 2:
                    print("mensaje invalido")
                    conn.send("jugada invalida, juegas denuevo".encode())
                    continue
                input1,input2 = move
                #jugar la jugada en el tablero
                res=insertar(int(input1),int(input2),0,tablero,jugadas)
                if res=="Jugada invalida,No puede poner el elemento alli" or res=="Posicion fuera de rango":
                    #print("Jugada invalida reintentelo")
                    conn.send("Jugada invalida, juegas denuevo.\n".encode())
                    enviar_tablero(conn,tablero)
                    continue #no deja jugar al servidor gato
                else:
                    print(res)
                    jugadas += 1
                    if jugadas == 9:#empate
                        evento_especial_3 = True
                
                

                if verificar_estado(tablero)[0]!="neutral":
                    if verificar_estado(tablero)[1]=="X":
                        print("cliente gana")
                        evento_especial_1 = True
                        evento_especial_3 = False
                        enviar_tablero(conn,tablero)
                #------------------------

                
                if (not evento_especial_1) and (not evento_especial_3):#cliente puede jugar
                    serverSocket.sendto(msg.encode(), (address, serverPort))
                    print("esperando jugada del servidor")

                    puerto_aleatorio = randint(8000,65535)
                    msg, addr = serverSocket.recvfrom(puerto_aleatorio)#recibe de puerto aleatorio

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
                            print("cliente pierde")
                            evento_especial_2 = True
                    #--------------------

                if (evento_especial_1 or evento_especial_2) != evento_especial_3: #XOR
                    evento_especial_1, evento_especial_2, evento_especial_3, tablero, menu_inicio, jugadas = handle_evento_especial(evento_especial_1,evento_especial_2,evento_especial_3,conn,serverSocket,tablero,menu_inicio,jugadas)
                else:
                    enviar_tablero(conn,tablero) #siete envios
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

