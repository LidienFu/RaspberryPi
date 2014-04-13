#   Smart Fan on Raspberry Pi
""" 

License: LGPL
Get more informtion or discussion on http://geek.mr-fu.net

this sample logs temperatur and humidity into MySQL, 
if you dont want this, comment it in the code.

"""
# SmartFan
import RPi.GPIO as GPIO
import time
import sys
import dhtreader
import datetime
import MySQLdb

GPIO.setmode (GPIO.BOARD)
DHT11 = 11
DHT22 = 22
AM2302 = 22


#set GPIO-0 as output (pin11)
relaypinA = 11  #this pin is connect to Fan's Relay
GPIO.setup(relaypinA, GPIO.OUT)
#set dht pin
dhtpin = 4 #bgm2835 pin number


#switch rely
def switch(pin,status):
        GPIO.output(pin, status)
        return


def insertToMySql(t,h):
        db = MySQLdb.connect("localhost","username","password","tablename" )
        cursor = db.cursor()
        sql = "INSERT INTO dhtlog(time,tem,hum) \
                VALUES('%s','%d','%d')" % \
                (datetime.datetime.now(),t,h)
        try:
                cursor.execute(sql)
                db.commit()
        except:
                db.rollback()
        db.close()
        return

isFanOn=False
		
try:
	dhtreader.init()
	while(True):
		try:
			output = dhtreader.read(DHT11,dhtpin)
			if (output is not None):
				t, h = output
				if t and h:
					insertToMySql(t,h) #comment this line if you don't need to log into MySQL
					idx = t + (h *0.1) #adjust the idx based on your requirement, 38~40 is a good threshhold.
					if (idx > 40): #turn fan on
						if(not isFanOn):
							switch(relaypinA,GPIO.LOW)
							isFanOn=True
							print("{2}: Temp = {0} *C, Hum = {1} %".format(t, h,datetime.datetime.now()))
							print("Turn the Fan On!")
					else:#turn fan off
						if(isFanOn):
							switch(relaypinA,GPIO.HIGH)
							isFanOn=False
							print("{2}: Temp = {0} *C, Hum = {1} %".format(t, h,datetime.datetime.now()))
                                                        print("Turn the Fan Off!")
				else:
					print("Failed to read from sensor, maybe try again?")
					
			
			time.sleep(5) # adjust the sleep time by your requirment
		except TypeError:
				print("Sensor initiation error, retry in 5 secs...")
except KeyboardInterrupt:
	GPIO.cleanup()
	sys.exit(0)



