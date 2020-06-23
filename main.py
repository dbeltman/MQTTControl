import paho.mqtt.client as mqtt
import os
import R510_SSH


def on_connect(client, userdata, flags, rc):  # The callback for when the client connects to the broker
	print("Connected with result code {0}".format(str(rc)))  # Print result of connection attempt
	client.subscribe(
		'mqttcontrol/fansetpoint')  # Subscribe to the topic “digitest/test1”, receive any messages published on it


def on_message(client, userdata, msg):  # The callback for when a PUBLISH message is received from the server.
	print("Message received-> " + msg.topic + " " + str(msg.payload))  # Print a received msg
	print(str(msg.payload))
	payload = msg.payload.decode('utf-8')
	if str(payload) == 'auto':
		print('setting to auto')
		R510_SSH.set_auto()
	elif 0 < int(payload) <= 100:
		payload = int(payload)
		print("setting to " + str(payload))
		R510_SSH.set_manual(round(payload))



client = mqtt.Client("MQTTController")  # Create instance of client with client ID “digi_mqtt_test”
client.on_connect = on_connect  # Define callback function for successful connection
client.on_message = on_message  # Define callback function for receipt of a message
# client.connect("m2m.eclipse.org", 1883, 60)  # Connect to (broker, port, keepalive-time)
client.connect(os.environ.get('MQTTHOST'), 1883, 60)
client.loop_forever()  # Start networking daemon
