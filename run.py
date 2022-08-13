from flask import Flask
from app.bp.views import main_blueprint

app: Flask = Flask(__name__)

app.config['JSON_SORT_KEYS'] = False
app.register_blueprint(main_blueprint)


if __name__ == "__main__":
    app.run()

