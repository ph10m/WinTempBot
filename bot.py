import os
import re
from twitter import *
import wmi
import time
import datetime
import urllib2
import json
from weather import HARSTAD

time.sleep(15)  # wait for openhardwaremonitor to load.

c_key = 'PFuRYoFCdRvVqG3UMHfnfEXvZ'
c_secret = 'Hiv0VJCXuPbRNvhe7LhChIQJPJroBj5m4mPTwdp7cNaAwdYPBw'
a_token = '4915565709-7sm13JTJadJziX6SmnNPwidk6g7apuuG5dgPSnC'
a_secret = '8j4CZfkRXRDJ5ZnkRAWGFCawp8JbgxNolWLvK2qZQ0A2H'

t = Twitter(auth=OAuth(a_token, a_secret, c_key, c_secret))


def post(x):
    print 'submitting'
    t.statuses.update(status=x)
    print 'Updated status:\n' + x



def fetch_weather():
    w = urllib2.urlopen(HARSTAD)
    data = w.read()
    w.close()
    return str(json.loads(data)['main']['temp']) + 'C'


def get_gpu(identifier):
    regex = r'\/(\d)\/'
    groups = re.search(regex, identifier)
    return groups.group(1)


fetch_weather()
w = wmi.WMI(namespace="root\OpenHardwareMonitor")
cpu_temp, mobo_temp = -1, -1
gpu_stats = dict()
while True:
    temps = w.Sensor()
    _date = datetime.datetime.today().strftime("%B %d")
    _time = time.strftime("%H:%M")
    time_string = _date + ' ' + _time
    weather_string = ' (' + fetch_weather() + ' outside)\n'

    for sensor in temps:
        if sensor.SensorType == u'Temperature':
            if 'package' in sensor.Name.lower():
                cpu_temp = int(sensor.Value)
            elif 'gpu' in sensor.Name.lower():
                gpu_name = get_gpu(sensor.Identifier)
                gpu_temp = int(sensor.Value)
                gpu_stats[gpu_name] = gpu_temp


    gpu_temps = ' '.join([(str(int(k)+1)+'('+ str(v)+')') for k, v in sorted(gpu_stats.items())])
    temp_string = 'CPU: ' + str(cpu_temp) + \
                ' | GPUs: ' + str(gpu_temps)
    post_string = time_string + weather_string + temp_string
    print post_string
    post(post_string)
    # sleep for 30 minutes
    time.sleep(3600)
