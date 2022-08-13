from flask import Blueprint, jsonify
from app.bp.dao.netflix_dao import NetflixDAO

netflix_instance = NetflixDAO('netflix.db')

main_blueprint = Blueprint('main_blueprint', __name__)


@main_blueprint.route('/')
def index():
    return 'Я главная страничка'


@main_blueprint.route('/movie/<title>')
def search_movie(title):
    movie = netflix_instance.get_movie_by_title(title.lower())
    return jsonify(movie)


@main_blueprint.route('/movie/<int:year_from>/to/<int:year_to>')
def search_movies_by_years(year_from, year_to):
    movies = netflix_instance.get_movies_by_years(year_from, year_to)
    return jsonify(movies)


@main_blueprint.route('/rating/<category>')
def search_movies_by_rating(category):
    movies = netflix_instance.get_movies_by_rating(category.lower())
    return jsonify(movies)


@main_blueprint.route('/genre/<genre>')
def search_movies_by_genre(genre):
    movies = netflix_instance.get_movies_by_genre(genre)
    return jsonify(movies)

