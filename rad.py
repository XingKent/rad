import tkinter as tk
from tkinter import messagebox
import sqlite3

def conectar():
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pessoas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            idade INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def adicionar_pessoa(nome, idade):
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO pessoas (nome, idade) VALUES (?, ?)", (nome, idade))
    conn.commit()
    conn.close()

def obter_todos():
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pessoas")
    dados = cursor.fetchall()
    conn.close()
    return dados

def atualizar_pessoa(id, nome, idade):
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE pessoas SET nome = ?, idade = ? WHERE id = ?", (nome, idade, id))
    conn.commit()
    conn.close()

def deletar_pessoa(id):
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pessoas WHERE id = ?", (id,))
    conn.commit()
    conn.close()

def janela_adicionar():
    janela.withdraw()
    add = tk.Toplevel()
    centralizar_janela(add, 300, 300)
    add.title("Adicionar Pessoa")

    tk.Label(add, text="Nome:").pack()
    nome = tk.Entry(add)
    nome.pack()

    tk.Label(add, text="Idade:").pack()
    idade = tk.Entry(add)
    idade.pack()

    def salvar():
        if nome.get() and idade.get():
            try:
                adicionar_pessoa(nome.get(), int(idade.get()))
                messagebox.showinfo("Sucesso", "Pessoa adicionada.")
                nome.delete(0, tk.END)
                idade.delete(0, tk.END)
            except ValueError:
                messagebox.showerror("Erro", "Idade precisa ser um número.")
        else:
            messagebox.showwarning("Aviso", "Preencha todos os campos.")

    botoes_frame = tk.Frame(add)
    botoes_frame.pack(pady=30)
    tk.Button(botoes_frame, text="Salvar", command=salvar, width=10).pack(pady=5, padx=10)
    tk.Button(botoes_frame, text="Voltar", command=lambda: [add.destroy(), janela.deiconify()], width=10).pack(side=tk.LEFT, padx=10)

def janela_listar():
    janela.withdraw()
    lista = tk.Toplevel()
    centralizar_janela(lista, 300, 300)
    lista.title("Listar Pessoas")

    dados = obter_todos()

    for item in dados:
        tk.Label(lista, text=f"ID: {item[0]} | Nome: {item[1]} | Idade: {item[2]}").pack()

    tk.Button(lista, text="Voltar", command=lambda: [lista.destroy(), janela.deiconify()], width=10).pack(pady=5)

def janela_atualizar():
    janela.withdraw()
    upd = tk.Toplevel()
    centralizar_janela(upd, 300, 300)
    upd.title("Atualizar Pessoa")

    tk.Label(upd, text="ID da pessoa:").pack()
    id_entry = tk.Entry(upd)
    id_entry.pack()

    tk.Label(upd, text="Novo Nome:").pack()
    nome_entry = tk.Entry(upd)
    nome_entry.pack()

    tk.Label(upd, text="Nova Idade:").pack()
    idade_entry = tk.Entry(upd)
    idade_entry.pack()

    def atualizar():
        try:
            id_val = int(id_entry.get())
            novo_nome = nome_entry.get()
            nova_idade = int(idade_entry.get())
            atualizar_pessoa(id_val, novo_nome, nova_idade)
            messagebox.showinfo("Sucesso", "Pessoa atualizada.")
        except:
            messagebox.showerror("Erro", "Verifique os dados inseridos.")

    tk.Button(upd, text="Atualizar", command=atualizar, width=10).pack(pady=5)
    tk.Button(upd, text="Voltar", command=lambda: [upd.destroy(), janela.deiconify()], width=10).pack()

def janela_deletar():
    janela.withdraw()
    dele = tk.Toplevel()
    centralizar_janela(dele, 300, 300)
    dele.title("Deletar Pessoa")

    tk.Label(dele, text="ID da pessoa para deletar:").pack()
    id_entry = tk.Entry(dele)
    id_entry.pack()

    def deletar():
        try:
            id_val = int(id_entry.get())
            deletar_pessoa(id_val)
            messagebox.showinfo("Sucesso", "Pessoa deletada.")
        except:
            messagebox.showerror("Erro", "ID inválido.")

    tk.Button(dele, text="Deletar", command=deletar, width=10).pack(pady=5)
    tk.Button(dele, text="Voltar", command=lambda: [dele.destroy(), janela.deiconify()], width=10).pack()

def centralizar_janela(janela, largura, altura):
    tela_largura = janela.winfo_screenwidth()
    tela_altura = janela.winfo_screenheight()
    x = (tela_largura // 2) - (largura // 2)
    y = (tela_altura // 2) - (altura // 2)
    janela.geometry(f"{largura}x{altura}+{x}+{y}")

conectar()
janela = tk.Tk()
centralizar_janela(janela, 300, 300)
janela.title("App cadastral")
janela.geometry("300x300")

tk.Label(janela, text="Bem-vindo ao sistema!\nO que deseja fazer?", font=("Arial", 12)).pack(pady=20)

tk.Button(janela, text="Adicionar Pessoa", command=janela_adicionar, width=20).pack(pady=5)
tk.Button(janela, text="Listar Pessoas", command=janela_listar, width=20).pack(pady=5)
tk.Button(janela, text="Atualizar Pessoa", command=janela_atualizar, width=20).pack(pady=5)
tk.Button(janela, text="Deletar Pessoa", command=janela_deletar, width=20).pack(pady=5)

janela.mainloop()