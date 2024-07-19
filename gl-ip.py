#!/usr/bin/python

import requests
import json
import ipaddress
import socket

API = "https://api.ipify.org?format=json"

def local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)

    try:
        s.connect(("10.254.254.254", 1))
        IP = s.getsockname()[0]
        
    except Exception:
        IP = '127.0.0.1'
        
    finally:
        s.close()
        
    return IP

def global_ip():
    req = requests.get(API)
    
    data = req.json()
    
    return data['ip']


if __name__ == "__main__":
    print(f"Your global ip: {global_ip()}")
    print(f"Your local ip: {local_ip()}")