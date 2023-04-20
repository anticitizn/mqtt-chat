import paho.mqtt.client as mqtt

# Verbindungsinformationen zum Broker
broker_address = "10.50.12.150"
broker_port = 1883

# Callback, wenn eine Nachricht empfangen wird
def on_message(client, userdata, message):
    print("Nachricht empfangen: " + str(message.payload.decode()))

# Verbindung zum Broker herstellen
client = mqtt.Client()
client.connect(broker_address, broker_port)

# Auf empfangene Nachrichten warten
client.on_message = on_message
client.subscribe("/aichat/default")

# Schleife zum Aufrechterhalten der Verbindung und Warten auf Nachrichten
client.loop_start()


# Nachrichten senden
startMessage = '{"sender":"lorem_ipsum","text":"foo bar test 123", "clientId":"0dc5bf41-8e9d-4bba-8b3e-cd9ab2c2c2aa", "topic":"clientstate"}'
client.publish("/aichat", startMessage)
print("start message published")
while True:
    message = input("Nachricht eingeben: ")
   
    #message = '{"sender":"lorem_ipsum","text":"foo bar test 123", "clientId":"0dc5bf41-8e9d-4bba-8b3e-cd9ab2c2c2aa", "topic":"default"}'
    client.publish("/aichat", message)
    print("message published")

# Verbindung beenden
client.loop_stop()
client.disconnect()
