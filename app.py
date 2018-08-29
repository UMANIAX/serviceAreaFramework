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

@app.route('/ibm', methods=['GET'])
@cross_origin()
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

@app.route('/complaintsX',methods=['GET'])
@cross_origin()
def complaintAverage(**kwargs):
	k = [] 
	mycol4 = mongo.db.sentiments
	mydoc4 = mycol4.find({})
	i=0 
	for x in mongo.db.sentiments.find({}).sort('date',-1):
    	j = {} 
		print(x)
        print(x['date'])
        if i>6:
            break
        j["date"] = x['date']
        j["score"] = x['averageComplaintSentiment']
        k.append(j) 
        i+=1

    response = jsonify(k) 
    response.status_code = 200

    print(k ,"K is ")

    return response

@app.route('/sentimentX',methods=['GET'])
@cross_origin()
def sentimentAverage(**kwargs):
	k = [] 
	mycol6 = mongo.db.sentiments
	mydoc6 = mycol6.find({})

	i=0 

	for x in mongo.db.sentiments.find({}).sort('date',-1):
		j = {} 
		if i>6:
			break
		j["date"] = x['date']
		j["score"] = x['averageSentiment']
		k.append(j)
		i+=1  

	response = jsonify(k) 
	response.status_code = 200

	
	return response


@app.route('/reviewX',methods=['GET'])
@cross_origin()
def reviewAverage(**kwargs):

	k = [] 
	j = {} 

	i=0 

	for x in mongo.db.sentiments.find({}).sort('date',-1):
		j = {} 
		if i>6:
			break
		j["date"] = x['date']
		j["score"] = x['averageReview']
		k.append(j)
		i+=1 
	response = jsonify(k) 
	response.status_code = 200


	return response

@app.route('/productViewed',methods=['GET'])
@cross_origin()
def productViewed(**kwargs):
	mycol5 = mongo.db.customermls
	mydoc5 = mycol5.find({})
	l1 = 0
	l2 = 0
	l3 = 0
	for x in mydoc5:
		l1+=x['c1']
		l2+=x['c2']
		l3+=x['c3']
	k = [{"l1":l1},{"l1":l2},{"l1":l3}]

	response = jsonify(k) 
	response.status_code = 200

	print(k ,"K is ")

	return response

@app.route('/productBought',methods=['GET'])
@cross_origin()
def productBought(**kwargs):
	mycol5 = mongo.db.customermls
	mydoc5 = mycol5.find({})

	l1 = 0
	l2 = 0
	l3 = 0
	
	for x in mydoc5:
		l1+=x['p1']
		l2+=x['p2']
		l3+=x['p3']

	k = [{"l1":l1},{"l1":l2},{"l1":l3}]
	response = jsonify(k) 
	response.status_code = 200

	print(k ,"K is ")

	return response	
if __name__ == "__main__":
	app.run()	

