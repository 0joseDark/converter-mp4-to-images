import cv2  # Biblioteca para manipular vídeo
import os  # Para lidar com diretórios e ficheiros
import tkinter as tk  # Para criar a interface gráfica
from tkinter import filedialog  # Para abrir janelas de diálogo de ficheiros
from tkinter import messagebox  # Para mostrar mensagens ao usuário
from tkinter import ttk  # Para criar a barra de progresso
import threading  # Para rodar a conversão em paralelo
import math  # Para cálculos matemáticos do círculo de progresso

# Variável global para parar a conversão
parar = False

# Função para escolher o vídeo
def escolher_video():
    caminho_video.set(filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")])) 
    tamanho_video.set(os.path.getsize(caminho_video.get()))  # Obter tamanho do vídeo em bytes

# Função para escolher a pasta de destino
def escolher_pasta():
    pasta_destino.set(filedialog.askdirectory()) 

# Função para converter o tamanho em bytes para GB, MB, KB
def formatar_tamanho(tamanho_bytes):
    if tamanho_bytes >= 1e9:
        return f"{tamanho_bytes / 1e9:.2f} GB"
    elif tamanho_bytes >= 1e6:
        return f"{tamanho_bytes / 1e6:.2f} MB"
    elif tamanho_bytes >= 1e3:
        return f"{tamanho_bytes / 1e3:.2f} KB"
    else:
        return f"{tamanho_bytes} bytes"

# Função para fazer a conversão de MP4 para imagens
def converter_video():
    global parar
    if not caminho_video.get() or not pasta_destino.get():
        messagebox.showwarning("Atenção", "Escolha o vídeo e a pasta de destino!")
        return

    # Abrir o vídeo com opencv
    video = cv2.VideoCapture(caminho_video.get())
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))  # Obter número total de frames
    contador_frame = 0
    tamanho_acumulado_frames = 0  # Para contar o tamanho das imagens criadas

    # Verifica se o vídeo foi aberto corretamente
    if not video.isOpened():
        messagebox.showerror("Erro", "Não foi possível abrir o vídeo.")
        return

    while video.isOpened() and not parar:  # Loop até o fim do vídeo ou até a conversão ser interrompida
        ret, frame = video.read()  # Ler um frame do vídeo
        if not ret:
            break
        
        # Escrever cada frame na pasta destino
        nome_ficheiro = os.path.join(pasta_destino.get(), f"frame_{contador_frame:04d}.png")
        cv2.imwrite(nome_ficheiro, frame)
        
        # Contabilizar o tamanho do frame salvo
        tamanho_acumulado_frames += os.path.getsize(nome_ficheiro)

        # Atualizar progresso
        contador_frame += 1
        progresso = (contador_frame / total_frames) * 100
        atualiza_progresso(progresso, tamanho_acumulado_frames)

    video.release()  # Libertar o vídeo após o processamento
    if not parar:
        messagebox.showinfo("Concluído", "Conversão finalizada com sucesso!")
    parar = False  # Resetar o estado de parada

# Função para atualizar o progresso (círculo e barra de progresso)
def atualiza_progresso(progresso, tamanho_acumulado_frames):
    # Atualizar círculo de progresso
    canvas.delete("progress")
    canvas.create_arc(10, 10, 140, 140, start=90, extent=-progresso*3.6, outline="blue", width=10, tags="progress")
    
    # Atualizar barra de progresso
    barra_progresso['value'] = progresso
    
    # Exibir progresso em porcentagem
    label_progresso.config(text=f"{progresso:.2f}%")
    
    # Exibir tamanho acumulado dos frames convertidos
    label_tamanho_frames.config(text=f"Frames convertidos: {formatar_tamanho(tamanho_acumulado_frames)}")

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
janela.geometry("400x400")

# Variáveis de caminho e pasta
caminho_video = tk.StringVar()
pasta_destino = tk.StringVar()
tamanho_video = tk.IntVar()

# Interface Gráfica
tk.Label(janela, text="Caminho do Vídeo MP4:").pack(pady=5)
tk.Entry(janela, textvariable=caminho_video, width=50).pack()
tk.Button(janela, text="Escolher Vídeo", command=escolher_video).pack(pady=5)

tk.Label(janela, text="Pasta de Destino:").pack(pady=5)
tk.Entry(janela, textvariable=pasta_destino, width=50).pack()
tk.Button(janela, text="Escolher Pasta", command=escolher_pasta).pack(pady=5)

# Exibir o tamanho do vídeo
tk.Label(janela, text="Tamanho do Vídeo:").pack(pady=5)
label_tamanho_video = tk.Label(janela, textvariable=tamanho_video)
label_tamanho_video.pack()

# Botões de controle
tk.Button(janela, text="Converter", command=iniciar_conversao).pack(pady=10)
tk.Button(janela, text="Parar", command=parar_conversao).pack(pady=5)
tk.Button(janela, text="Sair", command=sair).pack(pady=5)

# Círculo de Progresso
canvas = tk.Canvas(janela, width=150, height=150)
canvas.pack()
label_progresso = tk.Label(janela, text="0%")
label_progresso.pack()

# Barra de Progresso
barra_progresso = ttk.Progressbar(janela, orient="horizontal", length=300, mode="determinate")
barra_progresso.pack(pady=10)

# Exibir o tamanho acumulado das frames convertidas
label_tamanho_frames = tk.Label(janela, text="Frames convertidos: 0 bytes")
label_tamanho_frames.pack(pady=5)

janela.mainloop()
