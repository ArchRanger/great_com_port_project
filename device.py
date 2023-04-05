class Device:
    def __init__(self, device_id, name, description):
        self.device_id = device_id
        self.name = name
        self.description = description
        self.status = 'off'

    def get_device_info(self):
        return f'Device ID: {self.device_id}, Name: {self.name}, Description: {self.description}, Status: {self.status}'

    def update_device_status(self, status):
        self.status = status
