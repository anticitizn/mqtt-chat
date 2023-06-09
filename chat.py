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

# Default values, can be modified within the application
username = "Haxor"
client_id = str(uuid.uuid4())
topic = "default"

message = {}

def send_message(text, topic):
    message["sender"] = dpg.get_value("username_input")
    message["clientId"] = dpg.get_value("client_id_input")
    message["topic"] = topic
    message["text"] = text
    message_data = json.dumps(message)

    client.publish("/aichat/" + topic, message_data)

def send_user_message():
    print(dpg.get_value("topic_input"))
    send_message(dpg.get_value("message_input"), dpg.get_value("topic_input"))

    dpg.set_value("message_input", "")

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("/aichat/#")

    # Send a clientstate message to let everyone know we're online
    send_message("Client " + client_id + " connected.", "clientstate")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global messages
    try:
        parsed = json.loads(msg.payload)
        messages += '\n' + parsed['sender'] + " - /aichat/" + parsed['topic'] + '\n' + parsed['text'] + '\n'

        dpg.set_value("message_display", messages)
        
    except (ValueError, KeyError) as e:
        print("Malformed data encountered")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Set last will message
message["sender"] = username
message["clientId"] = client_id
message["topic"] = "clienstate"
message["text"] = "Client " + client_id + " unexpectedly lost connection."
last_will_message_data = json.dumps(message)

client.will_set("/aichat/clientstate", last_will_message_data, 0, False)

# Connect to the broker and start listening/publishing messages
client.connect(broker_address, broker_port)
client.loop_start()

# Create the GUI window
dpg.create_context()
dpg.create_viewport(title='MQTT chat!', width=1000, height=800)

def checkbox_clicked():
    dpg.configure_item("message_display", tracked=dpg.get_value("autoscroll_checkbox"))

# Load our custom font because the default one does not support most Unicode characters
with dpg.font_registry():
    with dpg.font("unifont.otf", 16) as default_font:

        # Add the default and extended font ranges
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Japanese)
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Thai)
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Vietnamese)
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Korean)
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Chinese_Full) # bing chilling

        dpg.bind_font(default_font)

with dpg.window(tag="primary_window", width=1000, height=800):
    # Input fields for metadata (username, topic, clientId)
    with dpg.child_window(tag="metadata_inputs", autosize_x=True, height=40):
        with dpg.group(horizontal=True):
            dpg.add_text("Username:")
            dpg.add_input_text(tag="username_input", default_value=username, width=150)

            dpg.add_text("Topic:")
            dpg.add_input_text(tag="topic_input", default_value=topic, width=150)

            dpg.add_text("Client ID:")
            dpg.add_input_text(tag="client_id_input", default_value=client_id, width=300, enabled=False)

            dpg.add_text("Autoscroll:")
            dpg.add_checkbox(tag="autoscroll_checkbox", callback=checkbox_clicked)

    # Message history display
    with dpg.child_window(tag="messages_display", autosize_x=True, height=690):
        dpg.add_text(wrap=750, tag="message_display", tracked=False, track_offset=1.0)
        dpg.add_spacer(height=5)

    # Message input field
    with dpg.child_window(tag="message_inputs", height=40, autosize_x=True):
        with dpg.group(horizontal=True):
            dpg.add_input_text(hint="Enter message here...", tag="message_input", on_enter=True, callback=send_user_message, width=-100)
            dpg.add_button(label="Send", callback=send_message, width = 80)

#demo.show_demo()
#dpg.show_font_manager()

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("primary_window", True)
dpg.start_dearpygui()

send_message("Client " + client_id + " disconnected.", "clientstate")

client.disconnect()
client.loop_stop()

dpg.destroy_context()
