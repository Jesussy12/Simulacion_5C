import numpy as np
import matplotlib.pyplot as plt

# ----------------------------------------
# CONFIGURACIÓN GENERAL DE LA SIMULACIÓN
# ----------------------------------------

PARTIDOS = 1000               # Número de partidos simulados (Monte Carlo)
TIROS_LAMBDA = 12             # Media de tiros por partido (Poisson)

# Zonas del campo: Probabilidades condicionales de que el tiro sea gol
# Filas: distancia → Corta, Media, Larga
# Columnas: posición → Izquierda, Centro, Derecha
probabilidad_gol = np.array([
    [0.75, 0.70, 0.72],  # Corta distancia
    [0.55, 0.50, 0.53],  # Media distancia
    [0.35, 0.30, 0.33]   # Larga distancia
])

# Nombres para la visualización
distancias = ["Corta", "Media", "Larga"]
posiciones = ["Izquierda", "Centro", "Derecha"]

# ----------------------------------------
# VARIABLES DE CONTROL
# ----------------------------------------

goles_por_zona = np.zeros((3, 3))
atajas_por_zona = np.zeros((3, 3))
total_tiros = 0
total_atajadas = 0

# ----------------------------------------
# SIMULACIÓN MONTE CARLO
# ----------------------------------------

for _ in range(PARTIDOS):

    # Número de tiros por partido (Poisson)
    tiros_partido = np.random.poisson(TIROS_LAMBDA)

    for _ in range(tiros_partido):

        # Seleccionar zona de forma aleatoria
        fila = np.random.randint(0, 3)  # Distancia
        col = np.random.randint(0, 3)   # Posición

        # Probabilidad condicional de gol
        p_gol = probabilidad_gol[fila, col]

        # Distribución Bernoulli: 1 = gol, 0 = atajada
        es_gol = np.random.rand() < p_gol

        if es_gol:
            goles_por_zona[fila, col] += 1
        else:
            atajas_por_zona[fila, col] += 1
            total_atajadas += 1

        total_tiros += 1

# ----------------------------------------
# RESULTADOS NUMÉRICOS
# ----------------------------------------

porcentaje_atajadas = (total_atajadas / total_tiros) * 100

print("======================================")
print("RESULTADOS DE LA SIMULACIÓN DEL PORTERO")
print("======================================")
print(f"Partidos simulados: {PARTIDOS}")
print(f"Total de tiros: {total_tiros}")
print(f"Atajadas: {total_atajadas}")
print(f"Porcentaje de atajadas: {porcentaje_atajadas:.2f}%")

print("\nMatriz de goles por zona:")
print(goles_por_zona)

# ----------------------------------------
# MATRIZ DE CALOR (ZONAS DE PELIGRO)
# ----------------------------------------

plt.figure(figsize=(8,6))
plt.imshow(goles_por_zona, cmap="hot", interpolation="nearest")
plt.colorbar(label="Cantidad de goles")

plt.xticks([0,1,2], posiciones)
plt.yticks([0,1,2], distancias)

plt.title("Matriz de calor: Zonas de peligro (Goles)")
plt.xlabel("Posición del tirador")
plt.ylabel("Distancia del disparo")

plt.tight_layout()
plt.show()

# ----------------------------------------
# MATRIZ DE CALOR DE ATAJADAS (EXTRA)
# ----------------------------------------

plt.figure(figsize=(8,6))
plt.imshow(atajas_por_zona, cmap="Blues", interpolation="nearest")
plt.colorbar(label="Cantidad de atajadas")

plt.xticks([0,1,2], posiciones)
plt.yticks([0,1,2], distancias)

plt.title("Matriz de calor: Zonas de atajadas")
plt.xlabel("Posición del tirador")
plt.ylabel("Distancia del disparo")

plt.tight_layout()
plt.show()