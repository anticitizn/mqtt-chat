import paho.mqtt.client as mqtt
import dearpygui.dearpygui as dpg
import dearpygui.demo as demo

import json
import uuid

# Broker connection information
broker_address = "10.50.12.150"
broker_port = 1883

input_message = ""
messages = []

username = "Haxor1337"
user_id = str(uuid.uuid4())
topic = "default"

message = {}
message["sender"] = username
message["clientId"] = user_id
message["topic"] = topic
message["text"] = ""

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("/aichat/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    try:
        parsed = json.loads(msg.payload)
        print(parsed)
        messages.append(parsed['text'])

        dpg.set_value("input", messages)
        print('message received!')
        
    except (ValueError, KeyError) as e:
        print("Malformed data encountered")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_address, broker_port)

client.loop_start()

dpg.create_context()
dpg.create_viewport(title='MQTT chat!', width=800, height=600)

text1 = 'The lazy dong is a good dog. This paragraph should fit within the child. Testing a 1 character word. The quick brown fox jumps over the lazy dog.'
messages.append(text1)

def input_edited(sender, app_data):
    global input_message
    input_message = app_data

def btn_clicked(sender, app_data):
    message["text"] = input_message
    message_data = json.dumps(message)
    client.publish("/aichat/" + topic, message_data)

with dpg.window(label="Example Window"):
    dpg.add_text(wrap=600, tag="input")
    dpg.add_spacer(height=5)
    with dpg.group(horizontal=True):
        dpg.add_input_text(hint="Enter message here...", callback=input_edited, width=500)
        dpg.add_button(label="Send", callback=btn_clicked, width = 80)

#demo.show_demo()

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()