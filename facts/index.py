from flask import Flask, jasonify,request
app =Flask(__name__)


quotes =[
    {'type':'joke','content':"what fields are engineers found in- evwerything except engineering"}
]


@app.route("/jokes")
def jokes():
    return jasonify(jokes)


@app.route('/route',ethods=['POST'])
def add_jokes():
    jokes.append(request.get_json())
    return '',204