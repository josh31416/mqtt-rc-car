# MQTT for controlling a gas RC car

A couple of simple scripts two control an RC car with a PS3 controller, a RaspberryPi and an Arduino WiFi module.

## Prerequisites

- PS3 Dual shock controller
- RaspberryPi
- Arduino ESP8266

## How it works

1. PS3 controller sends input to RaspberryPi via Bluetooth.
2. ``ps3_mqtt_controller.py`` script receives the the input from the controller, translates it to degrees for the servo and publishes it to the MQTT broker.
3. The ESP8266 module, which is subscribed to the ``servo/sterring`` and ``servo/throttle`` topics of the broker, receives the degrees. Thanks to the ``servo.h`` library, it translates the degrees into the PWM (Pulse-width modulation) signal needed by the servos.

## Install
- Clone repository
```sh
git clone https://github.com/josh31416/mqtt-rc-car.git
cd mqtt_rc_car
```
- Install a Mosquitto Broker in your RaspberryPi. You can find a tutorial [here](https://randomnerdtutorials.com/how-to-install-mosquitto-broker-on-raspberry-pi/). Feel free to investigate on your own.
- Pair PS3 controller using [Sixpair tool](https://github.com/rdepena/node-dualshock-controller/wiki/Pairing-The-Dual-shock-3-controller-in-Linux-(Ubuntu-Debian))
- Install python dependencies:
```sh
pip3 install pygame
pip3 install paho-mqtt
```
- Run ps3_mqtt_controller.py. This will listen to the input of the controller and publish to the MQTT the degrees for the servos. Feel free to adjust the servo degree constants at the beginning of the script so that it works for your car.
``./ps3_mqtt_controller.py``
- Flash your ESP8266 chip with the ``mqtt_server_controller.ino`` script. Connect sterring servo to D4 pin (version 12 of ESP8266) and throttle servo to D5 pin. Don't forget to also connect negative jumper cable.

Congratulations! You should be racing your car now with your PS3 controller.
