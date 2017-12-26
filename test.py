from communication import Link

l = Link('/dev/ttyUSB0')
# l = Link()

simg = l.getSensorImage()

# ['AverageWindSpeed', 'Forecast', 'IndoorRelativeHumidity', 'IndoorTemperature', 'OutdoorDewpoint', 'OutdoorRelativeHumidity', 'OutdoorTemperature', 'QFE', 'QFETrend', 'RainDay', 'RainRate', 'Timestamp', 'WindDirection', 'WindSpeed', '_SensorImage__getitemp', '_SensorImage__getotemp', '_SensorImage__getwd', '_SensorImage__getws', '_SensorImage__itemp', '_SensorImage__otemp', '_SensorImage__setitemp', '_SensorImage__setotemp', '_SensorImage__setwd', '_SensorImage__setws', '_SensorImage__wd', '_SensorImage__ws', '__doc__', '__init__', '__module__', '__str__']

# print dir(simg)

print simg.OutdoorTemperature
print simg.OutdoorRelativeHumidity
print round(simg.QFE, 2)
print simg.WindSpeed
print simg.AverageWindSpeed
print simg.WindDirection
print simg.OutdoorDewpoint
print simg.RainRate
print simg.RainDay
print simg.SolarRadiation
print simg.UVI
