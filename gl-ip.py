#!/usr/bin/python

try:
    import requests
    import socket
    import psutil
except ModuleNotFoundError as e:
    print(f"Missing module: {e}")
    exit()
    
API = "https://api.ipify.org?format=json"

def local_ipv4():
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

def local_ipv6():
    s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    s.settimeout(0)
    
    try:
        s.connect(("2001:4860:4860::8888", 80))
        IP = s.getsockname()[0]
        
    except Exception:
        IP = "::1"
    
    finally:
        s.close()
    
    return IP if IP != "::1" else "Not found"

def global_ipv4():
    req = requests.get(API)
    
    data = req.json()
    
    return data['ip']

def global_ipv6():
    IPv6_addrs = {}
    
    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == socket.AF_INET6:
                ipv6_address = addr.address
                
                if not ipv6_address.startswith("fe80::"):
                    ipv6_address = ipv6_address.split("%")[0]
                    
                    IPv6_addrs[interface] = ipv6_address
    
    return IPv6_addrs

if __name__ == "__main__":
    print(f"Local IPv4: {local_ipv4()}")
    print(f"Global IPv4: {global_ipv4()}")
    print(f"\nLocal IPv6: {local_ipv6()}")
    print(f"Global IPv6: ")
    for interface, ipv6 in global_ipv6().items():
        print(f"    Interface: {interface}, IPv6: {ipv6}")
