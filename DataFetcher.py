import serial
import time
from datetime import datetime

try:
    ard = serial.Serial("COM6", 9600, timeout=1)
except:
    print('Please check the port')

file = open('Dat.txt', 'a') # TODO: Edit Dat.txt to Data.txt
while True:
    temp = str(ard.readline())
    if temp != "b''":
        temp = temp.split('\\')[0][2:]
        now = datetime.now().strftime("%m/%d/%Y %I:%M:%S %p")
        if temp == 'Entry':
            now += ' 1'
        elif temp == 'Exit':
            now += ' 0'
        print(now, file=file)
    time.sleep(0.1)