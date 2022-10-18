import time
import os
from types import NoneType
import numpy as np
from dotenv import load_dotenv

from rpi_lcd import LCD
from temperature import read_temp
from LED import *
from Oksi import Oksi, shutDownOksi, resetOksi
from sendUbidots import sendData
from location import buildLocation
from sendDataMongoDB import buildData, getTime, sendDataMongoDB, getLatestData

load_dotenv()

LATITUDE=float(os.getenv('LATITUDE'))
LONGITUDE=float(os.getenv('LONGITUDE'))

lcd = LCD()
LEDRed_Off()
LEDGreen_Off()
LEDBlue_On()

def logic(temp, spo2, bpm):
    '''
    Check condition using temperature, spo2, and bpm
    Take argument temp, spo2, bpm
    '''
    if spo2 <= 90:
        return 'Sakit parah'
    
    elif 90 < spo2 <= 95:
        if 36.5 <= temp <= 38.5:
            return 'Sakit'

        elif temp > 38.5:
            return 'Sakit parah'

        else:
            return 'Sakit'

    elif 95 < spo2 <= 100:
        if 36 <= temp <= 37.5:
            if bpm < 60:
                return 'Sakit'

            else:
                return 'Normal'

        elif 37.5 < temp <= 38.5:
            return 'Sakit'

        elif temp > 38.5:
            return 'Sakit parah'

        else:
            return 'Sakit'

def averageOksi2(statusPrint=True, banyak=20):
    '''
    Find average hearth rate and spo2 measurment, accept bol int
    Take minimum 100 value by default
    Returning (averagehr, averagesp2)
    '''
    hr =[]
    sp2 = []
    sw = False

    resetOksi()
    
    while len(hr) <= banyak or len(sp2) <= banyak:
        dta = Oksi(statusPrint)

        if dta[2]:
            if dta[0] < 40:
                hr.append(40)
            elif dta[0] > 130:
                hr.append(130)
            else:
                hr.append(dta[0])

        if dta[3]:
            sp2.append(dta[1])

        if not dta[2] or not dta[3]:
            lcd.text('Oksimeter:', 1)
            time.sleep(0.5)
            lcd.text('Not detected', 2)
            sw = True          #LCD menunjukkan selain mengukur... -> sw = True
        else:
            if sw:
                lcd.clear()
                time.sleep(0.5)
                lcd.text('Mengukur...', 1)
                sw = False      #LCD menunjukkan mengukur... -> sw = False

    avhr = int(np.average(hr))
    avsp2 = int(np.amax(sp2))

    return avhr, avsp2

def startSensor():
    '''
    Starting sensor, measure temperature, BPM, and SPO2
    Return (temperature, bpm, spo2)
    '''
    print('Mengukur...')

    oks = averageOksi2()
    time.sleep(5)

    temp = read_temp()

    return temp[0], oks[0], oks[1]

def showLCD(status=None, temp=None, bpm=None, spo2=None):
    '''
    Show LCD Data from sensor
    '''
    lcd.text(status, 1)
    lcd.text(f'{temp}C H{bpm} O{spo2}', 2)

def main(name):
    dta = startSensor()
    status = logic(dta[0], dta[2], dta[1])
    loc = buildLocation(LATITUDE, LONGITUDE)
    waktu = getTime()

    print(f"Temperature     : {dta[0]}")
    print(f'BPM             : {dta[1]}')
    print(f'SPO2            : {dta[2]}')
    print(f'Health status   : {status}')
    print(f'Location        : {loc}')

    lcd.clear()
    time.sleep(0.1)
    lcd.text('Sending data', 1)
    time.sleep(0.1)
    lcd.text('to database',2)

    try:
        sendData(dta[1], name, dta[2], status, dta[0], loc)

    except TypeError:
        lcd.text('Cannot send data', 1)
        lcd.text('to Ubidots', 2)

    time.sleep(0.5)
    showLCD(status, dta[0], dta[1], dta[2])

    if status == 'Normal':
        LEDGreen_On()
    elif status == 'Sakit':
        LEDRed_On()
    elif status == 'Sakit parah':
        for k in range(1,11):
            LEDRed_On()
            LEDRed_Off()
            
    try:
        latestMongoDB = getLatestData()

        if latestMongoDB is None:
            mongoData = buildData(1, name, dta[0], dta[2], dta[1], status, waktu, loc)
        else:
            idNew = latestMongoDB['id'] + 1
            mongoData = buildData(idNew, name, dta[0], dta[2], dta[1], status, waktu, loc)

            sendDataMongoDB(mongoData)
    except:
        print('[INFO] Cannot send data to MongoDB')
    

if __name__ == '__main__':
    LEDBlue_On()
    try:
        while True:
            lcd.text('Enter name...', 1)
            name = input('Enter name: ')
            lcd.clear()
            lcd.text('Mengukur...', 1)
            main(name)

            time.sleep(1)
            shutDownOksi()

            time.sleep(10)
            LEDGreen_Off()
            LEDRed_Off()

            time.sleep(10)
            lcd.clear()
    
    except KeyboardInterrupt:
        print('Keyboard interupt!')
        lcd.text('Program stopped', 1)
        lcd.text('Manual stop', 2)

        shutDownOksi()
        print('[Info] Oksimeter shuted down')

        LEDOffAll()
        print('[INFO] LED shuted down!')

        time.sleep(120)

        lcd.clear()
    