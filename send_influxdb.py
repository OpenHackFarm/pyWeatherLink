#!/usr/bin/env python
# encoding: utf-8

from communication import Link
from influxdb import InfluxDBClient
from config import *
from conversions import *
import urllib2

WUNDERGROUND_BASEURL = 'http://weatherstation.wunderground.com/weatherstation/updateweatherstation.php'
WUNDERGROUND_UPDATEURL = '%s?ID=%s&PASSWORD=%s&action=updateraw&dateutc=now' % (WUNDERGROUND_BASEURL, WUNDERGROUND_ID, WUNDERGROUND_PASSWORD)

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

    print 'Outdoor Temperature', f2c(simg.OutdoorTemperature)
    print 'Outdoor Relative Humidity:', simg.OutdoorRelativeHumidity
    print 'QFE:', round(inHg2hPa(simg.QFE), 2)
    print 'Wind Speed:', mph2ms(simg.WindSpeed)
    print 'Average Wind Speed:', mph2ms(simg.AverageWindSpeed)
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
        "pressure_hpa": round(inHg2hPa(simg.QFE), 2),
        "temperature_c": f2c(simg.OutdoorTemperature),
        "dew_point_c": simg.OutdoorDewpoint,
        "humidity": simg.OutdoorRelativeHumidity,
        "wind_speed_ms": mph2ms(simg.WindSpeed),
        "wind_degree": simg.WindDirection,
        "rain_1hr_mm": simg.RainRate,
        "rain_24hr_mm": simg.RainDay,
        "radiation_Wm2": simg.SolarRadiation,
        "UVI": int(round(simg.UVI))
    }

    upload_to_influxdb(INFLUXDB_MEASUREMENT, tags, fields)

    # upload to weather underground
    w = urllib2.urlopen(WUNDERGROUND_UPDATEURL +
                        "&humidity=%s&tempf=%s&UV=%s&baromin=%s&winddir=%s&windspeedmph=%s&rainin=%s&solarradiation=%s" % (simg.OutdoorRelativeHumidity, simg.OutdoorTemperature, simg.UVI, simg.QFE, simg.WindDirection, simg.WindSpeed, simg.RainRate, simg.SolarRadiation))
    print w.read()
    w.close()
