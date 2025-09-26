#  Búsqueda de sobrevivientes con Drones usando PSO

Este proyecto simula la **coordinación de 10 drones autónomos** para la búsqueda de sobrevivientes en una zona costera inundada después de un tsunami.  
Se utiliza el algoritmo de **Optimización por Enjambre de Partículas (PSO)** para posicionar los drones de forma que se **maximice la probabilidad de encontrar sobrevivientes** en el menor tiempo posible.

---

##  Escenario del Problema

- **Área de búsqueda:** 5 km × 5 km (coordenadas: 0 a 5000 metros).  
- **Número de drones:** 10.  
- **Sensores de detección:** cada dron puede detectar señales de vida en un radio de **200 metros**.  
- **Mapa de probabilidades:** algunas zonas tienen mayor chance de encontrar sobrevivientes.  
- **Tiempo máximo de búsqueda:** 120 minutos.  

El reto es **coordinar los drones** para cubrir las áreas con mayor probabilidad de hallazgo.

---

##  Objetivo

Implementar un algoritmo **PSO (Particle Swarm Optimization)** que:  

1. Coordine la ubicación de los drones.  
2. Maximice la probabilidad de detección de sobrevivientes.  
3. Evite redundancia y optimice el tiempo de búsqueda.  

---

##  Funcionamiento del Código

### 1. Parámetros principales
```python
AREA_SIZE = 5000       # metros
NUM_DRONES = 10        # cantidad de drones
RADIO_DETECCION = 200  # radio de detección de cada dron
MAX_ITER = 100         # iteraciones del PSO
PARTICULAS = 30        # tamaño del enjambre
```

## 2. Mapa de Probabilidades

Se genera un mapa aleatorio donde cada celda tiene un valor de probabilidad asociado a la presencia de sobrevivientes:
```python
def generar_mapa_probabilidades(tamaño=50):
    mapa = np.random.rand(tamaño, tamaño)
    return mapa / np.sum(mapa)
```

El resultado es una matriz normalizada (la suma de todas las probabilidades es 1).

## 3. Función de Fitness

Evalúa qué tan buenas son las posiciones de los drones midiendo la probabilidad cubierta en sus radios de detección:
```python
def fitness(posiciones, mapa):
    # Calcula el área cubierta por los drones
    # Retorna la probabilidad total cubierta
```

Mientras más drones estén en zonas amarillas/claras, mejor será el fitness.

Se penaliza si los drones se concentran en la misma zona.

## 4. Algoritmo PSO

Cada partícula representa un posicionamiento posible de los drones.

El PSO actualiza las posiciones usando tres componentes:

Inercia: mantiene la dirección actual.

Cognitivo: mueve hacia la mejor posición individual encontrada.

Social: mueve hacia la mejor posición global encontrada.
```python
particle.velocity = (
    inertia * particle.velocity
    + cognitive
    + social
)
```

Al final, obtenemos la mejor disposición de los drones.

## 5. Visualización

El mapa se muestra con matplotlib:

Fondo en colores: mapa de probabilidades.

Puntos azules: drones.

Círculos punteados: radios de detección de 200 m.
```python
plt.imshow(mapa.T, origin='lower', cmap='hot', extent=[0, AREA_SIZE, 0, AREA_SIZE])
plt.plot(x, y, 'bo')  # drones
plt.Circle((x, y), RADIO_DETECCION, color='blue', fill=False, linestyle="--")
```


## Conceptos Clave

PSO (Particle Swarm Optimization): algoritmo inspirado en el comportamiento de enjambres (aves, peces, insectos).

Exploración vs Explotación: el enjambre explora varias soluciones y converge a la mejor encontrada.

Fitness: en este caso es la probabilidad acumulada de sobrevivientes cubierta por los drones.


