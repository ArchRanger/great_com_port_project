import paho.mqtt.client as mqtt
import json

class MQTTPublisher:
    def __init__(self, broker_address, broker_port, username=None, password=None):
        self.broker_address = broker_address
        self.broker_port = broker_port
        self.username = username
        self.password = password
        self.client = None

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    def on_disconnect(self, client, userdata, rc):
        print("Disconnected from MQTT Broker with return code = " + str(rc))

    def connect(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect

        if self.username is not None and self.password is not None:
            self.client.username_pw_set(self.username, self.password)

        self.client.connect(self.broker_address, self.broker_port)
        self.client.loop_start()

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()

    def publish(self, topic, payload):
        self.client.publish(topic, json.dumps(payload))
