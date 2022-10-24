import os
from flask import Flask
from flask_restful import Resource,Api
from application import config
from application.config import Config
from application.database import db
from application.api import User_API, trackerAPI, logAPI
from flask_security import Security, SQLAlchemyUserDatastore, auth_required, SQLAlchemySessionUserDatastore
from application.models import Users as User, Role
from flask_security import utils

app = None
api = None

def create_app():
    app = Flask(__name__, template_folder="templates")
    print("Staring Local Development")
    app.config.from_object(Config)
    db.init_app(app)
    api = Api(app)
    app.app_context().push()
    user_datastore = SQLAlchemySessionUserDatastore(db.session, User,Role)
    security = Security(app, user_datastore)
    return app, api

app, api = create_app()

api.add_resource(User_API, "/api/user")
api.add_resource(trackerAPI, "/api/tracker/<uID>","/api/tracker/delete/<tID>", "/api/tracker")
api.add_resource(logAPI, "/api/log", "/api/log/delete/<lid>", "/api/log/<tid>")


# Import all the controllers so they are loaded
from application.controllers import *

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.errorhandler(403)
def not_authorized(e):
    # note that we set the 403 status explicitly
    return render_template('403.html'), 403

if __name__ == '__main__':
  app.run(host='0.0.0.0',port=8080)
