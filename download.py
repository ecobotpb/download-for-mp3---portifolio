import tkinter as tk
from tkinter import messagebox
from pytube import YouTube
from moviepy.editor import VideoFileClip
import os
import re

# função para remover caracteres especiais
def limpar_nome(nome):
    return re.sub(r'[\\/*?:"<>|]', '', nome)

# função para baixar o vídeo e extrair o áudio
def baixar_e_extrair():
    url = entry_link.get()  # Obtém o link do vídeo da entrada
    try:
        # Instancia um objeto YouTube com a URL do vídeo
        yt = YouTube(url)
        
        # Obtém o título do vídeo e remove caracteres especiais
        titulo_original = yt.title
        titulo_limpo = limpar_nome(titulo_original)
        
        # Escolhe o formato e a qualidade desejada do vídeo (MP4, maior resolução disponível)
        video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        
        # Diretório de destino para o vídeo
        diretorio_video = os.path.join(os.getcwd(), 'download-auto')
        
        # Cria o diretório de destino para o vídeo, se não existir
        if not os.path.exists(diretorio_video):
            os.makedirs(diretorio_video)
        
        # Baixa o vídeo para o diretório de destino com o nome igual ao título do vídeo
        caminho_video = os.path.join(diretorio_video, f"{titulo_limpo}.mp4")
        video.download(output_path=diretorio_video, filename=f"{titulo_limpo}.mp4")
        
        # Diretório de destino para o áudio (MP3)
        diretorio_mp3 = os.path.join(os.getcwd(), 'mp3')
        
        # Cria o diretório de destino para o áudio (MP3), se não existir
        if not os.path.exists(diretorio_mp3):
            os.makedirs(diretorio_mp3)
        
        # Carrega o vídeo usando o moviepy
        video_clip = VideoFileClip(caminho_video)
        
        # Extrai o áudio do vídeo
        audio_clip = video_clip.audio
        
        # Salva o áudio como um arquivo MP3
        caminho_mp3 = os.path.join(diretorio_mp3, f"{titulo_limpo}.mp3")
        audio_clip.write_audiofile(caminho_mp3)
        
        messagebox.showinfo("Sucesso", "Vídeo baixado e áudio extraído com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

# Cria a janela principal
root = tk.Tk()
root.title("Baixar Vídeo e Extrair Áudio")

# Label e entrada para o link do vídeo
label_link = tk.Label(root, text="Cole o link do vídeo aqui para baixar:")
label_link.pack()
entry_link = tk.Entry(root, width=50)
entry_link.pack()

# Botão para iniciar o processo de download e extração
btn_baixar = tk.Button(root, text="Baixar e Extrair Áudio", command=baixar_e_extrair)
btn_baixar.pack()

# Inicia o loop da interface
root.mainloop()
