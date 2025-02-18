from tkinter import *
from tkinter import Tk, ttk, filedialog
from PIL import ImageTk, Image, ImageEnhance
import cv2 
import os

#cores no modo Dark
cor_fundo = "#1e1e1e" #modo dark
cor_texto = "#ffffff" #Texto branco
cor_destaque = "#FF1493" #rosa de destaque
cor_botao = "#473C8B" #roxo azulado
cor_botao1 = "#0000CD" #Azul 
cor_botao2 = "#8B3A62" #rosa escuro

# aqui estou criando a janela
janela = Tk()
janela.title("Conversor de Esboço a Lapis")
janela.geometry('450x550')
janela.configure(background=cor_fundo)
janela.resizable(width=FALSE, height=FALSE)

# variaveis globais
global imagem_original, imagem_convertida
imagem_original = None
imagem_convertida = None

# funcao para escolher a imagem
def escolher_imagem():
    global imagem_original
    caminho =  filedialog.askopenfilename()
    if caminho:
        imagem_original = Image.open(caminho)
        imagem_preview = imagem_original.resize((200,200))
        imagem_preview = ImageTk.PhotoImage(imagem_preview)
        l_preview_original.configure(image=imagem_preview)
        l_preview_original.image = imagem_preview

#funcao para converter a imagem
def converter_imagem(event=None):
    global imagem_original, imagem_convertida
    if imagem_original is None:
        return
    #ajustes do usuario
    r = s_intensidade.get()
    brilho = s_brilho.get() / 100
    contraste = s_contraste.get() / 100

    #conversao para desenho a lapis
    imagem_cv = cv2.cvtColor(cv2.imread(imagem_original.filename), cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(imagem_cv,(21,21), 0)
    sketch = cv2.divide(imagem_cv, blur, scale=r)


    # ajustar brilhoe contrate
    pil_sketch = Image.fromarray(sketch)
    enhancer_brilho = ImageEnhance.Brightness(pil_sketch)
    pil_sketch = enhancer_brilho.enhance(brilho)
    enhancer_contraste = ImageEnhance.Contrast(pil_sketch)
    pil_sketch = enhancer_contraste.enhance(contraste)


    imagem_convertida = pil_sketch
    imagem_preview = imagem_convertida.resize((200,200))
    imagem_preview = ImageTk.PhotoImage(imagem_preview)
    l_preview_convertida.configure(image=imagem_preview)
    l_preview_convertida.image = imagem_preview

# funcao para salvar a imagem convertida 
def salvar_imagem():
    if imagem_convertida:
        caminho = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if caminho:
            imagem_convertida.save(caminho)

frame_top=Frame(janela, width=450, height=50, bg=cor_fundo)
frame_top.grid(row=0, column=0, padx=10, pady=5)

frame_preview=Frame(janela, width=450, height=220, bg=cor_fundo)
frame_preview.grid(row=1, column=0, padx=10, pady=5)

frame_controls=Frame(janela, width=450, height=226, bg=cor_fundo)
frame_controls.grid(row=2, column=0, padx=10, pady=5)

#esses são logo e titulo
logo = Label(frame_top, text="Conversor para Desenho a Lapis", font=("Arial", 16, "bold"), bg=cor_fundo, fg=cor_texto)
logo.pack()

# previews
l_preview_original = Label(frame_preview, text="Previa Original", font=("Arial", 12), bg=cor_fundo, fg=cor_destaque)
l_preview_original.place(x=30, y=10)

l_preview_convertida = Label(frame_preview, text="Previa Convertida", font=("Arial", 12), bg=cor_fundo, fg=cor_destaque)
l_preview_convertida.place(x=240, y=10)

# Controles
ttk.Label(frame_controls, text="Intensidade", background=cor_fundo, foreground=cor_texto).place(x=10, y=10)
s_intensidade = Scale(frame_controls, command=converter_imagem, from_=50, to=300, orient=HORIZONTAL, length=200, bg=cor_fundo, fg=cor_texto)
s_intensidade.set(120)
s_intensidade.place(x=10, y=30)

ttk.Label(frame_controls, text="Brilho", background=cor_fundo, foreground=cor_texto).place(x=10, y=80)
s_brilho = Scale(frame_controls, command=converter_imagem, from_=50, to=200, orient=HORIZONTAL, length=200, bg=cor_fundo, fg=cor_texto)
s_brilho.set(100)
s_brilho.place(x=10, y=100)

ttk.Label(frame_controls, text="Contraste", background=cor_fundo, foreground=cor_texto).place(x=10, y=150)
s_contraste = Scale(frame_controls, command=converter_imagem, from_=50, to=200, orient=HORIZONTAL, length=200, bg=cor_fundo, fg=cor_texto)
s_contraste.set(100)
s_contraste.place(x=10, y=170)

# botoes
b_escolher = Button(janela, command=escolher_imagem, text="Escolher Imagem", bg=cor_botao, fg=cor_texto, font=("Arial", 10, ), width=15)
b_escolher.place(x=20, y=500)

b_salvar = Button(janela, command=salvar_imagem, text="Salvar imagem", bg=cor_botao2, fg=cor_texto, font=("Arial", 10, ), width=15)
b_salvar.place(x=300, y=500)


estilo = ttk.Style()
estilo.theme_use("clam")

janela.mainloop()