import logging

from flask import Flask, request
from flask_cors import CORS
from rq import Queue

from worker import conn
from routes import bp as routes

app = Flask(__name__)
CORS(app)

q = Queue(connection=conn)

logging.basicConfig(level=logging.DEBUG)
app.register_blueprint(routes)

if __name__ == "__main__":      
    app.run()                     