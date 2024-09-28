# mini-boat

# Joystick Controlled Motor System

## Overview
This project controls two DC motors using a joystick connected to a computer, an Arduino board for motor control, and a Jetson device as an intermediary to relay commands between the joystick and Arduino. The joystick inputs are processed by the `controller.py` script, which sends motor speed data to the Jetson (`jetson_client.py`) via a TCP socket. The Jetson forwards these commands to the Arduino over a serial connection, and the Arduino adjusts the motors accordingly.

## Components:
1. **`controller.py` (Joystick Controller)**
   - Captures joystick inputs using `pygame`.
   - Calculates motor speed and direction based on joystick axes and buttons.
   - Sends motor speed data to the Jetson device over a TCP socket connection.

2. **`jetson_client.py` (Jetson Client)**
   - Acts as a server to receive motor speed data from the controller.
   - Forwards the data to the Arduino over a serial connection.
   - Optionally reads back feedback from the Arduino.

3. **`board.ino` (Arduino Motor Controller)**
   - Receives motor speed data from the Jetson via serial communication.
   - Controls two DC motors using PWM signals based on the received data.
   - Handles motor direction (forward/reverse) based on the sign of the speed values.

## Connection Flow:
1. The user operates the joystick connected to the computer.
2. The `controller.py` script reads joystick input, calculates the motor speeds, and sends this data to the Jetson over TCP.
3. The Jetson, running `jetson_client.py`, receives the motor speed data and sends it to the Arduino over a serial connection.
4. The Arduino, using the `board.ino` program, receives the motor speed data and adjusts the motors' speed and direction accordingly.

## Hardware Setup:
- **Computer (Controller):** Runs the `controller.py` script and captures joystick input.
- **Jetson Device:** Runs the `jetson_client.py` script, acting as a middleman between the computer and Arduino.
- **Arduino Board:** Controls the motors based on the commands sent by the Jetson.
- **DC Motors:** Connected to the Arduino via a motor driver. Motor control pins should be connected as follows:
    - Motor 1: `ENA (5)`, `IN1 (3)`, `IN2 (2)`
    - Motor 2: `ENB (6)`, `IN3 (12)`, `IN4 (11)`

## Software Dependencies:
- `controller.py` requires:
  - Python 3.x
  - `pygame` library for joystick input.
  
- `jetson_client.py` requires:
  - Python 3.x
  - `pyserial` library for serial communication with the Arduino.

## Usage Instructions:

1. **Arduino Setup:**
   - Upload `board.ino` to the Arduino board using the Arduino IDE.
   - Ensure the motor driver and motors are correctly wired to the Arduino.

2. **Jetson Setup:**
   - Run the `jetson_client.py` script on the Jetson device.
   - Ensure the Arduino is connected to the Jetson via USB (adjust the serial port in the code if necessary).

3. **Controller Setup:**
   - Run `controller.py` on the computer.
   - Ensure the computer can connect to the Jetson over the network (adjust the IP address in `controller.py` to match the Jetson's IP).
   - Use the joystick to control the motors.

## Troubleshooting:

- **Connection Issues:**
  - Ensure the correct IP address and port are specified in `controller.py` and `jetson_client.py`.
  - Verify that the serial port in `jetson_client.py` matches the one used by the Arduino.

- **Motor Control Issues:**
  - Check the motor wiring to the Arduino.
  - Verify the Arduino's serial communication with the Jetson by reading debug output on the Jetson.

## Future Improvements:
- Add feedback from the Arduino to the Jetson to monitor motor performance.
- Implement more precise control (PID controller) to smooth out motor movements.


## Connection Graph:

+-----------------+          +-----------------+          +-----------------+
|   Joystick      |          |  Controller     |          |   Jetson Device  |
|  (Computer)     |          |   (controller.py)|          |  (jetson_client.py)|
|                 |          |                 |          |                 |
|  (USB or Bluetooth) <--------| (TCP Socket) <---| (IP: 192.168.1.3)  |
+-----------------+          +-----------------+          +-----------------+
                                                             |
                                                             | (Serial)
                                                             |
                                                     +-----------------+
                                                     |   Arduino       |
                                                     |   (board.ino)   |
                                                     |                 |
                                                     +-----------------+
                                                             |
                                                             | (Motor Control)
                                                             |
                                                     +-----------------+
                                                     |   Motor Driver   |
                                                     |                 |
                                                     +-----------------+
                                                             |
                                                +------------+-------------+
                                                |                          |
                                        +-----------------+        +-----------------+
                                        |    Motor 1      |        |    Motor 2      |
                                        |                 |        |                 |
                                        +-----------------+        +-----------------+

