from flask import Flask, send_from_directory, request, Response
import requests
import codecs, json
import os
from nodes import *


#Threading
from threading import Thread

#WSGIServer
from gevent.pywsgi import WSGIServer

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
	return "RAID0"

@app.route('/announce_self', methods=['POST'])
def announcment():
	if request.method == 'POST':
		try:
			url = json.loads(request.form["request"])["node_url"]
			return add_node(url)
		except:
			return 400
	return 400


if __name__ == '__main__':
	#Run server forever
	keep_alive()
