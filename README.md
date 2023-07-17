# sqlalchemy_challenge
This project involves:

1. Analysis and exploration of the climate data.
  
2. Designing the climate app.

PART 1: Analysis and exploration of the climate data:

I used Python and SQLAlchemy to do a basic climate analysis and data exploration of the climate database. Specifically, I used SQLAlchemy ORM queries, Pandas, and Matplotlib.
The provided files (climate_starter.ipynb and hawaii.sqlite) were used to complete the climate analysis and data exploration. SQLAlchemy create_engine() was used function to connect to the SQLite database. SQLAlchemy automap_base() function was used to reflect the tables into classes and then save references to the classes named station and measurement. SQLAlchemy session was created to connect Python to the database. For precipitation analysis, queries were written to:

1. find the most recent date in the dataset.

2. get the precipitation data by querying the previous twelve months of data.

3. select the data and prcp values.

4. load the query results into the pandas data frame and plot the results.

   For station analysis, queries were written to:

1. calculate the total number of stations in the dataset.

2. find the most active station and list the stations and observation counts in descending order.

3. calculate the lowest, highest, and average temperatures that filter on the most-active station id found in the previous query.

4. to get the previous 12 months of temperature observation (TOBS) data.


PART 2: Designing the climate app

Flask was used to create the routes. The following routes were created:

1. (/)

  Start at the homepage.

  List all the available routes.

2. (/api/v1.0/precipitation)
   
   This converts the query results from the precipitation analysis (i.e., only the last 12 months of data) to a dictionary using a date as the key and prcp as the value.       Return the JSON representation of your dictionary.

3. (/api/v1.0/stations)

   This returns a JSON list of stations from the dataset.

4. (/api/v1.0/<start>)

   This returns a JSON list of the minimum, average, and maximum temperatures for a specified start date. For a specified start, calculates TMIN, TAVG, and 
   TMAX for all the dates greater than or equal to the start date.

5. (/api/v1.0/<start>/<end>)

   This returns a JSON list of the minimum, average, and maximum temperatures for a specified start-end range. For a specified start date and end date, calculates TMIN, 
   TAVG, and TMAX for the dates from the start to the end date, inclusive.

   
   

