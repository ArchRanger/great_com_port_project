import time
from device import Device
from mqtt_publisher import MQTTPublisher
from uart_communication import UartCommunication

DEVICE_NAME = "COM5"
MQTT_BROKER_ADDRESS = "test.mosquitto.org"
MQTT_TOPIC = "test/topic"


def run():
    device = Device(DEVICE_NAME, "QR Code Scanner")
    mqtt = MQTTPublisher(MQTT_BROKER_ADDRESS)
    uart = UartCommunication(DEVICE_NAME, 115200)

    while True:
        if not device.is_available():
            print("Device is not available. Retrying in 5 seconds...")
            time.sleep(5)
            continue

        try:
            uart.open_connection()
            print("Connection to device is established.")
            while True:
                data = uart.read_data()
                if data:
                    print(f"Received data from device: {data}")
                    mqtt.publish_data(MQTT_TOPIC, data)
        except Exception as e:
            print(f"Error occurred: {e}")
            uart.close_connection()
