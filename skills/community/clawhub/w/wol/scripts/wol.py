#!/usr/bin/env python3
"""Wake-on-LAN script to send magic packets to wake computers."""

import argparse
import socket
import struct
import subprocess
import yaml
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEVICES_FILE = os.path.join(os.path.dirname(SCRIPT_DIR), 'references', 'devices.yaml')
WOL_PORT = 9

def load_devices():
    """Load device configurations from YAML file."""
    if not os.path.exists(DEVICES_FILE):
        return {}
    with open(DEVICES_FILE, 'r') as f:
        data = yaml.safe_load(f)
    return data.get('devices', {})

def save_devices(devices):
    """Save device configurations to YAML file."""
    with open(DEVICES_FILE, 'w') as f:
        yaml.dump({'devices': devices}, f, default_flow_style=False, allow_unicode=True)

def mask_mac(mac):
    """Mask MAC address, showing only first and last segments."""
    if not mac:
        return 'N/A'
    parts = mac.upper().replace('-', ':').split(':')
    if len(parts) >= 2:
        return f"{parts[0]}:***:{parts[-1]}"
    return mac

def list_devices():
    """List all configured devices."""
    devices = load_devices()
    if not devices:
        print("No devices configured. Add one with: wol --add-device <name> <mac> <ip> <subnet_mask>")
        return []
    
    print("\n📋 Configured devices:")
    print("-" * 50)
    for name, info in devices.items():
        mac = info.get('mac', 'N/A')
        ip = info.get('ip', 'N/A')
        subnet = info.get('subnet_mask', 'N/A')
        masked_mac = mask_mac(mac)
        print(f"  • {name}")
        print(f"    MAC: {masked_mac}")
        print(f"    IP:  {ip}")
        print(f"    Subnet: {subnet}")
    print("-" * 50)
    return list(devices.keys())

def add_device(name, mac, ip, subnet_mask):
    """Add a new device or update existing one."""
    devices = load_devices()
    
    # Validate name
    if not name or not name.strip():
        print("✗ Error: Device name cannot be empty")
        return False
    
    # Validate IP (format and value)
    ip_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    if not ip or not re.match(ip_pattern, ip):
        print(f"✗ Invalid IP address format: {ip}")
        return False
    
    # Validate IP octets (each must be 0-255)
    ip_octets = [int(x) for x in ip.split('.')]
    if any(o > 255 for o in ip_octets):
        print(f"✗ Invalid IP address (octets must be 0-255): {ip}")
        return False
    
    # Validate subnet mask (format and value)
    if not subnet_mask or not re.match(ip_pattern, subnet_mask):
        print(f"✗ Invalid subnet mask format: {subnet_mask}")
        return False
    
    subnet_octets = [int(x) for x in subnet_mask.split('.')]
    if any(o > 255 for o in subnet_octets):
        print(f"✗ Invalid subnet mask (octets must be 0-255): {subnet_mask}")
        return False
    
    # Validate subnet mask is valid (must be contiguous 1s followed by 0s)
    # Convert to binary and check
    binary_mask = ''.join(f'{o:08b}' for o in subnet_octets)
    if '01' in binary_mask:  # Must not have 0 after 1
        print(f"✗ Invalid subnet mask (must be contiguous 1s followed by 0s): {subnet_mask}")
        return False
    
    # Validate MAC
    try:
        parse_mac(mac)
    except ValueError as e:
        print(f"✗ Invalid MAC address: {e}")
        return False
    
    # Check for duplicate name
    if name in devices:
        print(f"⚠ Warning: Device '{name}' already exists and will be overwritten")
    
    devices[name] = {
        'mac': mac.upper(),
        'ip': ip,
        'subnet_mask': subnet_mask
    }
    
    save_devices(devices)
    print(f"✓ Device '{name}' added: MAC={mac}, IP={ip}, Subnet={subnet_mask}")
    return True

def delete_device(name):
    """Delete a device."""
    devices = load_devices()
    
    # Try case-insensitive match
    target_lower = name.lower()
    found = None
    for dev_name in devices:
        if dev_name.lower() == target_lower:
            found = dev_name
            break
    
    if not found:
        print(f"✗ Device '{name}' not found")
        return False
    
    del devices[found]
    save_devices(devices)
    print(f"✓ Device '{found}' deleted")
    return True

def show_device(name):
    """Show details of a specific device."""
    devices = load_devices()
    
    # Try case-insensitive match
    target_lower = name.lower()
    found = None
    for dev_name in devices:
        if dev_name.lower() == target_lower:
            found = dev_name
            break
    
    if not found:
        print(f"✗ Device '{name}' not found")
        return None
    
    info = devices[found]
    masked_mac = mask_mac(info.get('mac', 'N/A'))
    print(f"\n📟 Device: {found}")
    print(f"   MAC: {masked_mac}")
    print(f"   IP:  {info.get('ip', 'N/A')}")
    print(f"   Subnet: {info.get('subnet_mask', 'N/A')}")
    return found

def get_mac_from_arp(ip):
    """Try to get MAC address from ARP cache."""
    try:
        result = subprocess.run(['arp', '-n', ip], capture_output=True, text=True)
        for line in result.stdout.split('\n'):
            if ip in line:
                # Format: address           ether (ethernet)   [ether] on en0
                parts = line.split()
                if len(parts) >= 3 and parts[1] == 'ether':
                    mac = parts[2].upper()
                    # Ensure MAC has colons
                    if '-' in mac:
                        mac = mac.replace('-', ':')
                    return mac
    except Exception:
        pass
    return None

def parse_mac(mac_str):
    """Parse MAC address string to bytes."""
    # Remove common separators and ensure uppercase
    mac = mac_str.replace('-', ':').replace('.', ':').upper()
    
    # Expand short formats like AA:BB:CC or AA:BB:CC:DD
    parts = mac.split(':')
    if len(parts) == 3:
        # AA:BB:CC -> AA:BB:CC:00:00:00
        mac = ':'.join(parts + ['00', '00', '00'])
    elif len(parts) == 4:
        # AA:BB:CC:DD -> AA:BB:CC:DD:00:00
        mac = ':'.join(parts + ['00', '00'])
    
    # Validate and convert
    mac_clean = mac.replace(':', '')
    if len(mac_clean) != 12:
        raise ValueError(f"Invalid MAC address: {mac_str}")
    
    return bytes.fromhex(mac_clean)

def calculate_broadcast(ip, subnet_mask):
    """Calculate broadcast address from IP and subnet mask."""
    try:
        ip_bytes = socket.inet_aton(ip)
        mask_bytes = socket.inet_aton(subnet_mask)
        # Broadcast = IP OR (NOT subnet mask)
        broadcast_bytes = bytes(a | (~b & 0xFF) for a, b in zip(ip_bytes, mask_bytes))
        return socket.inet_ntoa(broadcast_bytes)
    except Exception as e:
        print(f"Warning: Failed to calculate broadcast: {e}")
        return '255.255.255.255'  # Fallback

def create_magic_packet(mac_bytes):
    """Create a Wake-on-LAN magic packet."""
    # Magic packet: 6 bytes of 0xFF followed by MAC address repeated 16 times
    return b'\xFF' * 6 + mac_bytes * 16

def send_wol(mac_address, broadcast='255.255.255.255'):
    """Send Wake-on-LAN magic packet."""
    mac_bytes = parse_mac(mac_address)
    packet = create_magic_packet(mac_bytes)
    
    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    
    try:
        sock.sendto(packet, (broadcast, WOL_PORT))
        print(f"✓ Magic packet sent to {mac_address}")
        return True
    except Exception as e:
        print(f"✗ Failed to send packet: {e}")
        return False
    finally:
        sock.close()

def resolve_target(target):
    """Resolve target (name or IP) to MAC, subnet mask, and IP."""
    devices = load_devices()
    
    # Check if it's an IP address
    ip_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    if re.match(ip_pattern, target):
        # It's an IP - try to find in devices first
        for name, info in devices.items():
            if info.get('ip') == target:
                mac = info.get('mac')
                subnet = info.get('subnet_mask')
                print(f"Found {target} in devices as '{name}': {mac}")
                return mac, subnet, target
        
        # Try ARP lookup
        mac = get_mac_from_arp(target)
        if mac:
            print(f"Found {target} in ARP cache: {mac}")
            return mac, None, target  # No subnet info from ARP
        
        # If no MAC found, use broadcast (will work if device is on same subnet)
        print(f"Warning: Could not find MAC for {target}, using broadcast")
        return None, None, None
    
    # It's a device name - lookup in devices
    if target in devices:
        info = devices[target]
        return info.get('mac'), info.get('subnet_mask'), info.get('ip')
    
    # Try case-insensitive match
    target_lower = target.lower()
    for name, info in devices.items():
        if name.lower() == target_lower:
            return info.get('mac'), info.get('subnet_mask'), info.get('ip')
    
    raise ValueError(f"Unknown device: {target}. Add it to {DEVICES_FILE}")

def main():
    parser = argparse.ArgumentParser(description='Wake-on-LAN utility')
    parser.add_argument('--target', help='Device name or IP address to wake')
    parser.add_argument('--broadcast', default='255.255.255.255', 
                        help='Broadcast address (default: 255.255.255.255)')
    
    # Device management arguments
    parser.add_argument('--list-devices', action='store_true', help='List all configured devices')
    parser.add_argument('--add-device', nargs='+', 
                        help='Add a new device: NAME MAC IP SUBNET_MASK')
    parser.add_argument('--delete-device', metavar='NAME', 
                        help='Delete a device by name')
    parser.add_argument('--show-device', metavar='NAME', 
                        help='Show details of a specific device')
    
    args = parser.parse_args()
    
    # Handle device management commands
    if args.list_devices:
        list_devices()
        return
    
    if args.add_device:
        if len(args.add_device) != 4:
            print("✗ Error: --add-device requires exactly 4 arguments: NAME MAC IP SUBNET_MASK")
            print("   Usage: wol --add-device <name> <mac> <ip> <subnet_mask>")
            print("   Example: wol --add-device desktop AA:BB:CC:DD:EE:FF 192.168.1.100 255.255.255.0")
            exit(1)
        name = args.add_device[0]
        mac = args.add_device[1]
        ip = args.add_device[2]
        subnet = args.add_device[3]
        add_device(name, mac, ip, subnet)
        return
    
    if args.delete_device:
        delete_device(args.delete_device)
        return
    
    if args.show_device:
        show_device(args.show_device)
        return
    
    # Default: wake target
    if not args.target:
        parser.print_help()
        print("\n💡 Quick commands:")
        print("   wol --list-devices                    # List all devices")
        print("   wol --add-device <name> <mac> <ip> <subnet>  # Add device (required)")
        print("   wol --delete-device <name>            # Delete device")
        print("   wol --show-device <name>              # Show device details")
        print("   wol --target <name|ip>                # Wake a device")
        print("\n📝 Example: wol --add-device desktop AA:BB:CC:DD:EE:FF 192.168.1.100 255.255.255.0")
        return
    
    try:
        mac, subnet, target_ip = resolve_target(args.target)
        if mac:
            # Calculate broadcast address if subnet provided
            broadcast = args.broadcast
            if subnet and target_ip:
                broadcast = calculate_broadcast(target_ip, subnet)
                print(f"Using calculated broadcast: {broadcast}")
            
            send_wol(mac, broadcast)
        else:
            # Send to broadcast anyway (may work on local subnet)
            print(f"Sending broadcast WOL packet to {args.broadcast}...")
            send_wol('FF:FF:FF:FF:FF:FF', args.broadcast)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

if __name__ == '__main__':
    main()
