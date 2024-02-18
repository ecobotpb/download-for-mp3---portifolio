import os
import re
from pytube import YouTube
from moviepy.editor import VideoFileClip

# Função para remover caracteres especiais
def limpar_nome(nome):
    return re.sub(r'[\\/*?:"<>|]', '', nome)

# URL do vídeo do YouTube que você deseja baixar
url = 'https://www.youtube.com/watch?v=VDLisVhhrh8&list=RDVDLisVhhrh8&start_radio=1'

# Instancia um objeto YouTube com a URL do vídeo
yt = YouTube(url)

# Obtém o título do vídeo e remove caracteres especiais
titulo_original = yt.title
titulo_limpo = limpar_nome(titulo_original)

# Escolhe o formato e a qualidade desejada
# Exemplo: baixar o vídeo no formato MP4 e na maior resolução possível
video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

# Diretório de destino para o vídeo
diretorio_video = os.path.join(os.getcwd(), 'download-auto')

# Cria o diretório de destino para o vídeo, se não existir
if not os.path.exists(diretorio_video):
    os.makedirs(diretorio_video)

# Baixa o vídeo para o diretório de destino com o nome igual ao título do vídeo
caminho_video = os.path.join(diretorio_video, f"{titulo_limpo}.mp4")
video.download(output_path=diretorio_video, filename=f"{titulo_limpo}.mp4")

print("Vídeo baixado!")

# Diretório de destino para o áudio (MP3)
diretorio_mp3 = os.path.join(os.getcwd(), 'mp3')

# Cria o diretório de destino para o áudio (MP3), se não existir
if not os.path.exists(diretorio_mp3):
    os.makedirs(diretorio_mp3)

# Carrega o vídeo usando o MoviePy
video_clip = VideoFileClip(caminho_video)

# Extrai o áudio do vídeo
audio_clip = video_clip.audio

# Salva o áudio como um arquivo MP3
caminho_mp3 = os.path.join(diretorio_mp3, f"{titulo_limpo}.mp3")
audio_clip.write_audiofile(caminho_mp3)

print(f"{titulo_limpo}, Áudio extraído e salvo como MP3!")
