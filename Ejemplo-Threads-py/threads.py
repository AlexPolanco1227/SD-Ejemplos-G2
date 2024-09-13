import threading
import time
import random

# Definimos una clase para el plato
class Plato:
    def __init__(self, nombre, cantidad):
        self.nombre = nombre
        self.cantidad = cantidad
        self.lock = threading.Lock()  # Cada plato tiene su propio candado para control de acceso

# Array de platos disponibles
platos = [
    Plato('Pizza', 3),  # Solo hay 3 pizzas disponibles
    Plato('Hamburguesa', 2),  # Solo hay 2 hamburguesas disponibles
    Plato('Ensalada', 1)  # Solo 1 ensalada disponible
]

# Función que simula un cliente haciendo un pedido
def hacer_pedido(plato, cliente_id):
    while True:
        time.sleep(random.uniform(0.1, 1))  # Simulamos el tiempo que tarda en hacer el pedido
        # Intentamos adquirir el lock para asegurarnos que solo un hilo modifica la cantidad
        with plato.lock:
            if plato.cantidad > 0:
                plato.cantidad -= 1
                print(f"Cliente {cliente_id} ha pedido {plato.nombre}. Quedan {plato.cantidad} disponibles.")
            else:
                print(f"Cliente {cliente_id} intentó pedir {plato.nombre}, pero ya no está disponible.")
                break

# Función que simula varios clientes haciendo pedidos en paralelo
def pedidos_concurrentes():
    hilos = []
    
    # Creamos 10 clientes que intentarán hacer pedidos
    for i in range(10):
        # Cada cliente intenta pedir un plato al azar
        plato_escogido = random.choice(platos)
        hilo = threading.Thread(target=hacer_pedido, args=(plato_escogido, i))
        hilos.append(hilo)
        hilo.start()

    # Esperamos a que todos los hilos terminen
    for hilo in hilos:
        hilo.join()

# Ejecutamos la simulación
pedidos_concurrentes()
