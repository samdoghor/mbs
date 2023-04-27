from flasgger import Swagger
from flask import Blueprint, Flask, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api

import config
import routes
from models import db

# configurations
server = Flask(__name__)
server.config['SECRET_KEY'] = config.SECRET_KEY

server.config["SWAGGER"] = {
    "swagger_version": "2.0",
    "title": "MSB API",
    "uiversion": 3,
    "static_url_path": "/apidocs",
}
swagger_config = Swagger.DEFAULT_CONFIG.copy()
swagger_config["openapi"] = "3.0.2"
swagger = Swagger(server, config=swagger_config)

server.debug = config.DEBUG
server.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
server.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config.SQLALCHEMY_TRACK_MODIFICATIONS
db.init_app(server)
db.app = server
migrate = Migrate(server, db)
api = Api(server)

for blueprint in vars(routes).values():
    if isinstance(blueprint, Blueprint):
        server.register_blueprint(
            blueprint, url_prefix=config.APPLICATION_ROOT)

# homepage
@server.route('/')
def index():
        """ Create an customer based on the sent information """

        server = jsonify ({
            "App Name": "MSB App",
            "Current URL" : f"{request.url}",
            "Endpoints Access" : "http://127.0.0.1:3303/api/[endpoints]",
            "Message": "The server is up and running",
            "Version" : "1.0.0"
        })

        return server 


""" Error handling """
# error handler for 422


@server.errorhandler(422)
def unprocessable(error):
    print(error)
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422

# error handler for 400


@server.errorhandler(400)
def bad_request(error):
    print(error)
    return jsonify({
        "success": False,
        "error": 400,
        "message": error.description
    }), 400


# error handler for 401
@server.errorhandler(401)
def unauthorized(error):
    print(error)
    return jsonify({
        "success": False,
        "error": 401,
        "message": error.description
    }), 401


# error handler for 403
@server.errorhandler(403)
def forbidden(error):
    print(error)
    return jsonify({
        "success": False,
        "error": 403,
        "message": error.description
    }), 403


# error handler for 404
@server.errorhandler(404)
def not_found(error):
    print(error)
    return jsonify({
        "success": False,
        "error": 404,
        "message": error.description
    }), 404


# error handler for 500
@server.errorhandler(500)
def internal_server_error(error):
    print({"error": error})
    return jsonify({
        "success": False,
        "error": 500,
        "message": "Internal server error"
    }), 500


if __name__ == "__main__":
    server.debug = config.DEBUG
    server.run(host=config.HOST, port=config.PORT)
