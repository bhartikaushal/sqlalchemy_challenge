# Import the dependencies.

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify


#################################################
# Database Setupy
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
#engine = create_engine("sqlite:////c/Users/bhart/Documents/SQLalchemy_Project/SQLalchemy/Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables

Base.prepare(autoload_with=engine)
# Save references to each table

Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

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
        f"/api/v1.0/<start>/<end><br/>"
    )


# create station route of a list of the stations in the dataset
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    # Query precipitation data from last 12 months from the most recent date from Measurement table
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)

    prcp_data = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date > year_ago).\
    order_by(Measurement.date).all()
    session.close()

    prcp_list = []
    for date,prcp in prcp_data:
        prcp_dict = {}
        prcp_dict['date']= date
        prcp_dict['prcp']= prcp
        prcp_list.append(prcp_dict)


    # Return a list of jsonified precipitation data for the previous 12 months 
    return jsonify(prcp_list)


# create station route of a list of the stations in the dataset
@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(Station.station).all()
    # Close the session                   
    session.close()
     # Convert list of tuples into normal list
    station_list = list(np.ravel(stations))
    return jsonify(station_list)

# create tobs route of date and temperature for the most active station over last 12 months
@app.route("/api/v1.0/tobs")
def tobs():
    most_active_station = session.query(Measurement.station,func.count(Measurement.station)).\
    order_by(func.count(Measurement.station).desc()).\
    group_by(Measurement.station).first()

    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)

    yearly_temp = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date > year_ago).\
    filter(Measurement.station == most_active_station[0]).all()

    # Close the session                   
    session.close()

    # Create a dictionary from the row data and append to a list of tobs_list
    tobs_list = []
    for date, tobs in yearly_temp:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs_list.append(tobs_dict)
    # Return a list of jsonified tobs data for the previous 12 months
    return jsonify(tobs_list)


#  create start route that gives minimum temp,maximum temp and average temp for a specified start date
@app.route("/api/v1.0/<start>")
# Define function, set "start" date entered by user as parameter for start_date decorator 
def start_date(start):
    session = Session(engine)
    #start = '2014-08-23'

    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start date."""

    # Create query for minimum, average, and max tobs where query date is greater than or equal to the date the user submits in URL
    start_date_tobs_results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    
    session.close() 

    # Create a list of min,max,and average temps that will be appended with dictionary values for min, max, and avg tobs queried above
    start_date_tobs_values =[]
    for min, avg, max in start_date_tobs_results:
        start_date_tobs_dict = {}
        start_date_tobs_dict["min"] = min
        start_date_tobs_dict["average"] = avg
        start_date_tobs_dict["max"] = max
        start_date_tobs_values.append(start_date_tobs_dict)
    
    return jsonify(start_date_tobs_values)

# Create a route for start and end date that gives minimum, average, and maximum temperature observed for all dates greater than or equal to the start date entered by a user

@app.route("/api/v1.0/<start>/<end>")

# Define function, set start and end dates entered by user as parameters for start_end_date decorator
def Start_end_date(start, end):
    session = Session(engine)
    start = '2014-08-23'
    end = '2017-08-23'

    """Return a list of min, avg and max tobs between start and end dates entered"""
    
    # Create query for minimum, average, and max tobs where query date is greater than or equal to the start date and less than or equal to end date user submits in URL

    start_end_date_tobs_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()

    session.close()
  
    # Create a list of min,max,and average temps that will be appended with dictionary values for min, max, and avg tobs queried above
    start_end_tobs_date_values = []
    for min, avg, max in start_end_date_tobs_results:
        start_end_tobs_date_dict = {}
        start_end_tobs_date_dict["min_temp"] = min
        start_end_tobs_date_dict["avg_temp"] = avg
        start_end_tobs_date_dict["max_temp"] = max
        start_end_tobs_date_values.append(start_end_tobs_date_dict) 
    

    return jsonify(start_end_tobs_date_values)
   
if __name__ == '__main__':
    app.run(debug=True) 