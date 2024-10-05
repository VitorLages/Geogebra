import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image, ImageTk


# Gera o gráfico limitado a 6 em todas as direções, e desenha a partir dos inputs dos pontos
def generate_points_graph(points):
    fig, ax = plt.subplots()
    ax.set_xlim([-6, 6])
    ax.set_ylim([-6, 6])
    ax.grid(True)

    # Plotar os pontos | Scatter posiciona no plano cartesiano os pontos, tendo como parametros as posições (x,y)
    if points:
        for i, point in enumerate(points):
            ax.scatter(point[0], point[1], color='blue')
            ax.text(point[0], point[1], f'{chr(65 + i)}({point[0]:.1f}, {point[1]:.1f})', fontsize=12, color='blue')

    # Salva o gráfico em um formato .png na memória para que não tenha que salvar no disco usando a biblioteca Matplotlib
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)

    return buf


# Gera o gráfico limitado a 6 em todas as direções, e desenha a partir dos inputs dos vetores
def generate_vectors_graph(vectors):
    fig, ax = plt.subplots()
    ax.set_xlim([-6, 6])
    ax.set_ylim([-6, 6])
    ax.grid(True)

    # Desenha os vetores do ponto (x1, y1) até o (x2, y2) também usando a biblioteca Matplotlib
    if vectors:
        for i, vector in enumerate(vectors):
            ax.arrow(vector[0], vector[1], vector[2] - vector[0], vector[3] - vector[1],
                     head_width=0.2, head_length=0.3, fc='red', ec='red')
            ax.text((vector[0] + vector[2]) / 2, (vector[1] + vector[3]) / 2,
                    f'{chr(117 + i)}=({vector[2] - vector[0]:.1f}, {vector[3] - vector[1]:.1f})', fontsize=12,
                    color='red')
    # Salva o gráfico em um formato .png na memória para que não tenha que salvar no disco usando a biblioteca Matplotlib
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)

    return buf


# Através da biblioteca Tkinter desenha as imagens geradas
def show_graphs(points, vectors):
    # Utiliza as funções de gerar pontos e gerar vetores, para transformar em uma imagem para o GUI
    points_img_data = generate_points_graph(points)
    vectors_img_data = generate_vectors_graph(vectors)

    # Converter as imagens para um formato compatível com Tkinter
    points_image = Image.open(points_img_data)
    points_img = ImageTk.PhotoImage(points_image)

    vectors_image = Image.open(vectors_img_data)
    vectors_img = ImageTk.PhotoImage(vectors_image)

    # Exibir as imagens em uma nova janela
    img_window = tk.Toplevel(root)
    img_window.title("Plano Cartesiano - Pontos e Vetores")

    # Exibir os pontos
    points_label = tk.Label(img_window, image=points_img)
    points_label.image = points_img  # Manter a referência
    points_label.pack(side="top", pady=10)

    # Exibir os vetores
    vectors_label = tk.Label(img_window, image=vectors_img)
    vectors_label.image = vectors_img  # Manter a referência
    vectors_label.pack(side="bottom", pady=10)


# Janela de inputs para vetores e pontos | Parte do GUI
def input_window():
    input_window = tk.Toplevel(root)
    input_window.title("Entrada de Pontos e Vetores")

    # Labels para Pontos
    tk.Label(input_window, text="Pontos (máx 5):").grid(row=0, column=0, padx=10, pady=5)

    point_entries = []
    for i in range(5):
        tk.Label(input_window, text=f"Ponto {chr(65 + i)}:").grid(row=i + 1, column=0, padx=10, pady=5)
        x_entry = tk.Entry(input_window, width=5)
        y_entry = tk.Entry(input_window, width=5)
        x_entry.grid(row=i + 1, column=1, padx=5, pady=5)
        y_entry.grid(row=i + 1, column=2, padx=5, pady=5)
        point_entries.append((x_entry, y_entry))

    # Labels para Vetores
    tk.Label(input_window, text="Vetores (máx 4):").grid(row=6, column=0, padx=10, pady=5)

    vector_entries = []
    for i in range(4):
        tk.Label(input_window, text=f"Vetor {chr(117 + i)}:").grid(row=i + 7, column=0, padx=10, pady=5)
        x1_entry = tk.Entry(input_window, width=5)
        y1_entry = tk.Entry(input_window, width=5)
        x2_entry = tk.Entry(input_window, width=5)
        y2_entry = tk.Entry(input_window, width=5)
        x1_entry.grid(row=i + 7, column=1, padx=5, pady=5)
        y1_entry.grid(row=i + 7, column=2, padx=5, pady=5)
        x2_entry.grid(row=i + 7, column=3, padx=5, pady=5)
        y2_entry.grid(row=i + 7, column=4, padx=5, pady=5)
        vector_entries.append((x1_entry, y1_entry, x2_entry, y2_entry))

    # Botão para gerar gráficos
    def generate():
        points = []
        for x_entry, y_entry in point_entries:
            try:
                x = float(x_entry.get())
                y = float(y_entry.get())
                points.append((x, y))
            except ValueError:
                break

        vectors = []
        for x1_entry, y1_entry, x2_entry, y2_entry in vector_entries:
            try:
                x1 = float(x1_entry.get())
                y1 = float(y1_entry.get())
                x2 = float(x2_entry.get())
                y2 = float(y2_entry.get())
                vectors.append((x1, y1, x2, y2))
            except ValueError:
                break

        show_graphs(points, vectors)

    submit_button = tk.Button(input_window, text="Gerar Gráfico", command=generate)
    submit_button.grid(row=12, column=0, columnspan=5, pady=10)


# Inicializar a interface Tkinter
root = tk.Tk()
root.title("Desenhador de Pontos e Vetores")

# Botão para abrir a janela de input
start_button = tk.Button(root, text="Inserir Pontos e Vetores", command=input_window)
start_button.pack(pady=20)

# Iniciar o loop principal da interface
root.mainloop()
