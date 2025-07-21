#!/usr/bin/env python3

import serial
import subprocess
import time
import glob

# Constants
BAUD_RATE = 115200
TIMEOUT = 1
DEFAULT_SPEED = 10
CLICK_COOLDOWN = 0.5
LEFT_CLICK_CODE = '0xC0'
RIGHT_CLICK_CODE = '0xC1'
SPEED_MIN = 1
SPEED_MAX = 6
SPEED_MULTIPLIER = 10

def find_serial_port():
    """Scans for and returns the first available serial port that sends data."""
    ports = glob.glob('/dev/ttyUSB*') + glob.glob('/dev/ttyACM*')
    for port in ports:
        try:
            print(f"Testing port {port}...")
            ser = serial.Serial(port, BAUD_RATE, timeout=1)
            # Give the device a moment to send an initial message
            time.sleep(2)
            line = ser.readline()
            ser.close()
            if line:
                print(f"Found active device on port: {port}")
                return port
            else:
                print(f"Port {port} is silent.")
        except (OSError, serial.SerialException) as e:
            print(f"Could not open or read from port {port}: {e}")
            pass
    return None

def ydotool_cmd(*args):
    try:
        subprocess.run(['ydotool', *args], check=True)
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"Error executing ydotool command: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def ydotool_move(x, y):
    ydotool_cmd('mousemove', '-x', str(x), '-y', str(y))

def ydotool_click():
    ydotool_cmd('click', LEFT_CLICK_CODE)

def ydotool_esc():
    ydotool_cmd('key', 'ESC')

def ydotool_right_click():
    ydotool_cmd('click', RIGHT_CLICK_CODE)

def process_serial_data(ser, last_click_time, speed):
    try:
        line = ser.readline()
        if not line:
            return last_click_time, speed

        try:
            line = line.decode(errors='ignore').strip()
        except UnicodeDecodeError:
            return last_click_time, speed

        if not line:
            return last_click_time, speed

        print(f"Received: {line}")

        if "UP" in line:
            ydotool_move(0, -speed)
        elif "DOWN" in line:
            ydotool_move(0, speed)
        elif "LEFT" in line:
            ydotool_move(-speed, 0)
        elif "RIGHT" in line:
            ydotool_move(speed, 0)
        elif "CLICK" in line:
            current_time = time.time()
            if current_time - last_click_time > CLICK_COOLDOWN:
                ydotool_click()
                last_click_time = current_time
        elif "RC" in line:
            current_time = time.time()
            if current_time - last_click_time > CLICK_COOLDOWN:
                ydotool_right_click()
                last_click_time = current_time
        elif line.startswith("X") and line[1:].isdigit():
            num = int(line[1:])
            if SPEED_MIN <= num <= SPEED_MAX:
                speed = num * SPEED_MULTIPLIER
        elif "ESC" in line:
            ydotool_esc()
    except serial.SerialException as e:
        print(f"Serial error: {e}")
        time.sleep(5)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return last_click_time, speed

def main():
    last_click_time = 0
    speed = DEFAULT_SPEED

    while True:
        port = find_serial_port()
        if port:
            print(f"Attempting to connect to {port}...")
            try:
                ser = serial.Serial(port, BAUD_RATE, timeout=TIMEOUT)
                print(f"Successfully connected to {port}")
                while True:
                    last_click_time, speed = process_serial_data(ser, last_click_time, speed)
            except serial.SerialException as e:
                print(f"Lost connection to {port}: {e}. Rescanning...")
                time.sleep(5)
            except KeyboardInterrupt:
                print("\nExiting.")
                break
        else:
            print("No active serial port found. Retrying in 5 seconds...")
            time.sleep(5)

if __name__ == "__main__":
    main()
