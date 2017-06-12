import os
from twitter import *
import wmi

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
temperature_infos = w.Sensor()
for sensor in temperature_infos:
    if sensor.SensorType==u'Temperature':
        print(sensor.Name)
        print(sensor.Value)
