
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#Data base set-up
engine = create_engine('sqlite:///./Resources/hawaii.sqlite')

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
ME = Base.classes.measurement

ST = Base.classes.station

#Flask
app = Flask(__name__)

#1 list all the available routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/measurement<br/>"
        f"/api/v1.0/station<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/(insert start date yyyy-mm-dd)<br/>"
        f"/api/v1.0/(insert start date yyyy-mm-dd)/(insert end date yyyy-mm-dd)"
    )

#2/api/v1.0/precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Results from the precipitation analysis"""
    # Query from the analysis
    results = session.query(ME.date, ME.prcp).filter(ME.date >= '2016-08-23').all()

    session.close()

    # create the dictionary 
    pre_months = []
    for date, prcp in results:
        pre_dict = {}
        pre_dict["date"] = date
        pre_dict["prcp"] = prcp
        pre_months.append(pre_dict)

    return jsonify(pre_months)

#3api//v1.0/stations
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all stations
    results = session.query(ST.station).all()

    session.close()

    # Convert list 
    stations_names = list(np.ravel(results))

    return jsonify(stations_names)


#4/api/v1.0/tobs
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of temperature observations"""
    # Query all stations
    results=session.query(ME.tobs).filter(ME.date >= '2016-08-23').filter(ME.station == 'USC00519281').all()

    session.close()

    # Convert list 
    temp_obs = list(np.ravel(results))

    return jsonify(temp_obs)

#5 /api/v1.0/<start> and /api/v1.0/<start>/<end>
@app.route("/api/v1.0/<start>")
def api(start):
     # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a Min, Max and AVG for all dates greater than or equal to the start date yyyy-mm-dd"""
    # Query all stations
    results=session.query(func.min(ME.tobs),func.max(ME.tobs),func.avg(ME.tobs)).filter(ME.date >= start).all()

    session.close()

    # Convert list 
    start_list = list(np.ravel(results))

    return jsonify(start_list)

@app.route("/api/v1.0/<start>/<end>")
def api1(start, end):
     # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a Min, Max and AVG for all for the dates from the start date to the end date yyyy-mm-dd"""
    # Query all stations
    results=session.query(func.min(ME.tobs),func.max(ME.tobs),func.avg(ME.tobs)).filter(ME.date >= start).filter(ME.date <= end).all()

    session.close()

    # Convert list 
    startend_list = list(np.ravel(results))

    return jsonify(startend_list)

if __name__ == '__main__':
    app.run(debug=True)
