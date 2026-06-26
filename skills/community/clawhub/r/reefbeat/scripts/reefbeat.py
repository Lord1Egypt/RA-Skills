#!/usr/bin/env python3
"""ReefBeat CLI — direct HTTP control for Red Sea ReefBeat devices.

Usage:
  python3 reefbeat.py discover [subnet]     # Auto-detect all ReefBeat devices
  python3 reefbeat.py <ip> info             # Device info + type
  python3 reefbeat.py <ip> status           # /dashboard status
  python3 reefbeat.py <ip> get <endpoint>
  python3 reefbeat.py <ip> post <endpoint> [<json_payload>]
  python3 reefbeat.py <ip> put <endpoint> <json_payload>
  python3 reefbeat.py <ip> delete <endpoint>
"""

from __future__ import annotations

import ipaddress
import json
import socket
import sys
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from multiprocessing import Pool
from typing import Optional

TIMEOUT = 3  # seconds per probe during discovery
DEVICE_TIMEOUT = 10  # seconds for control commands

# ---------------------------------------------------------------------------
# Known hardware model IDs (from ha-reefbeat-component/const.py)
# ---------------------------------------------------------------------------

HW_G1_LED    = ("RSLED50", "RSLED90", "RSLED160")
HW_G2_LED    = ("RSLED60", "RSLED115", "RSLED170")
HW_LED       = HW_G1_LED + HW_G2_LED
HW_DOSE      = ("RSDOSE2", "RSDOSE4")
HW_MAT       = ("RSMAT", "RSMAT250", "RSMAT500", "RSMAT1200")
HW_RUN       = ("RSRUN",)
HW_ATO       = ("RSATO+",)
HW_WAVE      = ("RSWAVE25", "RSWAVE45")
HW_ALL       = HW_LED + HW_DOSE + HW_MAT + HW_RUN + HW_ATO + HW_WAVE


def device_type(hw_model: str) -> str:
    if hw_model in HW_G1_LED:  return f"ReefLED G1 ({hw_model})"
    if hw_model in HW_G2_LED:  return f"ReefLED G2 ({hw_model})"
    if hw_model in HW_DOSE:    return f"ReefDose ({hw_model})"
    if hw_model in HW_MAT:     return f"ReefMat ({hw_model})"
    if hw_model in HW_RUN:     return f"ReefRun ({hw_model})"
    if hw_model in HW_ATO:     return f"ReefATO+ ({hw_model})"
    if hw_model in HW_WAVE:    return f"ReefWave ({hw_model})"
    return f"Unknown ({hw_model})"


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------

def _http(ip: str, method: str, path: str, payload=None, timeout: int = DEVICE_TIMEOUT):
    url = f"http://{ip}{path}"
    data = json.dumps(payload).encode() if payload is not None else None
    headers = {"Content-Type": "application/json"} if data else {}
    req = urllib.request.Request(url, data=data, headers=headers, method=method.upper())
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode()
            try:
                return json.loads(body)
            except Exception:
                return body
    except urllib.error.HTTPError as e:
        return {"error": e.code, "reason": e.reason, "body": e.read().decode()}
    except Exception as e:
        return {"error": str(e)}


def _get_uuid(ip: str) -> Optional[str]:
    """Fetch UUID from UPnP description.xml."""
    try:
        req = urllib.request.Request(f"http://{ip}/description.xml")
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            root = ET.fromstring(resp.read().decode())
            for el in root.iter():
                if isinstance(el.tag, str) and el.tag.split("}")[-1] == "UDN":
                    if el.text:
                        return el.text.strip().replace("uuid:", "")
    except Exception:
        pass
    return None


# ---------------------------------------------------------------------------
# Auto-discovery
# ---------------------------------------------------------------------------

def _probe(ip: str):
    """Probe one IP. Returns (is_reefbeat, ip, hw_model, name, uuid) or None."""
    try:
        req = urllib.request.Request(f"http://{ip}/device-info")
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            if resp.status != 200:
                return None
            data = json.loads(resp.read().decode())
        hw_model = data.get("hw_model", "")
        if not hw_model:
            return None
        # Check if it's a known ReefBeat device
        matched = any(hw_model == h or hw_model.startswith(h.rstrip("+")) for h in HW_ALL)
        if not matched:
            return None
        name = data.get("name") or data.get("hostname") or ip
        uuid = _get_uuid(ip)
        return {"ip": ip, "hw_model": hw_model, "name": name, "uuid": uuid or "", "type": device_type(hw_model)}
    except Exception:
        return None


def discover(subnet: Optional[str] = None, threads: int = 64) -> list[dict]:
    """Scan subnet and return all detected ReefBeat devices."""
    # Infer local subnet if not given
    if subnet is None:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                local_ip = s.getsockname()[0]
            subnet = f"{local_ip}/24"
        except OSError:
            print("Could not determine local subnet. Pass subnet explicitly.")
            return []

    net = ipaddress.ip_network(subnet, strict=False)
    ips = [str(h) for h in net.hosts()]
    print(f"Scanning {subnet} ({len(ips)} hosts, {threads} threads)...")

    if threads <= 1:
        results = [_probe(ip) for ip in ips]
    else:
        with Pool(min(threads, len(ips))) as pool:
            results = pool.map(_probe, ips)

    found = [r for r in results if r is not None]
    return found


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return

    cmd = args[0]

    # discover [subnet]
    if cmd == "discover":
        subnet = args[1] if len(args) > 1 else None
        devices = discover(subnet)
        if devices:
            print(f"\nFound {len(devices)} ReefBeat device(s):\n")
            for d in devices:
                print(f"  IP:    {d['ip']}")
                print(f"  Type:  {d['type']}")
                print(f"  Name:  {d['name']}")
                print(f"  UUID:  {d['uuid']}")
                print()
            print(json.dumps(devices, indent=2))
        else:
            print("No ReefBeat devices found.")
        return

    # Device commands: reefbeat.py <ip> <action> [endpoint] [payload]
    ip = cmd
    if len(args) < 2:
        print("Usage: reefbeat.py <ip> <action> [endpoint] [payload]")
        return

    action = args[1].lower()
    endpoint = args[2] if len(args) > 2 else "/dashboard"
    payload_str = args[3] if len(args) > 3 else None
    payload = json.loads(payload_str) if payload_str else None

    if action == "info":
        info = _http(ip, "GET", "/device-info")
        hw_model = info.get("hw_model", "") if isinstance(info, dict) else ""
        if hw_model:
            info["_device_type"] = device_type(hw_model)
            info["_uuid"] = _get_uuid(ip) or ""
        print(json.dumps(info, indent=2))

    elif action == "status":
        result = _http(ip, "GET", "/dashboard")
        print(json.dumps(result, indent=2))

    elif action in ("get", "post", "put", "delete"):
        result = _http(ip, action, endpoint, payload)
        print(json.dumps(result, indent=2))

    else:
        print(f"Unknown action: {action}")
        print("Actions: discover, info, status, get, post, put, delete")


if __name__ == "__main__":
    main()
