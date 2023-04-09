# Gerekli kütüphaneleri import ediyoruz
import time
import threading
import paho.mqtt.client as mqtt

import serial.tools.list_ports as list_ports
import serial

class PortScanThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.daemon = True
        self.devices = []  # Bulunan cihazları tutacak liste

    def run(self):
        while True:
            # Seri portları tara
            ports = list_ports.comports()
            for port in ports:
                # Burada port taraması yapılır
                # Eğer cihaz bulunursa self.devices listesine eklenir
                # Eğer yeni bir cihaz bulunmazsa, 5 saniye sonra tekrar tarama yaparız
                if port.device not in self.devices:
                    self.devices.append(port.device)
            time.sleep(5) # 5 saniye sonra tekrar tara

    def get_devices(self):
        return self.devices

class MqttClient:
    def __init__(self):
        self.client = mqtt.Client()
        self.connected = False
        self.topic = "mytopic"

    def connect(self):
        self.client.connect("broker.hivemq.com", 1883) # MQTT broker adresi ve portu
        self.connected = True

    def send_data(self, data):
        if not self.connected:
            self.connect()
        try:
            self.client.publish(self.topic, payload=data) # MQTT mesaj gönderimi
        except:
            pass # MQTT bağlantısı kesildiği zaman hata almamak için try-except bloğu kullanıyoruz



class UartClient:
    def __init__(self):
        self.connected = False
        self.port = 'COM8'

    def connect(self):
        self.ser = serial.Serial(self.port, baudrate=9600, timeout=1)
        self.connected = True

    def send_data(self, data):
        if not self.connected:
            self.connect()
        try:
            self.ser.write(data.encode())  # Veriyi string olarak gönderir
        except:
            pass


if __name__ == "__main__":
    port_scan_thread = PortScanThread()
    port_scan_thread.start()

    mqtt_client = MqttClient()
    uart_client = UartClient()

    try:
        while True:
            devices = port_scan_thread.get_devices()
            for device in devices:
                # Her bir cihaz için MQTT mesajı gönderimi yaparız
                mqtt_client.send_data(device)

                # Her bir cihaz için UART mesajı gönderimi yaparız
                uart_client.send_data(device)

            time.sleep(1) # Cihaz tarama sıklığını belirleyebilirsiniz
    except KeyboardInterrupt:
        pass
