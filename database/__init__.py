from pymongo import MongoClient
from .db import Database
import app_config

database = Database(app_config.CONST_DATABASE, app_config.CONST_MONGO_URL)
database.connect()