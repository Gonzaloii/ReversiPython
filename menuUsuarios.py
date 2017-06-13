import random, string
#Funciones
def abrir(directorio):
    f = open(directorio, 'r+')
    return f

def cerrar(f):
    f.close()

def cargarArchivo(directorio):
    f = open(directorio, 'r+')
    return f

def crearArchivo(directorio):
    f = open(directorio,'w+')
    return f

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
    f.close

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
#Apareo de Archivos
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

def menu(f):
    print("Desea: a)resetear el archivo de usuarios existente b)cargar un archivo de usuarios existente c)generar un archivo random de usuarios d)ver todos los usuarios existentes")
    opcion = input()
    if opcion == 'a':
        crearArchivo(r'C:/Users/Gonzalo/Desktop/Reversi Python/usuarios.txt')
    elif opcion == 'b':
        print("Ingrese directorio de su archivo de usuarios")
        directorio = input()
        cerrar(f)
        f = cargarArchivo(directorio)
    elif opcion == 'c':
        print("Ingrese cuantos usuarios quiere crear aleatoriamente: ")
        cantidadUsuarios = int(input())
        f = crearArchivo(r'C:/Users/Gonzalo/Desktop/Reversi Python/usuarios.txt')
        archivoRandom(f,cantidadUsuarios)
    elif opcion == 'd':
        mostrar(f)

#Cuerpo principal______
directorio = r'C:/Users/Gonzalo/Desktop/Reversi Python/usuarios.txt'
directorioDos = r'C:/Users/Gonzalo/Desktop/Reversi Python/usuariosDos.txt'
directorioNuevo = r'C:/Users/Gonzalo/Desktop/Reversi Python/usuariosNuevos.txt'
#try:
f = abrir(directorio)
fDos = abrir(directorioDos)
fNuevo = crearArchivo(directorioNuevo)
aparearArchivos(f,fDos,fNuevo)
#menu(f)
cerrar(f)
cerrar(fDos)
cerrar(fNuevo)
#except Exception:
 #   print("No se encontro ningun archivo de usuarios creado, se creara un nuevo archivo.")
  #  crearArchivo(directorio)
   # pass

