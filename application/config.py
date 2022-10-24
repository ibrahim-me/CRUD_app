import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    SQLITE_DB_DIR = os.path.join(basedir, "../db_directory")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(SQLITE_DB_DIR, "database.sqlite3")
    DEBUG = True
    SECRET_KEY =  "12345678"
    SECURITY_PASSWORD_HASH = "bcrypt"    
    SECURITY_PASSWORD_SALT = "salt123" 
    SECURITY_REGISTERABLE = True
    SECURITY_CONFIRMABLE = False
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_UNAUTHORIZED_VIEW = None
    SECURITY_USERNAME_ENABLE = True
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authentication-Token"
    
