from pytube import YouTube
from moviepy.editor import VideoFileClip
import os
import re


# função para remover caracteres especiais
def limpar_nome(nome):
    return re.sub(r'[\\/*?:"<>|]', '', nome)

# URL do vídeo do video a ser baixado
url = 'https://www.youtube.com/watch?v=VDLisVhhrh8&list=RDVDLisVhhrh8&start_radio=1'

# instancia um objeto youtube com a URL do vídeo
yt = YouTube(url)

# obtém o título do vídeo e remove caracteres especiais
titulo_original = yt.title
titulo_limpo = limpar_nome(titulo_original)

# escolhe o formato e a qualidade desejada
# exemplo: baixar o vídeo no formato MP4 e na maior resolução possível
video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

# diretório de destino para o vídeo
diretorio_video = os.path.join(os.getcwd(), 'download-auto')

# cria o diretório de destino para o vídeo, se não existir
if not os.path.exists(diretorio_video):
    os.makedirs(diretorio_video)

# baixa o vídeo para o diretório de destino com o nome igual ao título do vídeo
caminho_video = os.path.join(diretorio_video, f"{titulo_limpo}.mp4")
video.download(output_path=diretorio_video, filename=f"{titulo_limpo}.mp4")

print("Vídeo baixado!")

# diretório de destino para o áudio (MP3)
diretorio_mp3 = os.path.join(os.getcwd(), 'mp3')

# criando o diretório de destino para o áudio (MP3), se não existir
if not os.path.exists(diretorio_mp3):
    os.makedirs(diretorio_mp3)

# carrega o vídeo usando o moviepy
video_clip = VideoFileClip(caminho_video)

# extrai o áudio do vídeo
audio_clip = video_clip.audio

# salva o áudio como um arquivo MP3
caminho_mp3 = os.path.join(diretorio_mp3, f"{titulo_limpo}.mp3")
audio_clip.write_audiofile(caminho_mp3)

print(f"{titulo_limpo}, Áudio extraído e salvo como MP3!")