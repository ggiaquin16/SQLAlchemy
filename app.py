from flask import Flask, jsonify
app = Flask(__name__)

@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation:<br/>"
        f"/api/v1.0/tobs:<br/>"
        f"/api/v1.0/stations:<br/>"
    )
