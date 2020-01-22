# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 13:46:14 2019

@author: tugba

1. Receive Data from Arduino
2. Report Stream Values to the Web Server(i.e Pico Server) use HTTP POST to the servers Web API. 
3. Listen to 1 data stream by making HTTP Get requests to the API once every 5 seconds

"""

"""
    Simple program structure
    PROGRAM STRUCTURE PY
    
"""
"""
    Simple program structure
    
"""
import time
import serial

import requests
import json
import random
import datetime

base = 'http://127.0.0.1:5000'
network_id = 'local'
header = {}

serial_port_name = 'COM4'
ser = serial.Serial(serial_port_name, 9600, timeout=1)
delay = 1*5 # Delay in seconds

endpoint_solar_voltage = '/networks/local/objects/solar-pv/streams/solar-voltage/points'
endpoint_battery_voltage = '/networks/local/objects/battery/streams/battery-voltage/points'
endpoint_battery_current = '/networks/local/objects/battery/streams/battery-current/points'
endpoint_load_current = '/networks/local/objects/load/streams/load-current/points'

# Run once at the start
query = {
    'object-name': 'Solar PV'
}
endpoint = '/networks/'+network_id+'/objects/solar-pv'
response = requests.request('PUT', base + endpoint, params=query, headers=header, timeout=120 )
resp = json.loads( response.text )
if resp['object-code'] == 201:
    print('Create object solar-voltage: ok')
else:
    print('Create object solar-voltage: error')
    print( response.text )

query = {
    'object-name': 'Battery'
}
endpoint = '/networks/'+network_id+'/objects/battery'
response = requests.request('PUT', base + endpoint, params=query, headers=header, timeout=120 )
resp = json.loads( response.text )
if resp['object-code'] == 201:
    print('Create object battery ok')
else:
    print('Create object battery: error')
    print( response.text )
    
query = {
    'object-name': 'Load'
}
endpoint = '/networks/'+network_id+'/objects/load'
response = requests.request('PUT', base + endpoint, params=query, headers=header, timeout=120 )
resp = json.loads( response.text )
if resp['object-code'] == 201:
    print('Create object load: ok')
else:
    print('Create object load: error')
    print( response.text )

query = {
    'stream-name': 'Battery Voltage',
    'points-type': 'i' # 'i', 'f', or 's'
}
endpoint = '/networks/'+network_id+'/objects/battery/streams/battery-voltage'
response = requests.request('PUT', base + endpoint, params=query, headers=header, timeout=120 )
resp = json.loads( response.text )
if resp['stream-code'] == 201:
    print('Create stream battery-voltage: ok')
else:
    print('Create stream battery-voltage: error')
    print( response.text )
    
query = {
    'stream-name': 'Battery Current',
    'points-type': 'i' # 'i', 'f', or 's'
}
endpoint = '/networks/'+network_id+'/objects/battery/streams/battery-current'
response = requests.request('PUT', base + endpoint, params=query, headers=header, timeout=120 )
resp = json.loads( response.text )
if resp['stream-code'] == 201:
    print('Create stream battery-current: ok')
else:
    print('Create stream battery-current: error')
    print( response.text )
    
query = {
    'stream-name': 'Solar Voltage',
    'points-type': 'i' # 'i', 'f', or 's'
}
endpoint = '/networks/'+network_id+'/objects/solar-pv/streams/solar-voltage'
response = requests.request('PUT', base + endpoint, params=query, headers=header, timeout=120 )
resp = json.loads( response.text )
if resp['stream-code'] == 201:
    print('Create stream solar-voltage: ok')
else:
    print('Create stream solar-voltage: error')
    print( response.text )
    
query = {
    'stream-name': 'Load Current',
    'points-type': 'i' # 'i', 'f', or 's'
}
endpoint = '/networks/'+network_id+'/objects/load/streams/load-current'
response = requests.request('PUT', base + endpoint, params=query, headers=header, timeout=120 )
resp = json.loads( response.text )
if resp['stream-code'] == 201:
    print('Create stream load-current: ok')
else:
    print('Create stream load-current: error')
    print( response.text )
    
print("Start sending measurements received from ARDUINO (Ctrl+C to stop)")

def setup():
    try:
        print "Setup"
    except:
        print "Setup Error"

# Run continuously forever
def loop():
    if ser.inWaiting()> 0: 
        try:
            v_solar = ser.readline()
            print "v_solar:",v_solar
            print "Type:", type(v_solar)
            
            query = {
                    'points-value': v_solar,
                    'points-at': datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                    }
            response = requests.request('POST', base + endpoint_solar_voltage, params=query, headers=header, timeout=120 )
            resp = json.loads( response.text )
            if resp['points-code'] == 200:
                print( 'Update solar-voltage points: ok')
            else:
                    print( 'Update solar-voltage points: error')
                    print( response.text )
            
            v_battery = ser.readline()
            
            print "v_battery:",v_battery
            print "Type:", type(v_battery)
            
            query = {
                    'points-value': v_battery,
                    'points-at': datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                    }
            response = requests.request('POST', base + endpoint_battery_voltage, params=query, headers=header, timeout=120 )
            resp = json.loads( response.text )
            if resp['points-code'] == 200:
                print( 'Update battery_voltage points: ok')
            else:
                    print( 'Update battery_voltage points: error')
                    print( response.text )
            
            i_battery = ser.readline()
            print "i_battery:",i_battery
            print "Type:", type(i_battery)
            
            query = {
                    'points-value': i_battery,
                    'points-at': datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                    }
            response = requests.request('POST', base + endpoint_battery_current, params=query, headers=header, timeout=120 )
            resp = json.loads( response.text )
            if resp['points-code'] == 200:
                print( 'Update battery_current points: ok')
            else:
                    print( 'Update battery_current points: error')
                    print( response.text )
            
            i_load = ser.readline()
            print "i_load:",i_load
            print "Type:", type(i_load)
            
            query = {
                    'points-value': i_load,
                    'points-at': datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                    }
            response = requests.request('POST', base + endpoint_load_current, params=query, headers=header, timeout=120 )
            resp = json.loads( response.text )
            if resp['points-code'] == 200:
                print( 'Update load-current points: ok')
            else:
                    print( 'Update load-current  points: error')
                    print( response.text )
                
            ledState = ser.readline()
            print "ledState:",ledState
            print "Type:", type(ledState),"\n"
            
            get_requests = requests.request('GET', base + endpoint_solar_voltage, timeout=120)
            solar_voltage_server = json.loads(get_requests.text)
            if  solar_voltage_server['points-code'] == 200:
                print( 'Content Received from Server: ok')
                print "Last Measurement on Server:" ,solar_voltage_server['points'][-1]["value"] 
                
            else:
                print( 'Content Received from Server: error')
            last_reading = solar_voltage_server['points'][-1]["value"]    
            
            ser.write(str(last_reading))
        except: 
            print "Error"
    time.sleep(5)
    return

# Run continuously forever
# with a delay between calls
def delayed_loop():
    print ""
    #if ser.inWaiting()> 0: 
        #try:
         #   get_requests = requests.request('GET', base + endpoint_solar_voltage, timeout=120)
          #  solar_voltage_server = json.loads(get_requests.text)
           # if resp['points-code'] == 200:
            #    print 'Content Received from Server: ok'
            #else:
            #    print 'Content Received from Server: error'
        #except: 
         #   print "Error"


# Run once at the end
def close():
    try:
        print "Close Serial Port"
        ser.close()
    except:
        print "Close Error"
    
# Program Structure    
def main():
    # Call setup function
    setup()
    # Set start time
    nextLoop = time.time()
    while(True):
        # Try loop() and delayed_loop()
        try:
            loop()
            
            if time.time() > nextLoop:
                # If next loop time has passed...
                nextLoop = time.time() + delay
                delayed_loop()
        except KeyboardInterrupt:
            # If user enters "Ctrl + C", break while loop
            break
        except:
            # Catch all errors
            print "Unexpected error."
    # Call close function
    close()

# Run the program


main()