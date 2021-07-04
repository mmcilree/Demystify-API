from flask import Flask
from demystify.explain import Explainer  

app = Flask(__name__)             


@app.route("/")                   
def hello():                      
    return "Hello World!"

if __name__ == "__main__":        
    app.run()                     