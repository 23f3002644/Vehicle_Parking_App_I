from flask import Flask
from application.database import db

app = None

def create_app():
    app = Flask(__name__)
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parking.sqlite3'
    db.init_app(app)
    app.app_context().push() #if you dont write the line, run time error, bring everything under the context of flask application
    return app

app = create_app()
from application.controllers import *

#from application.models import *    
#indirect importation from controllers.py

if __name__ =='__main__':
    app.run()


