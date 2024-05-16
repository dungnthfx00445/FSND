import os
from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from database.models import db_drop_and_create_all, setup_db, Movie, Actor, Property
from auth.auth import requires_auth, AuthError

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object('config')

    # Set up database
    if not test_config:
        setup_db(app)

    # Set up CORS. Allow '*' for origins.
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    app.route('/', methods=['GET']
              )(lambda: jsonify({'message': 'Hello end-user!'}))

    @app.after_request
    def after_request(response):
        """Use the after_request decorator to set Access-Control-Allow"""
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Authorization')
        response.headers.add(
            'Access-Control-Allow-Headers',
            'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    @app.route('/actors', methods=['GET'])
    @requires_auth(permission='get:actors')
    def get_actors(payload=None):
        actors_list = [actor.short() for actor in Actor.query.all()]
        return jsonify({
            'success': True,
            'actors': actors_list
        }), 200

    @app.route('/actors-detail', methods=['GET'])
    @requires_auth(permission='get:actors-detail')
    def get_actors_detail(payload=None):
        actors_list = [actor.long() for actor in Actor.query.all()]
        return jsonify({
            'success': True,
            'actors': actors_list
        }), 200

    @app.route('/actors/<int:actor_id>', methods=['GET'])
    @requires_auth(permission='get:actors-detail')
    def get_actor(payload, actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if not actor:
            abort(code=404)
        return jsonify({
            'success': True,
            'actors': [actor.long()]
        }), 200

    @app.route('/actors', methods=['POST'])
    @requires_auth(permission='post:actors')
    def post_actor(payload=None):
        body = request.get_json()
        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)

        if not name and not age and not gender:
            abort(code=403)
        actor = Actor(name=name, age=age, gender=gender)
        actor.insert()
        return jsonify({
            'success': True,
            'actors': [actor.long()]
        }), 200

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth(permission='patch:actors')
    def patch_actor(payload, actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if not actor:
            abort(code=404)
        body = request.get_json()
        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)

        if not name and not age and not gender:
            abort(code=400)
        actor.name = name
        actor.age = age
        actor.gender = gender
        actor.update()

        return jsonify({
            'success': True,
            'actors': [actor.long()]
        }), 200

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth(permission='delete:actors')
    def delete_actor(payload, actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if not actor:
            abort(code=404)
        actor.delete()
        return jsonify({
            'success': True,
            'delete': id
        }), 200

    @app.route('/movies', methods=['GET'])
    @requires_auth(permission='get:movies')
    def get_movies(payload=None):
        movies_list = [movie.format() for movie in Movie.query.all()]
        return jsonify({
            'success': True,
            'movies': movies_list
        }), 200

    @app.route('/movies', methods=['POST'])
    @requires_auth(permission='post:movies')
    def post_movie(payload=None):
        body = request.get_json()
        title = body.get('title', None)
        release_date = body.get('release_date', None)
        if not title and not release_date:
            abort(code=403)
        movie = Movie(title=title, release_date=release_date)
        movie.insert()
        return jsonify({
            'success': True,
            'movies': movie.format()
        }), 200

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth(permission='patch:movies')
    def patch_movie(payload, movie_id):
        movie = Movie.query.filter(
            Movie.id == movie_id).one_or_none()
        if not movie:
            abort(code=404)
        body = request.get_json()
        title = body.get('title', None)
        release_date = body.get('release_date', None)
        if not title:
            abort(code=400)
        movie.title = title
        movie.release_date = release_date
        movie.update()
        return jsonify({
            'success': True,
            'movies': movie.format()
        }), 200

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth(permission='delete:movies')
    def delete_movie(payload, movie_id):
        movie = Movie.query.filter(
            Movie.id == movie_id).one_or_none()
        if not movie:
            abort(code=404)
        movie.delete()
        return jsonify({
            'success': True,
            'delete': id
        }), 200

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": error.description
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": error.description
        }), 400

    @app.errorhandler(AuthError)
    def auth_error(error):
        response_error = jsonify(error.error)
        response_error.status_code = error.status_code
        return response_error

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
