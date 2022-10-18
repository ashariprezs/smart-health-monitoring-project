import time
import requests
import os
from dotenv import load_dotenv
import random

from location import getLocation, buildLocation

load_dotenv()

# TOKEN = "..."  # Put your TOKEN here
TOKEN = os.getenv('TOKEN') # Put your TOKEN here
DEVICE_LABEL = os.getenv('DEVICE_LABEL')  # Put your device label here 
VARIABLE_LABEL_1 = os.getenv('VARIABLE_LABEL_1')  
VARIABLE_LABEL_2 = os.getenv('VARIABLE_LABEL_2')
VARIABLE_LABEL_3 = os.getenv('VARIABLE_LABEL_3')
VARIABLE_LABEL_4 = os.getenv('VARIABLE_LABEL_4')
VARIABLE_LABEL_5 = os.getenv('VARIABLE_LABEL_5')
VARIABLE_LABEL_6 = os.getenv('VARIABLE_LABEL_6')

VARIABLE_ID = os.getenv('VARIABLE_ID')  # Put your first variable label here


def build_payload(variable_1, variable_2, variable_3, variable_4, variable_5, variable_6,
                    value_1, value_2, value_3, value_4, value_5, value_6):

    payload = {
                variable_1: value_1, 
                variable_2: {
                                'value': 2, 
                                'context':{
                                            'name': value_2
                                          }
                            }, 
                variable_3: value_3, 
                variable_4: {
                                'value': 4, 
                                'context':{
                                            'name': value_4
                                          }
                            }, 
                variable_5: value_5, 
                variable_6: value_6
              }

    return payload

def post_request(payload):
    # Creates the headers for the HTTP requests
    try:
        url = "http://industrial.api.ubidots.com/api/v1.6/devices/"+ DEVICE_LABEL +"/" 
        headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

        # Makes the HTTP requests
        req = requests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        time.sleep(1)

        # Processes results
        # print(req.status_code, req.json())
        if status >= 400:
            print("[ERROR] Could not send data after 5 attempts, please check \
                your token credentials and internet connection")
            pass

        print("[INFO] request made properly, your device is updated")
        return True
    except:
        print("Cannot send to ubidots")
        pass

def randomData():
    value_1 = random.randint(60,100)
    value_2 = 'Nauval'
    value_3 = random.randint(90,100)
    value_4 = 'Normal'
    value_5 = round(random.uniform(37,42),1)

    return value_1, value_2, value_3, value_4, value_5


def sendData(value_1, value_2, value_3, value_4, value_5, value_6):
    '''
    Send data to Ubidots
    '''

    payload = build_payload(
        VARIABLE_LABEL_1, VARIABLE_LABEL_2, VARIABLE_LABEL_3, VARIABLE_LABEL_4, VARIABLE_LABEL_5,
        VARIABLE_LABEL_6, value_1, value_2, value_3, value_4, value_5, value_6)

    print("[INFO] Attemping to send data")

    attempt = 0
    # print(payload)

    for attempt in range(1,6):
        print(f'[INFO] Attempt #{attempt}')
        a = post_request(payload)

        if a:

            print('[INFO] Data sent:')
            print(f'[INFO] {VARIABLE_LABEL_1}: {value_1}')
            print(f'[INFO] {VARIABLE_LABEL_2}: {value_2}')
            print(f'[INFO] {VARIABLE_LABEL_3}: {value_3}')
            print(f'[INFO] {VARIABLE_LABEL_4}: {value_4}')
            print(f'[INFO] {VARIABLE_LABEL_5}: {value_5}')
            print(f'[INFO] {VARIABLE_LABEL_6}: {value_6}')
            print("[INFO] finished")

            return True
        attempt += 1
    print('Failed to send data after 5 attempt!')
    return False

if __name__ == '__main__':
    while True:
        val = randomData()
        location = buildLocation()

        sendData(val[0], val[1], val[2], val[3], val[4], location)
        time.sleep(3)