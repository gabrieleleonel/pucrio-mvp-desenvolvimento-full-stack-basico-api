from flask import Flask, redirect, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///games.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
swagger = Swagger(app, template={
    "info": {
        "title": "Game Tracker API",
        "description": "API para gerenciar uma lista de jogos",
        "version": "1.0.0"
    }
})

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    platform = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), nullable=False) # 'Quero Jogar', 'Jogando', 'Finalizado'
    url_image = db.Column(db.String(200), nullable=True) # URL da imagem do jogo

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'platform': self.platform,
            'status': self.status,
            'url_image': self.url_image,
        }

with app.app_context():
    db.create_all()

@app.route('/')
def redirect_to_docs():
    return redirect('/apidocs')

@app.route('/games', methods=['GET'])
def get_games():
    """
    Lista todos os jogos cadastrados
    ---
    responses:
      200:
        description: Retorna a lista de jogos
    """
    games = Game.query.all()
    return jsonify([game.to_dict() for game in games]), 200

@app.route('/games/<int:id>', methods=['GET'])
def get_game(id):
    """
    Busca um jogo específico pelo ID
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID do jogo
    responses:
      200:
        description: Dados do jogo
      404:
        description: Jogo não encontrado
    """
    game = Game.query.get(id)
    if game:
        return jsonify(game.to_dict()), 200
    return jsonify({'mensagem': 'Jogo não encontrado'}), 404

@app.route('/games', methods=['POST'])
def add_game():
    """
    Cadastra um novo jogo
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
              example: The Legend of Zelda
            platform:
              type: string
              example: Nintendo Switch
            status:
              type: string
              example: Quero Jogar
            url_image:
              type: string
              example: https://example.com/image.jpg
    responses:
      201:
        description: Jogo cadastrado com sucesso
      400:
        description: Dados incompletos
    """
    data = request.get_json()

    print(data.get('platform'))

    if not data or not data.get('title') or not data.get('platform') or not data.get('status'):
        print("oxi")
        return jsonify({'mensagem': 'data incompletos!'}), 400
        
    new_game = Game(
        title=data.get('title'),
        platform=data.get('platform'),
        status=data.get('status'),
        url_image=data.get('urlImage') or ''
    )
    
    db.session.add(new_game)
    db.session.commit()
    
    return jsonify({'mensagem': 'Jogo adicionado com sucesso!', 'game': new_game.to_dict()}), 201

@app.route('/games/<int:id>', methods=['PUT'])
def update_game(id):
    """
    Atualiza o status ou dados de um jogo
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            status:
              type: string
              example: Finalizado
    responses:
      200:
        description: Jogo atualizado
      404:
        description: Jogo não encontrado
    """
    game = Game.query.get(id)
    if not game:
        return jsonify({'mensagem': 'Jogo não encontrado'}), 404
        
    data = request.get_json()
    if 'status' in data:
        game.status = data.get('status')
    if 'platform' in data:
         game.platform = data.get('platform')
    if 'url_image' in data:
         game.url_image = data.get('urlImage')
    if 'title' in data:
         game.title = data.get('title')
         
    db.session.commit()
    return jsonify({'mensagem': 'Jogo atualizado!', 'jogo': game.to_dict()}), 200

@app.route('/games/<int:id>', methods=['DELETE'])
def delete_game(id):
    """
    Remove um jogo da lista
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Jogo removido
      404:
        description: Jogo não encontrado
    """
    game = Game.query.get(id)
    if not game:
        return jsonify({'mensagem': 'Jogo não encontrado'}), 404
        
    db.session.delete(game)
    db.session.commit()
    return jsonify({'mensagem': 'Jogo removido com sucesso!'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)    
    