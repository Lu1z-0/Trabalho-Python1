from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import sqlite3
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class LoginWindow:
    #Função iniciar Login
    def __init__(self, main_app):
        self.success = False
        self.main_app = main_app
        self.janela = Toplevel()
        self.janela.geometry("200x100")
        self.janela.title("Login")
        
        Label(self.janela, text="E-mail:").grid(row=0, column=0)
        Label(self.janela, text="Senha:").grid(row=1, column=0)
        self.ed1 = Entry(self.janela)
        self.ed1.grid(row=0, column=1)

        self.ed2 = Entry(self.janela, show="*")
        self.ed2.grid(row=1, column=1)

        Button(self.janela, text="Entrar", command=self.clique).grid(column=1, row=2)
    #Conexão com o banco de dados com as informações dos fucnionarios
    def conectar_banco_de_dados(self):
        conn = sqlite3.connect('ecommerce.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS funcionario (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Nome TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                senha TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
    #Autentificação do Usuario
    def clique(self):
        email = self.ed1.get()
        senha = self.ed2.get()

        banco = sqlite3.connect('ecommerce.db')
        cursor = banco.cursor()

        cursor.execute("SELECT senha FROM funcionario WHERE email = ?", (email,))
        resultado = cursor.fetchone()

        if resultado and senha == resultado[0]:
            messagebox.showinfo("Login", "Bem Vindo!")
            self.success = True
            self.janela.destroy()  # Fecha a janela de login
            print("Login bem-sucedido! Abrindo a janela principal...")
            self.main_app.destroy()  # Fecha a janela de login
            MainWindow()  # Cria a instância da janela principal
        else:
            messagebox.showerror("Erro", "E-mail ou senha incorretos!")
        banco.close()

    

class MainWindow:
    
    def __init__(self):
        self.root = Tk()
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.iconbitmap("logo.ico")
        self.root.title("Gerador de Orçamentos")

        self.conectar_banco_de_dados()
        total_columns = 3

        self.img = ImageTk.PhotoImage(Image.open("logo.png"))
        Label(self.root, image=self.img).grid(row=0, column=0, columnspan=total_columns, sticky=N+S+E+W, padx=(200, 0))

        Label(self.root, text="Gerador de Orçamentos", font=("Times", 20), foreground='purple1').grid(row=1, column=0, columnspan=total_columns, sticky=N+S+E+W, padx=(200,0))

        Button(self.root, text="Cadastrar Cliente", width=18, height=2, command=self.abrir_janela_cadastrar_cliente).grid(row=2, column=0, pady=30, padx=10)
        Button(self.root, text="Gerar Orçamento", width=18, height=2, command=self.abrir_janela_gerar_orcamento).grid(row=2, column=1, pady=30, padx=10)
        Button(self.root, text="Consultar Cliente", width=18, height=2, command=self.abrir_janela_consultar_cliente).grid(row=2, column=2, pady=30, padx=10)
        Button(self.root, text="Cadastrar Funcionário", width=18, height=2, command=self.abrir_janela_cadastrar_funcionario).grid(row=2, column=3, pady=30, padx=10)

        for i in range(total_columns):
            self.root.grid_columnconfigure(i, weight=1)

    
    def run(self):
        self.root.mainloop()

    def on_closing(self):
        if messagebox.askokcancel("Sair", "Você realmente deseja sair?"):
            self.root.destroy()

    def conectar_banco_de_dados(self):
        conn = sqlite3.connect('clientes.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cpf TEXT NOT NULL,
                empresa TEXT
            )
        ''')
        conn.commit()
        conn.close()

    # Função para abrir a janela "Cadastrar Cliente"
    def abrir_janela_cadastrar_cliente(self):
        nova_janela = Toplevel(self.root)
        nova_janela.title("Cadastrar Cliente")
        nova_janela.geometry("500x500")

        # Campos de entrada
        Label(nova_janela, text="Nome do Cliente:", font=("Arial", 10)).grid(row=0, column=0, padx=10, pady=10, sticky=W)
        self.nome_cliente = Entry(nova_janela, width=30)
        self.nome_cliente.grid(row=0, column=1, padx=10, pady=10)

        Label(nova_janela, text="CPF:", font=("Arial", 10)).grid(row=1, column=0, padx=10, pady=10, sticky=W)
        self.cpf_cliente = Entry(nova_janela, width=30)
        self.cpf_cliente.grid(row=1, column=1, padx=10, pady=10)

        Label(nova_janela, text="Nome da Empresa:", font=("Arial", 10)).grid(row=2, column=0, padx=10, pady=10, sticky=W)
        self.nome_empresa = Entry(nova_janela, width=30)
        self.nome_empresa.grid(row=2, column=1, padx=10, pady=10)

        # Botão para salvar os dados
        Button(nova_janela, text="Salvar", width=15, command=self.salvar_cliente).grid(row=3, column=0, columnspan=2, padx=100, pady=20, sticky=N+S+E+W)

        # Botões "Voltar" e "Fechar"
        Button(nova_janela, text="Voltar", width=15, command=nova_janela.destroy).grid(row=4, column=0, columnspan=2, padx=100, sticky=N+S+E+W)
        

    # Função para salvar os dados do cliente no banco de dados
    def salvar_cliente(self):
        nome = self.nome_cliente.get()
        cpf = self.cpf_cliente.get()
        nome_empresa = self.nome_empresa.get()

        # Conectar ao banco de dados e inserir os dados
        conn = sqlite3.connect('clientes.db')
        cursor = conn.cursor()

        # Inserindo os dados do cliente na tabela
        cursor.execute('''
            INSERT INTO clientes (nome, cpf, empresa) 
            VALUES (?, ?, ?)
        ''', (nome, cpf, nome_empresa))

        # Confirmando a transação e fechando a conexão
        conn.commit()
        conn.close()

        messagebox.showinfo("Cliente Cadastrado", f"Nome: {nome}\nCPF: {cpf}\nEmpresa: {nome_empresa}")

    # Função para abrir a janela "Gerar Orçamento"
    def abrir_janela_gerar_orcamento(self):
        nova_janela = Toplevel(self.root)
        nova_janela.title("Gerar Orçamento")
        nova_janela.geometry("500x500")
    
        # Campo de entrada para CPF ou Nome do Cliente
        Label(nova_janela, text="Digite o CPF ou Nome do Cliente:", font=("Arial", 10)).grid(row=0, column=0, padx=10, pady=10, sticky=W)
        self.cpf_nome_orcamento = Entry(nova_janela, width=30)
        self.cpf_nome_orcamento.grid(row=0, column=1, padx=10, pady=10)

        # Botão para pesquisar cliente
        Button(nova_janela, text="Buscar Cliente", width=15, command=self.buscar_cliente_orcamento).grid(row=1, column=0, columnspan=2, pady=20)

        # Labels para exibir os dados do cliente
        self.label_nome_orcamento = Label(nova_janela, text="Nome:", font=("Arial", 10))
        self.label_nome_orcamento.grid(row=2, column=0, padx=10, pady=5, sticky=W)
        self.label_nome_orcamento_result = Label(nova_janela, text="", font=("Arial", 10))
        self.label_nome_orcamento_result.grid(row=2, column=1, padx=10, pady=5, sticky=W)

        self.label_empresa_orcamento = Label(nova_janela, text="Empresa:", font=("Arial", 10))
        self.label_empresa_orcamento.grid(row=3, column=0, padx=10, pady=5, sticky=W)
        self.label_empresa_orcamento_result = Label(nova_janela, text="", font=("Arial", 10))
        self.label_empresa_orcamento_result.grid(row=3, column=1, padx=10, pady=5, sticky=W)

        # Dropdown para escolher o tipo de serviço
        Label(nova_janela, text="Tipo de Serviço:", font=("Arial", 10)).grid(row=4, column=0, padx=10, pady=10, sticky=W)
        self.servico_var = StringVar(value="Básico")
        self.servicos = {"Básico": 800, "PLUS": 1200, "Premium": 1500}
        OptionMenu(nova_janela, self.servico_var, *self.servicos.keys()).grid(row=4, column=1, padx=10, pady=10)

        # Dropdown para escolher o tipo de plano
        Label(nova_janela, text="Tipo de Plano:", font=("Arial", 10)).grid(row=5, column=0, padx=10, pady=10, sticky=W)
        self.plano_var = StringVar(value="Mensal")
        self.planos = {"Mensal": 0, "Trimestral": 0.05, "Semestral": 0.07, "Anual": 0.10}
        OptionMenu(nova_janela, self.plano_var, *self.planos.keys()).grid(row=5, column=1, padx=10, pady=10)

        # Botão para calcular o valor do orçamento
        Button(nova_janela, text="Calcular Valor", width=15, command=self.calcular_valor_orcamento).grid(row=6, column=0, columnspan=2, pady=20)

        # Label para exibir o valor calculado
        self.label_valor_orcamento = Label(nova_janela, text="Valor:", font=("Arial", 10))
        self.label_valor_orcamento.grid(row=7, column=0, padx=10, pady=5, sticky=W)
        self.label_valor_orcamento_result = Label(nova_janela, text="", font=("Arial", 10))
        self.label_valor_orcamento_result.grid(row=7, column=1, padx=10, pady=5, sticky=W)

        # Botão para gerar o PDF do orçamento
        Button(nova_janela, text="Gerar PDF", width=15, command=self.gerar_pdf_orcamento).grid(row=8, column=0, columnspan=2, pady=20)

        # Botões "Voltar" e "Fechar"
        Button(nova_janela, text="Voltar", width=15, command=nova_janela.destroy).grid(row=9, column=0, columnspan=2, padx=10, pady=10)
        

    # Função para abrir a janela "Consultar Cliente"
    def abrir_janela_consultar_cliente(self):
        nova_janela = Toplevel(self.root)
        nova_janela.title("Consultar Cliente")
        nova_janela.geometry("500x500")

        # Campo de entrada para CPF ou Nome do Cliente
        Label(nova_janela, text="Digite o CPF ou Nome do Cliente:", font=("Arial", 10)).grid(row=0, column=0, padx=10, pady=10, sticky=W)
        self.cpf_nome_consulta = Entry(nova_janela, width=30)
        self.cpf_nome_consulta.grid(row=0, column=1, padx=10, pady=10)

        # Botão para pesquisar cliente
        Button(nova_janela, text="Buscar Cliente", width=15, command=self.buscar_cliente_consulta).grid(row=1, column=0, columnspan=2, pady=20)

        # Labels para exibir os dados do cliente
        self.label_nome_consulta = Label(nova_janela, text="Nome:", font=("Arial", 10))
        self.label_nome_consulta.grid(row=2, column=0, padx=10, pady=5, sticky=W)
        self.label_nome_consulta_result = Label(nova_janela, text="", font=("Arial", 10))
        self.label_nome_consulta_result.grid(row=2, column=1, padx=10, pady=5, sticky=W)

        self.label_empresa_consulta = Label(nova_janela, text="Empresa:", font=("Arial", 10))
        self.label_empresa_consulta.grid(row=3, column=0, padx=10, pady=5, sticky=W)
        self.label_empresa_consulta_result = Label(nova_janela, text="", font=("Arial", 10))
        self.label_empresa_consulta_result.grid(row=3, column=1, padx=10, pady=5, sticky=W)

        self.label_cpf_consulta = Label(nova_janela, text="CPF:", font=("Arial", 10))
        self.label_cpf_consulta.grid(row=4, column=0, padx=10, pady=5, sticky=W)
        self.label_cpf_consulta_result = Label(nova_janela, text="", font=("Arial", 10))
        self.label_cpf_consulta_result.grid(row=4, column=1, padx=10, pady=5, sticky=W)

        # Botão para editar dados do cliente
        Button(nova_janela, text="Editar Cliente", width=15, command=self.abrir_janela_editar_cliente).grid(row=5, column=0, padx=10, pady=10)

        # Botão para excluir cliente
        Button(nova_janela, text="Excluir Cliente", width=15, command=self.excluir_cliente).grid(row=5, column=1, padx=10, pady=10)

        # Botões "Voltar" e "Fechar"
        Button(nova_janela, text="Voltar", width=15, command=nova_janela.destroy).grid(row=9, column=0, columnspan=2, padx=10, pady=10)
        

    # Função para buscar o cliente na consulta e exibir os dados
    def buscar_cliente_consulta(self):
        cpf_nome = self.cpf_nome_consulta.get()

        conn = sqlite3.connect('clientes.db')
        cursor = conn.cursor()

        cursor.execute("SELECT nome, empresa, cpf FROM clientes WHERE cpf=? OR nome=?", (cpf_nome, cpf_nome))
        cliente = cursor.fetchone()
        conn.close()

        if cliente:
            self.label_nome_consulta_result.config(text=cliente[0])
            self.label_empresa_consulta_result.config(text=cliente[1])
            self.label_cpf_consulta_result.config(text=cliente[2])
        else:
            messagebox.showinfo("Cliente Não Encontrado", "Nenhum cliente encontrado com o CPF ou Nome informado.")

    # Função para abrir a janela "Editar Cliente"
    def abrir_janela_editar_cliente(self):
        nova_janela = Toplevel(self.root)
        nova_janela.title("Editar Cliente")
        nova_janela.geometry("400x300")

        # Campos de entrada para edição
        Label(nova_janela, text="Nome do Cliente:", font=("Arial", 10)).grid(row=0, column=0, padx=10, pady=10, sticky=W)
        self.nome_cliente_editar = Entry(nova_janela, width=30)
        self.nome_cliente_editar.grid(row=0, column=1, padx=10, pady=10)

        Label(nova_janela, text="CPF:", font=("Arial", 10)).grid(row=1, column=0, padx=10, pady=10, sticky=W)
        self.cpf_cliente_editar = Entry(nova_janela, width=30)
        self.cpf_cliente_editar.grid(row=1, column=1, padx=10, pady=10)

        Label(nova_janela, text="Nome da Empresa:", font=("Arial", 10)).grid(row=2, column=0, padx=10, pady=10, sticky=W)
        self.nome_empresa_editar = Entry(nova_janela, width=30)
        self.nome_empresa_editar.grid(row=2, column=1, padx=10, pady=10)

        # Preenchendo os campos com os dados atuais
        self.nome_cliente_editar.insert(0, self.label_nome_consulta_result.cget("text"))
        self.cpf_cliente_editar.insert(0, self.label_cpf_consulta_result.cget("text"))
        self.nome_empresa_editar.insert(0, self.label_empresa_consulta_result.cget("text"))

        # Botão para salvar as alterações
        Button(nova_janela, text="Salvar Alterações", width=15, command=self.salvar_alteracoes_cliente).grid(row=3, column=0, columnspan=2, pady=20)

        # Botões "Voltar" e "Fechar"
        Button(nova_janela, text="Voltar", width=15, command=nova_janela.destroy).grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    # Função para salvar as alterações feitas no cliente
    def salvar_alteracoes_cliente(self):
        novo_nome = self.nome_cliente_editar.get()
        novo_cpf = self.cpf_cliente_editar.get()
        nova_empresa = self.nome_empresa_editar.get()

        conn = sqlite3.connect('clientes.db')
        cursor = conn.cursor()

        cursor.execute("UPDATE clientes SET nome=?, cpf=?, empresa=? WHERE cpf=?",
                       (novo_nome, novo_cpf, nova_empresa, self.label_cpf_consulta_result.cget("text")))
        conn.commit()
        conn.close()

        messagebox.showinfo("Alterações Salvas", "As alterações foram salvas com sucesso!")

    # Função para excluir o cliente
    def excluir_cliente(self):
        cpf = self.label_cpf_consulta_result.cget("text")

        if cpf:
            conn = sqlite3.connect('clientes.db')
            cursor = conn.cursor()

            cursor.execute("DELETE FROM clientes WHERE cpf=?", (cpf,))
            conn.commit()
            conn.close()

            messagebox.showinfo("Cliente Excluído", "O cliente foi excluído com sucesso.")
        else:
            messagebox.showwarning("Ação Inválida", "Nenhum cliente selecionado para exclusão.")

    # Função para buscar o cliente na geração de orçamento
    def buscar_cliente_orcamento(self):
        cpf_nome = self.cpf_nome_orcamento.get()

        conn = sqlite3.connect('clientes.db')
        cursor = conn.cursor()

        cursor.execute("SELECT nome, empresa, cpf FROM clientes WHERE cpf=? OR nome=?", (cpf_nome, cpf_nome))
        cliente = cursor.fetchone()
        conn.close()

        if cliente:
            self.label_nome_orcamento_result.config(text=cliente[0])
            self.label_empresa_orcamento_result.config(text=cliente[1])
        else:
            messagebox.showinfo("Cliente Não Encontrado", "Nenhum cliente encontrado com o CPF ou Nome informado.")

    # Função para calcular o valor do orçamento
    def calcular_valor_orcamento(self):
        tipo_servico = self.servico_var.get()
        tipo_plano = self.plano_var.get()

        valor_base = self.servicos[tipo_servico]
        desconto = self.planos[tipo_plano]
        valor_final = valor_base * (1 - desconto)

        self.label_valor_orcamento_result.config(text=f"R$ {valor_final:.2f}")

    # Função para gerar o PDF do orçamento
    def gerar_pdf_orcamento(self):
        nome_cliente = self.label_nome_orcamento_result.cget("text")
        empresa_cliente = self.label_empresa_orcamento_result.cget("text")
        valor_orcamento = self.label_valor_orcamento_result.cget("text")

        

        nome_arquivo = f"Orçamento_{nome_cliente.replace(' ', '_')}.pdf"
        c = canvas.Canvas(nome_arquivo, pagesize=letter)
        c.drawString(250, 750, "Orçamento")
        c.drawString(100, 730, f"Nome do Cliente: {nome_cliente}")
        c.drawString(100, 710, f"Empresa: {empresa_cliente}")
        c.drawString(100, 690, f"Valor: {valor_orcamento}")
        c.save()

        messagebox.showinfo("PDF Gerado", f"O PDF foi gerado com sucesso:\n{nome_arquivo}")
    # Função Cadastrar novo funcionario
    def abrir_janela_cadastrar_funcionario(self):
        nova_janela = Toplevel(self.root)
        nova_janela.title("Cadastrar Funcionário")
        nova_janela.geometry("400x300")

        Label(nova_janela, text="Nome:", font=("Arial", 10)).grid(row=0, column=0, padx=10, pady=10, sticky=W)
        nome_entry = Entry(nova_janela, width=30)
        nome_entry.grid(row=0, column=1, padx=10, pady=10)

        Label(nova_janela, text="E-mail:", font=("Arial", 10)).grid(row=1, column=0, padx=10, pady=10, sticky=W)
        email_entry = Entry(nova_janela, width=30)
        email_entry.grid(row=1, column=1, padx=10, pady=10)

        Label(nova_janela, text="Senha:", font=("Arial", 10)).grid(row=2, column=0, padx=10, pady=10, sticky=W)
        senha_entry = Entry(nova_janela, show="*", width=30)
        senha_entry.grid(row=2, column=1, padx=10, pady=10)

        Button(nova_janela, text="Salvar", width=15, command=lambda: self.salvar_funcionario(nome_entry.get(), email_entry.get(), senha_entry.get())).grid(row=3, column=0, columnspan=2, pady=20)

    #Função salvar dados do novo funcionario
    def salvar_funcionario(self, nome, email, senha):
        conn = sqlite3.connect('ecommerce.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO funcionario (nome, email, senha) VALUES (?, ?, ?)', (nome, email, senha))
        conn.commit()
        conn.close()
        messagebox.showinfo("Funcionário Cadastrado", "Funcionário cadastrado com sucesso!")


    # Função para fechar a aplicação com confirmação
    def on_closing(self):
        if messagebox.askokcancel("Sair", "Você realmente deseja sair?"):
            self.root.destroy()


# Na parte principal do código, depois do login bem-sucedido
if __name__ == "__main__":
    root = Tk()  # Cria a janela raiz
    root.withdraw()  # Oculta a janela principal por enquanto
    
    login_window = LoginWindow(root)  # Abre a janela de login
    root.mainloop()  # Mantém a aplicação rodando
