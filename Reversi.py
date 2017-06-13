import os
import sys
# Configuracion inicial
matriz = []
colorJugador = 'B'
colorPc = 'N'
nombre = ' '
resultado = 0
pasoturno = 0
sinmovidas = 0
libres = 0
blancas = 0
negras = 0
usuario = 0
listaUsuarios = []

#Funciones base de datos______________________
def leer(f):
    #Leo la lista entera y la separo por lineas y despues por comas y la devuelvo
    #Fomato: [usuario,puntaje,jugadas,ganadas,perdidas,empatadas]
    lista = f.readlines()
    lista = [x.strip().split(',') for x in lista]
    return lista

def topTen(listaUsuarios):
    #Ordeno la lista que paso como parametro por orden de importancia: puntaje, ganadas, jugadas, alfabeticamente. Uso el "-" como reverse
    listaOrdenada = sorted(listaUsuarios, key=lambda x: (-int(x[1]), -int(x[3]), -int(x[2]), (x[0])))
    #Muestro solo los primeros 10
    for i in range(10):
        print('Puntaje:', listaOrdenada[i][1].ljust(2, " "), 'Nombre:', listaOrdenada[i][0].capitalize().ljust(8, " "),
              'Partidas Jugadas:', listaOrdenada[i][2].ljust(2, " "), 'Partidas ganadas:',
              listaOrdenada[i][3].ljust(2, " "), 'Partidas perdidas:', listaOrdenada[i][4].ljust(2, " "),
              'Partidas empatadas', listaOrdenada[i][5].ljust(2, " "))

def actualizar(directorio,listaUsuarios):
    #Sobreescribo el archivo y lo lleno con la nueva lista, con el usuario nuevo, o la modificacion si ya existia
    a = open(directorio, 'w+')
    for i in range(len(listaUsuarios)):
        a.write(listaUsuarios[i][0] + "," + listaUsuarios[i][1]+ "," + listaUsuarios[i][2] + "," + listaUsuarios[i][3] + "," + listaUsuarios[i][4] + "," + listaUsuarios[i][5] + '\n')
    a.close()

# Funciones____________________________________
def crear_matriz(matriz):
    for i in range(10):
        matriz.append([' '] * 10)

def llenar_matriz(matriz):
    for i in range(10):
        matriz[i][0] = i
        matriz[i][9] = i
        matriz[0][i] = i
        matriz[9][i] = i
    matriz[0][0] = ' '
    matriz[9][9] = ' '
    matriz[0][9] = ' '
    matriz[9][0] = ' '
    matriz[4][4] = 'B'
    matriz[5][5] = 'B'
    matriz[4][5] = 'N'
    matriz[5][4] = 'N'

def mostrar_matriz(matriz):
    #Con el cls limpio la screen
    os.system('cls')
    for i in range(10):
        for j in range(10):
            print(matriz[i][j], end=' ')
        print()

def movimientos(fila, columna, cond):
    #Recorre las 8 posiciones posibles, N - S - E - O - NO - NE - SE - SO
    if (cond == 1):
        fila = fila - 1
        columna = columna
    elif (cond == 2):
        fila = fila - 1
        columna = columna + 1
    elif (cond == 3):
        fila = fila
        columna = columna + 1
    elif (cond == 4):
        fila = fila + 1
        columna = columna + 1
    elif (cond == 5):
        fila = fila + 1
        columna = columna
    elif (cond == 6):
        fila = fila + 1
        columna = columna - 1
    elif (cond == 7):
        fila = fila
        columna = columna - 1
    elif (cond == 8):
        fila = fila - 1
        columna = columna - 1

    return fila, columna

def inicio(nombre, colorJugador, colorPc, turno,usuario,listaUsuarios,f):
    print('---------------------------')
    print('---------Reversi-----------')
    print('---------------------------')
    print()
    print()
    nombre = input('Ingresar Nombre: ')
    listaUsuarios = leer(f)
    #Chequea si existe el usuario o no (guarda su posicion en la variable usuario) y muestra sus actuales datos si asi es, si no crea uno nuevo con sus datos todos en cero
    existe = 0
    for i in range(len(listaUsuarios)):
        if(nombre == listaUsuarios[i][0]):
            existe += 1
            usuario = i
    if(existe == 1):
        print('Sus datos actuales son Puntaje:', listaUsuarios[usuario][1].ljust(2, " "),'Partidas Jugadas:', listaUsuarios[usuario][2].ljust(2, " "), 'Partidas ganadas:',
              listaUsuarios[usuario][3].ljust(2, " "), 'Partidas perdidas:', listaUsuarios[usuario][4].ljust(2, " "), 'Partidas empatadas: ', listaUsuarios[usuario][5].ljust(2, " "))
    if(existe == 0):
        print('Su usuario no existe, se creara uno nuevo')
        usuario = (len(listaUsuarios))
        listaUsuarios.append([nombre,'0','0','0','0','0'])

    siguiente = 0
    #Pregunta que opcion quiere elegir hasta que elija la de jugar asi no tiene que volver a iniciar el programa
    while (siguiente == 0):
        primeraOpcion = input('Bienvenido '+ nombre+ ' desea: a)Jugar b)Administrar usuarios c)Ver top ten d)Instrucciones e)Salir  Opcion: ')
        if(primeraOpcion == 'a'):
            opcion = input('Elija un color: a)Blancas b)Negras  Opcion: ')
            if(opcion == 'a'):
                colorJugador = 'B'
                colorPc = 'N'
                turno = 1
                siguiente = 1
            elif(opcion == 'b'):
                colorJugador = 'N'
                colorPc = 'B'
                siguiente = 1
        elif(primeraOpcion == 'c'):
                topTen(listaUsuarios)
                f.close()
        elif(primeraOpcion == 'd'):
            input('El juego se inicia con cuatro fichas posicionadas en el centro del tablero...Seguir..')
        elif(primeraOpcion == 'e'):
            sys.exit()
        else:
            print('Opcion incorrecta')
    return nombre, colorJugador, colorPc, turno, usuario, listaUsuarios

def resultado_final(matriz, libres, blancas, negras, nombre, colorJugador, colorPc,usuario,listaUsuarios,directorio,f):
    #Modifica los datos sobre el diccionario del usuario correspondiente, para luego actualizarlos
    if (blancas < negras):
        if (colorJugador == 'B'):
            print('Ganron las Negras , perdiste', nombre)
            listaUsuarios[usuario][1] = (int(listaUsuarios[usuario][1])+(blancas - negras)).__str__()
            listaUsuarios[usuario][2] = (int(listaUsuarios[usuario][2]) + 1).__str__()
            listaUsuarios[usuario][4] = (int(listaUsuarios[usuario][4]) + 1).__str__()
        if (colorJugador == 'N'):
            print('Ganron las Negras , ganaste', nombre)
            listaUsuarios[usuario][1] = (int(listaUsuarios[usuario][1])+(negras - blancas)).__str__()
            listaUsuarios[usuario][2] = (int(listaUsuarios[usuario][2]) + 1).__str__()
            listaUsuarios[usuario][3] = (int(listaUsuarios[usuario][3]) + 1).__str__()
    if (blancas == negras):
        print('Juego Empatado')
        listaUsuarios[usuario][5] = (int(listaUsuarios[usuario][5]) + 1).__str__()
    if (blancas > negras):
        if (colorJugador == 'B'):
            print('Ganron las Blancas , ganaste', nombre)
            listaUsuarios[usuario][1] = (int(listaUsuarios[usuario][1]) + (blancas - negras)).__str__()
            listaUsuarios[usuario][2] = (int(listaUsuarios[usuario][2]) + 1).__str__()
            listaUsuarios[usuario][3] = (int(listaUsuarios[usuario][3]) + 1).__str__()
        if (colorJugador == 'N'):
            print('Ganron las Blancas , perdiste', nombre)
            listaUsuarios[usuario][1] = (int(listaUsuarios[usuario][1]) + (negras - blancas)).__str__()
            listaUsuarios[usuario][2] = (int(listaUsuarios[usuario][2]) + 1).__str__()
            listaUsuarios[usuario][4] = (int(listaUsuarios[usuario][4]) + 1).__str__()
    listaUsuarios[usuario][0] = nombre
    f.close()
    actualizar(directorio,listaUsuarios)
def intercambiador(matriz, fila, columna, newfila, newcolumna, i, tipo, colorJugador, colorPc):
    if (tipo == 1):
        ficha = colorJugador
    if (tipo == 2):
        ficha = colorPc

    tempfila = fila
    tempcolumna = columna
    tempfila, tempcolumna = movimientos(tempfila, tempcolumna, i)

    while ((tempfila != newfila) or (tempcolumna != newcolumna)):
        matriz[tempfila][tempcolumna] = ficha
        tempfila, tempcolumna = movimientos(tempfila, tempcolumna, i)
    return matriz

def detector_de_sandwitch(matriz, fila, columna, newfila, newcolumna, cantidad, i, tipo, colorJugador, colorPc):
    if (tipo == 1):
        ficha = colorJugador
    if (tipo == 2):
        ficha = colorPc
    salir = 0
    cantidad = 0
    while (salir == 0):
        newfila, newcolumna = movimientos(newfila, newcolumna, i)
        cantidad = cantidad + 1
        if (matriz[newfila][newcolumna] == ficha):
            salir = 1
        if ((matriz[newfila][newcolumna] != 'B') and (matriz[newfila][newcolumna] != 'N')):
            salir = 2
    if (salir == 1):
        return True, cantidad, newfila, newcolumna
    if (salir == 2):
        return False, cantidad, newfila, newcolumna

def chequeador(matriz, fila, columna, newfila, newcolumna, tipo, colorJugador, colorPc):
    if (tipo == 1):
        ficha = colorPc
    if (tipo == 2):
        ficha = colorJugador
    if (matriz[fila][columna] == ' '):
        if (matriz[newfila][newcolumna] == ficha):
            return True
        else:
            return False
    else:

        return False

def orientacion(matriz, fila, columna, tipo, bien, pasoturno, maxcantidad, colorJugador, colorPc):
    ok = 0
    cantidad = 0
    maxcantidad = 0

    for i in range(1, 9):
        newfila = fila
        newcolumna = columna
        newfila, newcolumna = movimientos(newfila, newcolumna, i)
        if (chequeador(matriz, fila, columna, newfila, newcolumna, tipo, colorJugador, colorPc)):
            condicion, cantidad, newfila, newcolumna = detector_de_sandwitch(matriz, fila, columna, newfila, newcolumna,
                                                                             cantidad, i, tipo, colorJugador, colorPc)
            if (condicion):
                maxcantidad = cantidad + maxcantidad
                if ((tipo == 1) or (bien == 100)):
                    matriz = intercambiador(matriz, fila, columna, newfila, newcolumna, i, tipo, colorJugador, colorPc)
                    ok = ok + 1
                if (tipo == 2):
                    ok = ok + 1
    if (ok == 0):
        return False, maxcantidad, matriz
    else:
        return True, maxcantidad, matriz

def contador_de_fichas(matriz, libres, blancas, negras):
    libres = 0
    blancas = 0
    negras = 0
    for i in range(1, 9):
        for j in range(1, 9):
            if (matriz[i][j] == ' '):
                libres = libres + 1
            if (matriz[i][j] == 'B'):
                blancas = blancas + 1
            if (matriz[i][j] == 'N'):
                negras = negras + 1
    print('Cantidad de Blancas: ', blancas)
    print('Cantidad de Negras: ', negras)
    print('Cantidad de Libres: ', libres)
    print()

    return libres, blancas, negras

def posicion_de_la_pc(matriz, fila, columna, maxcantidad, tipo, pasoturno, turno, bien, colorPc, colorJugador):
    mayorcantidad = 0

    for i in range(1, 9):
        for j in range(1, 9):
            fila = i
            columna = j
            condicion, maxcantidad, matriz = orientacion(matriz, fila, columna, tipo, bien, pasoturno, maxcantidad,
                                                         colorJugador, colorPc)
            if (condicion):

                if (mayorcantidad < maxcantidad):
                    mayorcantidad = maxcantidad
                    mejorfila = i
                    mejorcolumna = j
                    bien = bien + 1
            else:
                pasoturno = pasoturno + 1
    if (pasoturno == 64):
        print('Se pasara el turno automaticamente, no hay jugadas disponibles')
    if (bien != 0):
        maxcantidad = 0
        bien = 100
        fila = mejorfila
        columna = mejorcolumna

    return fila, columna, maxcantidad, pasoturno, bien

def ingresar_datos(matriz, turno, libres, blancas, negras, resultado, pasoturno, sinmovidas, colorJugador, colorPc):
    bien = 0
    maxcantidad = 0
    fila = 0
    columna = 0
    print()
    # Usuario
    if (turno == 0):
        print('Tu Turno')
        tipo = 2
        pasoturno = 0
        fila, columna, maxcantidad, pasoturno, bien = posicion_de_la_pc(matriz, fila, columna, maxcantidad, tipo,
                                                                        pasoturno, turno, bien, colorJugador, colorPc)
        if (bien != 0):

            fila = int(input('Posicion de la Fila : '))
            columna = int(input('Posicion de la Columna : '))
            tipo = 1
            turno = 1
            condicion1, maxcantidad, matriz = orientacion(matriz, fila, columna, tipo, bien, pasoturno, maxcantidad,
                                                          colorJugador, colorPc)
            if (condicion1):
                print('Cantidad de fichas convertidas = ', maxcantidad)
                matriz[fila][columna] = colorJugador
                libres, blancas, negras = contador_de_fichas(matriz, libres, blancas, negras)
                sinmovidas = 0
            else:
                print('Error de Posicion , Ingrese nueva posicion')
                turno = 0
        else:
            sinmovidas += 1
            turno = 1
    # Computadora
    else:
        print('Turno de la Pc')
        tipo = 2
        turno = 0
        pasoturno = 0
        fila, columna, maxcantidad, pasoturno, bien = posicion_de_la_pc(matriz, fila, columna, maxcantidad, tipo,
                                                                        pasoturno, turno, bien, colorPc, colorJugador)
        condicion2, maxcantidad, matriz = orientacion(matriz, fila, columna, tipo, bien, pasoturno, maxcantidad,
                                                      colorJugador, colorPc)
        if (condicion2):
            print('Cantidad de fichas convertidas = ', maxcantidad)
            matriz[fila][columna] = colorPc
            libres, blancas, negras = contador_de_fichas(matriz, libres, blancas, negras)
            sinmovidas = 0
        else:
            sinmovidas += 1
            turno = 0
    if (sinmovidas == 2):
        resultado = 1

    return matriz, turno, resultado, pasoturno, sinmovidas, libres, blancas, negras

def desarrollo(matriz, nombre, colorJugador, colorPc, turno, libres, blancas, negras, resultado, pasoturno, sinmovidas,usuario,listaUsuarios,directorio,f):
    fin = 0
    while (fin != 1):
        mostrar_matriz(matriz)
        matriz, turno, resultado, pasoturno, sinmovidas, libres, blancas, negras = ingresar_datos(matriz, turno, libres,
                                                                                                  blancas, negras,
                                                                                                  resultado, pasoturno,
                                                                                                  sinmovidas,
                                                                                                  colorJugador, colorPc)
        if (resultado == 1):
            resultado_final(matriz, libres, blancas, negras, nombre, colorJugador, colorPc,usuario,listaUsuarios,directorio,f)
            fin = 1

def juego(matriz, nombre, colorJugador, colorPc, libres, blancas, negras, resultado, pasoturno, sinmovidas,usuario,listaUsuarios):
    directorio = r'C:/Users/Gonzalo/Desktop/Reversi Python/usuarios.txt'
    f = open(directorio, 'r+')
    turno = 1
    volverAJugar = 's'
    while (volverAJugar == 's'):
        nombre, colorJugador, colorPc, turno, usuario, listaUsuarios = inicio(nombre, colorJugador, colorPc, turno,usuario, listaUsuarios,f)
        llenar_matriz(matriz)
        resultado = 0
        pasoturno = 0
        sinmovidas = 0
        desarrollo(matriz, nombre, colorJugador, colorPc, turno, libres, blancas, negras, resultado, pasoturno,
                   sinmovidas,usuario, listaUsuarios,directorio,f)
        volverAJugar = input('Juego terminado , Desea volver a Jugar? s/n')

# Cuerpo Principal
crear_matriz(matriz)
juego(matriz, nombre, colorJugador, colorPc, libres, blancas, negras, resultado, pasoturno, sinmovidas,usuario, listaUsuarios)