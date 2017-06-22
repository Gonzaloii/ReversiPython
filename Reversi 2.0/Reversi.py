import os, sys, random, string
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
def abrir(directorio):
    f = open(directorio, 'r+')
    return f

def cerrar(f):
    f.close()

def crearArchivo(directorio):
    f = open(directorio,'w+')
    return f

def leerEntero(f):
    #Leo la lista entera y la separo por lineas y despues por comas y la devuelvo
    #Fomato: [usuario,puntaje,jugadas,ganadas,perdidas,empatadas]
    lista = f.readlines()
    lista = [x.strip().split(',') for x in lista]
    return lista

def topTen(listaUsuarios):
    #Ordeno la lista que paso como parametro por orden de importancia: puntaje, ganadas, jugadas, alfabeticamente. Uso el "-" como reverse
    listaOrdenada = sorted(listaUsuarios, key=lambda x: (-int(x[1]), -int(x[3]), -int(x[2]), (x[0])))
    #Muestro solo los primeros 10
    if(len(listaUsuarios) > 10):
        for i in range(10):
            print('Puntaje:', listaOrdenada[i][1].ljust(2, " "), 'Nombre:', listaOrdenada[i][0].capitalize().ljust(8, " "),
                  'Partidas Jugadas:', listaOrdenada[i][2].ljust(2, " "), 'Partidas ganadas:',
                  listaOrdenada[i][3].ljust(2, " "), 'Partidas perdidas:', listaOrdenada[i][4].ljust(2, " "),
                  'Partidas empatadas', listaOrdenada[i][5].ljust(2, " "),'\n')
    else:
        for i in range(len(listaUsuarios)):
            print('Puntaje:', listaOrdenada[i][1].ljust(2, " "), 'Nombre:',
                  listaOrdenada[i][0].capitalize().ljust(8, " "),
                  'Partidas Jugadas:', listaOrdenada[i][2].ljust(2, " "), 'Partidas ganadas:',
                  listaOrdenada[i][3].ljust(2, " "), 'Partidas perdidas:', listaOrdenada[i][4].ljust(2, " "),
                  'Partidas empatadas', listaOrdenada[i][5].ljust(2, " "))

def actualizar(directorio,listaUsuarios):
    #Sobreescribo el archivo y lo lleno con la nueva lista, con el usuario nuevo, o la modificacion si ya existia
    a = open(directorio, 'w+')
    for i in range(len(listaUsuarios)):
        a.write(listaUsuarios[i][0] + "," + listaUsuarios[i][1]+ "," + listaUsuarios[i][2] + "," + listaUsuarios[i][3] + "," + listaUsuarios[i][4] + "," + listaUsuarios[i][5] + '\n')
    a.close()

def archivoRandom(f,cantidadUsuarios):
    lista = {}
    #Con este for creo los randoms de cada lista de usuario y los escribo en el archivo con un pase de linea.
    for i in range(cantidadUsuarios):
        nombre = ''.join(random.sample(string.ascii_lowercase, 4))
        puntaje = random.randint(-100,100)
        jugadas = random.randint(0,100)
        ganadas = random.randint(0,jugadas)
        perdidas = jugadas-ganadas
        empatadas = (jugadas-ganadas-perdidas)
        f.write(nombre+","+puntaje.__str__()+","+jugadas.__str__()+","+ganadas.__str__()+","+perdidas.__str__()+","+empatadas.__str__()+'\n')

def mostrar(f):
    #Leo la lista entera y la separo por lineas y despues por comas, la ordeno alfabeticamente y la muestro
    lista = f.readlines()
    lista = [x.strip().split(',') for x in lista]
    listaOrdenada = sorted(lista, key=lambda x: (x[0]))
    for i in range(len(listaOrdenada)):
        print('Nombre:', listaOrdenada[i][0].capitalize().ljust(3, " "),'Puntaje:', listaOrdenada[i][1].ljust(3, " "),
              'Partidas Jugadas:', listaOrdenada[i][2].ljust(3, " "), 'Partidas ganadas:',
              listaOrdenada[i][3].ljust(3, " "), 'Partidas perdidas:', listaOrdenada[i][4].ljust(3, " "),
              'Partidas empatadas', listaOrdenada[i][5].ljust(3, " "))

def leer(f,devolver):
    linea = f.readline()
    linea = linea.strip()
    if linea:
        return linea.split(',')
    else:
        return devolver.split(',')

def grabarNuevo(fNuevo, nombre, puntaje, jugadas, ganadas, perdidas, empatadas):
    fNuevo.write(nombre + ',' + puntaje + ',' + jugadas + ','  + ganadas + ',' + perdidas + ',' + empatadas +'\n')

def aparearArchivos(fUno,fDos,fNuevo):
    nombre, puntaje, jugadas, ganadas, perdidas, empatadas = leer(fUno, ',,,,,')
    nombreDos, puntajeDos, jugadasDos, ganadasDos, perdidasDos, empatadasDos = leer(fDos, ',,,,,')
    while(nombre and nombreDos):
        if(nombre != nombreDos):
            grabarNuevo(fNuevo, nombre, puntaje, jugadas, ganadas, perdidas, empatadas)
            grabarNuevo(fNuevo, nombreDos, puntajeDos, jugadasDos, ganadasDos, perdidasDos, empatadasDos)
            # Vuelvo a leer los Dos
            nombre, puntaje, jugadas, ganadas, perdidas, empatadas = leer(fUno, ',,,,,')
            nombreDos, puntajeDos, jugadasDos, ganadasDos, perdidasDos, empatadasDos = leer(fDos, ',,,,,')
        else:
        # son iguales. Deberia ser una modificacion
            grabarNuevo(fNuevo, nombre, (int(puntaje)+int(puntajeDos)).__str__(), jugadas, (int(ganadas)+int(ganadasDos)).__str__(), perdidas, empatadas)
        # Vuelvo a leer los Dos
            nombre, puntaje, jugadas, ganadas, perdidas, empatadas = leer(fUno, ',,,,,')
            nombreDos, puntajeDos, jugadasDos, ganadasDos, perdidasDos, empatadasDos = leer(fDos, ',,,,,')
# Del while puedo estar saliendo porque encontre el final de ambos archivos
# o porque encontre el de solo uno. Por lo tanto, puede haber registros a
# a procesar y debo hacerlo
    while nombre:
        grabarNuevo(fNuevo, nombre, puntaje, jugadas, ganadas, perdidas, empatadas)
        nombre, puntaje, jugadas, ganadas, perdidas, empatadas = leer(fUno, ',,,,,')
    while nombreDos:
        grabarNuevo(fNuevo, nombreDos, puntajeDos, jugadasDos, ganadasDos, perdidasDos, empatadasDos)
        nombreDos, puntajeDos, jugadasDos, ganadasDos, perdidasDos, empatadasDos = leer(fDos, ',,,,,')

def menu(f,directorio):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Desea: \na)resetear el archivo de usuarios existente\nb)cargar un archivo de usuarios existente\nc)generar un archivo random de usuarios\nd)ver todos los usuarios existentes\ne)Aparear dos archivos de usuario\n")
    opcion = input()
    if opcion == 'a':
        os.system('cls' if os.name == 'nt' else 'clear')
        f = crearArchivo('usuarios.csv')
        input('El archivo fue reseteado')
        cerrar(f)
    elif opcion == 'b':
        # Lo que hago es llamar a actualizar con todos los datos del nuevo archivo usuarios, asi me lo reemplaza por el archivo que usa el programa.
        os.system('cls' if os.name == 'nt' else 'clear')
        ciclo = True
        while(ciclo):
            try:
                print("Ingrese directorio de su archivo de usuarios, con el siguiente formato C:/Users/Juan/Desktop/usuario.csv")
                directorioDos = input()
                fDos = abrir(directorioDos)
                listaUsuarios = leerEntero(fDos)
                actualizar(directorio,listaUsuarios)
                cerrar(fDos)
                cerrar(f)
                f = abrir(directorio)
                ciclo = False
            except Exception:
                print( "No existe tal archivo o el directorio es incorrecto")
    elif opcion == 'c':
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Ingrese cuantos usuarios quiere crear aleatoriamente: ")
        cantidadUsuarios = int(input())
        f = crearArchivo('usuarios.csv')
        archivoRandom(f,cantidadUsuarios)
        cerrar(f)
    elif opcion == 'd':
        os.system('cls' if os.name == 'nt' else 'clear')
        f = abrir(directorio)
        mostrar(f)
        cerrar(f)
    elif opcion == 'e':
        os.system('cls' if os.name == 'nt' else 'clear')
        # Lo que hago es llamar a actualizar con todos los datos del nuevo archivo usuarios, asi me lo reemplaza por el archivo que usa el programa.
        ciclo = True
        while (ciclo):
            try:
                directorioDos = input('Ingrese directorio del archivo a aparear con el actual, con el siguiente formato: C:/Users/Juan/Desktop/usuario.csv')
                #directorioDos = r'C:/Users/Gonzalo/Desktop/Reversi Python/usuariosDos.csv'
                directorioNuevo = 'usuariosNuevos.csv'
                f = abrir(directorio)
                fDos = abrir(directorioDos)
                fNuevo = crearArchivo(directorioNuevo)
                aparearArchivos(f,fDos,fNuevo)
                fNuevo = abrir(directorioNuevo)
                listaUsuarios = leerEntero(fNuevo)
                actualizar(directorio,listaUsuarios)
                cerrar(fDos)
                cerrar(f)
                cerrar(fNuevo)
                f = abrir(directorio)
                input('Apareamiento realizado con exito')
                ciclo = False
            except Exception:
                print("No existe tal archivo o el directorio es incorrecto")

# Funciones____________________________________
def crear_matriz(matriz):
    for i in range(10):
        matriz.append([' '] * 10)


def llenar_matriz(matriz):
    # Pongo en blanco la matriz
    for i in range(10):
        for j in range(10):
            matriz[i][j] = ' '
    # Lleno con las fichas iniciales
    for i in range(1, 9):
        matriz[i][0] = i
        matriz[i][9] = i
        matriz[0][i] = i
        matriz[9][i] = i

    matriz[4][4] = 'B'
    matriz[5][5] = 'B'
    matriz[4][5] = 'N'
    matriz[5][4] = 'N'
def mostrar_matriz(matriz):
    #limpio la pantalla de la terminal sea en windows o linux
    #os.system('cls')
    os.system('cls' if os.name == 'nt' else 'clear')
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

def inicio(nombre, colorJugador, colorPc, turno,usuario,listaUsuarios,f,directorio):
    print('---------------------------')
    print('---------Reversi-----------')
    print('---------------------------')
    print()
    print()
    nombre = 'a'
    while(len(nombre)> 8 or len(nombre)<4):
        nombre = input('Ingresar Nombre de 4 a 8 caracteres: ')
    listaUsuarios = leerEntero(f)
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
        primeraOpcion = input('Bienvenido '+ nombre+ ' desea:\na)Jugar \nb)Administrar usuarios \nc)Ver top ten \nd)Instrucciones \ne)Salir  \nOpcion: ')
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
                turno = 0
                siguiente = 1
        elif (primeraOpcion == 'b'):
                menu(f,directorio)
        elif(primeraOpcion == 'c'):
                os.system('cls' if os.name == 'nt' else 'clear')
                f.close()
                f = abrir(directorio)
                listaUsuarios = leerEntero(f)
                topTen(listaUsuarios)

        elif(primeraOpcion == 'd'):
            os.system('cls' if os.name == 'nt' else 'clear')
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
            ciclo = True
            while (ciclo):
                try:
                    fila = int(input('Posicion de la Fila : '))
                    columna = int(input('Posicion de la Columna : '))
                    if ((0 < fila < 9) and (0 < columna < 9)):
                        ciclo = False

                except ValueError:
                    print('\n\n\nError en valor de la fila intentalo de nuevo.\n\n\n')
                else:
                    print('\n\n\nFuera de rango intentalo de nuevo.\n\n\n')
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
    directorio = 'usuarios.csv'
    try:
        f = abrir(directorio)
    except Exception:
        print("No se encontro ningun archivo de usuarios creado, se creara un nuevo archivo.")
        crearArchivo(directorio)
        f = abrir(directorio)
        pass
    turno = 1
    volverAJugar = 's'
    while (volverAJugar == 's'):
        nombre, colorJugador, colorPc, turno, usuario, listaUsuarios = inicio(nombre, colorJugador, colorPc, turno,usuario, listaUsuarios,f,directorio)
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