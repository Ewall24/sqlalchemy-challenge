# sqlalchemy-challenge

#Part 1: Analyze and Explore the Climate Data

In this section, you’ll use Python and SQLAlchemy to do a basic climate analysis and data exploration of your climate database. Specifically, you’ll use SQLAlchemy ORM queries, Pandas, and Matplotlib. 
To do so, complete the following steps:

   Use the provided files (climate_starter.ipynb and hawaii.sqlite) to complete your climate analysis and data exploration.

   Use the SQLAlchemy create_engine() function to connect to your SQLite database.
       engine = create_engine("sqlite:///Resources/hawaii.sqlite")

   Use the SQLAlchemy automap_base() function to reflect your tables into classes, and 
       # View all of the classes that automap found
        Base.classes.keys()
   
   then save references to the classes named station and measurement.
       # reflect an existing database into a new model
Base = automap_base()
Base.prepare(autoload_with=engine)

   # reflect the tables
measurement= Base.classes.measurement 
station  = Base.classes.station 
  
  Link Python to the database by creating a SQLAlchemy session. 
   # Create our session (link) from Python to the DB
session = Session(engine)  
  

               Remember to close your session at the end of your notebook.

Perform a precipitation analysis and then a station analysis by completing the steps in the following two subsections.

#Precipitation Analysis

  Find the most recent date in the dataset.
  # Find the most recent date in the data set.
recent_date =session.query(func.max(measurement.date)).scalar() 
recent_date
 
  Using that date, get the previous 12 months of precipitation data by querying the previous 12 months of data.
  # Calculate the date one year from the last date in data set.
year_one = dt.date(2017,8,23) - dt.timedelta(days=365) 
year_one 



Select only the "date" and "prcp" values.

# Perform a query to retrieve the data and precipitation scores
perception_data = session.query(measurement.date,measurement.prcp).filter(measurement.date >=year_one).all()
perception_data
# Save the query results as a Pandas DataFrame. Explicitly set the column names
df=pd.DataFrame(perception_data,columns=['date','perception']) 
df

Load the query results into a Pandas DataFrame. Explicitly set the column names.
# Use Pandas Plotting with Matplotlib to plot the data
df.plot(xlabel='Date',ylabel='Inches',rot=90)

Sort the DataFrame values by "date".
# Sort the dataframe by date
df.set_index('date',inplace=True) 
df=df.sort_values(by='date') 

Plot the results by using the DataFrame plot method, as the following image shows: 
<img width="468" alt="precipitation" src="https://github.com/user-attachments/assets/45ab1cff-be24-402c-a243-87a0572ca3ba">


Use Pandas to print the summary statistics for the precipitation data. 
# Use Pandas Plotting with Matplotlib to plot the data
df.plot(xlabel='Date',ylabel='Inches',rot=90) 
<Axes: xlabel='Date', ylabel='Inches'>

#Station Analysis 


Design a query to calculate the total number of stations in the dataset.
# Design a query to calculate the total number of stations in the dataset
total_stations=session.query(func.count(station.station.distinct())).scalar() 
total_stations  

total stations in the dataset are 9.


Design a query to find the most-active stations (that is, the stations that have the most rows). To do so, complete the following steps:

    List the stations and observation counts in descending order.
total_stations=session.query(measurement.station,func.count(measurement.station))\
    .group_by(measurement.station).order_by(func.count(measurement.station).desc()).all() 
total_stations 

    Answer the following question: which station id has the greatest number of observations?
Station ID USC00519281 has the highest number of observations at 2772.

Design a query that calculates the lowest, highest, and average temperatures that filters on the most-active station id found in the previous query.
   # Using the most active station id from the previous query, calculate the lowest, highest, and average temperature.
lowest_temp= session.query(func.min(measurement.tobs)).filter(measurement.station == 'USC00519281').scalar()
highest_temp= session.query(func.max(measurement.tobs)).filter(measurement.station == 'USC00519281').scalar()
average_temp= session.query(func.avg(measurement.tobs)).filter(measurement.station == 'USC00519281').scalar()
print(lowest_temp,highest_temp,average_temp)

54.0 85.0 71.66378066378067 

lowest_temp = 54.0
highest_temp =85.0
average_temp =71.66378066378067

Design a query to get the previous 12 months of temperature observation (TOBS) data. 
To do so, complete the following steps:

    Filter by the station that has the greatest number of observations.
    
    # Using the most active station id
    most_active_station_id = 'USC00519281' 
# Query the last 12 months of temperature observation data for this station and plot the results as a histogram


# Query the last 12 months of temperature observation data for the most active station
temperature_data = session.query(measurement.tobs).filter(
    measurement.station == most_active_station_id,
    measurement.date >= year_one
).all()

# Convert query results to a list of temperatures
temperatures = [temp[0] for temp in temperature_data]  

Query the previous 12 months of TOBS data for that station.

    Plot the results as a histogram with bins=12, as the following image shows:<img width="478" alt="station-histogram" src="https://github.com/user-attachments/assets/2170bdb9-c71d-4e7a-89f0-cba1c8545a5f"> 

# Plot the results as a histogram

plt.figure(figsize=(10, 6))
plt.hist(temperatures, bins=12, edgecolor= "gray", label='tobs')
plt.xlabel('Temperature')
plt.ylabel('Frequency') 
plt.legend()
plt.show()   

![image](https://github.com/user-attachments/assets/154591f9-410c-4c6f-aed6-bc333339eae0)


#Close Session 
session.close()

    
    

#Part 2: Design Your Climate App 

Now that you’ve completed your initial analysis, you’ll design a Flask API based on the queries that you just developed. To do so, use Flask to create your routes as follows:

    

        Start at the homepage. 
        engine = create_engine("sqlite:///Resources/hawaii.sqlite")

        List all the available routes. 
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

    

    /api/v1.0/precipitation

        Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value. 
        @app.route("/api/v1.0/precipitation") 
def precipitation(): 
    session = Session(engine) 
    one_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    scores = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year).all()
    session.close 

    precipitation_dict ={date: prcp for date, prcp in scores } 

    Return the JSON representation of your dictionary.
   return jsonify(precipitation_dict)      

    /api/v1.0/stations
        Return a JSON list of stations from the dataset.
        @app.route("/api/v1.0/stations") 
def stations(): 
           session =Session(engine) 
           stations_data = session.query(Station.station).all() 
           session.close()

           stations_list =list(np.ravel(stations_data)) 
           return jsonify(stations_list) 

    /api/v1.0/tobs 

        Query the dates and temperature observations of the most-active station for the previous year of data.
         @app.route("/api/v1.0/tobs") 
def tobs():
    session = Session(engine)
    one_year = dt.date(2017, 8, 23) - dt.timedelta(days = 365)
    temperature_data = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281')\
    .filter(Measurement.date >= one_year).all()
        Return a JSON list of temperature observations for the previous year.
   observed_temps = list(np.ravel(temperature_data))
    return jsonify(observed_temps) 
   
    
    /api/v1.0/<start> and /api/v1.0/<start>/<end> 
    

        Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.

        For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.

        For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.


    Join the station and measurement tables for some of the queries.

    Use the Flask jsonify function to convert your API data to a valid JSON response object. 

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


acknowledgments
collab
Gursimran Kaur - kaursimran081999@gmail.com - SimranBoparai\
Omid K - omidk414@gmail.com - omidk414\
  

    
