import os
from sqlalchemy import create_engine
import urllib

class Config(object):
  SECRET_KEY = "21000028UTL"
  SESSION_COOKIE_SECURE = False
  
class DevelopmentConfig(object):
  DEBUG = True
  SQLALCHEMY_DATABASE_URL = "mysql+pymsql://root:1234@127.0.01/bdidgs801"
  SQLALCHEMY_TRACK_MODIFIVATIONS = False