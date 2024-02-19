from flask import Flask, render_template, request, send_file
from pytube import YouTube
from moviepy.editor import VideoFileClip
import os
import re

app = Flask(__name__)

# função para remover caracteres especiais
def limpar_nome(nome):
    return re.sub(r'[\\/*?:"<>|]', '', nome)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        return render_template('index.html', url=url)
    return render_template('index.html', url=None)

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    if 'youtube.com' in url or 'youtu.be' in url:
        try:
            yt = YouTube(url)
            titulo_original = yt.title
            titulo_limpo = limpar_nome(titulo_original)
            video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            diretorio_video = os.path.join(os.getcwd(), 'downloads')
            if not os.path.exists(diretorio_video):
                os.makedirs(diretorio_video)
            caminho_video = os.path.join(diretorio_video, f"{titulo_limpo}.mp4")
            video.download(output_path=diretorio_video, filename=f"{titulo_limpo}.mp4")
            video_clip = VideoFileClip(caminho_video)
            audio_clip = video_clip.audio
            diretorio_mp3 = os.path.join(os.getcwd(), 'mp3')
            if not os.path.exists(diretorio_mp3):
                os.makedirs(diretorio_mp3)
            caminho_mp3 = os.path.join(diretorio_mp3, f"{titulo_limpo}.mp3")
            audio_clip.write_audiofile(caminho_mp3)
            return send_file(caminho_mp3, as_attachment=True)
        except Exception as e:
            return render_template('index.html', error=str(e))
    else:
        return render_template('index.html', error='URL inválida. Por favor, insira uma URL do YouTube.')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    
