import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


import numpy as np
import pandas as pd
import datetime as dt

from flask import Flask, jsonify

# create an engine with the database
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect the existing database to perform CRUD operations 
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# reference the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# create a session object to use for each session
session = Session(engine)

# start of the flask app
app = Flask(__name__)

# routes
@app.route("/")
def welcome():
    return (
    '''
     Welcome to the Hawaii Climate API!
     Available routes are:
     /api/v1.0/precipitation
     /api/v1.0/stations
     /api/v1.0/tobs 
     /api/v1.0/<start>/<end>
 ''')

@app.route("/api/v1.0/precipitation")
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365) 
    precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year).all()
    session.close()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

@app.route("/api/v1.0/stations")

def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

@app.route("/api/v1.0/tobs")

def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    results = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').\
    filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<end>")

### to finish  #####
     
if __name__ == "__main__":
    app.run(debug=True)


