import time
import paho.mqtt.client as mqtt
import Adafruit_CharLCD as LCD

# Set up the LCD Display
lcd_rs        = 25
lcd_en        = 24
lcd_d4        = 23
lcd_d5        = 17
lcd_d6        = 21
lcd_d7        = 22

lcd_columns = 16
lcd_rows    = 2

# Initialize the LCD using the pins above.
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows)

def find_spaces(message):
	spaces = []
	i = 0
	while i < len(message):
		if message[i] == " ":
			spaces.append(i)
		i += 1
	return spaces

#Setup the MQTT connection
def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))
	
	client.subscribe("test")

def on_message(client, userdata, msg):
	lcd.clear()
	message = str(msg.payload)
	print(message)
	spaces = find_spaces(message)
	lines = []

	if len(message) < lcd_columns:
		lines.append(message)
		format = False
	else:
		format = True

	while format:
		i = lcd_columns	
		while i >= 0:
			if i in spaces:
				lines.append(message[0:i])
				if len(message[i+1:]) <= lcd_columns:
					lines.append(message[i+1:])
					format = False
				else:
					message = message[i+1:]
					spaces = find_spaces(message)
				break
			i -= 1

	if len(lines) == 1:
		lcd.message(lines[0])
	elif len(lines) == 2:
		lcd.message(lines[0]+"\n"+lines[1])
	else:
		i = 0
		while i < len(lines)-1:
			lcd.clear()
			lcd.message(lines[i]+"\n"+lines[i+1])
			time.sleep(2)
			i += 1

client = mqtt.Client(## YOUR USERNAME ##)
client.tls_set("## CA CRT ##", certfile="## CLIENT CERT##", keyfile="## CLIENT KEY##")
client.username_pw_set("## YOUR USERNAME ##", password="## YOUR PASSWORD##")
#client.tls_insecure_set(True)
client.on_connect = on_connect
client.on_message = on_message

client.connect("159.203.220.102", 8883, 60)
client.loop_forever()
