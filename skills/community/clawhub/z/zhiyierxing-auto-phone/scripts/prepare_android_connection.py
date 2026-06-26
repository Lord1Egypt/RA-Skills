#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from device_memory import adb_devices, find_preferred_connected_device, get_known_wifi_targets, remember_device


def run(cmd: list[str], timeout: int = 10) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)


def adb_connect(address: str) -> tuple[bool, str]:
    if ':' not in address:
        address = f'{address}:5555'
    result = run(['adb', 'connect', address])
    output = (result.stdout or '') + (result.stderr or '')
    lower = output.lower()
    if 'connected' in lower or 'already connected' in lower:
        return True, output.strip() or f'connected to {address}'
    return False, output.strip() or f'failed to connect to {address}'


def adb_tcpip(device_id: str, port: int = 5555) -> tuple[bool, str]:
    result = run(['adb', '-s', device_id, 'tcpip', str(port)])
    output = (result.stdout or '') + (result.stderr or '')
    lower = output.lower()
    if result.returncode == 0 or 'restarting' in lower:
        return True, output.strip() or f'tcpip enabled on {device_id}:{port}'
    return False, output.strip() or f'failed to enable tcpip on {device_id}'


def adb_get_device_ip(device_id: str) -> str | None:
    for cmd in (
        ['adb', '-s', device_id, 'shell', 'ip', 'route'],
        ['adb', '-s', device_id, 'shell', 'ip', 'addr', 'show', 'wlan0'],
    ):
        result = run(cmd, timeout=5)
        for line in (result.stdout or '').splitlines():
            if ' src ' in line:
                parts = line.split()
                for i, part in enumerate(parts):
                    if part == 'src' and i + 1 < len(parts):
                        return parts[i + 1]
            if 'inet ' in line:
                parts = line.strip().split()
                if len(parts) >= 2 and '/' in parts[1]:
                    return parts[1].split('/')[0]
    return None


def main() -> int:
    current = adb_devices()

    preferred = find_preferred_connected_device()
    if preferred:
        print(f'[device-memory] preferred connected device found: {preferred}')
        remember_device(preferred, source='connected')
        return 0

    for target in get_known_wifi_targets():
        ok, msg = adb_connect(target)
        print(f'[wifi-reuse] {msg}')
        if ok:
            remember_device(target, wifi_address=target, source='wifi-reconnect')
            return 0

    usb_devices = [d for d in current if ':' not in d]
    for device_id in usb_devices:
        ip = adb_get_device_ip(device_id)
        if not ip:
            continue
        ok, msg = adb_tcpip(device_id, 5555)
        print(f'[wifi-prepare] {device_id}: {msg}')
        if not ok:
            continue
        target = f'{ip}:5555'
        ok2, msg2 = adb_connect(target)
        print(f'[wifi-connect] {target}: {msg2}')
        if ok2:
            remember_device(device_id, wifi_address=target, source='usb-to-wifi')
            remember_device(target, wifi_address=target, source='usb-to-wifi')
            return 0
        remember_device(device_id, wifi_address=target, source='usb-ip-known')

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
