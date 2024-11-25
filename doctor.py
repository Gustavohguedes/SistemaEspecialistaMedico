import tkinter as tk
from tkinter import ttk, messagebox
import json

# Carregar base de conhecimento de um arquivo JSON
def carregar_base_conhecimento(arquivo):
    with open(arquivo, "r") as f:
        return json.load(f)

# Função para calcular ranking de diagnósticos
def diagnosticar_ranking(sintomas_selecionados, base_conhecimento):
    ranking = []
    for diagnostico, sintomas in base_conhecimento.items():
        correspondencias = set(sintomas_selecionados).intersection(sintomas)
        if correspondencias:
            score = len(correspondencias) / len(sintomas)  # Proporção de sintomas correspondentes
            ranking.append((diagnostico, score, list(correspondencias)))

    # Ordenar por pontuação (decrescente)
    ranking.sort(key=lambda x: x[1], reverse=True)
    return ranking

# Função para avaliação ao clicar no botão
def avaliar():
    sintomas_selecionados = {sintomas[i] for i in range(len(sintomas)) if var[i].get()}
    ranking = diagnosticar_ranking(sintomas_selecionados, base_conhecimento)

    if ranking:
        resultado = "Diagnósticos possíveis:\n\n"
        for diagnostico, score, correspondencias in ranking:
            resultado += f"{diagnostico.capitalize()}: {score*100:.1f}% de correspondência ({', '.join(correspondencias)})\n"
    else:
        resultado = "Não foi possível determinar um diagnóstico com base nos sintomas fornecidos."

    messagebox.showinfo("Resultado", resultado)

# Carregar base de conhecimento
base_conhecimento = carregar_base_conhecimento("base_conhecimento.json")

# Sintomas disponíveis
sintomas = sorted({s for sintomas_list in base_conhecimento.values() for s in sintomas_list})

# Interface gráfica com Tkinter
janela = tk.Tk()
janela.title("Sistema Especialista - Diagnóstico Médico")
janela.geometry("500x600")
janela.configure(bg="#f0f0f0")

# Cabeçalho
ttk.Label(janela, text="Diagnóstico Médico", font=("Arial", 18, "bold"), foreground="#333", background="#f0f0f0").pack(pady=10)
ttk.Label(janela, text="Selecione os sintomas abaixo:", font=("Arial", 12), foreground="#555", background="#f0f0f0").pack()

# Frame para sintomas
frame_sintomas = ttk.Frame(janela)
frame_sintomas.pack(fill="both", expand=True, pady=10, padx=10)

canvas = tk.Canvas(frame_sintomas, bg="#f0f0f0")
scrollbar = ttk.Scrollbar(frame_sintomas, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

# Adicionando sintomas com checkboxes
var = [tk.BooleanVar() for _ in sintomas]
for i, sintoma in enumerate(sintomas):
    ttk.Checkbutton(scrollable_frame, text=sintoma.capitalize(), variable=var[i]).pack(anchor="w", pady=2)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Botão de Diagnóstico
botao = ttk.Button(janela, text="Diagnosticar", command=avaliar)
botao.pack(pady=20)

# Rodapé
ttk.Label(janela, text="Desenvolvido por Você", font=("Arial", 10), foreground="#999", background="#f0f0f0").pack(pady=5)

# Inicializar a janela
janela.mainloop()
