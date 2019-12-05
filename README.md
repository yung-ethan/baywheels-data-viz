**Baywheels Trip Data Visualization**

I started playing around with the publicly available Baywheels trip data out of curiosity in what bikeshare usage 
patterns look like in the San Francisco area. This has also been a fun exercise in creating interactive plots using Bokeh.
I am also considering Plotly as another alternative.

The dataset is available here:
https://www.lyft.com/bikes/bay-wheels/system-data

The HTML output is included in the repo as net_bikes.html.

**Requirements**
- Python3
- pip
- use pipenv to install dependencies from the Pipfile: https://pipenv.kennethreitz.org/en/latest/
- download and extract '201909-baywheels-tripdata.csv' to project directory from here:
https://s3.amazonaws.com/baywheels-data/index.html

**How to Run**
python net_bikes_visualization.py

Next Steps and Potential Improvements:
- change to take CSV file as an argument (currently hardcoded to Sept. 2019 CSV in net_bikes_visualization.py, but can easily be modified to run on any month)
- Increased time granularity? Hourly, or otherwise?
- Show cumulative change in bikes over time, due to trips. 
    At the end of the day, which bike stations are sources vs. sinks?
- Run an exploratory analysis:
    - min/max. net change in bikes docked
    - highlight stations of interest: e.g., the Caltrain dock
- include a toggle to switch to total bikes departing + arriving
- Try in Plotly 