#! /usr/bin/env python3

# IMPORTS
# ===========================
import os
import pygame, sys
from time import sleep
import paho.mqtt.client as mqtt
import math
# ===========================

# CONSTANTS
# ===========================
# Sterring constants
STERRING_MAX_DEGREES_LEFT = 40
STERRING_DEGREES_CENTER = 90
STERRING_MAX_DEGREES_RIGHT = 120

# Throttle constants
THROTTLE_MAX_DEGREES_BRAKING = 75
THROTTLE_DEGREES_CENTER = 100
THROTTLE_MAX_DEGREES_THROTTLE = 123
# ===========================

# Wait till PS3 controller is connected
while True:
	pygame.init()
	window = pygame.display.set_mode((200, 200))
	joystick_count = pygame.joystick.get_count()
	if joystick_count == 0:
		pygame.quit()
		print("Looking for PS3 controller...")
		sleep(3)
	else:
		joystick = pygame.joystick.Joystick(0)
		joystick.init()
		break

# MQTT ASYNC FUNCTIONS
# ===========================
def on_connect(client, userdata, flags, rc):
	print("Connected ("+str(rc)+")")
	if rc != 0:
		pygame.quit()
		sys.exit()
# ===========================

# MQTT client setup
client = mqtt.Client("controller")
client.on_connect = on_connect
client.username_pw_set("josh", "")
client.connect("127.0.0.1", 1883)
client.loop_start()

# MISCELLANEOUS FUNCTIONS
# ===========================
def get_sterring(sterringAxis):
	if sterringAxis < 0:
		sterringRange = abs(STERRING_DEGREES_CENTER - STERRING_MAX_DEGREES_LEFT)
		return STERRING_DEGREES_CENTER - sterringRange*abs(sterringAxis)
	elif sterringAxis > 0:
		sterringRange = abs(STERRING_DEGREES_CENTER - STERRING_MAX_DEGREES_RIGHT)
		return STERRING_DEGREES_CENTER + sterringRange*abs(sterringAxis)
	return STERRING_DEGREES_CENTER

def get_throttle(throttleAxis, brakingAxis):
	throttle = (throttleAxis + 1)/2
	braking = (brakingAxis + 1)/2
	if braking > 0:
		brakingRange = abs(THROTTLE_DEGREES_CENTER - THROTTLE_MAX_DEGREES_BRAKING)
		return THROTTLE_DEGREES_CENTER - braking*brakingRange
	elif throttle > 0:
		throttleRange = abs(THROTTLE_DEGREES_CENTER - THROTTLE_MAX_DEGREES_THROTTLE)
		return THROTTLE_DEGREES_CENTER + throttle*throttleRange
	return THROTTLE_DEGREES_CENTER
# ===========================

# PS3 controller connected
# Initialize controller output values
sterringAxis = 0
throttleAxis = -1
brakingAxis = -1
# Start recording controller activity
while True:
	# If click on pygame exit, quit
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
	# If pushed start button, quit and shutdown
	if joystick.get_button(9) == 1:
		pygame.quit()
		os.system("sudo shutdown now")
	# Polling frequency
	sleep(0.01)
	# Get controller output values
	sterringAxis = joystick.get_axis(0)
	throttleAxis = joystick.get_axis(5)
	brakingAxis = joystick.get_axis(2)

	# Perform scalñing and conversion
	sterringDegrees = math.ceil(get_sterring(sterringAxis))
	throttleDegrees = math.ceil(get_throttle(throttleAxis, brakingAxis))

	# Publish values to MQTT broker
	client.publish("servo/sterring", sterringDegrees)
	client.publish("servo/throttle", throttleDegrees)