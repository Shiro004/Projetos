import tkinter as tk
from tkinter import ttk, messagebox

# Dicionário de taxas de câmbio fixas
taxas_de_cambio = {
    "USD": {"BRL": 5.27, "EUR": 0.85, "JPY": 110.15, "GBP": 0.74, "CAD": 1.25, "AUD": 1.35},
    "BRL": {"USD": 0.19, "EUR": 0.16, "JPY": 20.90, "GBP": 0.14, "CAD": 0.24, "AUD": 0.26},
    "EUR": {"USD": 1.18, "BRL": 6.19, "JPY": 129.53, "GBP": 0.86, "CAD": 1.47, "AUD": 1.60},
    "JPY": {"USD": 0.0091, "BRL": 0.048, "EUR": 0.0077, "GBP": 0.0066, "CAD": 0.011, "AUD": 0.012},
    "GBP": {"USD": 1.35, "BRL": 7.27, "EUR": 1.17, "JPY": 151.13, "CAD": 1.70, "AUD": 1.86},
    "CAD": {"USD": 0.80, "BRL": 4.32, "EUR": 0.68, "JPY": 89.07, "GBP": 0.59, "AUD": 1.10},
    "AUD": {"USD": 0.74, "BRL": 3.92, "EUR": 0.62, "JPY": 81.02, "GBP": 0.54, "CAD": 0.91},
}

def obter_cotacao():
    try:
        moeda_de = combo_moeda_de.get()
        moeda_para = combo_moeda_para.get()
        quantidade = float(entry_quantidade.get())

        if moeda_de == moeda_para:
            messagebox.showinfo("Informação", "Escolha moedas diferentes para converter.")
            return

        taxa_cambio = taxas_de_cambio.get(moeda_de, {}).get(moeda_para)
        if taxa_cambio is None:
            messagebox.showerror("Erro", "Conversão entre estas moedas não está disponível.")
            return

        resultado = quantidade * taxa_cambio
        label_resultado.config(text=f"{quantidade} {moeda_de} = {resultado:.2f} {moeda_para}")
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira um número válido.")

# Configuração da janela principal
root = tk.Tk()
root.title("Conversor de Moedas")
root.geometry("600x500")  # Define a janela maior
root.configure(bg="#f7f9fc")
root.minsize(500, 400)  # Define o tamanho mínimo da janela

# Estilos de tema e botões arredondados
style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", background="#f7f9fc", foreground="#4a4a4a", font=("Arial", 10))
style.configure("TButton", padding=6, relief="flat", background="#4a90e2", foreground="white", font=("Arial", 10, "bold"))
style.configure("TEntry", padding=6, relief="flat")

# Título
label_titulo = tk.Label(root, text="Conversor de Moedas", font=("Arial", 18, "bold"), bg="#f7f9fc", fg="#4a4a4a")
label_titulo.pack(pady=20)

# Quadro de Entrada da Quantidade com fundo arredondado
frame_quantidade = tk.Frame(root, bg="#ffffff", bd=2, relief="groove")
frame_quantidade.pack(pady=15, padx=30, fill="x", expand=True)

label_quantidade = tk.Label(frame_quantidade, text="Quantidade:", font=("Arial", 10), bg="#ffffff", fg="#4a4a4a")
label_quantidade.pack(side="left", padx=10, pady=10)

entry_quantidade = ttk.Entry(frame_quantidade, font=("Arial", 10))
entry_quantidade.pack(side="right", padx=10, pady=10, fill="x", expand=True)

# Quadro Seletor de Moedas com fundo arredondado
frame_moedas = tk.Frame(root, bg="#ffffff", bd=2, relief="groove")
frame_moedas.pack(pady=15, padx=30, fill="x", expand=True)

label_moeda_de = tk.Label(frame_moedas, text="De:", font=("Arial", 10), bg="#ffffff", fg="#4a4a4a")
label_moeda_de.grid(row=0, column=0, padx=10, pady=10)

combo_moeda_de = ttk.Combobox(frame_moedas, values=list(taxas_de_cambio.keys()), font=("Arial", 10))
combo_moeda_de.grid(row=0, column=1, padx=10)
combo_moeda_de.set("USD")

label_moeda_para = tk.Label(frame_moedas, text="Para:", font=("Arial", 10), bg="#ffffff", fg="#4a4a4a")
label_moeda_para.grid(row=0, column=2, padx=10, pady=10)

combo_moeda_para = ttk.Combobox(frame_moedas, values=list(taxas_de_cambio.keys()), font=("Arial", 10))
combo_moeda_para.grid(row=0, column=3, padx=10)
combo_moeda_para.set("BRL")

# Botão de Conversão
button_converter = tk.Button(root, text="Converter", command=obter_cotacao, bg="#4a90e2", fg="white",
                             font=("Arial", 12, "bold"), bd=0, relief="flat", activebackground="#357ABD",
                             cursor="hand2", padx=10, pady=10)
button_converter.pack(pady=20)

# Resultado com fundo arredondado
frame_resultado = tk.Frame(root, bg="#f0f4f8", bd=2, relief="groove")
frame_resultado.pack(pady=15, padx=30, fill="x", expand=True)

label_resultado = tk.Label(frame_resultado, text="", font=("Arial", 12), bg="#f0f4f8", fg="#4a90e2")
label_resultado.pack(pady=10, padx=10)

# Rodapé
label_rodape = tk.Label(root, text="Conversor Simples de Moedas", font=("Arial", 8), bg="#f7f9fc", fg="#7f8c8d")
label_rodape.pack(side="bottom", pady=10)

# Tornar a janela principal responsiva
root.columnconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

# Executar a aplicação
root.mainloop()
