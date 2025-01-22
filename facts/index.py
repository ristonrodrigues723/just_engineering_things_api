from flask import Flask, jsonify,request
from model.quotes import JokeSchema,QuoteSchema,FactSchema
# from marshmallow import ValidationError was for dtaa-type validation but now theres really no use of it
import json
import logging
import os 

app =Flask(__name__)


# jokes =[- the data needs to be saved and retrived so im tryin to use json file will be more useful
#     {   
#         'varient':'joke',
#         'content':"what fields are engineers found in- evwerything except engineering"}
# ]
# jokes=[]

logging.basicConfig(level=logging.INFO)
logger =logging.getLogger(__name__)

DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")



def load_the_data_from_json():
    try:
        with open(DATA_FILE, 'r') as file:
            data = json.load(file)
            return data.get('jokes',[]), data.get('quotes',[]),data.get('facts',[])
            
    except FileNotFoundError:
        logger.warning(f"file for data {DATA_FILE}isnt there u sure, well create new till tgen ")
        return [],[],[]
    except json.JSONDecodeError:
        logger.error(f"error decoding{DATA_FILE}. damn curruption")
        return [],[],[]
        raise

jokes, quotes,facts =load_the_data_from_json()




def save_data(jokes,quotes,facts):
    try:
    
        with open(DATA_FILE, 'w') as file:
            json.dump({'jokes': jokes, 'quotes': quotes, 'facts': facts}, file, indent=2)
        logger.info("data successfully saved to file")
    except Exception as e:
        logger.error(f"error saving data:{str(e)}")
        raise




@app.route("/jokes")
def get_jokes():
    # schema = JokeSchema(many=True)
    return jsonify(jokes)



@app.route('/jokes',methods=['POST'])
def add_jokes():
    try:

        if not request.is_json:
            return jsonify({"error":"Content -type is wrng json it shld be"}), 415
        joke = request.get_json()
        if not isinstance(joke, dict) or 'content' not in joke:
            return jsonify({"error":"Invalid format "}) , 400
         
        new_joke = {
            'id':len(jokes) +1,
            'content':joke['content'],
            'ratings':[],
            'average_rating':0
         }

        jokes.append(new_joke)
        save_data(jokes,quotes,facts)
        logger.info(f"addednewer jok:{new_joke}")
        return jsonify({"message": "success", "joke": new_joke}), 201

    except Exception as e:
        logger.error(f"error adding joke: {str(e)}")

        return jsonify({"error":"internal server error"}), 500
    


@app.route("/quotes")
def get_quotes():
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

@app.route("/rate/<string:content_type>/<int:content_id>",methods=['POST'])
def rate_content(content_type, content_id):
    try:
        if not request.is_json:
            return jsonify({'error':"content not app/json"}), 415
        
        rating = request.get_json().get('rating') 
        # fixed used grt insted of get thats why i as getting error for server
        if not isinstance(rating, (int,float)) or not 1<= rating <=5:
            return jsonify({"error " :"pls keep it between 1 and 5 bro"}), 400
    
        content_map={
            'jokes':jokes,
            'quotes':quotes,
            'facts':facts,
        }


        if content_type not in content_map:
            return jsonify({"error":"invalid type pls only 3 among jokes facts and quotes are allowed"}), 400

        content_list = content_map[content_type]




        for item in content_list:
            if item['id']== content_id:
                item['ratings'].append(rating)
                item['average_rating']= sum(item['ratings']) /len(item['ratings'])
                save_data(jokes,quotes,facts)
                return jsonify({
                    "message":"sucessfully added rating",
                    "content_type": content_type,
                    "content":item


         
         
                }), 200

        return jsonify({"error":f"{content_type} with id {content_id} not found pls tary aggain or msg the owner"}), 404

    except Exception as e:
        return jsonify({"error":"internal server"}), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5050,debug=True)