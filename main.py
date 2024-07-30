from flask import Flask, render_template, request, flash, session, jsonify, redirect
from hashlib import md5
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = f"S3gur4n@c0"

# Desativar seguranca = False || Ativar seguranca = True
USAR_SEGURANCA_ADICIONAL = False

@app.route("/cadastrar", methods=['GET', 'POST'])
def cadastro():
    
    if request.method == 'POST':
        login = request.form.get('username')
        login_arquivo = f"{login}.txt"
        senha = request.form.get('password')
        senha_md5 = md5(f"{senha}".encode()).hexdigest()

        if len(login) > 4 or len(senha) > 4:
            flash('Não é possivel registrar login e senha com mais de 4 caracteres', 'danger')
            return render_template("cadastrar.html")

        for _, _, files in os.walk('./sessoes/'):
            if login_arquivo in files:
                flash('Já existe um registro com o login informado', 'danger')
            else:
                with open(f"./sessoes/{login_arquivo}", "w") as arquivo:
                    arquivo.write(senha_md5)
                flash(f"{login} foi registrado", 'success')

        

    return render_template("cadastrar.html")

@app.route("/teste_user", methods=['GET'])
def teste_user():
    retorno = {}
    if 'logado' in session:
        retorno['status'] = session.get('logado')
        retorno['login'] = session.get('nome')
    
    return jsonify(retorno)

@app.route("/", methods=['GET', 'POST'])
def index():

    session.pop('logado', None)
    session.pop('nome', None)

    if request.method == 'POST':
        login = request.form.get('username')
        login_arquivo = f"{login}.txt"
        senha = request.form.get('password')
        senha_md5 = md5(f"{senha}".encode()).hexdigest()
        login_ok = False

        if len(login) > 4 or len(senha) > 4:
            flash('Não é possivel registrar login e senha com mais de 4 caracteres', 'danger')
            return render_template("cadastrar.html")

        for _, _, files in os.walk('./sessoes/'):
            if login_arquivo in files:
                with open(f"./sessoes/{login_arquivo}", "r") as arquivo:
                    senha_arquivo = arquivo.readline()
                    if senha_arquivo == senha_md5:
                        login_ok = True
        
        if login_ok:
            session['logado'] = True
            session['nome'] = login
            
            # Limpar bloqueio de excesso de tentativas
            session['tentativas_erro'] = 0
            if 'momento_bloqueado' in session:
                session.pop('momento_bloqueado')
            
            flash("Login OK", 'success')

            return redirect('/teste_user')
        else:
            if not 'tentativas_erro' in session:
                session['tentativas_erro'] = 0

            if USAR_SEGURANCA_ADICIONAL:
                if session['tentativas_erro'] == 3:
                    if not 'momento_bloqueado' in session:
                        session['momento_bloqueado'] = datetime.now()
                    
                    # Sessão Bloqueada
                    if 'momento_bloqueado' in session:
                        diff = (datetime.now() - session['momento_bloqueado']).total_seconds()
                        diff = 240 - diff 

                        if diff > 0:
                            flash(f"Aguarde {'%02d' %  int(diff// 3600)}:{'%02d' % int(diff// 60)}:{'%02d' %  int(diff % 60)} para fazer o login", 'danger')
                        # Liberar após 4 minutos
                        else:
                            session['tentativas_erro'] = 3
                            session.pop('momento_bloqueado')

                # Aumentar tentativa de erro
                else:
                    session['tentativas_erro'] += 1
                    
                    flash(f"Login e/ou Senha incorreto(s), restam {4 - session['tentativas_erro']} tentativa(s)", 'warning')
            else:
                flash(f"Login e/ou Senha incorreto(s)", 'warning')

    
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)