import tkinter as tk
import mysql.connector

# Conexão com o banco de dados
conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    database="test"
)
cursor = conexao.cursor()

# Criar tabela
criar_tabela = """
CREATE TABLE IF NOT EXISTS votacao (
    id_votacao INT AUTO_INCREMENT PRIMARY KEY,
    voto INT NOT NULL
)
"""
cursor.execute(criar_tabela)
print("Tabela criada com sucesso!")


def votar():
    candidatos = {
        22: "José",
        54: "Carlos"
    }

    def cadastrar():
        voto = int(voto_entry.get())
        inserir_dado = "INSERT INTO votacao (voto) VALUES (%s)"
        dado = (voto,)
        cursor.execute(inserir_dado, dado)
        print("DADOS CADASTRADOS!")
        conexao.commit()
        top.destroy()

    def atualizar_voto(num):
        voto_entry.insert(tk.END, num)

    # Janela para votação
    top = tk.Toplevel(root)
    top.title("Votar")
    top.geometry("300x300")

    label = tk.Label(top, text="Candidatos:\n[22] José\n[54] Carlos")
    label.pack()

    voto_label = tk.Label(top, text="Digite o número do seu candidato:")
    voto_label.pack()

    voto_entry = tk.Entry(top)
    voto_entry.pack()

    cadastrar_button = tk.Button(top, text="Cadastrar", command=cadastrar)
    cadastrar_button.pack()

    b1 = tk.Button(top, text="1", command=lambda: atualizar_voto("1"))
    b1.place(x=95 , y=140)

    b2 = tk.Button(top, text="2", command=lambda: atualizar_voto("2"))
    b2.place(x=130 , y=140)

    b3 = tk.Button(top, text="3", command=lambda: atualizar_voto("3"))
    b3.place(x=165 , y=140)

    b4 = tk.Button(top, text="4", command=lambda: atualizar_voto("4"))
    b4.place(x=95 , y=170)

    b5 = tk.Button(top, text="5", command=lambda: atualizar_voto("5"))
    b5.place(x=130 , y=170)

    b6 = tk.Button(top, text="6", command=lambda: atualizar_voto("6"))
    b6.place(x=165 , y=170)

    b7 = tk.Button(top, text="7", command=lambda: atualizar_voto("7"))
    b7.place(x=95 , y=200)

    b8 = tk.Button(top, text="8", command=lambda: atualizar_voto("8"))
    b8.place(x=130 , y=200)

    b9 = tk.Button(top, text="9", command=lambda: atualizar_voto("9"))
    b9.place(x=165 , y=200)

    b0 = tk.Button(top, text="0", command=lambda: atualizar_voto("0"))
    b0.place(x=130 , y=230)


def contar():
    candidatos = {
        22: "José",
        54: "Carlos"
    }

    leitura_dado = "SELECT voto, COUNT(*) as total FROM votacao GROUP BY voto"
    cursor.execute(leitura_dado)
    retorno_dado = cursor.fetchall()

    vencedor = None
    max_votos = 0

    for candidato in retorno_dado:
        voto, total = candidato
        if total > max_votos:
            max_votos = total
            vencedor = voto

        nome_candidato = candidatos.get(voto)
        print(f"Candidato {nome_candidato}: {total} votos")

    if vencedor is not None:
        nome_vencedor = candidatos.get(vencedor)
        resultado_label = tk.Label(root, text=f"Vencedor: {nome_vencedor}!\nVotos: {total}", font=("Arial", 12, "bold"))
        resultado_label.pack(pady=10)

    print("CONTAGEM REALIZADA!")
    conexao.commit()


def apagar():
    delete_dado = "DELETE FROM votacao"
    cursor.execute(delete_dado)
    print("Todos os votos foram apagados!")
    conexao.commit()

def limpar_line_edit():
    line_edit.clear()


# Funções para os botões
def votar_click():
    votar()


def contar_click():
    contar()


def apagar_click():
    apagar()
    root.quit()


# Interface gráfica usando Tkinter
root = tk.Tk()
root.title("Sistema de Votação")
root.geometry("300x300")

titulo_label = tk.Label(root, text="Sistema de Votação", font=("Arial", 14, "bold"))
titulo_label.pack(pady=10)

votar_button = tk.Button(root, text="Votar", command=votar_click, font=("Arial", 12))
votar_button.pack()

contar_button = tk.Button(root, text="Apresentar Dados", command=contar_click, font=("Arial", 12))
contar_button.pack()

apagar_button = tk.Button(root, text="Zerar Votação", command=apagar_click, font=("Arial", 12))
apagar_button.pack()

root.mainloop()