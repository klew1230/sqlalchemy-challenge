# 1. import libraries
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import json


engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f'/api/v1.0/start/end'
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Convert the query results to a dictionary using date as the key and prcp as the value. Return the JSON representation of your dictionary."""
    # Query all precipitation
    prcp_results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Convert list of tuples into normal list
    prcp_list = list(np.ravel(prcp_results))

    return jsonify(prcp_list)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of stations from the dataset."""
    # Query all passengers
    stations_results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    station_list = list(np.ravel(stations_results)) 

    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Query the dates and temperature observations of the most active station for the last year of data. Return a JSON list of temperature observations (TOBS) for the previous year."""
    # Query all passengers
    tobs_results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281').all()

    session.close()

     # Return a JSON list of temperature observations (TOBS) for the previous year.
    tobs_list = list(np.ravel(tobs_results)) 
    return jsonify(tobs_list)


@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")

def start(start, end = 'now'):
    session = Session(engine)
    
    
    
    if end == 'now':
        lowest  = engine.execute(f"SELECT MIN(tobs) FROM measurement WHERE date >= '{start}'").fetchall()[0][0]
        highest = engine.execute(f"SELECT MAX(tobs) FROM measurement WHERE date >= '{start}'").fetchall()[0][0]
        average = engine.execute(f"SELECT AVG(tobs) FROM measurement WHERE date >= '{start}'").fetchall()[0][0]
    else:
        lowest  = engine.execute(f"SELECT MIN(tobs) FROM measurement WHERE date >= '{start}' AND date <= '{end}'").fetchall()[0][0]
        highest = engine.execute(f"SELECT MAX(tobs) FROM measurement WHERE date >= '{start}' AND date <= '{end}'").fetchall()[0][0]
        average = engine.execute(f"SELECT AVG(tobs) FROM measurement WHERE date >= '{start}' AND date <= '{end}'").fetchall()[0][0]
    
    return {
        'TMIN': lowest,
        'TMAX': highest,
        'TAVG': average
    }

    


if __name__ == '__main__':
    app.run(debug=True)