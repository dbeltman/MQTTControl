import paho.mqtt.client as mqtt
import os
from components import SSH_controller
import paho.mqtt.publish as mqtt_publish
import json

mqtt_host = os.getenv('MQTTHOST', '192.168.1.101')
mqtt_port = os.getenv('MQTTPORT', 1883)
mqtt_control_topic = os.getenv('CONTROLTOPIC', 'dellmqttfan/fansetpoint')
mqtt_state_topic = os.getenv('STATETOPIC', 'dellmqttfan/fanspeed')
mqtt_client_name = os.getenv('MQTTCLIENTNAME', 'dellmqttchecker')
fan_name = os.getenv('FANNAME', 'HomeassistantFanName')
config_topic = os.getenv('MQTTDISCOVERYTOPIC', 'homeassistant/fan/' + fan_name + '/config')
config_template = {
    "name": fan_name,
    "command_topic": mqtt_control_topic,
    "speed_state_topic": mqtt_state_topic,
    "speed_command_topic": mqtt_control_topic,
    "qos": 0,
    "payload_on": "auto",
    "payload_off": "1",
    "payload_low_speed": "10",
    "payload_medium_speed": "30",
    "payload_high_speed": "50",
    "speeds": ["off", "low", "medium", "high"]
}
json_template = json.dumps(config_template)
mqtt_publish.single(config_topic, json_template,
                    hostname=mqtt_host,
                    client_id=mqtt_client_name,
                    port=mqtt_port,
                    retain=True)


def on_connect(client, userdata, flags, rc):  # The callback for when the client connects to the broker
    print("Connected with result code {0}".format(str(rc)))  # Print result of connection attempt

    client.subscribe(
        mqtt_control_topic)  # Subscribe to the topic “digitest/test1”, receive any messages published on it


def on_message(client, userdata, msg):  # The callback for when a PUBLISH message is received from the server.
    # print("message received: " + msg.payload.decode('utf-8'))
    command = msg.payload.decode('utf-8')
    if command == 'CHECKINSTALL':
        SSH_controller.check_install()
        # SSH_controller.set_auto()

    print("Message received-> " + msg.topic + ": " + str(msg.payload.decode('utf-8')))  # Print a received msg
    # print(str(msg.payload))
    payload = msg.payload.decode('utf-8')

    if str(payload) == 'auto':
        print('setting to auto')
        SSH_controller.set_auto()
    elif 0 < int(payload) <= 100:
        payload = int(payload)
        print("setting to " + str(payload))
        SSH_controller.set_manual(round(payload))


client = mqtt.Client(mqtt_client_name)  # Create instance of client with client ID “digi_mqtt_test”
client.on_connect = on_connect  # Define callback function for successful connection
client.on_message = on_message  # Define callback function for receipt of a message
client.connect(mqtt_host, 1883, 60)
client.loop_forever()  # Start networking daemon
