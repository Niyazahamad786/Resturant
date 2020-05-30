from flask import Flask
app = Flask(__name__)
app.config['SECRET_KEY']='heelo therer'
from flask_bcrypt import Bcrypt
bcrypt=Bcrypt(app)

from all  import routes