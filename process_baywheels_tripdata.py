#!/usr/bin/env python
"""Process Baywheels trip data. Made publicly available by Lyft."""
import pandas as pd


def get_df_from_csv(csv_filepath):
    """Read the CSV into a Dataframe, and add two columns with the timestamp truncated to the hour."""
    df = pd.read_csv(csv_filepath)
    df['start_time']= pd.to_datetime(df['start_time'])
    df['end_time']= pd.to_datetime(df['end_time'])
    df['start_time_hr'] = df.start_time.apply(lambda x: pd.Timestamp(x.year, x.month, x.day, x.hour))
    df['end_time_hr'] = df.end_time.apply(lambda x: pd.Timestamp(x.year, x.month, x.day, x.hour))
    return df


def get_unique_stations(df):
    """Return a Dataframe with one record per station."""
    start_stations = df.loc[:,['start_station_id', 'start_station_name',
                               'start_station_latitude', 'start_station_longitude']] \
        .rename(columns={'start_station_id':'id', 'start_station_name': 'name',
                         'start_station_latitude': 'lat', 'start_station_longitude': 'long'})
    end_stations = df.loc[:,['end_station_id', 'end_station_name',
                             'end_station_latitude', 'end_station_longitude']] \
        .rename(columns={'end_station_id':'id', 'end_station_name': 'name',
                         'end_station_latitude': 'lat', 'end_station_longitude': 'long'})
    stations = pd.concat([start_stations, end_stations]).drop_duplicates().sort_values('id')
    stations = stations.set_index('id')
    return stations


def get_net_bikes_from_df_stations(df, stations):
    """Get the Dataframe that shows net change in bikes by hour, using the original Dataframe and stations df."""
    sg = df.groupby(['start_station_id', 'start_time_hr'])
    eg = df.groupby(['end_station_id', 'end_time_hr'])
    depart = sg['start_station_id'].count()
    depart = depart.unstack()
    depart = depart.rename_axis('hr', axis='columns').rename_axis('station_id').fillna(0)
    arrive = eg['end_station_id'].count()
    arrive = arrive.unstack()
    arrive = arrive.rename_axis('hr', axis='columns').rename_axis('station_id').fillna(0)
    # This causes some NAs where depart has a few missing hour X station ID entries
    net_bikes = arrive - depart
    net_bikes = stations.join(net_bikes)
    return net_bikes.reset_index()


def get_net_bikes_from_csv(csv_filepath):
    """Do the data processing. Preferably, save Dataframes to a Pickle file for later loading."""
    df = get_df_from_csv(csv_filepath)
    stations = get_unique_stations(df)
    net_bikes = get_net_bikes_from_df_stations(df, stations)
    return net_bikes
