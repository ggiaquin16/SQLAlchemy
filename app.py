import numpy as np
import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#Database init 
Engine = create_engine("sqlite:///Resources/hawaii.sqlite", echo=False)
Base = automap_base()
Base.prepare(Engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

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
    results = session.query(Measurement.date, Measurement.prcp).all()
    
    session.close()

    prcpList = []

    for date, prcp in results:
        measurementDict = {}
        measurementDict["Date"] = date
        measurementDict["Prcp"] = prcp
        prcpList.append(measurementDict)

    return jsonify(prcpList)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(Engine)

    results = session.query(Station.station).all()
    
    session.close()
    
    stationList = list(np.ravel(results))

    return jsonify(stationList)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(Engine)

    LatestDate = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    LatestDate

    queryDate = dt.date(2017,8,23) - dt.timedelta(days=365)

    results = session.query(Measurement.tobs, Measurement.date).filter(Measurement.date >= queryDate).order_by(Measurement.date).all()
    
    session.close()

    tobsList = list(np.ravel(results))

    return jsonify(tobsList)

@app.route("/api/v1.0/<start>")
def start(start):

    startDate = start.replace(" ", "-")

    session = Session(Engine)
    
    results = session.query(func.max(Measurement.tobs), func.min(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= startDate).all()
        
    session.close()

    tobsStartList = list(np.ravel(results))

    return jsonify(tobsStartList)

@app.route("/api/v1.0/<start>/<end>")
def startEnd(start, end):

    startDate = start.replace(" ", "-")
    endDate = end.replace(" ", "-")
    
    session = Session(Engine)
    
    results = session.query(func.max(Measurement.tobs), func.min(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= startDate).\
        filter(Measurement.date <= endDate).all()
        
    session.close()

    tobsRangeList = list(np.ravel(results))

    return jsonify(tobsRangeList)