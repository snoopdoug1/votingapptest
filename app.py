import os
from random import randrange
from multiprocessing import Pool, cpu_count

import simplejson as json
import boto3
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

cors = CORS(app, resources={r"/api/*": {"Access-Control-Allow-Origin": "*"}})

cpustressfactor = int(os.getenv('CPUSTRESSFACTOR', 1))
memstressfactor = int(os.getenv('MEMSTRESSFACTOR', 1))
ddb_aws_region = os.getenv('DDB_AWS_REGION')
ddb_table_name = os.getenv('DDB_TABLE_NAME', "votingapp-restaurants")

ddb = boto3.resource('dynamodb', region_name=ddb_aws_region)
ddbtable = ddb.Table(ddb_table_name)

print(f"The cpustressfactor variable is set to: {cpustressfactor}")
print(f"The memstressfactor variable is set to: {memstressfactor}")
memeater = [0 for _ in range(10000)]


def consume_cpu(_):
    for _ in range(1000000 * cpustressfactor):
        pass


def readvote(restaurant):
    response = ddbtable.get_item(Key={'name': restaurant})
    # this is required to convert decimal to integer
    normilized_response = json.dumps(response)
    json_response = json.loads(normilized_response)
    votes = json_response["Item"]["restaurantcount"]
    return str(votes)


def updatevote(restaurant, votes):
    ddbtable.update_item(
        Key={'name': restaurant},
        UpdateExpression='SET restaurantcount = :value',
        ExpressionAttributeValues={':value': votes},
        ReturnValues='UPDATED_NEW'
    )
    return str(votes)


@app.route('/')
def home():
    return (
        "<h1>Welcome to the Voting App</h1>"
        "<p><b>To vote, you can call the following APIs:</b></p>"
        "<p>/api/outback</p><p>/api/bucadibeppo</p><p>/api/ihop</p><p>/api/chipotle</p>"
        "<b>To query the votes, you can call the following APIs:</b>"
        "<p>/api/getvotes</p>"
        "<p>/api/getheavyvotes (this generates artificial CPU/memory load)</p>"
    )


@app.route("/api/outback")
def outback():
    return vote_for("outback")


@app.route("/api/bucadibeppo")
def bucadibeppo():
    return vote_for("bucadibeppo")


@app.route("/api/ihop")
def ihop():
    return vote_for("ihop")


@app.route("/api/chipotle")
def chipotle():
    return vote_for("chipotle")


def vote_for(restaurant):
    string_votes = readvote(restaurant)
    votes = int(string_votes)
    votes += 1
    return updatevote(restaurant, votes)


@app.route("/api/getvotes")
def getvotes():
    restaurants = ["outback", "bucadibeppo", "ihop", "chipotle"]
    votes = [readvote(restaurant) for restaurant in restaurants]
    return json.dumps([
        {"name": restaurant, "value": vote}
        for restaurant, vote in zip(restaurants, votes)
    ])


@app.route("/api/getheavyvotes")
def getheavyvotes():
    votes = getvotes()
    consume_memory()
    consume_cpu_heavy()
    return votes


def consume_memory():
    print(f"Consuming 100MB * {memstressfactor} of memory")
    memeater[randrange(10000)] = bytearray(1024 * 1024 * 100 * memstressfactor)


def consume_cpu_heavy():
    print(f"Consuming CPU with factor: {cpustressfactor}")
    processes = cpu_count()
    with Pool(processes) as pool:
        pool.map(consume_cpu, range(processes))


if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)))
    app.debug = True
