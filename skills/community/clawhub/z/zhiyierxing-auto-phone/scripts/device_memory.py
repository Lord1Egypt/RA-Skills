#!/usr/bin/env python3
import json
import os
import subprocess
from pathlib import Path

MEMORY_PATH = Path(os.path.expanduser('~/.openclaw/workspace/.device-memory/zhiyierxing-auto-phone.json'))


def ensure_parent() -> None:
    MEMORY_PATH.parent.mkdir(parents=True, exist_ok=True)


def load_memory() -> dict:
    if MEMORY_PATH.exists():
        try:
            return json.loads(MEMORY_PATH.read_text(encoding='utf-8'))
        except Exception:
            return {}
    return {}


def save_memory(data: dict) -> None:
    ensure_parent()
    MEMORY_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')


def adb_devices() -> list[str]:
    try:
        result = subprocess.run(['adb', 'devices'], capture_output=True, text=True, timeout=5)
        lines = [line.strip() for line in result.stdout.splitlines()[1:] if line.strip()]
        return [line.split()[0] for line in lines if len(line.split()) >= 2 and line.split()[1] == 'device']
    except Exception:
        return []


def remember_device(device_id: str, wifi_address: str | None = None, source: str | None = None) -> None:
    data = load_memory()
    devices = data.get('devices', {})
    entry = devices.get(device_id, {})
    entry['device_id'] = device_id
    if wifi_address:
        entry['wifi_address'] = wifi_address
    if source:
        entry['last_seen_source'] = source
    entry['last_seen_connected'] = True
    devices[device_id] = entry
    data['devices'] = devices
    data['last_device_id'] = device_id
    save_memory(data)


def find_preferred_connected_device() -> str | None:
    data = load_memory()
    connected = set(adb_devices())
    last_device_id = data.get('last_device_id')
    if last_device_id and last_device_id in connected:
        return last_device_id

    devices = data.get('devices', {})
    for key, value in devices.items():
        device_id = value.get('device_id') or key
        wifi_address = value.get('wifi_address')
        if device_id in connected:
            return device_id
        if wifi_address and wifi_address in connected:
            return wifi_address
    return None


def get_known_wifi_targets() -> list[str]:
    data = load_memory()
    devices = data.get('devices', {})
    targets = []
    for key, value in devices.items():
        wifi_address = value.get('wifi_address')
        if wifi_address:
            targets.append(wifi_address)
    return list(dict.fromkeys(targets))
