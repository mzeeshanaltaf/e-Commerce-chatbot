from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv
from ecommercebot.retrieval_generation import generation
from ecommercebot.ingest import ingest_data

app = Flask(__name__)

load_dotenv()

vstore = ingest_data("done")
chain = generation(vstore)


@app.route("/")
def index():
    return render_template('chat.html')


@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    result = chain.invoke(msg)
    print("Response : ", result)
    return str(result)


if __name__ == '__main__':
    app.run(debug=True)
