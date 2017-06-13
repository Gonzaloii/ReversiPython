import operator

# Funciones____________
def leer(f):
    #Leo la lista entera y la separo por lineas y despues por comas y la devuelvo
    lista = f.readlines()
    lista = [x.strip().split(',') for x in lista]
    return lista

def topTen(listaUsuarios):
    #Ordeno la lista que paso como parametro por orden de importancia, puntaje, ganadas, jugadas, alfabeticamente. Uso el "-" como reverse
    listaOrdenada = sorted(listaUsuarios, key=lambda x: (-int(x[1]), -int(x[3]), -int(x[2]), (x[0])))
    #Muestro solo los primeros 10
    for i in range(10):
        print('Puntaje:', listaOrdenada[i][1].ljust(2, " "), 'Nombre:', listaOrdenada[i][0].capitalize().ljust(8, " "),
              'Partidas Jugadas:', listaOrdenada[i][2].ljust(2, " "), 'Partidas ganadas:',
              listaOrdenada[i][3].ljust(2, " "), 'Partidas perdidas:', listaOrdenada[i][4].ljust(2, " "),
              'Partidas empatadas', listaOrdenada[i][5].ljust(2, " "))


#Cuerpo principal___________
f = open(r'C:/Users/Gonzalo/Desktop/Reversi Python/usuarios.txt','r+')
listaUsuarios = leer(f)
print(listaUsuarios)
topTen(listaUsuarios)

f.close()