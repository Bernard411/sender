import serial
import requests
import time

# Local Config
SERIAL_PORT = "/dev/ttyACM0"  # Change this if using a different port
BAUD_RATE = 9600
REMOTE_API_URL = "https://chief265.pythonanywhere.com/api/update_data/"

# Initialize serial connection
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud")
    time.sleep(2)  # Give some time for the connection to stabilize
except serial.SerialException as e:
    print(f"Error: Could not open serial port {SERIAL_PORT}. {e}")
    exit(1)

# Function to send data
def send_to_api(sensor_value):
    data = {"sensor_value": sensor_value}
    try:
        response = requests.post(REMOTE_API_URL, json=data)
        if response.ok:
            print(f"✅ Sent: {sensor_value} | Response: {response.text}")
        else:
            print(f"❌ Failed to send data | Status Code: {response.status_code} | Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Request Error: {e}")

# Read serial data and send it
while True:
    try:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()  # Read and decode the line
            if line:  # Ensure it's not empty
                try:
                    sensor_value = float(line)  # Convert to float
                    send_to_api(sensor_value)  # Send to API
                except ValueError:
                    print(f"⚠️ Invalid data received: {line}")
        time.sleep(2)  # Adjust frequency of sending data
    except KeyboardInterrupt:
        print("\n🔴 Stopping script.")
        ser.close()
        break
