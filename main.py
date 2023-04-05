from flask import Flask, render_template, request, jsonify
import random
import folium
import time
import threading
from mqtt_client import MqttClient
import json


mqtt = MqttClient(id="1234")
mqtt.getMqttBroker("broker.hivemq.com")
mqtt.getMqttPort(1883)
mqtt.getMqttSubTopic("UWV/Vehicle")
mqtt.getMqttPubTopic("UWV/Vehicle")


app = Flask(__name__)
sensor_data = {
        'compass_heading': random.randint(0,360),
        'gps_heading': random.randint(0, 255),
        'bot_speed': random.randint(1, 25),
        'gps_speed': random.randint(1, 25),
        'rudder_angle': random.randint(0, 30),
        'satellite': random.randint(1, 25),
        'valid': random.randint(0, 1)
    }


# GPS Speed, Bot Seed, Rudder angle, Comass heading, GPS Heading, satellite , valid
# total milestone, complete milstone, nex mileston distance
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_sensor_value/<sensor>', methods=['GET'])
def get_sensor_value(sensor):
    # sensor_data = {
    #     'compass_heading': random.randint(0,360),
    #     'gps_heading': random.randint(0, 255),
    #     'bot_speed': random.randint(1, 25),
    #     'gps_speed': random.randint(1, 25),
    #     'rudder_angle': random.randint(0, 30),
    #     'satellite': random.randint(1, 25),
    #     'valid': random.randint(0, 1)
    # }
    global sensor_data
    # print(jsonify({sensor: sensor_data[sensor]}))
    return jsonify({sensor: sensor_data[sensor]})

# Handle button presses
@app.route('/button_press', methods=['POST'])
def button_press():
    button = request.form['button']
    print('Button pressed:', button)
    mqtt.publish(topic="UWV/Vehicle/1234", payload=button)
    return 'Button pressed: ' + button


@app.route('/switch_press', methods=['POST'])
def switch_press():
    switch = request.form.get('switch')
    print('Kill Switch pressed:', switch)
    return 'Kill Switch pressed: ' + switch

#auto pilot
@app.route('/auto_flight_press', methods=['POST'])
def auto_flight_press():
    switch = request.form.get('switch')
    print('auto flight mode:', switch)
    return 'auto flight mode: ' + switch


# Laptop Location: 23.7854103,90.4309706
current_location = [23.783724898550883,90.42016804218294]

# Create a map object
map = folium.Map(location=current_location, zoom_start=18)
# Show my current location
folium.Marker(location=current_location).add_to(map)

map.add_child(folium.ClickForMarker(popup="Waypoint"))
map.add_child(folium.LatLngPopup().add_to(map))

# Display the map
map.save("static/map.html")

def onMqttMessage(msg):
    global sensor_data
    try:
        sensor_data = json.loads(msg.payload.decode('utf-8'))
        print(sensor_data)
    except:
        print("Error in JSON Format")


if __name__ == '__main__':
    mqtt.setOnMessageCallbackFunction(onMqttMessage)
    mqtt.connect()
    mqtt.client.loop_start()
    app.run(debug=True)


# heading, sat, valid, speed, 