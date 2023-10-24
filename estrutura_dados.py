# MODULO 09 / AULA 16

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'SA44#$$#@dsf%$@4'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:lQ61OUVM3Qy5aNsv@db.ttisrunypahnqmvjyllh.supabase.co:5432/postgres'

db = SQLAlchemy(app)
db:SQLAlchemy

class Musica(db.Model):
    __tablename__ = 'musica'
    id_musica = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String)
    artista = db.Column(db.String)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'))

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id_usuario = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String)
    cpf = db.Column(db.String)
    email = db.Column(db.String)
    senha = db.Column(db.String)
    admin = db.Column(db.Boolean)
    musicas = db.relationship('Musica')
  

def inicializar_banco():  
    with app.app_context():  
        db.drop_all()
        db.create_all()
        db.session.commit()    


if __name__ == '__main__':
    inicializar_banco()
    