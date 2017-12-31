#!/usr/bin/env python
# encoding: utf-8

from communication import Link
from influxdb import InfluxDBClient
from config import *

l = Link('/dev/ttyUSB0')

inClient = InfluxDBClient(host=INFLUXDB_HOST, database=INFLUXDB_DATABASE)


def upload_to_influxdb(measurement, tags, fields, time=None):
    _ = {
        "measurement": measurement,
        "tags": tags,
        "fields": fields
    }
    if time:
        _['time'] = time

    data = []
    data.append(_)

    inClient.write_points(data)


if __name__ == "__main__":
    simg = l.getSensorImage()

    # print dir(simg)
    # ['AverageWindSpeed', 'Forecast', 'IndoorRelativeHumidity', 'IndoorTemperature', 'OutdoorDewpoint', 'OutdoorRelativeHumidity', 'OutdoorTemperature', 'QFE', 'QFETrend', 'RainDay', 'RainRate', 'Timestamp', 'WindDirection', 'WindSpeed', '_SensorImage__getitemp', '_SensorImage__getotemp', '_SensorImage__getwd', '_SensorImage__getws', '_SensorImage__itemp', '_SensorImage__otemp', '_SensorImage__setitemp', '_SensorImage__setotemp', '_SensorImage__setwd', '_SensorImage__setws', '_SensorImage__wd', '_SensorImage__ws', '__doc__', '__init__', '__module__', '__str__']

    print 'Outdoor Temperature', simg.OutdoorTemperature
    print 'Outdoor Relative Humidity:', simg.OutdoorRelativeHumidity
    print 'QFE:', round(simg.QFE, 2)
    print 'Wind Speed:', simg.WindSpeed
    print 'Average Wind Speed:', simg.AverageWindSpeed
    print 'Wind Direction:', simg.WindDirection
    print 'Outdoor Dewpoint:', simg.OutdoorDewpoint
    print 'Rain Rate:', simg.RainRate
    print 'Rain Day:', simg.RainDay
    print 'Solar Radiation:', simg.SolarRadiation
    print 'UVI:', simg.UVI

    tags = {
        "name": STATION_NAME,
        "device": STATION_DEVICE,
        "model": STATION_MODEL,
    }

    fields = {
        "pressure_hpa": simg.QFE,
        "temperature_c": simg.OutdoorTemperature,
        "dew_point_c": simg.OutdoorDewpoint,
        "humidity": simg.OutdoorRelativeHumidity,
        "wind_speed_ms": simg.WindSpeed,
        "wind_degree": simg.WindDirection,
        "rain_1hr_mm": simg.RainRate,
        "rain_24hr_mm": simg.RainDay,
        "radiation_Wm2": simg.SolarRadiation,
        "UVI": simg.UVI
    }

    upload_to_influxdb(INFLUXDB_MEASUREMENT, tags, fields)
