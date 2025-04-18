#!/usr/bin/env python
import os
import sys
# insert root directory into python module search path
sys.path.insert(1, os.getcwd())

import requests
import socket
import sys
import os
import configparser

url = None
username = None
password = None
active = False

config = configparser.ConfigParser()
config.read('datas/config.ini')

try:
    url = config['GetHost']['url']
    username = config['GetHost']['username']
    password = config['GetHost']['password']
    active = True
except Exception as error:
    # raise RuntimeError('getHostConfig parameter missing') from error
    # print('config Reader parameter missing')
    pass

if not active:
    print("GetHost is inactive!")
    exit()

try:
    location = sys.argv[1]
except:
    location = ""
try:
    description = sys.argv[2]
except:
    description = ""

print("Hostname...: " + socket.gethostname())

eth0 = os.popen('ip addr show eth0 | grep -vw "inet6" | grep "global" | grep -w "inet" | cut -d/ -f1 | awk \'{ print $2 }\'').read().rstrip()
wlan0 = os.popen('ip addr show wlan0 | grep -vw "inet6" | grep "global" | grep -w "inet" | cut -d/ -f1 | awk \'{ print $2 }\'').read().rstrip()

def getserial():
    # Extract serial from cpuinfo file
    cpuserial = "0000000000000000"
    try:
        f = open('/proc/cpuinfo', 'r')
        for line in f:
            if line[0:6] == 'Serial':
                cpuserial = line[10:26]
        f.close()
    except:
        cpuserial = "ERROR000000000"

    return cpuserial


data = {}
data['serial'] = getserial()
data['hostname'] = socket.gethostname()
data['lan'] = eth0
data['wlan'] = wlan0
if (location != ""):
    data['location'] = location
if (description != ""):
    data['description'] = description

try:
    r = requests.post(url, auth=(username, password), json=data, timeout=3)
except requests.exceptions.Timeout as err:
    print('timeout')
    sys.exit(0)
except requests.exceptions.HTTPError as err:
    print('HTTP Error')
    sys.exit(0)
except requests.exceptions.ConnectionError as err:
    print('Connection Error')
    sys.exit(0)
except requests.exceptions.RequestException as err:
    print('RequestException Error')
    sys.exit(0)
except Exception as err:
    print('Other Error')
    sys.exit(0)

if (r.status_code == 200):
    try:
        json = r.json()
        if (json['error'] == "0"):
            print("ID.........: " + str(json['id']).zfill(3))
            print("Location...: " + str(json['location']))
            print("Description: " + str(json['description']))
        else:
            print("Error......: " + str(json['error']))

    except:
        print("incorrect return data")
        print("---------------------")
        print(r.text)

else:
    print("Error Webservice")
    print("Status:" + str(r.status_code))
    print(r.text)
