import random

# Número de lanzamientos
lanzamientos = 20

# Diccionario para contar frecuencias de cada suma
frecuencias = {i: 0 for i in range(2, 13)}

# Simulación de 20 lanzamientos de dos dados
for _ in range(lanzamientos):
    dado1 = random.randint(1, 6)
    dado2 = random.randint(1, 6)
    suma = dado1 + dado2
    frecuencias[suma] += 1
    print(f"Lanzamiento: dado1={dado1}, dado2={dado2}, suma={suma}")

print("\nResultados:")
for numero, veces in frecuencias.items():
    probabilidad = veces / lanzamientos
    print(f"Número {numero}: {veces} veces → Probabilidad = {probabilidad:.2f}")
