import tkinter as tk
from tkinter import messagebox

def calcular_investimento():
    try:
        # Capturar valores de entrada
        valor_inicial = float(entry_valor_inicial.get())
        taxa_juros = float(entry_taxa_juros.get())
        tempo = int(entry_tempo.get())

        # Calcular o montante com juros compostos
        montante_final = valor_inicial * (1 + taxa_juros / 100) ** tempo

        # Exibir o resultado
        label_resultado.config(text=f"Montante Final: R$ {montante_final:.2f}")
    except ValueError:
        messagebox.showerror("Erro de entrada", "Por favor, insira valores válidos.")

# Configuração da janela principal
root = tk.Tk()
root.title("Calculadora de Investimentos")
root.geometry("400x300")

# Título
label_titulo = tk.Label(root, text="Calculadora de Investimentos", font=("Arial", 16))
label_titulo.pack(pady=10)

# Entrada do Valor Inicial
label_valor_inicial = tk.Label(root, text="Valor Inicial (R$):")
label_valor_inicial.pack()
entry_valor_inicial = tk.Entry(root)
entry_valor_inicial.pack()

# Entrada da Taxa de Juros
label_taxa_juros = tk.Label(root, text="Taxa de Juros (% ao mês):")
label_taxa_juros.pack()
entry_taxa_juros = tk.Entry(root)
entry_taxa_juros.pack()

# Entrada do Tempo de Investimento
label_tempo = tk.Label(root, text="Tempo de Investimento (meses):")
label_tempo.pack()
entry_tempo = tk.Entry(root)
entry_tempo.pack()

# Botão de Calcular
button_calcular = tk.Button(root, text="Calcular", command=calcular_investimento)
button_calcular.pack(pady=10)

# Resultado
label_resultado = tk.Label(root, text="Montante Final: R$", font=("Arial", 14))
label_resultado.pack(pady=10)

# Executar a aplicação
root.mainloop()
