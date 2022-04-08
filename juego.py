
def ver_tablero(tablero):
    print(". 0   1   2   (x)")
    print("0 %c | %c | %c" %(tablero[0][0],tablero[1][0],tablero[2][0]))
    print(" ---+---+---")
    print("1 %c | %c | %c" %(tablero[0][1],tablero[1][1],tablero[2][1]))
    print(" ---+---+---")
    print("2 %c | %c | %c" %(tablero[0][2],tablero[1][2],tablero[2][2]))
    print("(y)")
    return()


def insertar(posX,posY,jugador,tablero,jugadas): #jugador=0: cliente; jugador=1:BOT

    if posY>3 or posX>3:
        return("Posicion fuera de rango")#jugada invalida

    if tablero[posX][posY]==" ":
        print("valido")
        """
        if jugador==0:
            elem="X"
        else:
            elem="O"
        """
        tablero[posX][posY]="X"*(jugador==0) + "O"*(jugador==1) 
        #jugadas+=1
        #ver_tablero(tablero)
        return(f"\njugadas: {jugadas} \n")#jugada valida
    else:
        return("Jugada invalida,No puede poner el elemento alli")#jugada invalida


def verificar_estado(tablero):
    if (tablero[0][0] == tablero[1][1] == tablero[2][2] != ' '):#primera diagonal 
        return(("gana diagonal 1",tablero[0][0]))

    if (tablero[2][0] == tablero[1][1] == tablero[0][2] != ' '):#segunda diagonal
        return("gana diagonal 1",tablero[0][2])
    
    for i in range(3):
        if(tablero[i][0] == tablero[i][1] == tablero[i][2] != ' '): #primera,segunda,tercera vertical
            return(f"gana vertical {i+1}", tablero[i][i])

        if(tablero[0][i] == tablero[1][i] == tablero[2][i] != ' '): #primera,segunda,tercera horizontal
            return(f"gana horizontal {i+1}", tablero[0][i])

    return("neutral","I")

"""
bucle=" "
tablero = [[' ', ' ', ' '],[ ' ', ' ', ' '], [' ', ' ', ' ']]
jugadas=0
comando="jugar"
print("Bienvenido, juegas como las X")
decision="1"
while decision=="1":
    decision=input("Que desea hacer:\n 1: Jugar \n 2: Salir\n")
    if decision=="2":
        break
    while bucle==" ":
        move = input("Ingrese coordenadas, separadas con ',': ")
        move = str(move).strip().split(",")
        input1,input2 = move
        if jugadas<9:
            print(insertar(int(input1),int(input2),0,tablero,jugadas))
            if verificar_estado(tablero)[0]!="neutral":
                if verificar_estado(tablero)[1]=="X":
                    print("¡Felicidades, has ganado!")
                    break
                elif verificar_estado(tablero)[1]=="O":
                    print("Lamentablemente has perdido contra el BOT")
                    break
        elif jugadas==9:
            print("Empate, el tablero esta lleno")
            break
    else:
        decision="1"
        print("Lo que ha ingresado no es valido")
"""
