from flask import Flask, request, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
from bson import ObjectId
import os, socket, json
from pprint import pprint

load_dotenv()
username = os.getenv('MONGO_USERNAME')
password = os.getenv('MONGO_PASSWORD')
hostname = os.getenv('MONGO_HOSTNAME')
database = os.getenv('MONGO_DATABASE')
collection = os.getenv('MONGO_COLLECTION')
URI = f"mongodb://{username}:{password}@{hostname}/{database}"
mongo_client = MongoClient(URI)
mydb = mongo_client[f"{database}"]
mycollection = mydb[f"{collection}"]

app = Flask(__name__)

@app.route('/')
def socket_info():
	host_info = socket.gethostname()
	ipaddr = socket.gethostbyname(host_info)
	device_info = {"host": host_info, "ipaddr": ipaddr}
	return jsonify(device_info)

@app.route('/dogs')
def dogs_records():
	dog_records = list(mycollection.find())
	for dog in dog_records:
		dog["_id"] = str(dog["_id"])
		pprint(dog)
	json_data = jsonify(dog_records)
	return json_data

if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0',port=5600)
