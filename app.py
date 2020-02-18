import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#Database init 
Engine = create_engine("sqlite:///../Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(Engine, reflect=True)
Hawaii = Base.Classes.Hawaii


#Flask init
app = Flask(__name__)


#API Endpoints
@app.route("/")
def welcome():
    return (
        f"Available endpoints:<br/>"
        f"/api/v1.0/precipitation:<br/>"
        f"/api/v1.0/tobs:<br/>"
        f"/api/v1.0/stations:<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(Engine)

    #query database
    results = session.query(measurement.date, measurement.prcp).all()
    
    session.close()

    prcpList = list(np.ravel(results))

    return jsonify(prcpList)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(Engine)

    results = session.query(station.station).all()
    
    stationList = list(np.ravel(results))

    return jsonify(stationList)


