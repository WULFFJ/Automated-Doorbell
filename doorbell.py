import threading
import RPi.GPIO as GPIO
import os
import time
import datetime
import requests
import random
import json
import ssl
import paho.mqtt.client as mqtt
from queue import Queue, Empty

counter=0

client = mqtt.Client("FrontDoor")
client.username_pw_set("doorbell", "Oxxxxxxcxxx")  # Replace with your MQTT broker's username and password

device_info = {
    "identifiers": ["pi_zero_2"],  # A unique identifier for your device
    "name": "Pi Zero 2",  # The name of your device
    "model": "Zero 2 W",  # The model of your device
    "manufacturer": "Raspberry Pi Foundation"  # The manufacturer of your device
}

# Set the TLS parameters
client.tls_set(
    ca_certs="/pathto/cert/ca.crt",
    certfile="/pathto/cert/client.crt",
    keyfile="/pathto/cert/client.key",
    cert_reqs=ssl.CERT_REQUIRED,
    tls_version=ssl.PROTOCOL_TLS,
    ciphers=None
)

client.tls_insecure_set(True)  # Allow self-signed certificates

client.connect("192.xxx.x.xxx",8883)  # Replace with the IP address of your Home Assistant Device
client.loop_start()
# Usage
bot_token = 'xxxxbottokenidxxxx'
chat_id = 'chatid'
text = 'Front Door Motion Detected'

# This variable will be used to control the motion detection
motion_detection_enabled = True

GPIO.setmode(GPIO.BCM)
pin_to_circuit = 12
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
gdir = "/home/homeaccount/sounds/"
imagedir = "/home/homeaccount/images/"
width = 1920
height = 1080
dgreeting = '/home/homeaccount/sounds/buttonpush/buttongreeting.mp3'
sounds = ['Greet1.mp3', 'Greet2.mp3', 'Greet3.mp3', 'Greet4.mp3', 'Greet5.mp3', 'Greet6.mp3','Greet7.mp3', 'Greet8.mp3','Greet9.mp3', 'Greet10.mp3']

def motion_message(chat_id,text,bot_token):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {'chat_id': chat_id, 'text': text}
    response = requests.post(url, data=data)
    return response.json()

def still_capture1():
    xdate = datetime.datetime.now().strftime("%m%d%Y"+"-"+"%H%M%S")
    output_image = imagedir + 'snap' + xdate + '.jpg'
    os.system(f'libcamera-still -t 1 -o {output_image}')

def still_capture2():
    xdate = datetime.datetime.now().strftime("%m%d%Y"+"-"+"%H%M%S")
    output_image = imagedir + 'snap' + xdate + '.jpg'
    os.system(f'libcamera-still -t 1 -o {output_image}')
    return output_image

def send_photo(chat_id, output_image, bot_token):
    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
    with open(output_image , 'rb') as photo:
        files = {'photo': photo}
        data = {'chat_id': chat_id}
        response = requests.post(url, files=files, data=data)
    return response.json()

def send_photo2(chat_id, output_image, bot_token):
    caption = 'Bell Ringer'
    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
    with open(output_image , 'rb') as photo:
        files = {'photo': photo}
        data = {'chat_id': self.destinationID,
                'caption': caption}
        response = requests.post(url, files=files, data=data)
    return response.json()

def button_pressed(channel):
    global motion_detection_enabled
    # Disable motion detection for 2 minutes
    motion_detection_enabled = False
    threading.Timer(120, enable_motion_detection).start()
    # Publish button pressed event to MQTT broker
    client.publish("doorbell/button_pressed", "doorbell")

    global counter
    global doorgreeting
    if GPIO.input(4) == False: # If button is pressed
        os.system('mpg123 -q ' + dgreeting)
        output_image = still_capture2()
        send_photo(chat_id, output_image, bot_token)
        time.sleep(0.2) # Debounce


GPIO.add_event_detect(4, GPIO.FALLING, callback=button_pressed, bouncetime=200)

def enable_motion_detection():
    global motion_detection_enabled
    motion_detection_enabled = True

def motion_detected(channel):
    global counter
    global motion_detection_enabled          
    motion_message(chat_id, text, bot_token)
          counter += 1
      elif counter == 1:
          sound = random.choice(sounds)
          greeting = gdir + sound
          os.system('mpg123 -q ' + greeting)
          output_image = still_capture2()
          send_photo(chat_id, output_image, bot_token)
          counter += 1

def delete_old_files():
    directory = "/home/homeaccount/images/"  # Replace with your directory
    now = datetime.datetime.now()

    for filename in os.listdir(directory):
        if filename.startswith("snap") and filename.endswith(".jpg"):
            # Extract the date from the filename
            date_str = filename[4:12]  # Get the date part of the filename
            file_date = datetime.datetime.strptime(date_str, "%m%d%Y")

            if (now - file_date).days > 7:
                os.remove(os.path.join(directory, filename))

def delete_old_files_every_day():
    while True:
        time.sleep(86400)  # Sleep for 24 hours

threading.Thread(target=delete_old_files_every_day).start()

GPIO.setup(pin_to_circuit, GPIO.IN)

GPIO.add_event_detect(pin_to_circuit, GPIO.RISING, callback=motion_detected)

time.sleep(60)

try:
    while True:
        # No Motion 2 min
        time.sleep(120)
        if not GPIO.input(pin_to_circuit):
            counter = 0

except KeyboardInterrupt:
    # Cleanup the GPIO when exiting
    GPIO.cleanup()

def delete_old_files_every_day():
    while True:
        time.sleep(86400)  # Sleep for 24 hours

    if motion_detection_enabled:
      client.publish("doorbell/motion_detected", "Motion detected")
      if counter == 0:
          # Play gong sound
          os.system('mpg123 -q /path/to/Gong.mp3')
          still_capture1()

