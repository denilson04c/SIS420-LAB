from busquedas_biblioteca import *

#INICIO = (4, 1, 0, 2, 7, 3, 8, 5, 6)
#OBJETIVO = (1, 2, 3, 4, 5, 6, 7, 8, 0)
INICIO = ( 1, 0, 2, 3, 4, 5)
OBJETIVO = (1, 2, 3, 4, 5, 0)

def encontrar_ubicacion(filas, elemento_a_encontrar):
    '''Encuentra la posicion de una pieza en el puzzle.
       Devuelve una tupla: fila, columna'''
    for infi, elemento in enumerate(filas):
        if elemento == elemento_a_encontrar:
            return infi // 3, infi % 2


# Se crea un cache para las posiciones del estado_objetivo position de cada piesa,
# para no tener que recalcularlos cada vez

posiciones_objetivo = {}
filas_objetivo = {str(c) for c in OBJETIVO}

for numero in '123450':
    posiciones_objetivo[numero] = encontrar_ubicacion(filas_objetivo, numero)


class PuzzleProblema(Problema):
    def __init__(self, estado_inicial, estado_objetivo=(1, 2, 3, 4, 5, 0)):
        """ Define estado_objetivo estado and initialize a problem """
        self.estado_inicial = estado_inicial
        self.estado_objetivo = estado_objetivo
        Problema.__init__(self, estado_inicial, estado_objetivo)

    def encontrar_cuadro_vacio(self, estado):
        """Devuelve el indice del cuadrado vacio en un estado"""
        return estado.index(0)

    def acciones(self, estado):
        """Devuelve las acciones que pueden se ejecutadas en un estado.
        El resultado sera una lista, ya que solo hay cuatro acciones posibles
        en un determinado estado."""

        acciones_posibles = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        indice_cuadro_vacio = self.encontrar_cuadro_vacio(estado)

        """se deshabilita el movimiento a la izquierda si el indice_cuadro_vacio(numero de la posicion del estado vacio)
        llega al extremo lateral izquierda, 
        con modulo 2==0 que evita a las posiciones 0 ,2 ,4 puedan moverse a la izquierda"""
        if indice_cuadro_vacio % 2 == 0:
            acciones_posibles.remove('LEFT')
            #print(indice_cuadro_vacio,acciones_posibles,"izquierda")

        """cuando se llega al limite superior las posiones 0, 1 no pueden continuar moviendose hacia arriba"""
        if indice_cuadro_vacio < 2:
            acciones_posibles.remove('UP')
            #print(indice_cuadro_vacio, acciones_posibles,"arriba")

        """se deshabilita el moviminento a la derecha si el indice_cuadro_vacio(numero de la posicion del estado vacio)
        llega al extremo lateral derecha, 
        con modulo 2==1 que evita a las posiciones 1 ,2 ,5 puedan moverse a la derecha"""
        if indice_cuadro_vacio % 2 == 1:
            acciones_posibles.remove('RIGHT')
            #print(indice_cuadro_vacio, acciones_posibles,"derecha")

        """cuando se llega al limite inferios las posiones 4, 5 no pueden continuar moviendose hacia abajo"""
        if indice_cuadro_vacio > 3:
            acciones_posibles.remove('DOWN')
        return acciones_posibles


    def resultado(self, estado, accion):
        """Dado un estado y accion, devuelve un nuevo estado que es resultado de ejecutar la accion.
        Accion es asumida para
        Se asume que la acción es un accion válido en el estado """

        # vacio es el indice del cuadrado en blanco
        indice_cuadro_vacio = self.encontrar_cuadro_vacio(estado)
        estado_nuevo = list(estado)
        """dimension de los moviminetos en el puzzle """
        delta = {'UP': -2, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
        indice_vecino = indice_cuadro_vacio + delta[accion]
        estado_nuevo[indice_cuadro_vacio], estado_nuevo[indice_vecino] = estado_nuevo[indice_vecino], estado_nuevo[
            indice_cuadro_vacio]

        return tuple(estado_nuevo)

    def es_objetivo(self, estado):
        '''Devuelve verdadero si un estado es estado objetivo.'''
        return estado == self.estado_objetivo

    def costo(self, estado1, accion, estado2):
        '''Devuelve el costo de ejecutar una accion. '''
        return 1

    def comprobar_solubilidad(self, estado):
        """ Verifica si estado es soluble """

        inversion = 0
        for i in range(len(estado)):
            for j in range(i + 1, len(estado)):
                if (estado[i] > estado[j]) and estado[i] != 0 and estado[j] != 0:
                    inversion += 1

        return inversion % 2 == 0

    def h(self, nodo):
        """ Devuelve un valor de heuristica para un estado.
        La funcion heuristica usada es:
        h(n) = cantidad de cuadros mal ubicados"""

        return sum(s != g for (s, g) in zip(nodo.estado, self.estado_objetivo))

puzzle = PuzzleProblema(INICIO, OBJETIVO)

""" Se envia la posicion Inicial y el Objetivo que se busca"""
def test_busqueda_a_estrella():
    return busqueda_a_estrella(puzzle)


def main():
    """se halla la solucion por la busqueda A*"""
    nodo_solucion = test_busqueda_a_estrella()

    # Mostrar resultado
    resultado = []
    nodo = nodo_solucion
    while nodo.padre is not None:
        resultado.append(nodo.estado)
        nodo = nodo.padre
    resultado.append(INICIO)
    resultado.reverse()
    cont=0
    for e in resultado:
        print("movimento nro: ",cont)
        print(e[:2])
        print(e[2:4])
        print(e[4:])
        print('\n')
        cont=cont+1
    print("Número de movimientos: ",cont-1)

if __name__ == '__main__':
    main()