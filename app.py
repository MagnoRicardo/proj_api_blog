# MODULO 09 / AULA 13

from flask import request, jsonify, make_response
from estrutura_dados import app, Usuario, Musica, db
from datetime import datetime, timedelta
from functools import wraps
import jwt


def token_obrigatorio(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'Mensagem':'Token nao incluído!!'})
        try:
            resultado = jwt.decode(token,app.config['SECRET_KEY'],algorithms=["HS256"])
            usuario = Usuario.query.filter_by(id_usuario = resultado['id_usuario']).first()
        except:
            return({'Mensagem':'Token Invalido'})
        return f(usuario,*args,**kwargs)
    return decorated


@app.route('/login')
def login():
    userpass = request.authorization
    if not userpass.username or not userpass.password:
        return make_response('Login inválido', {'WWW-Authenticate':'Basic realm="Login Obrigatório"'})
    usuario = Usuario.query.filter_by(nome = userpass.username).first()
    if not usuario:
        return make_response('Usuario não encontrado', {'WWW-Authenticate':'Basic realm="Login Obrigatório"'})
    if usuario.senha == userpass.password:
        token = jwt.encode({'id_usuario':usuario.id_usuario, 'exp':datetime.utcnow() + timedelta(minutes=30)}, app.config['SECRET_KEY'] )
        return jsonify({'token':token})
    return make_response('Token invalido', {'WWW-Authenticate':'Basic realm="Login Obrigatório"'})


# GERENCIAMENTO ALBUM

@app.route('/musicas', methods=['GET'])
@token_obrigatorio
def lista_album(usuario):
    musica = Musica.query.all()
    musica_list = []
    for c in musica:
        musica_dict = {}
        musica_dict['id'] = c.id_musica
        musica_dict['titulo'] = c.titulo
        musica_dict['artista'] = c.artista
        musica_list.append(musica_dict)
    return jsonify({'album':musica_list})


@app.route('/musicas/<int:id>', methods=['GET'])
@token_obrigatorio
def buscar_musica(usuario,id):
    musica = Musica.query.filter_by(id_musica = id).first()
    if not musica:
        return jsonify({'Mensagem':'Musica nao encontrada'})
    musica_dict = {}
    musica_dict['id'] = musica.id_musica
    musica_dict['artista'] = musica.artista
    musica_dict['titulo'] = musica.titulo
    return jsonify({'musica': musica_dict})


@app.route('/musicas', methods=['POST'])
@token_obrigatorio
def adicionar_musica(usuario):
    musica_nova = request.get_json()
    musica = Musica(titulo=musica_nova['titulo'], artista=musica_nova['artista'])
    db.session.add(musica)
    db.session.commit()
    return jsonify({'musica_nova':musica_nova},' Musica adicionada com sucesso!!')


@app.route('/musicas/<int:id>', methods=['PUT'])
@token_obrigatorio
def alterar_musica(usuario,id):
    novo_valor = request.get_json()
    musica = Musica.query.filter_by(id_musica = id).first()
    if not musica:
        return jsonify({'Mensagem':' Musica nao encontrada'})
    try:
        if novo_valor['titulo']:
            musica.titulo = novo_valor['titulo']
    except:
        pass
    try:
        if novo_valor['artista']:
            musica.artista = novo_valor['artista']
    except:
        pass
    db.session.commit()
    return jsonify({'musica_alterada':novo_valor}, 'Musica alterada com sucesso!!')   
    

@app.route('/musicas/<int:id>',  methods=['DELETE'])
@token_obrigatorio
def delete_musica(usuario,id):
    excluir = Musica.query.filter_by(id_musica = id).first()
    if not excluir:
        return jsonify({'Mensagem':'Musica nao encontrada'})
    db.session.delete(excluir)
    db.session.commit()
    return jsonify({'Mensagem':'Musica excluída com sucesso'})


# MODULO 09 / AULA 17

# GERENCIAMENTO USUARIO

@app.route('/usuarios', methods=['GET'])
@token_obrigatorio
def listar_usuarios(usuario):
    usuario = Usuario.query.all()
    usuario_list = []
    for c in usuario:
        usuario_dict = {}
        usuario_dict['id'] = c.id_usuario
        usuario_dict['nome'] = c.nome
        usuario_dict['cpf'] = c.cpf
        usuario_dict['email'] = c.email
        usuario_list.append(usuario_dict)
    return jsonify({'lista_usuarios':usuario_list})

@app.route('/usuarios/<int:id>', methods=['GET'])
@token_obrigatorio
def buscar_usuario(usuario,id):
    usuario = Usuario.query.filter_by(id_usuario = id).first()
    if not usuario:
        return jsonify({'Mensagem':' Usuario não encontrado!!'})
    usuario_dict = {}
    usuario_dict['id'] = usuario.id_usuario
    usuario_dict['nome'] = usuario.nome
    usuario_dict['cpf'] = usuario.cpf
    usuario_dict['email'] = usuario.email
    return jsonify({'usuario': usuario_dict})  
    
@app.route('/usuarios', methods=['POST'])
@token_obrigatorio
def adicionar_usuario(usuario):
    novo_usuario = request.get_json()
    usuario = Usuario(nome=novo_usuario['nome'], cpf=novo_usuario['cpf'], email=novo_usuario['email'], senha=novo_usuario['senha'], admin=False)
    db.session.add(usuario)
    db.session.commit()
    return jsonify({'novo_usuario':novo_usuario},' Usuario cadastrado com sucesso!')
   
           
@app.route('/usuarios/<int:id>', methods=['PUT'])
@token_obrigatorio
def alterar_usuario(usuario,id):
    novo_valor = request.get_json()
    usuario = Usuario.query.filter_by(id_usuario = id).first()
    if not usuario:
        return jsonify({'Mensagem':' Usuario nao encontrado!!'})
    try:
        if novo_valor['nome']:
            usuario.nome = novo_valor['nome']
    except:
        pass
    try:
        if novo_valor['cpf']:
            usuario.cpf = novo_valor['cpf']
    except:
        pass
    try:
        if novo_valor['email']:
            usuario.email = novo_valor['email']
    except:
        pass
    try:
        if novo_valor['senha']:
            usuario.senha = novo_valor['senha']
    except:
        pass
    try:
        if novo_valor['admin']:
            usuario.admin = novo_valor['admin']
    except:
        pass        
    
    db.session.commit()
    return jsonify({'usuario_alterado':novo_valor},' Usuario alterado com sucesso!!')

    
@app.route('/usuarios/<int:id>', methods=['DELETE'])
@token_obrigatorio
def excluir_usuario(usuario,id):
    excluir = Usuario.query.filter_by(id_usuario = id).first()
    if not excluir:
        return jsonify({'Mensagem':' Usuario não encontrado'})
    db.session.delete(excluir)
    db.session.commit()
    
    return jsonify({'Mensagem':' Usuario excluido com sucesso!!'})

app.run(host='localhost', port=5000, debug=True)
