import socket
import pygame
import time

# Initialize pygame and joystick
pygame.init()
pygame.joystick.init()

joystick = pygame.joystick.Joystick(0)
joystick.init()

def get_joystick_data():
    pygame.event.pump()
    axis_data = {}
    for i in range(joystick.get_numaxes()):
        axis_data[i] = joystick.get_axis(i)
    
    button_data = {}
    for i in range(joystick.get_numbuttons()):
        button_data[i] = joystick.get_button(i)
    
    return axis_data, button_data

def calculate_motor_speeds(axis_data, button_data):
    forward = -axis_data[1]  # Invert to match typical forward/backward logic
    turn = axis_data[0]

    # Check for button presses for in-place turning
    turn_left_button = button_data[9]  # Assuming button index 4 for left turn
    turn_right_button = button_data[10]  # Assuming button index 5 for right turn

    if turn_left_button:
        print("TURN LEFT")
        turn = -1  # Maximum turn left
    elif turn_right_button:
        turn = 1  # Maximum turn right

    # Calculate differential drive speeds
    left_motor_speed = forward + turn
    right_motor_speed = forward - turn

    # Scale the speeds to -255 to 255 range
    left_motor_speed = int(left_motor_speed * 255)
    right_motor_speed = int(right_motor_speed * 255)

    MAX_SPEED = 127
    # Ensure speed is under MAX_SPEED
    left_motor_speed = max(min(left_motor_speed, MAX_SPEED), -MAX_SPEED)
    right_motor_speed = max(min(right_motor_speed, MAX_SPEED), -MAX_SPEED)

    return left_motor_speed, right_motor_speed

def connect_to_server(server_ip, server_port):
    while True:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((server_ip, server_port))
            print(f"Connected to server at {server_ip}:{server_port}")
            return client_socket
        except ConnectionRefusedError:
            print("ConnectionRefusedError: Retrying connection in 5 seconds...")
            time.sleep(5)

# Setup socket
server_ip = '192.168.1.3'  # Replace with Jetson's IP address
server_port = 25565

client_socket = connect_to_server(server_ip, server_port)

try:
    while True:
        axis_data, button_data = get_joystick_data()
        left_motor_speed, right_motor_speed = calculate_motor_speeds(axis_data, button_data)
        print(f"Left: {left_motor_speed}, Right: {right_motor_speed}")
        message = f"{left_motor_speed},{right_motor_speed}\n"
        
        try:
            client_socket.sendall(message.encode())
        except BrokenPipeError:
            print("BrokenPipeError: The connection was lost. Reconnecting...")
            client_socket = connect_to_server(server_ip, server_port)

        time.sleep(0.1)
finally:
    print("Closing connection...")
    client_socket.close()
