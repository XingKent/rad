import tkinter as tk
from tkinter import messagebox
import sqlite3

def conectar():
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alunos ( 
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            nota REAL NOT NULL                
        )
    """)
    conn.commit()
    conn.close()

def adicionar_aluno(nome, nota):
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO alunos (nome, nota) VALUES (?, ?)", (nome, nota))
    conn.commit()
    conn.close()

def obter_todos():
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM alunos")
    dados = cursor.fetchall()
    conn.close()
    return dados

def atualizar_aluno(id, nome, nota):
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE alunos SET nome = ?, nota = ? WHERE id = ?", (nome, nota, id))
    conn.commit()
    conn.close()

def deletar_aluno(id):
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM alunos WHERE id = ?", (id,))
    conn.commit()
    conn.close()

def janela_adicionar():
    janela.withdraw()
    add = tk.Toplevel()
    centralizar_janela(add, 300, 300)
    add.title("Adicionar Aluno")

    tk.Label(add, text="Nome:").pack()
    nome = tk.Entry(add)
    nome.pack()

    tk.Label(add, text="Nota:").pack()
    nota = tk.Entry(add)
    nota.pack()

    def salvar():
        if nome.get() and nota.get():
            try:
                nota_valor = float(nota.get())
                adicionar_aluno(nome.get(), nota_valor)
                messagebox.showinfo("Sucesso", "Aluno adicionado.") 
                nome.delete(0, tk.END)
                nota.delete(0, tk.END)
            except ValueError:
                messagebox.showerror("Erro", "Nota precisa ser um número.")
        else:
            messagebox.showwarning("Aviso", "Preencha todos os campos.")

    botoes_frame = tk.Frame(add)
    botoes_frame.pack(pady=30)
    tk.Button(botoes_frame, text="Salvar", command=salvar, width=10).pack(side=tk.LEFT, padx=10)
    tk.Button(botoes_frame, text="Voltar", command=lambda: [add.destroy(), janela.deiconify()], width=10).pack(side=tk.LEFT, padx=10)

def janela_listar():
    janela.withdraw()
    lista = tk.Toplevel()
    centralizar_janela(lista, 300, 300)
    lista.title("Listar Alunos")

    dados = obter_todos()

    for item in dados:
        tk.Label(lista, text=f"ID: {item[0]} | Nome: {item[1]} | Nota: {item[2]}").pack()

    tk.Button(lista, text="Voltar", command=lambda: [lista.destroy(), janela.deiconify()], width=10).pack(pady=5)

def janela_atualizar():
    janela.withdraw()
    upd = tk.Toplevel()
    centralizar_janela(upd, 300, 300)
    upd.title("Atualizar Aluno")

    tk.Label(upd, text="ID do aluno:").pack()
    id_entry = tk.Entry(upd)
    id_entry.pack()

    tk.Label(upd, text="Novo Nome:").pack()
    nome_entry = tk.Entry(upd)
    nome_entry.pack()

    tk.Label(upd, text="Nova Nota:").pack()
    nota_entry = tk.Entry(upd)
    nota_entry.pack()

    def atualizar():
        try:
            id_val = int(id_entry.get())
            novo_nome = nome_entry.get()
            nova_nota = float(nota_entry.get())
            atualizar_aluno(id_val, novo_nome, nova_nota)
            messagebox.showinfo("Sucesso", "Aluno atualizado.")
        except:
            messagebox.showerror("Erro", "Verifique os dados inseridos.")

    tk.Button(upd, text="Atualizar", command=atualizar, width=10).pack(pady=5)
    tk.Button(upd, text="Voltar", command=lambda: [upd.destroy(), janela.deiconify()], width=10).pack()

def janela_deletar():
    janela.withdraw()
    dele = tk.Toplevel()
    centralizar_janela(dele, 300, 300)
    dele.title("Deletar Aluno")

    tk.Label(dele, text="ID do aluno para deletar:").pack()
    id_entry = tk.Entry(dele)
    id_entry.pack()

    def deletar():
        try:
            id_val = int(id_entry.get())
            deletar_aluno(id_val)
            messagebox.showinfo("Sucesso", "Aluno deletado.")
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
janela.title("Sistema de Notas")
janela.geometry("300x300")

tk.Label(janela, text="Bem-vindo ao sistema de notas!\nO que deseja fazer?", font=("Arial", 12)).pack(pady=20)

tk.Button(janela, text="Adicionar Aluno", command=janela_adicionar, width=20).pack(pady=5)
tk.Button(janela, text="Listar Alunos", command=janela_listar, width=20).pack(pady=5)
tk.Button(janela, text="Atualizar Aluno", command=janela_atualizar, width=20).pack(pady=5)
tk.Button(janela, text="Deletar Aluno", command=janela_deletar, width=20).pack(pady=5)

janela.mainloop()