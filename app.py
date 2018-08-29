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

@app.route('/ibm')
@cross_origin()
def tone_analysis():
	def ibm_score(**kwargs):
	tone_analyzer = ToneAnalyzerV3(
	version='2017-09-21',
	username="27edc35f-d026-4dd3-930e-bac1f6fe10ef",
	password="FmEiqWUBJmDN")

	data = request.args 

	reviewCount = int(data['reviewCount'])

	
	try :
		prevReviewScore = float(data['prevReviewScore'])
	except :
		prevReviewScore = 0 
		print("null value handled well ")
	text = data['reviewText'] 

	tone_analysis = tone_analyzer.tone({'text': text},'application/json')
	j = json.dumps(tone_analysis, indent=2)
	d = json.loads(j)
	print (d)

	intent = {"Anger":2,"Joy":5,"Sadness":3,"Fear":3,"Confident":4,"Tentative":2,"Analytical":3}

	i = 0
	s = 0
	count = 0
	while True:
		try:
			s+=(intent[d["document_tone"]["tones"][i]["tone_name"]])*(d["document_tone"]["tones"][i]["score"])
			i+=1
			count+=1
		except:
			if (count!=0):
				s= s/count
			count = 0	
			break	

	finalScore = (s*(reviewCount+1) + prevReviewScore*reviewCount )/(reviewCount * 2 + 1)  

	response = jsonify({'score': str(finalScore)})

	response.status_code = 200
	
	return response


if __name__ == "__main__":
	app.run()	

