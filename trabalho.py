import sqlite3
import tkinter as tk
from tkinter import messagebox

CAMINHO_BD = "alunos.db"
conn = sqlite3.connect(CAMINHO_BD)

cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS alunos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    nota REAL NULL
)
""")

conn.commit()
class SistemaCadastros(tk.Tk):

    def __init__(self):
        super().__init__()
        # Configurações da janela
        self.title("Sistema de Cadastros")
        fonte = ("Arial", 14)
        self.geometry("900x750")
        self.configure(bg="#38B8AA")


 
       
        #Caixa da lista
        self.lista = tk.Listbox(self,width=60,height=15,bg="#2D2D44",fg="white",selectbackground="#2ab16b",
        selectforeground="white",font=("Consolas", 11),bd=0)
        self.lista.pack(fill=tk.X, expand=True, pady=10)
        #Caixa de entrada para o nome e nota
        self.frame_campos = tk.Frame(self)
        self.frame_campos.pack(pady=10)
        
        tk.Label(self,text="Nome",bg="#1E1E2E",fg="white",font=("Arial", 11)).pack()
        self.entry_nome = tk.Entry(self,bg="#2D2D44",fg="white",insertbackground="white",font=("Arial", 11))
        self.entry_nome.pack()
        
        tk.Label(self,text="Nota",bg="#1E1E2E",fg="white",font=("Arial", 11)).pack()
        self.entry_nota = tk.Entry(self,bg="#2D2D44",fg="white",insertbackground="white",font=("Arial", 11))
        self.entry_nota.pack()
        #Caixa de entrada para o ID
        tk.Label(self,text="ID",bg="#1E1E2E",fg="white",font=("Arial", 11)).pack()
        self.entry_id = tk.Entry(self,bg="#2D2D44",fg="white",insertbackground="white",font=("Arial", 11))
        self.entry_id.pack()
        #botões para inserir, listar e excluir dados
        self.frame_botoes = tk.Frame(self)
        self.frame_botoes.pack(pady=5)

        self.btn_inserir = tk.Button(self,text="Inserir",command=self.inserir_dados,
        bg="#2ab16b",fg="white",font=("Arial", 10, "bold"),width=12)
        self.btn_inserir.pack(pady=5)
        
        #listar
        self.frame_botoes = tk.Frame(self)
        self.frame_botoes.pack(pady=5)

        self.btn_ler = tk.Button(self,text="Listar",command=self.ler_dados,bg="#2196F3",fg="white",font=("Arial", 10, "bold"),width=12)
        self.btn_ler.pack()

        #buscar
        self.frame_botoes = tk.Frame(self)
        self.frame_botoes.pack(pady=5)

        self.btn_buscar = tk.Button(self,text="Buscar",command=self.buscar_dados,bg="#944877",fg="white",font=("Arial", 10, "bold"),width=12)
        self.btn_buscar.pack()
        #atualizar
        self.frame_botoes = tk.Frame(self)
        self.frame_botoes.pack(pady=5)
        self.btn_atualizar = tk.Button(self,text="Atualizar",command=self.atualizar_dados,
         bg="#1d7f87",fg="white",font=("Arial", 10, "bold"),width=12)
        self.btn_atualizar.pack()

        #excluir
        self.frame_botoes = tk.Frame(self)
        self.frame_botoes.pack(pady=5)

        self.btn_excluir = tk.Button(self,text="Excluir",command=self.deletar_dados,bg="#d85e30"
        ,fg="white",font=("Arial", 10, "bold"),width=12)
        
        self.btn_excluir.pack()

        self.frame_botoes = tk.Frame(self)
        self.frame_botoes.pack(pady=5)

        btn_sair = tk.Button(self,text="Sair",command=self.quit,bg="#555555",fg="white",font=("Arial", 10, "bold"),width=12)
        btn_sair.pack()

        

    def inserir_dados(self):
        nota = float(self.entry_nota.get()) if self.entry_nota.get() else "avaliação pendente"
        try:
            nome = self.entry_nome.get()

            if not nome:
                messagebox.showerror(
                    "Erro",
                    "Preencha o nome."
                )
                return
        finally:

            cur.execute(
                "INSERT INTO alunos (nome, nota) VALUES (?, ?)",
                (nome, nota)
            )
        conn.commit()
        self.ler_dados()  

        messagebox.showinfo(
            "Sucesso!",
            "Dados inseridos com êxito!"
        )


    def ler_dados(self):
        cur.execute("SELECT * FROM alunos")
        alunos = cur.fetchall()

        self.lista.delete(0, tk.END)

        for aluno in alunos:
            self.lista.insert(
            tk.END,
            f"{aluno[0]} - {aluno[1]} - {aluno[2]}"
        )


    def deletar_dados(self):
        id_aluno = self.entry_id.get()
        if not id_aluno:
            messagebox.showerror(
                "Erro",
                "Preencha o ID."
            )
            return

        cur.execute(
        "DELETE FROM alunos WHERE id = ?",(id_aluno,))

        conn.commit()

        self.ler_dados()

        messagebox.showinfo(
            "Sucesso",
            "Aluno excluído com êxito")
    def atualizar_dados(self):
        id_aluno = self.entry_id.get()
        nome = self.entry_nome.get()
        nota_texto = self.entry_nota.get()

        if not nome or not nota_texto or not id_aluno:
            messagebox.showerror(
                "Erro",
                "Preencha ID, Nome e Nota."
            )
            return

        nota = float(nota_texto)

        cur.execute("""UPDATE alunos SET nome = ?, nota = ? WHERE id = ?""",(nome, nota, id_aluno))
        messagebox.showinfo(
        "Sucesso",
        "Aluno atualizado!")
        conn.commit()
        self.ler_dados()
    
    def buscar_dados(self):
        nome = self.entry_nome.get()

        cur.execute("SELECT * FROM alunos WHERE nome LIKE ?",(f"%{nome}%",))

        alunos = cur.fetchall()
        self.lista.delete(0, tk.END)

        for aluno in alunos:
            self.lista.insert(tk.END, f"{aluno[0]} - {aluno[1]} - {aluno[2]}")
    
    def quit(self):
        if messagebox.askokcancel("Sair", "Deseja realmente sair?"):
            self.destroy()


if __name__ == "__main__":
    try:
        app = SistemaCadastros()
        app.mainloop()
    finally:
        cur.close()
        conn.close()

