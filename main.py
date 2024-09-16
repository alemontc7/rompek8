from Tablero import Tablero
from AgenteRK8 import AgenteRK8
import random

def es_soluble(estado):
    plano = [num for fila in estado for num in fila if num != 0]

    inversiones = 0
    for i in range(len(plano)):
        for j in range(i + 1, len(plano)):
            if plano[i] > plano[j]:
                inversiones += 1

    return inversiones % 2 == 0

def generar_estado_inicial_soluble():
    while True:
        numeros = list(range(9))  
        random.shuffle(numeros)  

        matriz = [numeros[i:i + 3] for i in range(0, 9, 3)] 

        if es_soluble(matriz):   
            return matriz        

if __name__ == "__main__":
    juego = Tablero()
    juanito = AgenteRK8()
    estado = generar_estado_inicial_soluble()
    print(f"Estado inicial soluble generado: {estado}")

    juanito.estado_inicial = estado
    juanito.estado_meta = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    juego.insertar(juanito)
    juego.ejecutar()
