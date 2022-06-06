from flask import Flask, render_template, request, redirect, session, flash, url_for

class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console

jogo1 = Jogo('Valorant', 'FPS', 'PC')
jogo2 = Jogo('Dead By Daylight', 'Terror', 'PC')
jogo3 = Jogo('Devour', 'Terror', 'PC')
lista = [jogo1, jogo2, jogo3]

class User:
    def __init__(self, nome, nick, senha):
        self.nome = nome
        self.nick = nick
        self.senha = senha

usuario1 = User('admin', 'admin', 'alura')
usuario2 = User('nimda', 'nimda', 'caelum')

usuarios = {usuario1.nick : usuario1,
            usuario2.nick : usuario2, #dicionario
            }

app = Flask(__name__)
app.secret_key = 'alura' #criptografia para evitar que pessoas alterem dados nos cookies

@app.route('/') #cria rota
def index():
    return render_template('lista.html',titulo = 'Jogos', jogos = lista)

@app.route('/novo-jogo')
def novo_jogo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima = url_for('novo_jogo')))
    return render_template('novojogo.html', titulo = 'Novo Jogo')

@app.route('/criar', methods=['POST',]) #como padrão a rota so aceita GET, vc tem que colocar o POST
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console) #cria um objeto com os dados recebidos
    lista.append(jogo) #adiciona o jogo na lista, precisa ser global
    return redirect(url_for('index'))


@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima = proxima)

@app.route('/autenticar', methods=['POST',])
def autenticar():

    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nick
            flash(f' Boa noite, {usuario.nick}')
            proxima_pag = request.form['proxima']
            return redirect(proxima_pag)
    else:
        flash("Usuário inválido")
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None #deixa o session vazio, não grava mais o nome do user
    flash('Desconectado')
    return redirect(url_for('index'))


app.run(debug=True) #faz rodar a aplicação