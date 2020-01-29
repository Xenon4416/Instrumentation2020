import serial
import time

try:
    arduino = serial.Serial("COM6",timeout=1)
except:
    print('Please check the port')

while True:
    temp = str(arduino.readline())
    print(temp[2:-5])
    time.sleep(0.1)