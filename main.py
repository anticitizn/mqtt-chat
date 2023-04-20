import paho.mqtt.client as mqtt
import json
from dateutil import parser

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("/weather/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    try:
        parsed = json.loads(msg.payload)
       
        print(f'Current Temperature : {parsed["tempCurrent"]}')
        print(f'Max Temperature : {parsed["tempMax"]}')
        print(f'Min Temperature : {parsed["tempMin"]}')
        #YYYY-MM-DDTHH:mm:ss.sssZ
        print(f'Timestamp : {parser.parse(parsed["timeStamp"]).strftime("%d.%m.%Y %H:%M")}')
        print(f'City: {parsed["city"]}\n')

        #print(json.dumps(parsed, indent=3))
    except ValueError:
        print("Malformed Weather Data encounterd")
    

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("10.50.12.150", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
