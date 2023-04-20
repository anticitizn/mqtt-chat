import paho.mqtt.client as mqtt
import dearpygui.dearpygui as dpg
import dearpygui.demo as demo

import json
import uuid

# Broker connection information
broker_address = "10.50.12.150"
broker_port = 1883

input_message = ""
messages = ""

username = "Haxor"
client_id = str(uuid.uuid4())
topic = "default"

message = {}

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("/aichat/#")

    # Send a clientstate message to let everyone know we're online
    message["sender"] = username
    message["clientId"] = client_id
    message["topic"] = "clienstate"
    message["text"] = "Client " + client_id + " connected."
    message_data = json.dumps(message)
    
    client.publish("/aichat/clientstate", message_data)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global messages
    try:
        parsed = json.loads(msg.payload)
        messages += '\n' + parsed['sender'] + " - /aichat/" + parsed['topic'] + '\n' + parsed['text'] + '\n'

        dpg.set_value("input", messages)
        
    except (ValueError, KeyError) as e:
        print("Malformed data encountered")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_address, broker_port)

client.loop_start()

dpg.create_context()
dpg.create_viewport(title='MQTT chat!', width=800, height=600)

def send_message():
    message["sender"] = dpg.get_value("username_input")
    message["clientId"] = dpg.get_value("client_id_input")
    message["topic"] = dpg.get_value("topic_input")
    message["text"] = dpg.get_value("message_input")
    message_data = json.dumps(message)

    client.publish("/aichat/" + topic, message_data)

    dpg.set_value("message_input", "")

with dpg.window(tag="primary_window", width=800, height=600):
    with dpg.child_window(tag="metadata_inputs", autosize_x=True, height=40):
        with dpg.group(horizontal=True):
            dpg.add_text("Username:")
            dpg.add_input_text(tag="username_input", default_value=username, width=120)

            dpg.add_text("Topic:")
            dpg.add_input_text(tag="topic_input", default_value=topic, width=120)

            dpg.add_text("Client ID:")
            dpg.add_input_text(tag="client_id_input", default_value=client_id, width=280, enabled=False)

    with dpg.child_window(tag="messages_display", autosize_x=True, height=490):
        dpg.add_text(wrap=750, tag="input")
        dpg.add_spacer(height=5)
    
    with dpg.child_window(tag="message_inputs", height=40, autosize_x=True):
        with dpg.group(horizontal=True):
            dpg.add_input_text(hint="Enter message here...", tag="message_input", on_enter=True, callback=send_message, width=-100)
            dpg.add_button(label="Send", callback=send_message, width = 80)

#demo.show_demo()

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("primary_window", True)
dpg.start_dearpygui()

dpg.destroy_context()