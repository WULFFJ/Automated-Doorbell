# Automated-Doorbell
This is a python script, which accomplishes the following:

1. PIR sensor will detect someone walking up to the front door within about 12-15 feet
2. Once detected a "Gong" sound goes off
3. The first motion detection saves an image
4. The second motion detection sends an image to a Telegram channel where you get a picture of the person
5. A second greeting is played at random from a list of 10 selected greetings that are funny
6. When the button is pushed, it has a voice come on and say "we are fetching our master"
7. Telegram alert is sent once again.
8. Have a mumble server setup on the PI as well to talk and listen

SSL configuration:

* Do this on the HomeAssistant Device
* Do not use the same directory as your Home Assistant SSL for secure internet connections.  You will have some of your necessary files overwritten if you do so by the addon for duckdns.
* You will need to copy the ca.crt, client.key and client.crt to the Raspberry Pi Zero or device of your choice.


*****Server information for SSL
To start with the creation of a CA and a self-signed certificate anyway, open a terminal and execute the following commands:

Create ca.key and choose a strong password for this
Be sure to not add any passwords to anything after this step.
Only use your password in other steps for validation
openssl genrsa -des3 -out ca.key 2048

Next create a ca.cert from the ca.key 
Make sure you enter your common name as the device name in Home Assistant
Settings > System > Network     look under hostname
Write down what you enter for everything else when prompted. 
Keep the country, city and state identical going forward when re-entering on the future steps but make something slightly different at least in the organizaion name.
openssl req -new -x509 -days 1826 -key ca.key -out ca.crt

Create the server key pair
openssl genrsa -out server.key 2048

Create the server.key
openssl req -new -out server.csr -key server.key

Create the server.crt
openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 360 -extfile filename

Create a fullchain.pem
cat server.crt ca.crt > fullchain.pem

*****Client cert information for SSL

Use the same CN as for the server information listed above

Create a private client.key
openssl genrsa -out client.key 2048

Create the client.crt
openssl x509 -req -in client.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out client.crt -days 360


****Note on directory location, I put the files in a directory close to the typical SSL directory, but not in the same as the homeassistant fullchain.pem and privkey.pem.  You will need another fullchain.pem but will base it off on the files you created.  Instead of being in the typical /usr/share/hassio/ssl, I placed all these files in /usr/share/hassio/ssl/mqtt.  This translates to the mosquitto broker's default path of just /mqtt/.

Utilization:

***Mosquitto Broker Home Assistant in the configuration of the addon:

logins: []
require_certificate: true
certfile: /mqtt/fullchain.pem
keyfile: /mqtt/server.key
customize:
  active: false
  folder: mosquitto
cafile: /mqtt/ca.crt
debug: true

***MQTT integration use the following:
Client.crt
Client.key
Ca.crt


********Home Assistant Device configuration.yaml
Add the following:

 # Telegram Bot
telegram_bot:
  - platform: polling
    api_key: "YOURLONGAPIKEYHERE"
    allowed_chat_ids:
      - YourChatIDHERE


***Python Script Doorbell.py
Make a copy of the client.crt, client.key and ca.crt and place them on your device acting as the doorbell.

