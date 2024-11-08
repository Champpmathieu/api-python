from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///livros.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Definindo o modelo Livro
class Livro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    autor = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'título': self.titulo,
            'autor': self.autor
        }

# Cria o banco de dados
with app.app_context():
    db.create_all()

# Consultar todos
@app.route('/livros', methods=['GET'])
def obter_livros():
    livros = Livro.query.all()
    return jsonify([livro.to_dict() for livro in livros])

# Consultar por ID
@app.route('/livros/<int:id>', methods=['GET'])
def obter_livro_por_id(id):
    livro = Livro.query.get(id)
    if livro:
        return jsonify(livro.to_dict())
    return jsonify({"mensagem": "Livro não encontrado!"}), 404

# Editar
@app.route('/livros/<int:id>', methods=['PUT'])
def editar_livro_por_id(id):
    livro_alterado = request.get_json()
    livro = Livro.query.get(id)
    if livro:
        livro.titulo = livro_alterado.get('título', livro.titulo)
        livro.autor = livro_alterado.get('autor', livro.autor)
        db.session.commit()
        return jsonify(livro.to_dict())
    return jsonify({"mensagem": "Livro não encontrado!"}), 404

# Criar
@app.route('/livros', methods=['POST'])
def incluir_novo_livro():
    novo_livro = request.get_json()
    livro = Livro(titulo=novo_livro['título'], autor=novo_livro['autor'])
    db.session.add(livro)
    db.session.commit()
    return jsonify(livro.to_dict()), 201

# Excluir
@app.route('/livros/<int:id>', methods=['DELETE'])
def excluir_livro(id):
    livro = Livro.query.get(id)
    if livro:
        db.session.delete(livro)
        db.session.commit()
        return jsonify({"mensagem": "Livro excluído!"}), 204
    return jsonify({"mensagem": "Livro não encontrado!"}), 404

if __name__ == '__main__':
    app.run(port=5000, host='localhost', debug=True)

