package main

import (
	"fmt"
	"math/rand"
	"net"
	"strconv"
	"strings"
	"time"
)

func main() {

	DISCONNECT_MESSAGE := "DISCONNECT"
	REQUEST := "disponible"
	BOARD_CLEAR := "reinicio"

	//semilla para la aleatoriedad
	s1 := rand.NewSource(time.Now().UnixNano())
	r1 := rand.New(s1)

	var arraystring = [...]string{" ", " ", " "}
	var tablero [3][len(arraystring)]string
	for i := range tablero {
		tablero[i] = arraystring
	}

	PORT := ":5000"
	BUFFER := 1024

	s, err := net.ResolveUDPAddr("udp4", PORT)

	if err != nil {
		fmt.Println(err)
		return
	}

	connection, err := net.ListenUDP("udp4", s)
	if err != nil {
		fmt.Println(err)
		return
	}

	//defer connection.Close()

	for true {
		buffer := make([]byte, BUFFER)

		fmt.Println("esperando mensaje del servidor intermedio")
		n, addr, _ := connection.ReadFromUDP(buffer)
		msg := string(buffer[:n])

		fmt.Println("direccion:", addr)
		fmt.Println("mensaje del servidor intermedio:", msg)

		if msg == DISCONNECT_MESSAGE {
			_, _ = connection.WriteToUDP([]byte("Cerrando servidor gato..."), addr)
			return
		}

		if msg == BOARD_CLEAR { //reiniciar tablero si es necesario
			for i := range tablero {
				tablero[i] = arraystring
			}
			continue
		}

		if msg == REQUEST { //servidor gato responde si está disponible
			probabilidad := r1.Intn(10)
			if probabilidad == 10 {
				_, _ = connection.WriteToUDP([]byte("1"), addr)
			} else {
				_, _ = connection.WriteToUDP([]byte("0"), addr)
			}
			continue

		}
		//move = str(msg).strip().split(",")
		//input1,input2 = move
		//actualizar tablero local
		move := strings.Split(msg, ",")
		X_jugador, _ := strconv.Atoi(move[0])
		Y_jugador, _ := strconv.Atoi(move[1])
		tablero[X_jugador][Y_jugador] = "X"

		//realizar jugada
		var response []byte
		var argumento string

		for true {
			jugada_X := r1.Intn(3)
			jugada_Y := r1.Intn(3)
			if tablero[jugada_X][jugada_Y] == " " {
				argumento = fmt.Sprintf("%d,%d", jugada_X, jugada_Y)
				tablero[jugada_X][jugada_Y] = "O"
				break
			}
		}

		fmt.Print("jugada del bot: ")
		fmt.Print(argumento)
		fmt.Print("\n")
		response = []byte(argumento)
		//fmt.Print(response)
		//fmt.Print("\n")
		//fmt.Print(response)
		//response := []byte("adios")
		_, _ = connection.WriteToUDP(response, addr)
	}

	return
}
