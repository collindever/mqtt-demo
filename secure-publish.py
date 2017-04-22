import paho.mqtt.client as mqtt

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client("## YOUR USERNAME ##")
client.tls_set("## CA CERT ##", certfile="## CLIENT CERT ##", keyfile="## CLIENT KEY ##")
client.username_pw_set("## USERNAME", password="## PASSWORD ##")
client.on_connect = on_connect
client.on_message = on_message

client.connect(## YOUR SERVER##, 8883, 60)
client.publish('test', payload='Check Out My Sweet Server', qos=1, retain=True)