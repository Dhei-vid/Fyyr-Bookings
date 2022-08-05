from app import *
import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# TODO IMPLEMENT DATABASE URL
passw = 'admin'
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:'+passw+'@localhost:5432/fyyr'
