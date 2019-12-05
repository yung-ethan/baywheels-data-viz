#!/usr/bin/env python
"""Produce the net bikes data visualization. Implemented using Bokeh."""
from process_baywheels_tripdata import get_net_bikes_from_csv
import numpy as np
import datetime
from bokeh.plotting import figure, show, output_file
from bokeh.tile_providers import get_provider, Vendors
from bokeh.models import ColumnDataSource, LinearColorMapper, AdaptiveTicker, ColorBar, CustomJS, Slider, DateSlider, Toggle
from bokeh.layouts import column, row, widgetbox
from bokeh.palettes import RdBu


def wgs84_to_web_mercator(df, lon="lon", lat="lat"):
    """Converts a Dataframe from decimal longitude/latitude to Web Mercator format"""
    k = 6378137
    df["x"] = df[lon] * (k * np.pi/180.0)
    df["y"] = np.log(np.tan((90 + df[lat]) * np.pi/360.0)) * k
    return df


def long_to_merc(lon):
    """Converts decimal longitude to Web Mercator format"""
    k = 6378137
    return lon * (k * np.pi/180.0)


def lat_to_merc(lat):
    """Converts decimal latitude to Web Mercator format"""
    k = 6378137
    return np.log(np.tan((90 + lat) * np.pi/360.0)) * k


def get_column_data_source(net_bikes):
    """Reformat net_bikes Dataframe so that it can be used as a ColumnDataSource"""
    hr_fmt = '%Y%m%d %H'
    net_bikes = net_bikes.rename(columns=lambda x: x.strftime(hr_fmt) if isinstance(x, datetime.datetime) else x)
    # Set an arbitrary default datetime here.
    default_dt = datetime.datetime(2019,9,10,9)
    net_bikes['curr_date'] = default_dt.date().strftime('%Y%m%d')
    net_bikes['curr_hr'] = default_dt.strftime('%H')
    data = net_bikes.to_dict(orient='list')
    data['net_change'] = data[default_dt.strftime(hr_fmt)]
    return ColumnDataSource(data)


def show_data_visualization(source):
    """Show the data visualization in a webpage."""
    # Set up the plot window
    # Another map tile option: Vendors.STAMEN_TERRAIN)
    tile_provider = get_provider(Vendors.CARTODBPOSITRON)
    sf_lat = (37.73, 37.81)
    sf_long = (-122.47, -122.359720)
    sf_xrange = [long_to_merc(long) for long in sf_long]
    sf_yrange = [lat_to_merc(lat) for lat in sf_lat]
    plot_options = dict(plot_width=1000, plot_height=800, title='Hourly Net Change in Bikes Docked')
    p = figure(x_range=sf_xrange, y_range=sf_yrange,
               x_axis_type="mercator", y_axis_type="mercator",
               tooltips=[("Net Change", "@net_change"), ("ID", "@id"), ("Station", "@name")],
               **plot_options)
    p.add_tile(tile_provider)
    # Add a color bar
    palette = RdBu[11]
    palette.reverse()
    color_mapper = LinearColorMapper(palette=palette, low=-30, high=30)
    color_bar = ColorBar(color_mapper=color_mapper, ticker=AdaptiveTicker(),
                         label_standoff=12, border_line_color=None, location=(0,0))
    p.add_layout(color_bar, 'right')
    # Add the station points as circles
    p.circle(x='x', y='y', size=15,
             fill_color={'field': 'net_change', 'transform': color_mapper},
             fill_alpha=0.8, source=source,
             )
    # add two sliders: one for date, one for hour
    start_date, end_date = datetime.date(2019,9,1), datetime.date(2019,9,30)
    date_fmt = '%Y%m%d'
    # Out of simplicity, setting the dates to ints to make the slider work here
    date_slider = Slider(start=int(start_date.strftime(date_fmt)), end=int(end_date.strftime(date_fmt)), step=1, value=int(start_date.strftime(date_fmt)), title='Date')
    hour_slider = Slider(start=0, end=23, value=9, step=1, title="Hour of Day")
    date_callback = CustomJS(args=dict(source=source), code="""
        var data = source.data;
        var curr_date = cb_obj.value;
        data['net_change'] = data[curr_date + ' ' + data['curr_hr'][0]];
        source.change.emit();
    """)
    hour_callback = CustomJS(args=dict(source=source), code="""
        var data = source.data;
        function pad(n, width, z) {
          z = z || '0';
          n = n + '';
          return n.length >= width ? n : new Array(width - n.length + 1).join(z) + n;
        }
        var curr_hr = String(cb_obj.value).padStart(2, '0');
        data['curr_hr'][0] = curr_hr;
        data['net_change'] = data[data['curr_date'][0] + ' ' + curr_hr];
        source.change.emit();
    """)
    output_file("net_bikes.html")
    date_slider.js_on_change('value', date_callback)
    hour_slider.js_on_change('value', hour_callback)
    # Display on the page
    show(
        column(
            row(
                widgetbox(date_slider),
                widgetbox(hour_slider),
            ),
            p
        )
    )


def main():
    csv_filepath = "201909-baywheels-tripdata.csv"
    net_bikes = get_net_bikes_from_csv(csv_filepath)
    net_bikes = wgs84_to_web_mercator(net_bikes, lon='long', lat='lat')
    source = get_column_data_source(net_bikes)
    show_data_visualization(source)


if __name__ == '__main__':
    main()
