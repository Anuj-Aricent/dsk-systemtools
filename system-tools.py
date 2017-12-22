import sys
import os
import time
import requests
import redis

from flask import Flask, request
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)
redis_db = redis.StrictRedis(host=str(os.environ['REDIS_SERVICE_HOST']), port=str(os.environ['REDIS_SERVICE_PORT']))

class SystemToolTime(Resource):
    def get(self):
        ##url = "http://" + os.environ['APP'] + "-system-time:10002/time"
        #url = "http://" + os.environ['APP'] + "-system-time"
        
        ms_json = eval(redis_db.get('SYSTEM-TIME-DSK'))
        url = str(ms_json["10002"])
        headers = {            
            'API-KEY': redis_db.get('API-KEY')
            }
        resp = requests.request("GET", url, headers=headers)
        #resp = requests.get(url)
        return resp.json()


class SystemToolUpTime(Resource):
    def get(self):
        ##url = "http://" + os.environ['APP'] + "-system-uptime:10004/uptime"
        #url = "http://" + os.environ['APP'] + "-system-uptime"
        ms_json = eval(redis_db.get('SYSTEM-UPTIME-DSK'))
        url = str(ms_json["10004"])
        headers = {            
            'API-KEY': redis_db.get('API-KEY')
            }
        resp = requests.request("GET", url, headers=headers)
        #resp = requests.get(url)
        return resp.json()


api.add_resource(SystemToolTime, '/systemtoolstime')
api.add_resource(SystemToolUpTime, '/systemtoolsuptime')


if __name__ == '__main__':
    if(len(sys.argv) > 1):
        run_port = sys.argv[1]
    else:
        run_port = 10000
    
    app.run(host='0.0.0.0',port=int(run_port), debug=True)
