
# Clase Videos
class Videos:
    def __init__(self, numero, titulo, url):
        self.numero = numero
        self.titulo = titulo
        self.video = url
    def listar(self):
        videos = []
        videos.clear()
        videos.append({
            'numero': self.numero,
            'titulo': self.titulo,
            'url': f"https://www.youtube.com{self.video}"
        })
        return videos
    
    def guardar(self):
        return {
            'numero': self.numero,
            'titulo': self.titulo,
            'url': f"https://www.youtube.com{self.video}"
        }
    