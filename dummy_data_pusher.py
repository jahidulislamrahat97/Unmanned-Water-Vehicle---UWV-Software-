from mqtt_client import MqttClient
import random
import time
import json


if __name__ == "__main__":
    def execute(msg):
        print(msg.payload.decode('utf-8').split())
        
    client = MqttClient(id="1111002301290000", use_id_as_client_id=False)
    client.getMqttSubTopic("UWV/Vehicle")
    client.getMqttPubTopic("UWV/Vehicle")
    client.setOnMessageCallbackFunction(execute)
    client.connect()
    
    while True:
        sensor_data = {
        'compass_heading': random.randint(0,360),
        'gps_heading': random.randint(0, 255),
        'bot_speed': random.randint(1, 25),
        'gps_speed': random.randint(1, 25),
        'rudder_angle': random.randint(0, 30),
        'satellite': random.randint(1, 25),
        'valid': random.randint(0, 1)
        }
        
        payload = json.dumps(sensor_data)
        client.publish(payload = payload)
        time.sleep(1)
        client.client.loop()