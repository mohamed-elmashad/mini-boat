import socket
import serial

# Setup serial connection to Arduino
arduino_serial = serial.Serial('/dev/ttyUSB0', 9600)  # Adjust port as needed

# Setup socket
server_ip = '10.0.0.207'
server_port = 25565
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))
server_socket.listen(1)

print("Waiting for connection...")
client_socket, client_address = server_socket.accept()
print(f"Connection from {client_address} has been established.")

try:
    while True:
        data = client_socket.recv(1024).decode().strip()
        if data:
            print(f"Received: {data}")
            arduino_serial.write((data + '\n').encode())

            # Check what the arudino is reading
            arduino_data = arduino_serial.readline().decode().strip()
            print(f"Arduino: {arduino_data}")
finally:
    client_socket.close()
    arduino_serial.close()
