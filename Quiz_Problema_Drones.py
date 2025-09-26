import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Parámetros del problema
# -----------------------------
AREA_SIZE = 5000  # metros
NUM_DRONES = 10
RADIO_DETECCION = 200
MAX_ITER = 100
PARTICULAS = 30

# -----------------------------
# Crear mapa de probabilidades
# -----------------------------
def generar_mapa_probabilidades(tamaño=50):
    """Genera un mapa de probabilidades aleatorio normalizado"""
    mapa = np.random.rand(tamaño, tamaño)
    return mapa / np.sum(mapa)

MAPA = generar_mapa_probabilidades()

# -----------------------------
# Función de fitness
# -----------------------------
def fitness(posiciones, mapa):
    tamaño = mapa.shape[0]
    escala = AREA_SIZE / tamaño
    cubierto = np.zeros_like(mapa)

    for (x, y) in posiciones:
        i = int(x / escala)
        j = int(y / escala)
        radio = int(RADIO_DETECCION / escala)

        for dx in range(-radio, radio+1):
            for dy in range(-radio, radio+1):
                if 0 <= i+dx < tamaño and 0 <= j+dy < tamaño:
                    if dx**2 + dy**2 <= radio**2:
                        cubierto[i+dx, j+dy] = 1
    
    return np.sum(mapa * cubierto)

# -----------------------------
# Algoritmo PSO
# -----------------------------
class Particle:
    def __init__(self):
        self.position = np.random.rand(NUM_DRONES, 2) * AREA_SIZE
        self.velocity = np.random.randn(NUM_DRONES, 2)
        self.best_position = self.position.copy()
        self.best_score = -1

def PSO():
    swarm = [Particle() for _ in range(PARTICULAS)]
    global_best_position = None
    global_best_score = -1

    for _ in range(MAX_ITER):
        for particle in swarm:
            score = fitness(particle.position, MAPA)

            if score > particle.best_score:
                particle.best_score = score
                particle.best_position = particle.position.copy()

            if score > global_best_score:
                global_best_score = score
                global_best_position = particle.position.copy()

        for particle in swarm:
            inertia = 0.5
            cognitive = 1.5 * np.random.rand() * (particle.best_position - particle.position)
            social = 1.5 * np.random.rand() * (global_best_position - particle.position)

            particle.velocity = inertia * particle.velocity + cognitive + social
            particle.position = particle.position + particle.velocity

            # Mantener dentro del área
            particle.position = np.clip(particle.position, 0, AREA_SIZE)

    return global_best_position, global_best_score

# -----------------------------
# Ejecutar
# -----------------------------
best_pos, best_score = PSO()
print("Mejores posiciones de drones:\n", best_pos)
print("Probabilidad total cubierta:", best_score)

# -----------------------------
# Visualización
# -----------------------------
def plot_result(mapa, posiciones):
    tamaño = mapa.shape[0]
    escala = AREA_SIZE / tamaño

    plt.figure(figsize=(8, 8))
    plt.imshow(mapa.T, origin='lower', cmap='hot', extent=[0, AREA_SIZE, 0, AREA_SIZE])
    plt.colorbar(label="Probabilidad de sobrevivientes")

    for (x, y) in posiciones:
        circle = plt.Circle((x, y), RADIO_DETECCION, color='blue', fill=False, linestyle="--")
        plt.gca().add_patch(circle)
        plt.plot(x, y, 'bo')

    plt.title("Mapa de búsqueda y posiciones de drones")
    plt.xlabel("X (m)")
    plt.ylabel("Y (m)")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.show()

plot_result(MAPA, best_pos)
