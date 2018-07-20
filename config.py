import os

class Config(object):
    SECRET_KEY=os.getenv("secret_key")

class DevelopmentConfig(Config):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI = os.getenv("sql_uri")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
