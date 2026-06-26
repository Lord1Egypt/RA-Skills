#!/usr/bin/env python3
import os
import sys
import json
import socket
import platform
import subprocess
import time

class ProxyInfo:
    def __init__(self):
        self.address = ""
        self.is_active = False

def is_proxy_running(proxy_addr):
    """Check if proxy server is actually running"""
    # Remove protocol prefix if present
    proxy_addr = proxy_addr.replace("http://", "").replace("https://", "")
    
    # Ensure port is present
    if ":" not in proxy_addr:
        proxy_addr += ":8080"
    
    # Try to establish TCP connection
    try:
        host, port = proxy_addr.split(":")
        port = int(port)
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((host, port))
        sock.close()
        
        return result == 0
    except Exception:
        return False

def detect_windows_proxy():
    """Detect Windows system proxy settings"""
    try:
        # Query registry for proxy server setting
        cmd = ["reg", "query", "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings", "/v", "ProxyServer"]
        output = subprocess.check_output(cmd, universal_newlines=True, stderr=subprocess.STDOUT)
        
        # Parse output to find proxy address
        lines = output.strip().split("\n")
        for line in lines:
            parts = line.split()
            if len(parts) >= 3 and parts[1] == "REG_SZ":
                proxy_address = parts[2]
                if proxy_address:
                    # Check if proxy is running
                    full_address = f"http://{proxy_address}"
                    if is_proxy_running(full_address):
                        info = ProxyInfo()
                        info.address = full_address
                        info.is_active = True
                        return info
    except subprocess.CalledProcessError:
        pass
    except Exception:
        pass
    
    # Try common proxies if registry query fails
    return detect_common_proxies()

def detect_mac_proxy():
    """Detect macOS system proxy settings"""
    try:
        # Query HTTP proxy settings for Wi-Fi
        cmd = ["networksetup", "-getwebproxy", "Wi-Fi"]
        output = subprocess.check_output(cmd, universal_newlines=True, stderr=subprocess.STDOUT)
        
        # Check if proxy is enabled
        if "Enabled: Yes" not in output:
            return detect_common_proxies()
        
        # Extract proxy address and port
        proxy_address = ""
        proxy_port = ""
        
        lines = output.strip().split("\n")
        for line in lines:
            if line.startswith("Server:"):
                proxy_address = line.split(":", 1)[1].strip()
            elif line.startswith("Port:"):
                proxy_port = line.split(":", 1)[1].strip()
        
        if proxy_address and proxy_port:
            full_address = f"http://{proxy_address}:{proxy_port}"
            if is_proxy_running(full_address):
                info = ProxyInfo()
                info.address = full_address
                info.is_active = True
                return info
    except subprocess.CalledProcessError:
        pass
    except Exception:
        pass
    
    # Try common proxies if networksetup query fails
    return detect_common_proxies()

def detect_common_proxies():
    """Detect common proxy addresses"""
    common_proxies = [
        "http://127.0.0.1:7890",  # Clash/Clash for Windows
        "http://127.0.0.1:10809", # ShadowsocksR
        "http://127.0.0.1:8080",  # Other proxy tools
        "http://127.0.0.1:3128",  # Squid proxy
        "http://127.0.0.1:1080",  # Shadowsocks
        "http://localhost:15236", # Detected in previous run
    ]
    
    for proxy in common_proxies:
        if is_proxy_running(proxy):
            info = ProxyInfo()
            info.address = proxy
            info.is_active = True
            return info
    
    # No active proxy found
    info = ProxyInfo()
    info.is_active = False
    return info

def detect_proxy():
    """Detect current system proxy settings"""
    os_name = platform.system()
    
    if os_name == "Windows":
        return detect_windows_proxy()
    elif os_name == "Darwin":  # macOS
        return detect_mac_proxy()
    else:
        # For other OS, try common proxies
        return detect_common_proxies()

def main():
    print("=== Proxy Detector ===")
    print("Detecting system proxy settings...")
    
    # Detect proxy
    proxy_info = detect_proxy()
    
    # Display results
    print("\n=== Detection Results ===")
    if proxy_info.is_active:
        print(f"Active proxy detected: {proxy_info.address}")
        print("Proxy test successful!")
    else:
        print("No active proxy detected")
    
    # Output JSON format proxy information
    output_json = {
        "address": proxy_info.address,
        "isActive": proxy_info.is_active
    }
    
    print("\n=== PROXY_INFO_START ===")
    print(json.dumps(output_json, ensure_ascii=False))
    print("=== PROXY_INFO_END ===")

if __name__ == "__main__":
    main()