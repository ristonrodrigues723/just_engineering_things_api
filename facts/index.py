import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import os
import json
import logging
import tempfile

cred = credentials.Certificate('/home/maximus723/pub/vercel/serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL':'https://flask-api-fadda-default-rtdb.firebaseio.com'
})
from flask import Flask, jsonify,request

# from marshmallow import ValidationError was for dtaa-type validation but now theres really no use of it
from flask import Flask, jsonify,request

app =Flask(__name__)


# jokes =[- the data needs to be saved and retrived so im tryin to use json file will be more useful
#     {   
#         'varient':'joke',
#         'content':"what fields are engineers found in- evwerything except engineering"}
# ]
# jokes=[]

logging.basicConfig(level=logging.INFO)
logger =logging.getLogger(__name__)

# DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")- data is saved to firebase so its no longer nedded
jokes_ref =db.reference('jokes')
quotes_ref = db.reference('quotes')
facts_ref = db.reference('facts')



# def load_the_data_from_json():
#     try:
#         with open(DATA_FILE, 'r') as file:
#             data = json.load(file)
#             return data.get('jokes',[]), data.get('quotes',[]),data.get('facts',[])
            
#     except FileNotFoundError:
#         logger.warning(f"file for data {DATA_FILE}isnt there u sure, well create new till tgen ")
#         return [],[],[]
#     except json.JSONDecodeError:
#         logger.error(f"error decoding{DATA_FILE}. damn curruption")
#         return [],[],[]
#         raise

# jokes, quotes,facts =load_the_data_from_json()



#using firebase to support vercel so this isnt needed
# def save_data(jokes,quotes,facts):
#     try:
    
#         with open(DATA_FILE, 'w') as file:
#             json.dump({'jokes': jokes, 'quotes': quotes, 'facts': facts}, file, indent=2)
#         logger.info("data successfully saved to file")
#     except Exception as e:
#         logger.error(f"error saving data:{str(e)}")
#         raise


@app.route('/')
def home():
    return "Welcome to the API i made this is to test if it corretly works on vercel use !  the /jokes, /quotes, or /facts routes."
@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')


@app.route("/jokes")
def get_jokes():
    # schema = JokeSchema(many=True)
    #no schema verifiaction being done nor loading from json anymore 
    jokes_ref=db.reference('jokes')
    jokes =jokes_ref.get()
    return jsonify(jokes)



@app.route('/jokes',methods=['POST'])
def add_jokes():
    try:

        if not request.is_json:
            return jsonify({"error":"Content -type is wrng json it shld be"}), 415
        joke = request.get_json()
        if not isinstance(joke, dict) or 'content' not in joke:
            return jsonify({"error":"Invalid format "}) , 400
        

        jokes_ref =db.reference('jokes')
        new_joke_id =jokes_ref.push().key
        new_joke = {
            'id':len(jokes_ref.get() or []) +1,
            'content':joke['content'],
            'ratings':[],
            'average_rating':0
         }

        jokes_ref.child(new_joke_id).set(new_joke)
        return jsonify({"message": "success", "joke": new_joke}), 201

    except Exception as e:
        logger.error(f"error adding joke: {str(e)}")

        return jsonify({"error":"internal server error"}), 500
    


@app.route("/quotes")
def get_quotes():
    quotes_ref =db.reference('quotes')
    quotes =quotes_ref.get()
    # schema = QuoteSchema(many=True)-- it is used to verify data type advanced jasonification and so ill link the blog but when i proceed firther it gets medded upp
    return jsonify(quotes)


# @app.route("/quotes",methods=['POST'])
# def add_quotes():
#     if request.content_type !='application/json':
#         return jsonify({"error":"content not application/json"}),415
#     quote =request.get_json()
#     quotes.append(quote)
#     save_data()
#     return'',204


@app.route("/facts")
def get_facts():
    facts_ref =db.reference('facts')
    facts = facts_ref.get()
    # schema= FactSchema(many=True)
    return jsonify(facts)

# @app.route("/facts",methods=['POST'])
# def add_facts():
#     if request.content_type !='application/json':
#         return jsonify({"error:":"contwent not json"})
#     fact = request.get_json()
#     facts.append(fact)
#     save_data()
#     return'',204

@app.route("/rate/<int:content_id>",methods=['POST'])
# def rate_content(content_type, content_id):
def rate_joke(content_id):
    try:
        
        rating_data = request.get_json()
        rating =rating_data.get('rating')
        if not rating or not  (1 <= rating <=5 ):
            return jsonify({"error":"Invalid rating"}), 400
    
        jokes_ref = db.reference('jokes')
        jokes =jokes_ref.get()

        for key, joke in jokes.items():
            if joke.get('id') == content_id:
               ratings =joke.get('ratings',[])
               ratings.append(rating)
               joke['average_rating'] = sum(ratings) / len(ratings)
               joke['ratings'] = ratings
               jokes_ref.child(key).set(joke)
               return jsonify({"message":"success","joke":joke}), 200
        
        return jsonify({"error":"Joke not found"}), 404

    #     try:
#         if not request.is_json:
#             return jsonify({'error':"content not app/json"}), 415
        
#         rating = request.get_json().get('rating') 
#         # fixed used grt insted of get thats why i as getting error for server
#         if not isinstance(rating, (int,float)) or not 1<= rating <=5:
#             return jsonify({"error " :"pls keep it between 1 and 5 if u dont want to retry aGAIN"}), 400
    
#         content_map={
#             'jokes':jokes_ref,
#             'quotes':quotes_ref,
#             'facts':facts_ref,
#         }


#         if content_type not in content_map:
#             return jsonify({"error":"invalid type pls only 3 among jokes facts and quotes are allowed"}), 400
#         content_ref = db.reference(content_map[content_type]).child(str(content_id))
#         content =content_ref.get()
        

    except Exception as e:
        logger.error(f"same error addin string")
        return jsonify({"error":"internal server"}), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 8050)), debug=True)
