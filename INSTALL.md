# Install

## 安裝函式庫
```
$ sudo pip install -r requirements.txt
```

## 修改裝置名稱與資料庫連線設定
```
$ cp config.py.sample config.py

$ vi config.py
STATION_NAME = 'xxx'

INFLUXDB_HOST = 'xxx.xxx.xxx.xxx'
INFLUXDB_DATABASE = 'xxx'
INFLUXDB_MEASUREMENT = 'xxx'
```

## 設定排程 (每十分鐘自動執行)
```
$ sudo vi /etc/crontab
0,10,20,30,40,50 *      * * *   pi      python /home/pi/pyWeatherLink/send_influxdb.py

$ sudo /etc/init.d/cron restart
```
