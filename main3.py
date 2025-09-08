from busqueda import busca_videos
import subprocess
import os
import sys
import signal
import time
from yt_dlp import YoutubeDL
## clase principal que se encarga de todo el funcionamiento
class Reproductor:
    def __init__(self):
        ## Encargado de mostrar el video
        self.proceso_video = None
        ## Encargado de mostrar los datos
        self.datos_actuales = []
        ## Encargado de la busqueda 
        self.dato_buscado = ""
        ## por defecto se busca de la primera pagina
        self.pagina_busqueda = 1

    def limpiar_terminal(self):
        os.system('clear')

    def banner(self):
        print("▓"*60)
        print("▓" +" " *15 + "Buscador Videos Youtube" +" " *20 + "▓")
        print("▓"*60)
        print()

    ## esta saca los datos del buscador
    def extraer_datos(self,busqueda,pagina):
        try:
            datos = busca_videos(busqueda, pagina)
            return [v[0] for v in datos if v]
        except Exception as e:
            print(f"Error al buscar videos: {e}")
            return []
        
    def mostrar_datos(self,datos):
        if not datos:
            print("busqueda vacia")
            return
        print(f"-----resultados de la busqueda pagina: {self.pagina_busqueda}------")
        print('*'*60)
        for video in datos:
            numero = video.get('numero')

            titulo = video.get('titulo')
            print(f"[{numero}] {titulo}")
        print('*'*60)

    def opciones(self):
        print("\n menu de opciones: ")
        print(" num video -> Reproduce video ")
        print(" 0 -> Siguiente pagina ")
        print(" -1 -> Nueva busqueda")
        print(" 99 -> Salir")
        print('*'*60)

    def sacar_url(self,numero,datos):
        for video in datos:
            if int(video.get('numero'))== numero:
                return video.get('url')
            
    def reproducir(self, url):
        if not url:
            print("URL no válida")
            return False
        try:
            # Configurar yt-dlp directamente en Python
            formato = "best[height<=480][ext=mp4][acodec!=none][vcodec!=none]/best[height<=360]"
            resultado = subprocess.run(['yt-dlp','-f',formato,'-g',url],
                                       capture_output=True,
                                       text=False,
                                       timeout=20)
            if resultado.returncode!=0:
                print("error al obtener el video")
                return False
            video_url = resultado.stdout.strip()
            if not video_url:
                print("error al reproducir el video")

            self.limpiar_terminal()
            self.banner()
            print("="*20)
            print("Reproduciendo video:\n")
            print("="*20)
            print(" q → salir\n")
            print(" f → pantalla completa\n")
            print(" esc → reproducir / pausar\n")
            print("="*20)

            # Llamada a mplayer (debe estar instalado en el sistema host)
            self.proceso_video = subprocess.Popen(
                ["mplayer", "-quiet", "-zoom", video_url],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            self.proceso_video.wait()
            print("Video cerrado correctamente")
            return True

        except subprocess.TimeoutExpired:
            print("Tiempo de espera superado")
        except FileNotFoundError:
            print("No tienes instalado mplayer")
        except Exception as e:
            print(f"Error inesperado: {e}")
        finally:
            self.proceso_video = None

    def busca_por_numero(self, input_):
         while True:
            try:
                return int(input(input_))
            except ValueError:
                print("solo valores numericos validos")
        
    def buscador(self):
        try:
            busqueda = input("Buscador : \n").strip()
            if not busqueda:
                print("busqueda vacia")
                return False
            self.dato_buscado = busqueda
            self.pagina_busqueda = 1
            self.datos_actuales = self.extraer_datos(busqueda,self.pagina_busqueda)
            if not self.datos_actuales:
                print("No se encontraron datos")
                return False
            return True
        except KeyboardInterrupt:
            print("interrupcion de teclado")

    def ejecutar(self):
        self.limpiar_terminal()
        self.banner()
        if not self.buscador():
            return
        while True:
            try:
                self.limpiar_terminal()
                self.banner()
                self.mostrar_datos(self.datos_actuales)
                self.opciones()
                opcion = self.busca_por_numero("Selecciona una opcion del menu: ")
                if opcion == 99:
                    print("cerrando aplicacion")
                    time.sleep(2)
                    self.limpiar_terminal()
                    break
                if opcion == 0:
                    self.pagina_busqueda +=1
                    self.datos_actuales = self.extraer_datos(self.dato_buscado,self.pagina_busqueda)
                if opcion == -1:
                    self.limpiar_terminal()
                    self.banner()
                    if not self.buscador():
                        return
                    continue
                else:
                    url = self.sacar_url(opcion,self.datos_actuales)
                    if url:
                        self.reproducir(url)
                    else:
                        print("error al buscar el video seleccionado")

            except KeyboardInterrupt:
                print("algo salio mal")
            
if __name__ == "__main__":
    repro = Reproductor()
    repro.ejecutar()