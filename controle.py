from PyQt6 import uic, QtWidgets
import mysql.connector
import datetime

#Conexão com banco de dados
cnx = mysql.connector.connect(user='root', password='',
                              host='localhost',
                              database='lista_de_tarefas')

cursor = cnx.cursor()

#Iniciando primeira tela
def chama_primeira_tela():
    cadastro.show()
    inicial.close()

#Funções da Tela de Cadastro
def cadastrar_tarefa():
    linha1 = cadastro.lineEdit.text()
    linha2 = cadastro.lineEdit_2.text()
    data_str = datetime.datetime.now().strftime("%d/%m/%Y")

    status = ""
    if cadastro.radioButton.isChecked():
        print("Categoria Progresso selecionada")
        status = "Progresso"
    elif cadastro.radioButton_2.isChecked():
        print("Categoria Concluido selecionada")
        status = "Concluido"

    print("Titulo:",linha1)
    print("Descricao:",linha2)
    print("Data",data_str)

    add_tarefa_query = """INSERT INTO tarefas (titulo, descricao, data_de_criacao, status)
                           VALUES (%s, %s, %s, %s)"""

    dados = (str(linha1), str(linha2), data_str, status)
    cursor.execute(add_tarefa_query, dados)
    cnx.commit()
    cadastro.lineEdit.setText("")
    cadastro.lineEdit_2.setText("")

#função que chama segunda tela com a lista das tarefas
def chama_segunda_tela():
    cadastro.hide()
    segunda_tela.show()

    cursor.execute("SELECT * FROM tarefas")
    dados_lidos = cursor.fetchall()

    segunda_tela.tableWidget.setRowCount(len(dados_lidos))
    segunda_tela.tableWidget.setColumnCount(6)

    for i in range(0, len(dados_lidos)):
        for j in range(0, 6):
            segunda_tela.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))

#função para deletar dados da lista
def excluir_dados():
    linha = segunda_tela.tableWidget.currentRow()
    if linha >= 0:
        segunda_tela.tableWidget.removeRow(linha)

        cursor.execute("SELECT id FROM tarefas")
        dados_lidos = cursor.fetchall()
        valor_id = dados_lidos[linha][0]
        cursor.execute("DELETE FROM tarefas WHERE id=" + str(valor_id))
        cnx.commit()

#função do botão editar lista
def editar_dados():
    global numero_id

    linha = segunda_tela.tableWidget.currentRow()
    cursor.execute("SELECT id FROM tarefas")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("SELECT * FROM tarefas WHERE id=" + str(valor_id))
    tarefa = cursor.fetchall()
    tela_editar.show()

    tela_editar.lineEdit_2.setText(str(tarefa[0][1]))
    tela_editar.lineEdit_3.setText(str(tarefa[0][2]))
    tela_editar.lineEdit_4.setText(str(tarefa[0][3]))
    tela_editar.lineEdit_5.setText(str(tarefa[0][4]))
    tela_editar.lineEdit_6.setText(str(tarefa[0][5]))

    numero_id = valor_id

#função do botão exibir
def cadastro_exibir():
    cadastro.show()

#função de atualizar tarefa
def atualizar_tarefa():
    global numero_id

    titulo = tela_editar.lineEdit_2.text()
    descricao = tela_editar.lineEdit_3.text()
    status = tela_editar.lineEdit_4.text()
    data_de_criacao = tela_editar.lineEdit_5.text()
    data_de_conclusao = tela_editar.lineEdit_6.text()
    valores = (titulo, descricao, status, data_de_conclusao, data_de_criacao, numero_id)

    atualizar_tarefa_query = "UPDATE tarefas SET titulo = %s, descricao = %s, status = %s, data_de_conclusao = %s,data_de_criacao = %s WHERE id = %s"
    cursor.execute(atualizar_tarefa_query, valores)
    cnx.commit()

    tela_editar.close()
    segunda_tela.close()
    chama_segunda_tela()

#Chamadas de cada arquivo para tela correspondente
app = QtWidgets.QApplication([])
inicial = uic.loadUi("inicial.ui")
cadastro = uic.loadUi("tela_cadastro.ui")
segunda_tela = uic.loadUi("listar_dados.ui")
tela_editar = uic.loadUi("menu_editar.ui")


#Funções de botões do Pyqt6
inicial.pushButton.clicked.connect(chama_primeira_tela)
cadastro.pushButton.clicked.connect(cadastrar_tarefa)
cadastro.pushButton_2.clicked.connect(chama_segunda_tela)
segunda_tela.pushButton_3.clicked.connect(excluir_dados)
segunda_tela.pushButton_2.clicked.connect(editar_dados)
segunda_tela.pushButton.clicked.connect(cadastro_exibir)
tela_editar.pushButton.clicked.connect(atualizar_tarefa)

inicial.show()
app.exec()

