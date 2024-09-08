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

***Removed SSL from the instructions and moved them to "How-To"

Utilization:


********Home Assistant Device configuration.yaml
Add the following:


telegram_bot:
  - platform: polling
    api_key: "YOURLONGAPIKEYHERE"
    allowed_chat_ids:
      - YourChatIDHERE

#Helpful reminders
sudo dpkg-reconfigure mumble-server after installing Mumble-Server to setup SuperUser Password
sudo nano /etc/mumble-server.ini configure the options for Mumble-Server


***Python Script Doorbell.py
Make a copy of the client.crt, client.key and ca.crt and place them on your device acting as the doorbell.

