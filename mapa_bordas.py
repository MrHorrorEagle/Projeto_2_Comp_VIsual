"""
Fabio Oliveira da Silva - 10420458
Patrick Rocha de Andrade - 10410902
Mapa de Bordas 3D
-----------------
Esse código lê uma imagem, transforma em escala de cinza e aplica técnicas de detecção de bordas (Sobel, Laplaciano e Canny). 
Em seguida, gera gráficos 2D e 3D das bordas detectadas.
Toda a Navegação é feita em um menu interativo

Dependências:
    pip install opencv-python numpy matplotlib

Uso:
    python mapa_bordas.py

Executável presente no repositório do projeto
"""

import os
import tkinter as tk
from tkinter import filedialog, messagebox

import cv2
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  


# ----------------------------------------------------------------------
# Processamento
# ----------------------------------------------------------------------
def carregar_imagem(caminho):
    """Lê a imagem (aceita caminhos com acentos no Windows)."""
    dados = np.fromfile(caminho, dtype=np.uint8)
    img = cv2.imdecode(dados, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Não foi possível abrir a imagem.")
    return img


def normalizar(arr):
    """Converte qualquer array para 0-255 (uint8) para exibição."""
    arr = np.abs(arr).astype(np.float64)
    if arr.max() > 0:
        arr = arr / arr.max() * 255
    return arr.astype(np.uint8)


def processar(img_bgr, limiar_baixo=50, limiar_alto=150):
    """Retorna um dicionário com todas as etapas do processamento."""
    cinza = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    suave = cv2.GaussianBlur(cinza, (5, 5), 0)

    sobel_x = cv2.Sobel(suave, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(suave, cv2.CV_64F, 0, 1, ksize=3)
    magnitude = np.hypot(sobel_x, sobel_y)
    direcao = np.arctan2(sobel_y, sobel_x)  # em radianos (-pi a pi)
    laplaciano = cv2.Laplacian(suave, cv2.CV_64F, ksize=3)
    canny = cv2.Canny(suave, limiar_baixo, limiar_alto)

    return {
        "original": cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB),
        "cinza": cinza,
        "sobel_x": normalizar(sobel_x),
        "sobel_y": normalizar(sobel_y),
        "magnitude": normalizar(magnitude),
        "direcao": direcao,
        "laplaciano": normalizar(laplaciano),
        "canny": canny,
    }


# ----------------------------------------------------------------------
# Visualização
# ----------------------------------------------------------------------
def mostrar_bordas(res, titulo=""):
    fig, eixos = plt.subplots(2, 4, figsize=(16, 8))
    fig.suptitle(f"Divisão de bordas - {titulo}", fontsize=14)

    paineis = [
        ("Original", res["original"], None),
        ("Escala de cinza", res["cinza"], "gray"),
        ("Sobel X (bordas verticais)", res["sobel_x"], "gray"),
        ("Sobel Y (bordas horizontais)", res["sobel_y"], "gray"),
        ("Magnitude do gradiente", res["magnitude"], "inferno"),
        ("Laplaciano", res["laplaciano"], "gray"),
        ("Canny", res["canny"], "gray"),
    ]
    for ax, (nome, img, cmap) in zip(eixos.flat, paineis):
        ax.imshow(img, cmap=cmap)
        ax.set_title(nome)
        ax.axis("off")

    # Direção do gradiente, mostrando só onde há borda relevante
    ax = eixos.flat[7]
    mascara = res["magnitude"] > 40
    direcao = np.where(mascara, res["direcao"], np.nan)
    im = ax.imshow(direcao, cmap="hsv")
    ax.set_title("Direção das bordas")
    ax.axis("off")
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04, label="ângulo (rad)")

    plt.tight_layout()
    plt.show()


def mostrar_mapa_3d(res, titulo="", max_lado=150):
    mag = res["magnitude"].astype(np.float64)

    # Reduz a resolução para o gráfico 3D ficar leve
    h, w = mag.shape
    escala = min(1.0, max_lado / max(h, w))
    if escala < 1.0:
        mag = cv2.resize(mag, (int(w * escala), int(h * escala)),
                         interpolation=cv2.INTER_AREA)
    mag = cv2.GaussianBlur(mag, (3, 3), 0)

    h, w = mag.shape
    X, Y = np.meshgrid(np.arange(w), np.arange(h))

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection="3d")
    sup = ax.plot_surface(X, Y, mag, cmap="inferno", linewidth=0,
                          antialiased=True, rstride=1, cstride=1)
    ax.set_title(f"Mapa 3D de bordas - {titulo}")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("intensidade da borda")
    ax.invert_yaxis()  # mantém a orientação da imagem
    ax.view_init(elev=55, azim=-60)
    fig.colorbar(sup, ax=ax, shrink=0.5, label="magnitude")
    plt.tight_layout()
    plt.show()


def salvar_resultados(res, pasta, nome_base):
    os.makedirs(pasta, exist_ok=True)
    for chave in ["cinza", "sobel_x", "sobel_y", "magnitude", "laplaciano", "canny"]:
        caminho = os.path.join(pasta, f"{nome_base}_{chave}.png")
        ok, buf = cv2.imencode(".png", res[chave])
        if ok:
            buf.tofile(caminho)
    return pasta


# ----------------------------------------------------------------------
# Menu (interface)
# ----------------------------------------------------------------------
class App:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Mapa de Bordas 3D")
        self.raiz.geometry("380x360")
        self.raiz.resizable(False, False)

        self.caminho = None
        self.resultado = None

        tk.Label(raiz, text="Mapa de Bordas 3D",
                 font=("Arial", 16, "bold")).pack(pady=(15, 5))

        self.lbl_arquivo = tk.Label(raiz, text="Nenhuma imagem selecionada",
                                    fg="gray", wraplength=340)
        self.lbl_arquivo.pack(pady=5)

        # Limiares do Canny
        quadro = tk.Frame(raiz)
        quadro.pack(pady=5)
        tk.Label(quadro, text="Canny baixo").grid(row=0, column=0)
        tk.Label(quadro, text="Canny alto").grid(row=0, column=1)
        self.limiar_baixo = tk.Scale(quadro, from_=0, to=255, orient="horizontal")
        self.limiar_baixo.set(50)
        self.limiar_baixo.grid(row=1, column=0, padx=5)
        self.limiar_alto = tk.Scale(quadro, from_=0, to=255, orient="horizontal")
        self.limiar_alto.set(150)
        self.limiar_alto.grid(row=1, column=1, padx=5)

        opcoes = dict(width=28, pady=3)
        tk.Button(raiz, text="1. Escolher imagem", command=self.escolher, **opcoes).pack(pady=3)
        tk.Button(raiz, text="2. Ver divisão de bordas", command=self.ver_bordas, **opcoes).pack(pady=3)
        tk.Button(raiz, text="3. Ver mapa 3D de bordas", command=self.ver_3d, **opcoes).pack(pady=3)
        tk.Button(raiz, text="4. Salvar imagens de bordas", command=self.salvar, **opcoes).pack(pady=3)
        tk.Button(raiz, text="Sair", command=raiz.destroy, **opcoes).pack(pady=3)

    def escolher(self):
        caminho = filedialog.askopenfilename(
            title="Escolha uma imagem",
            filetypes=[("Imagens", "*.png *.jpg *.jpeg *.bmp *.tif *.tiff *.webp"),
                       ("Todos os arquivos", "*.*")],
        )
        if not caminho:
            return
        try:
            carregar_imagem(caminho)
        except ValueError as e:
            messagebox.showerror("Erro", str(e))
            return
        self.caminho = caminho
        self.resultado = None
        self.lbl_arquivo.config(text=os.path.basename(caminho), fg="black")

    def _processar(self):
        if not self.caminho:
            messagebox.showwarning("Atenção", "Escolha uma imagem primeiro.")
            return None
        img = carregar_imagem(self.caminho)
        self.resultado = processar(img, self.limiar_baixo.get(), self.limiar_alto.get())
        return self.resultado

    def ver_bordas(self):
        res = self._processar()
        if res is not None:
            mostrar_bordas(res, os.path.basename(self.caminho))

    def ver_3d(self):
        res = self._processar()
        if res is not None:
            mostrar_mapa_3d(res, os.path.basename(self.caminho))

    def salvar(self):
        res = self._processar()
        if res is None:
            return
        pasta = filedialog.askdirectory(title="Escolha a pasta para salvar")
        if not pasta:
            return
        nome = os.path.splitext(os.path.basename(self.caminho))[0]
        salvar_resultados(res, pasta, nome)
        messagebox.showinfo("Pronto", f"Imagens salvas em:\n{pasta}")


if __name__ == "__main__":
    raiz = tk.Tk()
    App(raiz)
    raiz.mainloop()
