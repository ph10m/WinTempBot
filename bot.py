import os
from twitter import *
import wmi
import time
import datetime
import urllib2
import json

# please don't mess around with my keys, thanks.
c_key = 'PFuRYoFCdRvVqG3UMHfnfEXvZ'
c_secret = 'Hiv0VJCXuPbRNvhe7LhChIQJPJroBj5m4mPTwdp7cNaAwdYPBw'
a_token = '4915565709-7sm13JTJadJziX6SmnNPwidk6g7apuuG5dgPSnC'
a_secret = '8j4CZfkRXRDJ5ZnkRAWGFCawp8JbgxNolWLvK2qZQ0A2H'

t = Twitter(auth=OAuth(a_token,a_secret,c_key,c_secret))
def post(x):
	t.statuses.update(status=x)
	print 'Updated status:\n'+x

weather_url = 'http://openweathermap.org/data/2.5/weather?id=3133880&appid=b1b15e88fa797225412429c1c50c122a1'
def fetch_weather():
	w = urllib2.urlopen(weather_url)
	data = w.read()
	w.close()
	print 'successfully fetched weather!'
	return str(json.loads(data)['main']['temp'])+'C'

fetch_weather()
w = wmi.WMI(namespace="root\OpenHardwareMonitor")
print 'found openhardwaremonitor!'
cpu_temp, gpu_temp, mobo_temp = -1,-1,-1
while True:
	temps = w.Sensor()
	_date = datetime.datetime.today().strftime("%B %d")
	_time = time.strftime("%H:%M")
	time_string = _date+' '+_time
	weather_string = ' ('+fetch_weather()+' outside)\n'
	voltage_string = 'Voltages: '
	for sensor in temps:
		if sensor.SensorType==u'Temperature':
			if 'package' in sensor.Name.lower():
				cpu_temp = int(sensor.Value)
			elif 'gpu' in sensor.Name.lower():
				gpu_temp = int(sensor.Value)
			elif 'motherboard' in sensor.Name.lower():
				mobo_temp = int(sensor.Value)
		elif sensor.SensorType==u'Voltage':
			if len(sensor.Name)<7:
				voltage_string += str(round(sensor.Value,3)) + ' '
	print 'sensor data gathered!'
	# temp_string = 'CPU: '+str(cpu_temp)+' | GPU: '+str(gpu_temp) +' | MB: '+str(mobo_temp) + '\n'
	temp_string = 'CPU: '+str(cpu_temp)+' | GPU: '+str(gpu_temp) + '\n'
	post_string = time_string + weather_string + temp_string + voltage_string
	if cpu_temp>50 or gpu_temp>65 or mobo_temp>45:
		# critical
		timenow = time.strftime('%H:%M:%S')
		post(timenow + '- High temperatures, check the computer!')
	else:
		post(post_string)
# sleep for 30 minutes
	time.sleep(3600)
