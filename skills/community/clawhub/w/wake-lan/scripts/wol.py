#!/usr/bin/env python3
"""WOL helper — manage and wake devices on your LAN.

No devices are pre-configured. Use `add` to register your devices,
then wake them by alias. All device data is stored in references/devices.json.
"""

import json, os, sys, subprocess

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEVICES_FILE = os.path.join(SKILL_DIR, "references", "devices.json")


def load_devices():
    if not os.path.exists(DEVICES_FILE):
        return {}
    with open(DEVICES_FILE) as f:
        return json.load(f)


def save_devices(devices):
    os.makedirs(os.path.dirname(DEVICES_FILE), exist_ok=True)
    with open(DEVICES_FILE, "w") as f:
        json.dump(devices, f, indent=2)


def wake(alias=None, mac=None, ip=None, port=9):
    if alias:
        devices = load_devices()
        if alias not in devices:
            print(f"Unknown alias: {alias}")
            print("Known devices:", ", ".join(devices.keys()) if devices else "(none)")
            sys.exit(1)
        d = devices[alias]
        mac, ip, port = d["mac"], d.get("ip", "255.255.255.255"), d.get("port", 9)
    elif not mac:
        print("Specify an alias or --mac")
        sys.exit(1)

    # Method 1: wakeonlan CLI
    cmd = ["wakeonlan", "-i", ip, "-p", str(port), mac]
    print(f"Sending WOL magic packet to {mac} via {ip}:{port}...")
    result = subprocess.run(cmd, capture_output=True, text=True)

    # Method 2: Raw UDP sockets (needed on Termux/Android)
    try:
        import socket
        mac_bytes = bytes.fromhex(mac.replace(":", ""))
        packet = b"\xff" * 6 + mac_bytes * 16
        for target in ["255.255.255.255", ip]:
            for p in [9, 7]:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                sock.sendto(packet, (target, p))
                sock.close()
    except Exception as e:
        print(f"Raw socket fallback: {e}")

    if result.stdout:
        print(result.stdout.strip())
    if result.returncode != 0:
        print(f"Error: {result.stderr.strip()}")
    print("✅ WOL packet sent!")


def add_device(name, mac=None, ip=None, port=9):
    devices = load_devices()
    devices[name] = {"mac": mac, "ip": ip, "port": port}
    save_devices(devices)
    print(f"✅ Added device '{name}' ({mac} @ {ip}:{port})")


def remove_device(name):
    devices = load_devices()
    if name in devices:
        del devices[name]
        save_devices(devices)
        print(f"✅ Removed device '{name}'")
    else:
        print(f"Unknown device: {name}")


def list_devices():
    devices = load_devices()
    if not devices:
        print("No devices configured. Use 'add' to register a device.")
        return
    print(f"{'Alias':<15} {'MAC':<20} {'IP':<18} {'Port':<6}")
    print("-" * 60)
    for name, info in devices.items():
        print(f"{name:<15} {info['mac']:<20} {info.get('ip', 'N/A'):<18} {info.get('port', 9):<6}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  wol.py list                              # Show devices")
        print("  wol.py <alias>                           # Wake by alias")
        print("  wol.py --mac MAC --ip IP [--port P]      # Wake by MAC")
        print("  wol.py add <name> --mac MAC --ip IP [--port P]")
        print("  wol.py remove <name>")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "list":
        list_devices()
    elif cmd == "add":
        if len(sys.argv) < 5:
            print("Usage: wol.py add <name> --mac MAC --ip IP [--port P]")
            sys.exit(1)
        name = sys.argv[2]
        kwargs = {}
        i = 3
        while i < len(sys.argv):
            a = sys.argv[i]
            if a == "--mac" and i + 1 < len(sys.argv):
                kwargs["mac"] = sys.argv[i + 1]; i += 2
            elif a == "--ip" and i + 1 < len(sys.argv):
                kwargs["ip"] = sys.argv[i + 1]; i += 2
            elif a == "--port" and i + 1 < len(sys.argv):
                kwargs["port"] = int(sys.argv[i + 1]); i += 2
            else:
                i += 1
        if "mac" not in kwargs:
            print("Error: --mac is required"); sys.exit(1)
        add_device(name, **kwargs)
    elif cmd == "remove":
        if len(sys.argv) < 3:
            print("Usage: wol.py remove <name>"); sys.exit(1)
        remove_device(sys.argv[2])
    elif cmd in load_devices():
        wake(alias=cmd)
    elif cmd == "--mac":
        mac = sys.argv[2] if len(sys.argv) > 2 else None
        ip = "255.255.255.255"
        port = 9
        i = 3
        while i < len(sys.argv):
            a = sys.argv[i]
            if a == "--ip" and i + 1 < len(sys.argv):
                ip = sys.argv[i + 1]; i += 2
            elif a == "--port" and i + 1 < len(sys.argv):
                port = int(sys.argv[i + 1]); i += 2
            else:
                i += 1
        wake(mac=mac, ip=ip, port=port)
    else:
        print(f"Unknown command or alias: {cmd}")
        sys.exit(1)
