import serial

class UartCommunication:
    def __init__(self, port, baudrate=9600, timeout=0.1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial = None

    def connect(self):
        try:
            self.serial = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            return True
        except serial.SerialException:
            return False

    def disconnect(self):
        if self.serial is not None:
            self.serial.close()

    def is_connected(self):
        if self.serial is not None:
            return self.serial.is_open
        return False

    def read(self):
        if self.serial is not None:
            return self.serial.readline().decode().strip()
        return None

    def write(self, data):
        if self.serial is not None:
            self.serial.write(data.encode())

    def send_message(self, message):
        if self.serial is not None:
            message = message.strip()
            self.serial.write(f"{len(message)}\n".encode())
            response = self.read()
            if response == "READY":
                self.write(message)
                response = self.read()
                return response
        return None
