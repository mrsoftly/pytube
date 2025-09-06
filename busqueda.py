from bs4 import BeautifulSoup
import requests
from classes import Videos
def busca_videos(input_, pages):
    url = "https://yewtu.be/"
    search = "search?q="
    page = "&page="
    url_final = url + search + input_ + page + str(pages)
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/117.0.0.0 Safari/537.36"
    }
    
    respuesta = requests.get(url_final, headers=headers)
    respuesta.encoding = "utf-8"
    if respuesta.status_code != 200:
        return f"Error: {respuesta.status_code} - algo salió mal"
    
    datos = BeautifulSoup(respuesta.text, 'html.parser')
    video_cards = datos.find_all("div", class_="video-card-row")
    
    resultados = []
    numero = 1

    for card in video_cards:
        a_tag = card.find("a")
        if not a_tag:
            continue
        
        p_tag = a_tag.find('p')
        if not p_tag:
            continue
        
        titulo = p_tag.text.strip()
        # Evitar errores de codificación
        titulo = titulo.encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')
        tit = titulo.split(",")[0] if "," in titulo else titulo
        
        video_url = a_tag.get("href")
        if video_url and '/watch?v=' in video_url:
            video = Videos(numero, tit, video_url)
            resultados.append(video.listar())
            numero += 1

    return resultados
