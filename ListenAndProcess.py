# -*- coding: utf-8 -*-
"""
Created on Sat Nov  9 17:42:22 2019

@author: tugba

1. Listen Web Server in every 5 Seconds
2. Check if the streams are updated since the last request. 
3. Process the values in some way. 
4. Report to the server by making POST request

"""

import time
import serial
import unicodedata
import requests
import json
import random
import datetime
from twilio.rest import Client

base = 'http://127.0.0.1:5000'
network_id = 'local'
header = {}
delay = 1*3600 # Delay in seconds

endpoint_battery_voltage = '/networks/local/objects/battery/streams/battery-voltage/points'
endpoint_SoC= '/networks/local/objects/data-analysis-results/streams/battery-soc/points'
query = {
    'object-name': 'Data Analysis Results'
}
endpoint = '/networks/'+network_id+'/objects/data-analysis-results'
response = requests.request('PUT', base + endpoint, params=query, headers=header, timeout=120 )
resp = json.loads( response.text )
if resp['object-code'] == 201:
    print('Create object test-object: ok')
else:
    print('Create object test-object: error')
    print( response.text )
    
query = {
    'stream-name': 'Battery State of Charge',
    'points-type': 'f' # 'i', 'f', or 's'
}
endpoint = '/networks/'+network_id+'/objects/data-analysis-results/streams/battery-soc'
response = requests.request('PUT', base + endpoint, params=query, headers=header, timeout=120 )
resp = json.loads( response.text )
if resp['stream-code'] == 201:
    print('Create stream test-stream: ok')
else:
    print('Create stream test-stream: error')
    print( response.text )

def SoC_dummy_function(V):
    if  V < 3:
        SoC = 0
    if  3 <= V <= 3.4:
        SoC = (V-3)* 20 / 0.4 
    if  3.4 <= V < 3.6:
        SoC = 20 + (V-3.4) * 70 / 0.2
    if  V >=3.6:
        SoC = 100
    return SoC
        
# Run once at the start
def setup():
    try:
        print ("Setup")
    except:
        print ("Setup Error")

# Run continuously forever
def loop():
    # 100 ms delay
    time.sleep(0.1)
    return

# Run continuously forever
# with a delay between calls
def delayed_loop():
    print ("Delayed Loop")
    get_requests = requests.request('GET', base + endpoint_battery_voltage, timeout=120)
    battery_voltage_server = json.loads(get_requests.text)
    #if  battery_voltage_server['points-code'] == 200:
        #print( 'Content Received from Server: ok')
        #print "Last Measurement on Server:" ,battery_voltage_server['points'][-1]
          
    #else:
        #print( 'Content Received from Server: error')
        
    time_unicode = battery_voltage_server['points'][-1]['at']
    time_at = unicodedata.normalize('NFKD', time_unicode).encode('ascii','ignore')
    #if time_at not in battery_voltage:
    #   battery_voltage[time_at] = battery_voltage_server['points'][-1]['value']
    
    state = SoC_dummy_function(battery_voltage_server['points'][-1]['value'])
    
    query = {
                    'points-value': state,
                    'points-at': datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                    }
    response = requests.request('POST', base+endpoint_SoC,params=query,headers=header,timeout=120 )
    resp = json.loads( response.text )
    #if resp['points-code'] == 200:
        #print( 'Update SoC points: ok')
    #else:
        #print( 'Update SoC points: error')
        #print( response.text )
    print(type(state) )
    return state

def send_message(state):
    account_sid = 'AC00be18befca33ff180a3beb74a4c1de7'
    auth_token = 'a2771ba9382c3257c0dda25b455cc2e7'
    client = Client(account_sid, auth_token)
    
    message = client.messages \
                .create(
                     body="Remaining battery power %state" %state,
                     from_='+14803510069',
                     to='+15109448745'
                 )
                
    print('SENT')
    print(message.sid)
    
     
# Run once at the end
def close():
    try:
        print ("Close")
    except:
        print ("Close Error")
    
# Program Structure    
def main():
    battery_voltage = {}
    # Call setup function
    setup()
    # Set start time
    nextLoop = time.time()
    
    while(True):
        # Try loop() and delayed_loop()
        try:
            state = delayed_loop()
            if time.time() > nextLoop:
                # If next loop time has passed...
                nextLoop = time.time() + delay
                send_message(state)
        except KeyboardInterrupt:
            # If user enters "Ctrl + C", break while loop
            break
        except:
            # Catch all errors
            print ("Unexpected error.")
    # Call close function
    close()

# Run the program
main()
