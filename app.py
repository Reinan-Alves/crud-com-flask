from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import json

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# configuração da conexão com bd,informando usuario,senha,local,banco de dado já criado, no cado o crudflask
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:reinan880216@localhost/crudflask'

db = SQLAlchemy(app)

# modelo da tabela que sera criada


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    email = db.Column(db.String(100))

    def to_json(self):
        return{"id": self.id, "nome": self.nome, "email": self.email}

# após criar o modelo inserimos no prompt o comando python(para entrar em modo de execursão python)
# from app import app
# db.create_all() para criar a tabela do banco
# no workbench podemos ve a tabela criada e adicionar linha

# selecionar tudo(read)


@app.route("/usuarios", methods=["GET"])
def seleciona_usuarios():
    usuarios_objetos = Usuario.query.all()
    usuarios_json = [usuario.to_json() for usuario in usuarios_objetos]

    return gera_response(200, "usuarios", usuarios_json, 'ok')

# selecionar individual(read)


@app.route("/usuario/<id>", methods=["GET"])
def seleciona_usuario(id):
    usuario_objeto = Usuario.query.filter_by(id=id).first()
    usuario_json = usuario_objeto.to_json()
    return gera_response(200, 'usuario', usuario_json, 'ok')


# cadastrar(create)
@app.route("/usuario", methods=["POST"])
def cria_usuario():
    body = request.get_json()

# obs: esta sem validação, em outras situações é nescessario validar os dados
# tratando os erros com try exept
    try:
        usuario = Usuario(nome=body['nome'], email=body['email'])
        db.session.add(usuario)
        db.session.commit()
        return gera_response(201, "usuario", usuario.to_json(), "Criado com suceso")
    except Exception as e:
        print(e)
        return gera_response(400, "usuario", {}, "Erro ao cadastrar")


# atualizar update
@app.route("/usuario/<id>", methods=["PUT"])
def atualiza_usuario(id):
    # pegar o usuario
    usuario_objeto = Usuario.query.filter_by(id=id).first()
    # pegar modificações
    body = request.get_json()

    try:
        if('nome' in body):
            usuario_objeto.nome = body['nome']
        if('email' in body):
            usuario_objeto.email = body['email']

        db.session.add(usuario_objeto)
        db.session.commit()
        return gera_response(200, "usuario", usuario_objeto.to_json(), "atualizado com suceso")
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "usuario", {}, "Erro ao atualizar")


# Deletar  delete
@app.route("/usuario/<id>", methods=["DELETE"])
def deleta_usuario(id):
    # pegar o usuario
    usuario_objeto = Usuario.query.filter_by(id=id).first()
    # deletar usuario

    try:
        db.session.delete(usuario_objeto)
        db.session.commit()
        return gera_response(200, "usuario", usuario_objeto.to_json(), "deletado com suceso")
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "usuario", {}, "Erro ao deletar")


# função para gerar os retornos json
def gera_response(status, nome_do_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_do_conteudo] = conteudo

    if(mensagem):
        body["mensagem"] = mensagem

    return Response(json.dumps(body), status=status, mimetype="application/json")


app.run()
