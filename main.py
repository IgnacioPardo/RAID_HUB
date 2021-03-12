from flask import Flask, send_from_directory, request, Response
import requests
import codecs, json
import os
from nodes import *
from nodes import _set, _get, _get_node, add_node, node_list
from checks import *

#Threading
from threading import Thread

#WSGIServer
from gevent.pywsgi import WSGIServer
"""
#Disable Warnings
import warnings
warnings.filterwarnings('ignore')

#Logging
import logging

#Logging configuration set to debug on debug.log file
logging.basicConfig(filename='debug.log',level=logging.DEBUG)
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

#Disable unneeded dependencies logging
werkzeugLog = logging.getLogger('werkzeug')
werkzeugLog.disabled = True
requestsLog = logging.getLogger('urllib3.connectionpool')
requestsLog.disabled = True
"""
def run():
	#WSGIServer
	WSGIServer(('', 8081), app).serve_forever()

#Thread
def keep_alive():
	t = Thread(target=run)
	t.start()

app = Flask(__name__)

@app.route('/')
def main():
	node_loc = str("https://" + os.getenv("REPL_SLUG") + "." + os.getenv("REPL_OWNER") + ".repl.co").lower()
	return '<head><meta name="viewport" content="initial-scale=1"></head><body style="background:black;font-family: Futura; color: white;"><style type="text/css">a:link {color: white;} a:visited {color: white;} a:hover {color: white;} a:active {color: white;} </style><br><br><center><a class="RAID_NODE" href="'+node_loc+'">' + os.getenv("REPL_SLUG") + '</a><br><br>'+str((amm := len(node_list())))+' node'+'s'*(not amm == 1)+'</center></body>'

@app.route('/set', methods=['POST'])
@app.route('/set/<_id>', methods=['POST'])
def set_data(_id=None):
	if request.method == 'POST':
		try:
			response = _set(json.loads(request.form["request"]), _id)
			return response
		except:
			return {'success': False, "error": "POST TO NODE ERROR"}
	return {'success': False, "error": "HUB ERROR, bad request"}

@app.route('/getAll')
@app.route('/get')
@app.route('/get/<_id>')
def get_data(_id=None):
	return _get(_id)

@app.route('/announce_self', methods=['POST'])
def announcment():
	if request.method == 'POST':
		try:
			url = json.loads(request.form["request"])["node_url"]
			i = add_node(url)
			return {'success': True, "node_id": str(i)}
		except:
			return {'success': False, "error": None}
	return {'success': False, "error": None}

if __name__ == '__main__':
	#Run server forever
	keep_alive()
