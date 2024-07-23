import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt


#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
#################################################


# reflect an existing database into a new model
Base = automap_base() 
# reflect the tables
Base.prepare(autoload_with=engine)

Measurement =Base.classes.measurement
Station =Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
app = Flask(__name__)
#################################################

#################################################
# Flask Routes
#################################################
@app.route("/") 
def welcome(): 
    return(
        f"All Available Routes: <br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>" 
        f"/api/v1.0/tobs<br/>" 
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )
        
    

@app.route("/api/v1.0/precipitation") 
def precipitation(): 
    session = Session(engine) 
    one_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    scores = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year).all()
    session.close 

    precipitation_dict ={date: prcp for date, prcp in scores } 
    return jsonify(precipitation_dict) 

@app.route("/api/v1.0/stations") 
def stations(): 
           session =Session(engine) 
           stations_data = session.query(Station.station).all() 
           session.close()

           stations_list =list(np.ravel(stations_data)) 
           return jsonify(stations_list) 

@app.route("/api/v1.0/tobs") 
def tobs():
    session = Session(engine)
    one_year = dt.date(2017, 8, 23) - dt.timedelta(days = 365)
    temperature_data = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281')\
    .filter(Measurement.date >= one_year).all()
    session.close()

    observed_temps = list(np.ravel(temperature_data))
    return jsonify(observed_temps) 

@app.route("/api/v1.0/<start>") 
@app.route("/api/v1.0/<start>/<end>") 
def temperature(start=None,end=None):
    session = Session(engine)
    result_temperatures = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    if not end:
        results = session.query(*result_temperatures).filter(Measurement.date <= start).all() 
        session.close
       
       
        temps = list(np.ravel(results))
        return jsonify(temps)
if __name__ == '__main__':
    app.run(debug=True) 









