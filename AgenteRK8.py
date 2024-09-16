from copy import deepcopy
from AgenteIA.AgenteBuscador import AgenteBuscador
import pyttsx3
engine = pyttsx3.init()

class AgenteRK8(AgenteBuscador):

    def __init__(self):
        AgenteBuscador.__init__(self)

    def get_costo(self, camino):
        return len(camino) - 1
    
    def get_heuristica(self, camino):
        estado_str = self.estado_to_string(camino)
        if(estado_str in self.memo):
            return self.memo[estado_str]
        else:
            if(self.heuristica == "manhattan"):
                posiciones = {1: [0,0], 2:[0,1], 3:[0,2], 4:[1,0], 5:[1,1], 6:[1,2], 7:[2,0], 8:[2,1], 0:[2,2]}
                calculo = 0
                for i in range(len(camino)):
                    for j in range(len(camino[i])):
                        if(camino[i][j] != 0):
                            posicion_elemento_actual = posiciones[camino[i][j]]
                            if(posicion_elemento_actual != [i, j]):
                                calculo += (abs(posicion_elemento_actual[0] - i) + abs(posicion_elemento_actual[1] - j))
                
                self.memo[estado_str] = calculo
                return calculo
            elif(self.heuristica == "hamming"):
                counter = 0
                acumulador = 0
                for i in range(len(camino)):
                    for j in range(len(camino[0])):
                        counter+=1
                        if(camino[i][j] != counter):
                            if(camino[i][j] == 0 and counter == 9):
                                 continue
                            else:
                                acumulador+=1
                self.memo[estado_str] = acumulador
                return acumulador
            elif(self.heuristica == "ale"):
                suma_diferencias_filas = 0
                for row_1, row_2 in zip(camino, self.estado_meta):
                    suma_fila_estado_actual = sum(num for num in row_1)
                    suma_fila_estado_meta = sum(num for num in row_2)
                    suma_diferencias_filas += abs(suma_fila_estado_actual - suma_fila_estado_meta)
                self.memo[estado_str] = suma_diferencias_filas
                return suma_diferencias_filas

            elif(self.heuristica == "pitagorica"):
                posiciones = {1: [0, 0], 2: [0, 1], 3: [0, 2], 4: [1, 0], 5: [1, 1], 6: [1, 2], 7: [2, 0], 8: [2, 1], 0: [2, 2]}
                suma_distancias = 0
            
                for i in range(len(camino)):
                    for j in range(len(camino[i])):
                        if camino[i][j] != 0:
                            posicion_elemento_actual = posiciones[camino[i][j]]
                            distancia = ((posicion_elemento_actual[0] - i) ** 2 + (posicion_elemento_actual[1] - j) ** 2) ** 0.5
                            suma_distancias += distancia
                self.memo[estado_str] = suma_distancias
                return suma_distancias

    def find_zero(self,mat):
        #print(mat)
        ans = (0,0)
        for i in range(len(mat)):
            for j in range(len(mat[i])):
                if(mat[i][j] == 0):
                    ans = (i, j)
                    break
        return ans

    def is_in_boundaries(self, zero, elem):
        return zero[0] + elem[0] >= 0 and zero[1] + elem[1] >= 0 and zero[0] + elem[0] < 3 and zero[1] + elem[1] < 3

    def make_son(self, mat, zero, elem):
        matias = deepcopy(mat)
        a,b = (zero[0] + elem[0], zero[1] + elem[1])
        aux = matias[a][b]
        matias [zero[0]][zero[1]] = aux
        matias[a][b] = 0
        return matias
    
    def generar_hijos(self, e):
        zero = self.find_zero(e)
        movs = [(0,1), (1,0), (-1,0), (0,-1)]    
        list = [self.make_son(e, zero, elem) for elem in movs if(self.is_in_boundaries(zero, elem))]
        return list


    def encontrar_movimiento(self, matriz1, matriz2):
        for i in range(3):
            for j in range(3):
                if matriz1[i][j] != matriz2[i][j]:
                    if matriz1[i][j] == 0: 
                        numero_movido = matriz2[i][j]
                        if i > 0 and matriz2[i-1][j] == 0:
                            return f"Mueve el {numero_movido} abajo"
                        elif i < 2 and matriz2[i+1][j] == 0:
                            return f"Mueve el {numero_movido} arriba"
                        elif j > 0 and matriz2[i][j-1] == 0:
                            return f"Mueve el {numero_movido} a la derecha"
                        elif j < 2 and matriz2[i][j+1] == 0:
                            return f"Mueve el {numero_movido} a la izquierda"
                    elif matriz2[i][j] == 0:
                        numero_movido = matriz1[i][j]
                        if i > 0 and matriz1[i-1][j] == 0:
                            return f"Mueve el {numero_movido} arriba"
                        elif i < 2 and matriz1[i+1][j] == 0:
                            return f"Mueve el {numero_movido} abajo"
                        elif j > 0 and matriz1[i][j-1] == 0:
                            return f"Mueve el {numero_movido} a la izquierda"
                        elif j < 2 and matriz1[i][j+1] == 0:
                            return f"Mueve el {numero_movido} a la derecha"
        return "Movimiento no identificado"
    
    def encontrar_movimiento_numeral(self, matriz1, matriz2):
        for i in range(3):
            for j in range(3):
                if matriz1[i][j] != matriz2[i][j]:
                    if matriz1[i][j] == 0: 
                        numero_movido = matriz2[i][j]
                        if i > 0 and matriz2[i-1][j] == 0:
                            return (numero_movido, 'abajo')
                        elif i < 2 and matriz2[i+1][j] == 0:
                            return (numero_movido, 'arriba')
                        elif j > 0 and matriz2[i][j-1] == 0:
                            return (numero_movido, 'derecha')
                        elif j < 2 and matriz2[i][j+1] == 0:
                            return (numero_movido, 'izquierda')
                    elif matriz2[i][j] == 0:
                        numero_movido = matriz1[i][j]
                        if i > 0 and matriz1[i-1][j] == 0:
                            return (numero_movido, 'arriba')
                        elif i < 2 and matriz1[i+1][j] == 0:
                            return (numero_movido, 'abajo')
                        elif j > 0 and matriz1[i][j-1] == 0:
                            return (numero_movido, 'izquierda')
                        elif j < 2 and matriz1[i][j+1] == 0:
                            return (numero_movido, 'derecha')
        return None
    

    
    def generar_instrucciones(self):
        instrucciones = []
        for k in range(len(self.acciones) - 1):
            instruccion = self.encontrar_movimiento(self.acciones[k], self.acciones[k + 1])
            instrucciones.append(instruccion)
        return instrucciones
    
    def decir_instruccion(self):
        instruccion = self.generar_instrucciones()[0]
        print(instruccion)
        engine.say(instruccion)
        engine.runAndWait()