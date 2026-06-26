import urllib.request

def get_public_ip():
    services = [
        "https://api.ipify.org",
        "https://ifconfig.me/ip",
        "https://icanhazip.com",
    ]
    for url in services:
        try:
            with urllib.request.urlopen(url, timeout=5) as resp:
                return resp.read().decode().strip()
        except Exception:
            continue
    return None

if __name__ == "__main__":
    ip = get_public_ip()
    print(ip if ip else "Failed to get public IP")