from flask import Flask , request ,jsonify
import simplejson as json
from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin



app = Flask(__name__)
 

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['MONGO_DBNAME'] = 'dellprod'
app.config['MONGO_URI'] = 'mongodb://umaniax:hello1234@ds125342.mlab.com:25342/dellprod'
          
mongo = PyMongo(app)    


@app.route('/')
@cross_origin()
def hello_world():
	return "Hello World,Pulkit and Saatvik here"


if __name__ == "__main__":
	app.run()	

