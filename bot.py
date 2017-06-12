import os
from twitter import *
import wmi
from time import time

c_key = 'PFuRYoFCdRvVqG3UMHfnfEXvZ'
c_secret = 'Hiv0VJCXuPbRNvhe7LhChIQJPJroBj5m4mPTwdp7cNaAwdYPBw'
a_token = '4915565709-7sm13JTJadJziX6SmnNPwidk6g7apuuG5dgPSnC'
a_secret = '8j4CZfkRXRDJ5ZnkRAWGFCawp8JbgxNolWLvK2qZQ0A2H'

t = Twitter(auth=OAuth(a_token,a_secret,c_key,c_secret))
def post(x):
    t.statuses.update(status=x)
    print 'Updated status: '+x
#post("gpu temps here goes here plz test 1xD23")

w = wmi.WMI(namespace="root\OpenHardwareMonitor")
cpu_temp, gpu_temp, mobo_temp = -1,-1,-1
while True:
    temps = w.Sensor()
    for sensor in temps:
        if sensor.SensorType==u'Temperature':
            if 'package' in sensor.Name.lower():
                cpu_temp = int(sensor.Value)
            elif 'gpu' in sensor.Name.lower():
                gpu_temp = int(sensor.Value)
            elif 'motherboard' in sensor.Name.lower():
                mobo_temp = int(sensor.Value)

    temp_string = 'CPU: '+str(cpu_temp)+'\nGPU: '+str(gpu_temp) +'\nMB: '+str(mobo_temp)
    if cpu_temp>20 and gpu_temp>20 and mobo_temp>20:
        # everything is ok
        post(temp_string)
    if cpu_temp>50 or gpu_temp>60 or mobo_temp>45:
        # critical
        post('High temperatures detected, check the computer!')
    sleep(10)
