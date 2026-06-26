import requests
import json
import sys

def get_public_ip():
    services = [
        "https://api.ipify.org?format=json",
        "https://ifconfig.me/all.json",
        "https://ipapi.co/json/",
        "https://api.myip.com"
    ]
    
    results = {}
    for service in services:
        try:
            response = requests.get(service, timeout=5)
            if response.status_code == 200:
                data = response.json()
                # Standardize the output
                if "ip" in data:
                    results[service] = data["ip"]
                elif "ip_addr" in data:
                    results[service] = data["ip_addr"]
                elif "query" in data: # ip-api.com style
                    results[service] = data["query"]
        except Exception as e:
            continue
            
    if not results:
        return {"error": "Unable to retrieve public IP address from any service."}
    
    # Get the most common result if multiple services return different IPs (unlikely but possible)
    ip_counts = {}
    for ip in results.values():
        ip_counts[ip] = ip_counts.get(ip, 0) + 1
    
    most_common_ip = max(ip_counts, key=ip_counts.get)
    
    return {
        "public_ip": most_common_ip,
        "details": results
    }

if __name__ == "__main__":
    result = get_public_ip()
    print(json.dumps(result, indent=2))
    if "error" in result:
        sys.exit(1)
