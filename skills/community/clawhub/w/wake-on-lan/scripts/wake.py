#!/usr/bin/env python3
"""
Wake on LAN (WOL) - Send magic packet to wake up a device

Usage:
    wake.py <mac_address> [broadcast_ip] [port]
    wake.py --device <device_name>

Examples:
    wake.py AA:BB:CC:DD:EE:FF
    wake.py AA:BB:CC:DD:EE:FF 192.168.1.255
    wake.py AA:BB:CC:DD:EE:FF 192.168.1.255 9
    wake.py --device my-pc

The magic packet is sent to the broadcast address (default: 255.255.255.255)
on port 9 (discard protocol). The target device must have WOL enabled in BIOS/UEFI
and the network card must support it.
"""

import argparse
import json
import socket
import struct
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional


def parse_mac_address(mac: str) -> bytes:
    """Parse MAC address string to bytes.
    
    Accepts formats: AA:BB:CC:DD:EE:FF, AA-BB-CC-DD-EE-FF, aabb.ccdd.eeff
    """
    # Remove common separators and normalize
    mac = mac.lower().replace(":", "").replace("-", "").replace(".", "")
    
    if len(mac) != 12:
        raise ValueError(f"Invalid MAC address: {mac} (expected 6 bytes)")
    
    try:
        return bytes.fromhex(mac)
    except ValueError as e:
        raise ValueError(f"Invalid MAC address: {mac}") from e


def create_magic_packet(mac: bytes) -> bytes:
    """Create WOL magic packet.
    
    Magic packet format:
    - 6 bytes of 0xFF (broadcast header)
    - 16 repetitions of the target MAC address (96 bytes)
    Total: 102 bytes
    """
    return b"\xff" * 6 + mac * 16


def send_wol_packet(
    mac: str,
    broadcast_ip: str = "255.255.255.255",
    port: int = 9,
    timeout: float = 2.0,
) -> bool:
    """Send WOL magic packet to wake up a device.
    
    Args:
        mac: MAC address string (e.g., "AA:BB:CC:DD:EE:FF")
        broadcast_ip: Broadcast IP address (default: 255.255.255.255)
        port: UDP port (default: 9, discard protocol)
        timeout: Socket timeout in seconds
        
    Returns:
        True if packet was sent successfully
    """
    try:
        mac_bytes = parse_mac_address(mac)
    except ValueError as e:
        print(f"Error: {e}")
        return False
    
    magic_packet = create_magic_packet(mac_bytes)
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.settimeout(timeout)
            sock.sendto(magic_packet, (broadcast_ip, port))
        print(f"WOL packet sent to {mac} via {broadcast_ip}:{port}")
        return True
    except socket.timeout:
        print(f"Error: Socket timeout while sending to {broadcast_ip}:{port}")
        return False
    except PermissionError:
        print("Error: Permission denied. Try running with elevated privileges or use port >= 1024.")
        return False
    except Exception as e:
        print(f"Error sending WOL packet: {e}")
        return False


def load_device_config() -> dict:
    """Load device configuration from JSON file."""
    config_path = Path(__file__).parent.parent / "references" / "devices.json"
    if config_path.exists():
        with open(config_path, "r") as f:
            return json.load(f)
    return {}


def save_device_config(devices: dict) -> None:
    """Save device configuration to JSON file."""
    config_path = Path(__file__).parent.parent / "references" / "devices.json"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    with open(config_path, "w") as f:
        json.dump(devices, f, indent=2)


def ping_host(ip: str, timeout: float = 2.0) -> bool:
    """Ping a host to check if it's online.
    
    Args:
        ip: IP address to ping
        timeout: Ping timeout in seconds
        
    Returns:
        True if host responds, False otherwise
    """
    try:
        # Use ping command with 1 count and timeout
        result = subprocess.run(
            ["ping", "-c", "1", "-W", str(int(timeout)), ip],
            capture_output=True,
            timeout=timeout + 1,
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        return False
    except Exception:
        return False


def wait_for_device(ip: str, timeout: float = 60.0, interval: float = 2.0) -> bool:
    """Wait for a device to come online by pinging it.
    
    Args:
        ip: IP address to check
        timeout: Maximum time to wait in seconds (default: 60s, recommended 30-120s)
        interval: Time between ping attempts in seconds
        
    Returns:
        True if device comes online within timeout, False otherwise
    """
    print(f"等待设备 {ip} 开机 (超时: {timeout}秒)...")
    start_time = time.time()
    attempt = 0
    
    while time.time() - start_time < timeout:
        attempt += 1
        elapsed = int(time.time() - start_time)
        
        if ping_host(ip):
            print(f"✓ 设备已上线! (耗时 {elapsed} 秒)")
            return True
        
        print(f"  尝试 {attempt}... ({elapsed}s/{int(timeout)}s)")
        time.sleep(interval)
    
    return False


def wake_device_by_name(device_name: str, wait: bool = False, timeout: float = 60.0) -> bool:
    """Wake a device by its configured name.
    
    Args:
        device_name: Name of the device to wake
        wait: If True, wait for device to come online
        timeout: Maximum time to wait for device (default: 60s)
        
    Returns:
        True if device was woken successfully (and came online if wait=True)
    """
    devices = load_device_config()
    
    # Case-insensitive lookup
    device_name_lower = device_name.lower()
    for name, config in devices.items():
        if name.lower() == device_name_lower:
            mac = config.get("mac")
            broadcast = config.get("broadcast", "255.255.255.255")
            port = config.get("port", 9)
            ip = config.get("ip")  # Optional IP for ping check
            print(f"Waking device '{name}'...")
            success = send_wol_packet(mac, broadcast, port)
            
            if success and wait and ip:
                if wait_for_device(ip, timeout):
                    print("✓ 开机成功")
                    return True
                else:
                    print("✗ 开机失败，请稍后再试或者检查网络设置是否正常")
                    return False
            
            return success
    
    print(f"Error: Device '{device_name}' not found in configuration")
    print(f"Known devices: {', '.join(devices.keys()) if devices else 'none'}")
    return False


def list_devices() -> None:
    """List all configured devices."""
    devices = load_device_config()
    # Filter out non-device entries (like _comment)
    device_entries = {k: v for k, v in devices.items() if isinstance(v, dict) and "mac" in v}
    
    if not device_entries:
        print("No devices configured.")
        print("\nTo add a device, create references/devices.json with:")
        print('  {"device-name": {"mac": "AA:BB:CC:DD:EE:FF", "broadcast": "192.168.1.255", "port": 9}}')
        return
    
    print("Configured devices:")
    for name, config in device_entries.items():
        mac = config.get("mac", "?")
        broadcast = config.get("broadcast", "255.255.255.255")
        port = config.get("port", 9)
        note = config.get("note", "")
        print(f"  {name}: {mac} ({broadcast}:{port})")
        if note:
            print(f"    Note: {note}")


def add_device(name: str, mac: str, broadcast: str = "255.255.255.255", port: int = 9) -> None:
    """Add or update a device in configuration."""
    devices = load_device_config()
    devices[name] = {"mac": mac, "broadcast": broadcast, "port": port}
    save_device_config(devices)
    print(f"Device '{name}' added: {mac}")


def main():
    parser = argparse.ArgumentParser(
        description="Send Wake on LAN magic packet to wake up a device",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s AA:BB:CC:DD:EE:FF
  %(prog)s AA:BB:CC:DD:EE:FF 192.168.1.255
  %(prog)s --device my-pc
  %(prog)s --list
  %(prog)s --add my-pc AA:BB:CC:DD:EE:FF
        """,
    )
    
    parser.add_argument("mac", nargs="?", help="MAC address of target device")
    parser.add_argument("broadcast", nargs="?", default="255.255.255.255", 
                        help="Broadcast IP (default: 255.255.255.255)")
    parser.add_argument("port", nargs="?", type=int, default=9,
                        help="UDP port (default: 9)")
    
    parser.add_argument("--device", "-d", metavar="NAME",
                        help="Wake a device by name from configuration")
    parser.add_argument("--list", "-l", action="store_true",
                        help="List configured devices")
    parser.add_argument("--add", nargs=2, metavar=("NAME", "MAC"),
                        help="Add a device to configuration")
    parser.add_argument("--broadcast-ip", metavar="IP",
                        help="Override broadcast IP for --add")
    parser.add_argument("--port-override", type=int, metavar="PORT",
                        help="Override port for --add")
    parser.add_argument("--wait", "-w", action="store_true",
                        help="Wait for device to come online after sending WOL")
    parser.add_argument("--timeout", "-t", type=float, default=60.0,
                        metavar="SECONDS",
                        help="Timeout for waiting device to come online (default: 60s)")
    
    args = parser.parse_args()
    
    # List devices
    if args.list:
        list_devices()
        return 0
    
    # Add device
    if args.add:
        name, mac = args.add
        broadcast = args.broadcast_ip or "255.255.255.255"
        port = args.port_override or 9
        add_device(name, mac, broadcast, port)
        return 0
    
    # Wake by device name
    if args.device:
        success = wake_device_by_name(args.device, wait=args.wait, timeout=args.timeout)
        return 0 if success else 1
    
    # Wake by MAC address
    if args.mac:
        success = send_wol_packet(args.mac, args.broadcast, args.port)
        if success and args.wait:
            print("Error: --wait requires device name (--device) with configured IP")
            return 1
        return 0 if success else 1
    
    # No arguments provided
    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
