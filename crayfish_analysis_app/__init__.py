from flask import Flask


def create_app(config_class_name):
    """Create and configure the Flask app"""
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "123"
    app.config.from_object(config_class_name)
    # Include the routes from hello.py
    with app.app_context():
        from . import hello

    return app