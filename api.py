# Importa as classes necessárias do Flask e do SQLAlchemy
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Cria uma instância da aplicação Flask
app = Flask(__name__)

# Configuração do banco de dados SQLite, criando arquivo movies.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'

# Cria uma instância do SQLAlchemy, para interagir com o banco de dados
db = SQLAlchemy(app)

# Cria uma instância do Migrate para facilitar as migrações do banco de dados
migrate = Migrate(app, db)

# Define uma classe Movie que herda de db.Model (SQLAlchemy) para representar a tabela 'movie' no banco de dados
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Float, nullable=True)

    # Método para facilitiar a conversão para o formato JSON
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'rating': self.rating
        }

# Cria uma rota para obter filmes não avaliados
@app.route('/movies/unrated', methods=['GET'])
def unrated_movies():
    # Consulta o banco de dados para obter todos os filmes sem avaliação
    unrated_movies = Movie.query.filter(Movie.rating.is_(None)).all()

    # Serializa os filmes obtidos para o formato JSON
    serialized_movies = [movie.serialize() for movie in unrated_movies]

    # Retorna a lista de filmes não avaliados em formato JSON
    if not serialized_movies:
        return jsonify({'message': 'Nenhum filme não avaliado encontrado'})
    
    return jsonify({'unrated_movies': serialized_movies})

# Cria uma rota para adicionar um novo filme
@app.route('/movies/add', methods=['POST'])
def add_movie():
    # Obtém os dados do corpo da requisição em formato JSON
    data = request.get_json()
    
    # Verifica se a chave 'rating' está presente 
    if 'rating' in data:
        new_movie = Movie(title=data['title'], rating=data['rating'])
    else:
        # Se 'rating' não estiver presente, atribui None ao campo 'rating'
        new_movie = Movie(title=data['title'], rating=None)

    # Adiciona o novo filme ao banco de dados
    db.session.add(new_movie)
    
    # Confirma a transação no banco de dados
    db.session.commit()

    # Retorna uma mensagem indicando que o filme foi adicionado com sucesso, junto com os dados do filme em formato JSON
    return jsonify({'message': 'Filme adicionado com sucesso', 'movie': new_movie.serialize()})


# Cria uma rota para visualizar todos os filmes no banco de dados
@app.route('/movies/all', methods=['GET'])
def view_all_movies():
    # Consulta o banco de dados para obter todos os filmes
    movies = Movie.query.all()

    # Serializa os filmes obtidos para o formato JSON
    serialized_movies = [movie.serialize() for movie in movies]

    # Retorna a lista de todos os filmes em formato JSON
    return jsonify({'movies': serialized_movies})

# Cria uma rota para visualizar um filme específico pelo seu ID
@app.route('/movies/<int:movie_id>', methods=['GET'])
def view_movie(movie_id):
    # Consulta o banco de dados para obter um filme pelo ID
    movie = Movie.query.get(movie_id)

    # Verifica se o filme foi encontrado
    if not movie:
        return jsonify({'message': 'Filme não encontrado'}), 404
    
    # Retorna os dados do filme em formato JSON
    return jsonify({'movie': movie.serialize()})

# Cria uma rota para atualizar as informações de um filme pelo seu ID
@app.route('/movies/update/<int:movie_id>', methods=['PUT'])
def update_movie(movie_id):
    # Consulta o banco de dados para obter um filme pelo ID
    movie = Movie.query.get(movie_id)

    # Verifica se o filme foi encontrado
    if not movie:
        return jsonify({'message': 'Filme não encontrado'}), 404

    # Obtém os dados do corpo da requisição em formato JSON
    data = request.get_json()

    # Atualiza as informações do filme com base nos dados fornecidos
    movie.title = data.get('title', movie.title)
    movie.rating = data.get('rating', movie.rating)

    # Confirma a transação no banco de dados
    db.session.commit()

    # Retorna uma mensagem indicando que o filme foi atualizado com sucesso
    return jsonify({'message': 'Filme atualizado com sucesso'})

# Cria uma rota para excluir um filme pelo seu ID
@app.route('/movies/delete/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    # Consulta o banco de dados para obter um filme pelo ID
    movie = Movie.query.get(movie_id)

    # Verifica se o filme foi encontrado
    if not movie:
        return jsonify({'message': 'Filme não encontrado'}), 404

    # Remove o filme do banco de dados
    db.session.delete(movie)

    # Confirma a transação no banco de dados
    db.session.commit()

    # Retorna uma mensagem indicando que o filme foi excluído com sucesso
    return jsonify({'message': 'Filme excluído com sucesso'})

# Rota padrão que retorna uma mensagem simples
@app.route('/')
def hello():
    return 'API de Filmes!'

# Executa a aplicação Flask
if __name__ == '__main__':
    app.run()
