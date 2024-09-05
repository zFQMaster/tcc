# Autor: Gabriel Padula  /  Versão 5.0  /  Dia: 23/07/24
# Programa feito para validação do sistema de logins e cadastros do TCC da Escola e Faculdade Senai 'Roberto Mange'

# Importação de bibliotecas
from flask import Flask, render_template, redirect, request, flash
import psycopg2
from psycopg2 import sql

# Criação de uma instância da aplicação Flask
app = Flask(__name__, static_folder='static')

# Configuração de uma chave secreta para a aplicação Flask
app.config['SECRET_KEY'] = 'admin'

# Função para criar uma nova conexão com o banco de dados
def get_db_connection():
    conn_str = {
        'dbname': "tcc_wt2c",
        'user' : "guilherme",
        'password' : "ArRqQLQVOtJcdPs8DZLVmGWHxZy2ZJR6",
        'host' : "dpg-crb3dsjtq21c73cf85rg-a.oregon-postgres.render.com",
        'port' : "5432"
    }
    return psycopg2.connect(**conn_str)

# Rota principal que renderiza a página inicial de login
@app.route('/')
def home():
    return render_template('login.html')

# Rota para a página de login do cliente
@app.route('/cliente')
def cliente():
    return render_template('login_cliente.html')

# Rota para a página de cadastro
@app.route('/cd')
def cadastro():
    return render_template('cadastro.html')

# Rota para a página de compras
@app.route('/compras')
def compras():
    return render_template('compras.html')

# Rota para a página de compra_realizada
@app.route('/compra_realizada')
def compra_realizada():
    return render_template('compra_realizada.html')






# Rota para processar o login do cliente
@app.route('/login_cliente', methods=['POST'])
def login():
    # Obtem os dados do formulário de login
    email = request.form.get('email')
    senha = request.form.get('senha')

    # Verifica se os campos foram preenchidos
    if not email or not senha:
        flash("Por favor, preencha todos os campos.")
        return redirect('/cliente')

    conn = None
    cursor = None

    try:
        # Conecta ao banco de dados
        conn = get_db_connection()
        cursor = conn.cursor()

        # Consulta SQL para verificar se as credenciais são válidas
        query = sql.SQL("SELECT * FROM usuarios WHERE email = %s AND senha = %s")
        cursor.execute(query, (email, senha))

        # Se as credenciais forem válidas, redireciona para a página de compras
        if cursor.fetchone():
            return redirect("/compras")
        else:
            flash("Usuário ou senha inválidos. Tente novamente!")
            return redirect('/cliente')

    except psycopg2.Error as e:
        # Realiza o rollback da transação em caso de erro
        if conn:
            conn.rollback()
        print(f"Erro ao conectar ou consultar o banco de dados: {e}")
        flash("Ocorreu um erro no servidor. Tente novamente mais tarde.")
        return redirect('/cliente')

    finally:
        # Fecha o cursor e a conexão
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Rota para processar o cadastro do usuário
@app.route('/cadastro', methods=['POST'])
def cadastros():
    # Obtem os dados do formulário de cadastro
    nome = request.form.get("nome")
    email = request.form.get('email')
    senha = request.form.get('senha')

    # Verifica se os campos foram preenchidos
    if not nome or not email or not senha:
        flash("Por favor, preencha todos os campos.")
        return redirect('/cd')

    conn = None
    cursor = None

    try:
        # Conecta ao banco de dados
        conn = get_db_connection()
        cursor = conn.cursor()

        # Consulta SQL para inserir os dados no banco de dados
        comando = """INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)"""
        cursor.execute(comando, (nome, email, senha))
        conn.commit()

        flash("Cadastro realizado com sucesso!")
        return redirect('/cd')

    except psycopg2.Error as e:
        # Realiza o rollback da transação em caso de erro
        if conn:
            conn.rollback()
        print(f"Erro ao conectar ou inserir no banco de dados: {e}")
        flash("Ocorreu um erro no servidor. Tente novamente mais tarde.")
        return redirect('/cd')

    finally:
        # Fecha o cursor e a conexão
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    # Executa a aplicação Flask em modo de depuração
    app.run(debug=True)
