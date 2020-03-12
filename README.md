# Baywheels Trip Data Visualization

I started playing around with Baywheels trip data out of a curiosity in what bikeshare usage 
patterns look like in the San Francisco area. The source data are CSVs that describes every bikeshare trip taken within a given month. Lyft maintains this data here:
https://www.lyft.com/bikes/bay-wheels/system-data

One question I developed here is how does the number of bikes docked at any given station change over time. Which docking stations are "sources" or "sinks" that require regular rebalancing? I came up with this data visualization that shows net change in bikes docked over time, for the month of September 2019. 

Check out the final output here:
https://yung-ethan.github.io/baywheels-data-viz/net_bikes.html

You can also download net_bikes.html from within this repository. 

This has also been a fun exercise in creating interactive plots using Bokeh. I am also considering Plotly as a plotting alternative.

## Installation Requirements
- Python3
- pip
- use pipenv to install dependencies from the Pipfile: https://pipenv.kennethreitz.org/en/latest/
    - if you choose not to use pipenv, then make sure you install the packages listed in that file
- download and extract '201909-baywheels-tripdata.csv' to project directory from here:
https://s3.amazonaws.com/baywheels-data/index.html

## How to Produce the Data Visualization
Simply run this to produce the data visualization in net_bikes.html:

`python net_bikes_visualization.py`

## Next Steps and Potential Improvements:
- take CSV file as an argument (currently hardcoded to the CSV from Sept. 2019 in net_bikes_visualization.py, but can easily be modified to run for any given month)
- Increased time granularity? Hourly, or otherwise?
- Show cumulative change in bikes over time, due to trips. 
    At the end of the day, which bike stations are sources vs. sinks?
- Run an exploratory analysis:
    - min/max. net change in bikes docked
    - highlight stations of interest: e.g., the Caltrain dock
- include a toggle to switch to total bikes departing + arriving
- Try in Plotly 
