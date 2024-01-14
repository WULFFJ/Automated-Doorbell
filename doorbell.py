# Automated-Doorbell
# PIR sensor to detect someone coming to the door
# Push button doorbell with led
# Notifications through the Telegram API with images
# Ability to add video with stream
# Automated greetings per detection by PIR and custom greeting when button is pushed

import RPi.GPIO as GPIO
import time
import os
import random
import datetime
import ffmpeg
import requests
import threading


# Usage
bot_token = 'UNIQUEBOTTOKENFROMSETUPOFTELEGRAM'
chat_id = 'CHATIDFROMAPIINQUOTES'
text = 'Front Door Motion Detected'

# Use the Broadcom SOC channel
GPIO.setmode(GPIO.BCM)

# Define the pin that goes to the circuit
pin_to_circuit = 27
GPIO.setmode(GPIO.BCM) # Use Broadcom pin numbering

# Set up GPIO 4 for the button with pull-up resistor
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

gdir = "/home/homeaccount/sounds/"
imagedir = "/home/homeaccount/images/"
width = 1920  # Replace with your desired width
height = 1080
stream_url = 'YOURRTSPSTREAMADDRESS'

#door greeting "Please wait, while we seek out our master!"
dgreeting = '/home/homeaccount/sounds/buttonpush/buttongreeting.mp3'

# List of sound files
sounds = ['Greet1.mp3', 'Greet2.mp3', 'Greet3.mp3', 'Greet4.mp3', 'Greet5.mp3', 'Greet6.mp3','Greet7.mp3', 'Greet8.mp3','Greet9.mp3', 'Greet10.mp3']

def motion_message(chat_id,text,bot_token):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {'chat_id': chat_id, 'text': text}
    response = requests.post(url, data=data)
    return response.json()

def still_capture1():
    xdate = datetime.datetime.now().strftime("%m%d%Y"+"-"+"%H%M%S")
    output_image = imagedir + 'snap' + xdate + '.jpg'
    ffmpeg.input(stream_url, t=0.1).output(output_image, vframes=1, vf='scale={}:{}'.format(width, height)).run()

def still_capture2():
    xdate = datetime.datetime.now().strftime("%m%d%Y"+"-"+"%H%M%S")
    output_image = imagedir + 'snap' + xdate + '.jpg'
    ffmpeg.input(stream_url, t=0.1).output(output_image, vframes=1, vf='scale={}:{}'.format(width, height)).run()
    return output_image

def send_photo(chat_id, output_image, bot_token):
    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
    with open(output_image , 'rb') as photo:
        files = {'photo': photo}
        data = {'chat_id': chat_id}
        response = requests.post(url, files=files, data=data)def send_photo2(chat_id, output_image, bot_token):
    caption = 'Bell Ringer'
    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
    with open(output_image , 'rb') as photo:
        files = {'photo': photo}
        data = {'chat_id': self.destinationID,
                'caption': caption}
        response = requests.post(url, files=files, data=data)
    return response.json()

# Initialize counter
counter = 0

def button_pressed(channel):
    global counter
    global doorgreeting
    if GPIO.input(4) == False: # If button is pressed
        os.system('mpg123 -q ' + dgreeting)
        output_image = still_capture2()
        send_photo(chat_id, output_image, bot_token)
        time.sleep(0.2) # Debounce delay

def motion_detected(channel):
    global counter
    if counter == 0:
        # Play gong sound
        os.system('mpg123 -q /home/homeaccount/sounds/Gong.mp3')
        still_capture1()
        motion_message(chat_id, text, bot_token)
        counter += 1
    elif counter == 1:
        # Choose a random sound
        sound = random.choice(sounds)
        greeting = gdir + sound
        # Play the sound
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

    return response.json()

 # If the file is more than 7 days old, delete it
            if (now - file_date).days > 7:
                os.remove(os.path.join(directory, filename))

def delete_old_files_every_day():
    while True:
        delete_old_files()
        time.sleep(86400)  # Sleep for 24 hours

# Start a separate thread that deletes old files every day
threading.Thread(target=delete_old_files_every_day).start()


# Set up the GPIO channel for the motion sensor
GPIO.setup(pin_to_circuit, GPIO.IN)

# Allow time for the PIR sensor to warm up
time.sleep(60)

try:
    # Add event listener on pin 4 for a falling edge (going from HIGH to LOW)
    GPIO.add_event_detect(4, GPIO.FALLING, callback=button_pressed)

    # Add event listener on pin_to_circuit for a rising edge (going from LOW to HIGH)
    GPIO.add_event_detect(pin_to_circuit, GPIO.RISING, callback=motion_detected)

    while True:
        # Reset counter if no motion is detected for 2 minutes
        time.sleep(120)
        if not GPIO.input(pin_to_circuit):
            counter = 0

except KeyboardInterrupt:
    # Cleanup the GPIO when exiting
    GPIO.cleanup()



