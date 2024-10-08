import cv2  # Biblioteca para manipular vídeo
import os  # Para lidar com diretórios e ficheiros
import tkinter as tk  # Para criar a interface gráfica
from tkinter import filedialog  # Para abrir janelas de diálogo de ficheiros
from tkinter import messagebox  # Para mostrar mensagens ao usuário
from PIL import Image, ImageTk  # Para manipular imagens no tkinter
import threading  # Para rodar a conversão em paralelo
import math  # Para cálculos matemáticos do círculo de progresso

# Variável global para parar a conversão
parar = False

# Função para escolher o vídeo
def escolher_video():
    caminho_video.set(filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")])) 

# Função para escolher a pasta de destino
def escolher_pasta():
    pasta_destino.set(filedialog.askdirectory()) 

# Função para fazer a conversão de MP4 para imagens
def converter_video():
    if not caminho_video.get() or not pasta_destino.get():
        messagebox.showwarning("Atenção", "Escolha o vídeo e a pasta de destino!")
        return

    # Abrir o vídeo com opencv
    video = cv2.VideoCapture(caminho_video.get())
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))  # Obter número total de frames
    contador_frame = 0

    # Verifica se o vídeo foi aberto corretamente
    if not video.isOpened():
        messagebox.showerror("Erro", "Não foi possível abrir o vídeo.")
        return

    while video.isOpened():
        ret, frame = video.read()  # Ler um frame do vídeo
        if not ret:
            break
        
        # Escrever cada frame na pasta destino
        nome_ficheiro = os.path.join(pasta_destino.get(), f"frame_{contador_frame:04d}.png")
        cv2.imwrite(nome_ficheiro, frame)

        # Atualizar progresso
        contador_frame += 1
        progresso = (contador_frame / total_frames) * 100
        tamanho_video = os.path.getsize(caminho_video.get())  # Tamanho do vídeo em bytes
        atualiza_circulo_progresso(progresso, tamanho_video)

        if parar:
            break

    video.release()  # Libertar o vídeo após o processamento
    messagebox.showinfo("Concluído", "Conversão finalizada com sucesso!")

# Função para atualizar o círculo de progresso
def atualiza_circulo_progresso(progresso, tamanho):
    canvas.delete("progress")
    canvas.create_arc(10, 10, 140, 140, start=90, extent=-progresso*3.6, fill="blue", tags="progress")
    
    if tamanho < 1024:
        unidade = f"{tamanho:.2f} KB"
    elif tamanho < 1024**2:
        unidade = f"{tamanho/1024:.2f} MB"
    else:
        unidade = f"{tamanho/(1024**2):.2f} GB"
    
    label_progresso.config(text=f"{unidade} - {progresso:.2f}%")

# Função para iniciar o processo de conversão em uma nova thread
def iniciar_conversao():
    global parar
    parar = False
    threading.Thread(target=converter_video).start()

# Função para parar a conversão
def parar_conversao():
    global parar
    parar = True

# Função para sair da aplicação
def sair():
    janela.quit()

# Criar janela principal
janela = tk.Tk()
janela.title("Conversor MP4 para Imagens")
janela.geometry("400x300")

# Variáveis de caminho e pasta
caminho_video = tk.StringVar()
pasta_destino = tk.StringVar()

# Interface Gráfica
tk.Label(janela, text="Caminho do Vídeo MP4:").pack(pady=5)
tk.Entry(janela, textvariable=caminho_video, width=50).pack()
tk.Button(janela, text="Escolher Vídeo", command=escolher_video).pack(pady=5)

tk.Label(janela, text="Pasta de Destino:").pack(pady=5)
tk.Entry(janela, textvariable=pasta_destino, width=50).pack()
tk.Button(janela, text="Escolher Pasta", command=escolher_pasta).pack(pady=5)

# Botões de controle
tk.Button(janela, text="Converter", command=iniciar_conversao).pack(pady=10)
tk.Button(janela, text="Parar", command=parar_conversao).pack(pady=5)
tk.Button(janela, text="Sair", command=sair).pack(pady=5)

# Círculo de Progresso
canvas = tk.Canvas(janela, width=150, height=150)
canvas.pack()
label_progresso = tk.Label(janela, text="0%")
label_progresso.pack()

janela.mainloop()
