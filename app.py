from flask import Flask, request
from flask_cors import CORS
from demystify.explain import Explainer  
import logging
from rq import Queue
from rq.job import Job
from worker import conn

import time

app = Flask(__name__)
CORS(app)

q = Queue(connection=conn)

logging.basicConfig(level=logging.DEBUG)

def run_demystify(eprime_name, eprime, param_name, param, num_steps):
    explainer = Explainer("cascade")

    eprime_file = open(eprime_name, "w")
    eprime_file.write(eprime)
    param_file = open(param_name, "w")
    param_file.write(param)

    explainer.init_from_essence(eprime_name, param_name)

    return explainer.explain_steps(num_steps=num_steps)

@app.route("/")                   
def index():                      
    return "Demystify API is running."

@app.route('/job', methods=['POST'])
def create_job():
    json = request.get_json(force=True)
    
    job = q.enqueue_call(
            func=run_demystify, 
            args=(
                json["eprimeName"], 
                json["eprime"],
                json["paramName"],
                json["param"],
                json["numberOfSteps"]
                ), result_ttl=5000
        )
    print(job.get_id())
    return "create_job()"

@app.route('/job/<string:job_id>', methods=['GET'])
def get_job(job_id):    
    job = Job.fetch(job_id, connection=conn)

    if job.is_finished:
        return "Job finished", 200
    else:
        return "Nay!", 202

@app.route('/job/<string:job_id>', methods=['POST'])
def continue_job(job_id):    
    return f'continue_job({job_id})'

@app.route('/job/<string:job_id>', methods=['GET'])
def get_job_output(job_id):    
    return f'get_job_output({job_id})'

if __name__ == "__main__":      
    app.run()                     