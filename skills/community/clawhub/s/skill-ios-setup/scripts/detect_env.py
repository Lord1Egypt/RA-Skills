#!/usr/bin/env python3
"""
Detect OpenClaw environment for iOS setup skill.
Outputs JSON with install type, ports, IPs, and tool availability.
"""
import json
import os
import subprocess
import socket
import sys


def run(cmd, timeout=5):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip()
    except Exception:
        return ""


def is_running(process_name):
    return bool(run(f"pgrep -f {process_name}"))


def detect_install_type():
    # Check if running inside Docker
    if os.path.exists("/.dockerenv"):
        return "docker"
    try:
        with open("/proc/1/cgroup") as f:
            if "docker" in f.read():
                return "docker"
    except Exception:
        pass
    return "direct"


def get_gateway_token():
    try:
        result = run("openclaw config get gateway.auth.token 2>/dev/null")
        if result and result != "null":
            return result.strip('"')
    except Exception:
        pass
    # Fallback: read from config file
    config_path = os.path.expanduser("~/.openclaw/openclaw.json")
    if os.path.exists(config_path):
        try:
            import re
            with open(config_path) as f:
                content = f.read()
            # Simple regex for token field (JSON5 may have comments)
            m = re.search(r'"token"\s*:\s*"([^"]+)"', content)
            if m:
                return m.group(1)
        except Exception:
            pass
    return None


def get_gateway_port():
    result = run("openclaw config get gateway.port 2>/dev/null")
    try:
        return int(result)
    except Exception:
        return 18789


def get_public_ip():
    result = run("curl -s --max-time 3 https://api.ipify.org")
    return result if result else None


def get_tailscale_ip():
    result = run("tailscale ip -4 2>/dev/null")
    return result if result else None


def get_tailscale_hostname():
    result = run("tailscale status --json 2>/dev/null")
    if result:
        try:
            d = json.loads(result)
            return d.get("Self", {}).get("DNSName", "").rstrip(".")
        except Exception:
            pass
    return None


def get_lan_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return run("hostname -I 2>/dev/null | awk '{print $1}'") or None


def get_workspace():
    result = run("openclaw config get agents.defaults.workspace 2>/dev/null")
    if result and result != "null":
        return result.strip('"')
    return os.path.expanduser("~/.openclaw/workspace")


def nginx_available():
    return bool(run("which nginx 2>/dev/null"))


def tailscale_available():
    return bool(run("which tailscale 2>/dev/null"))


def detect_os():
    import platform
    s = platform.system().lower()
    if "linux" in s:
        return "linux"
    if "darwin" in s:
        return "macos"
    return "other"


def main():
    install_type = detect_install_type()
    stats_running = is_running("stats_server.py")
    tailscale_ip = get_tailscale_ip()
    tailscale_hostname = get_tailscale_hostname() if tailscale_ip else None

    result = {
        "install_type": install_type,
        "workspace": get_workspace(),
        "gateway_token": get_gateway_token(),
        "gateway_port": get_gateway_port(),
        "stats_running": stats_running,
        "stats_port": 8765,
        "public_ip": get_public_ip(),
        "lan_ip": get_lan_ip(),
        "tailscale_ip": tailscale_ip,
        "tailscale_hostname": tailscale_hostname,
        "nginx_available": nginx_available(),
        "tailscale_available": tailscale_available(),
        "os": detect_os(),
    }

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
