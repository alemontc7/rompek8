# **********************************************************
# * Clase: Agente buscador                                 *
# * Autor: Victor Estevez                                  *
# * Version: v2023.03.29                                   *
# * Descripcion: Implementacion de algoritmos de busqueda  *
# *              sin informacion y con informacion         *
# **********************************************************

import hashlib
from AgenteIA.Agente import Agente
from copy import deepcopy
import time


class AgenteBuscador(Agente):
    def __init__(self):
        Agente.__init__(self)
        self.estado_inicial = None
        self.estado_meta = None
        self.funcion_sucesor = []
        self.tecnica = None
        self.heuristica = None
        self.memo = {}
        self.visitados = set()

    def add_funcion(self, f):
        self.funcion_sucesor.append(f)

    def test_objetivo(self, e):
        return e == self.estado_meta

    def generar_hijos(self, e):
        hijos = []
        for fun in self.funcion_sucesor:
            h = fun(e)
            hijos.append(h)
        return hijos

    def get_costo(self, camino):
        raise Exception("Error: No existe implementacion")

    def get_heuristica(self, camino):
        raise Exception("Error: No existe implementacion")

    def get_funcion_a(self, camino):
        return self.get_costo(camino) + self.get_heuristica(camino) 

    def mide_tiempo(funcion):
        def funcion_medida(*args, **kwards):
            inicio = time.time()
            c = funcion(*args, **kwards)
            print("Tiempo de ejecucion: ", time.time()-inicio)
            return c
        return funcion_medida

    def estado_to_string(self, estado):
        return hashlib.md5(str(estado).encode()).hexdigest()

    @mide_tiempo
    def programa(self):
        #print(f"estado inicial: {self.estado_inicial}, estado meta: {self.estado_meta}")
        frontera = [[self.estado_inicial]]
        contador = 0
        while frontera:
            contador +=1
            if(contador %1000 == 0):
                print(f"tardado {contador}")
            if self.tecnica == "profundidad":
                camino = frontera.pop()
            else:
                camino = frontera.pop(0)
            nodo = camino[-1]
            nodo_str = self.estado_to_string(nodo)
            self.visitados.add(nodo_str)
            if self.test_objetivo(nodo):
                print("Solucion encontrada!!!")
                print(camino)
                self.acciones = camino
                return self.acciones
                break
            else:
                for hijo in self.generar_hijos(nodo):
                    hijo_str = self.estado_to_string(hijo)
                    if hijo_str not in self.visitados:
                        aux = deepcopy(camino)
                        aux.append(hijo)
                        frontera.append(aux)
                if self.tecnica == "costouniforme":
                    frontera.sort(key=lambda tup: self.get_costo(tup))
                elif self.tecnica == "codicioso":
                    frontera.sort(key=lambda tup: self.get_heuristica(tup[-1]))
                elif self.tecnica == "a_estrella":
                    frontera.sort(key=lambda tup: self.get_funcion_a(tup[-1]))
