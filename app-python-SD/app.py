from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle
import io
import threading
import queue

# Autenticación y construcción del servicio de Google Drive
def autenticar_google_drive():
    SCOPES = ['https://www.googleapis.com/auth/drive.readonly']  # Permisos de solo lectura

    creds = None
    # Verificar si ya tenemos credenciales guardadas
    if os.path.exists('xxx.pickle'):
        with open('xxx.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # Si no hay credenciales válidas, pedir al usuario que se autentique
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('xxx.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Guardar las credenciales para la próxima vez
        with open('xxx.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # Construir el servicio de Google Drive
    service = build('drive', 'v3', credentials=creds)
    return service

# Descargar un archivo de Google Drive
def descargar_archivo(service, file_id, nombre_archivo):
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(nombre_archivo, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f"Descargando {nombre_archivo}: {int(status.progress() * 100)}% completado.")
    print(f"Descarga completada: {nombre_archivo}")

# Función del hilo productor (prepara las descargas)
def hilo_productor(queue_archivos):
    # Este hilo puede ser responsable de autenticar y agregar archivos a la cola
    print("Autenticando y preparando archivos para descarga...")
    servicio = autenticar_google_drive()

    # Lista de archivos a descargar (simula que se obtienen dinámicamente)
    archivos = [
        {"file_id": "xxx", "nombre": "archivo1.doc"},
        {"file_id": "xxx", "nombre": "archivo2.pptx"},
        {"file_id": "xxx", "nombre": "archivo3.pdf"},
        {"file_id": "xxx", "nombre": "archivo4.pdf"},
        {"file_id": "xxx", "nombre": "archivo5.rar"},
    ]
    # Agregar archivos a la cola
    for archivo in archivos:
        queue_archivos.put((servicio, archivo))
        print(f"Archivo {archivo['nombre']} agregado a la cola.")

    # Agregar una señal para indicar que ya no habrá más archivos
    queue_archivos.put(None)  # Señal para detener a los consumidores

# Función del hilo consumidor (descarga archivos)
def hilo_consumidor(queue_archivos):
    while True:
        item = queue_archivos.get()  # Obtener un archivo de la cola
        if item is None:  # Verificar la señal de parada
            print("No hay más archivos para descargar. Terminando hilo consumidor.")
            break
        
        servicio, archivo = item
        descargar_archivo(servicio, archivo["file_id"], archivo["nombre"])

# Colocar procesamiento adicional después de la descarga
def procesar_archivo(nombre_archivo):
    print(f"Procesando archivo {nombre_archivo}...")

# Función de procesamiento posterior al descargar (opcional)
def hilo_procesador(queue_procesar):
    while True:
        nombre_archivo = queue_procesar.get()
        if nombre_archivo is None:
            print("No hay más archivos para procesar. Terminando hilo procesador.")
            break
        
        procesar_archivo(nombre_archivo)

if __name__ == '__main__':
    # Cola compartida entre productor y consumidor
    queue_archivos = queue.Queue()

    # Crear y arrancar el hilo productor
    productor = threading.Thread(target=hilo_productor, args=(queue_archivos,))
    productor.start()

    # Crear y arrancar los hilos consumidores (descargas en paralelo)
    consumidores = []
    for _ in range(2):  # Creamos 2 hilos consumidores para descargar en paralelo
        consumidor = threading.Thread(target=hilo_consumidor, args=(queue_archivos,))
        consumidor.start()
        consumidores.append(consumidor)

    # Esperar a que el productor termine
    productor.join()

    # Esperar a que los consumidores terminen
    for consumidor in consumidores:
        consumidor.join()

    print("Todas las descargas han sido completadas.")
