#!/usr/bin/env python3
"""Test script for Tuya Cloud skill."""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Load private device IDs from test_data.env in the same folder
_TEST_DIR = Path(__file__).resolve().parent
load_dotenv(dotenv_path=_TEST_DIR / "test_data.env")

SENSOR_DEVICE_ID = os.environ["SENSOR_DEVICE_ID"]

# Add scripts directory to path (skill is self-contained, no tuya_agent)
sys.path.insert(0, str(_TEST_DIR.parent / 'scripts'))

from tuya_controller import (
    load_tuya_client,
    get_device_status,
    get_device_info,
    list_all_devices,
    parse_sensor_data,
    format_device_status,
)


def test_connection():
    """Test connection to Tuya API."""
    print("Testing connection to Tuya API...")
    try:
        client = load_tuya_client()
        print("✅ Connection successful")
        return client
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return None


def test_list_devices(client):
    """Test listing devices."""
    print("\nTesting device list...")
    try:
        devices = list_all_devices(client)
        print(f"✅ Found {len(devices)} device(s)")
        for device in devices:
            print(f"   - {device.get('name')} ({device.get('id')})")
        return devices
    except Exception as e:
        print(f"❌ Failed to list devices: {e}")
        return []


def test_device_status(client, device_id):
    """Test getting device status."""
    print(f"\nTesting device status for {device_id}...")
    try:
        # Get device info
        info = get_device_info(client, device_id)
        print(f"✅ Device info retrieved: {info.get('name')}")
        print(info)

        # Get device status
        status = get_device_status(client, device_id)
        print(f"✅ Device status retrieved")

        # Parse sensor data
        parsed = parse_sensor_data(status)  # no sensor_type filter; returns all fields
        print(f"✅ Sensor data parsed: {len(parsed)} fields")

        # Format output
        formatted = format_device_status(device_id, info, status, parsed, 'text')
        print("\n" + "=" * 50)
        print(formatted)
        print("=" * 50)

        return True
    except Exception as e:
        print(f"❌ Failed to get device status: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 50)
    print("Tuya Cloud Skill Test Suite")
    print("=" * 50)

    # Test 1: Connection
    client = test_connection()
    if not client:
        print("\n❌ Test suite failed: Cannot connect to Tuya API")
        sys.exit(1)

    # Test 2: List devices
    devices = test_list_devices(client)

    # Test 3: Device status
    test_device_id = SENSOR_DEVICE_ID

    if devices and not any(d.get('id') == test_device_id for d in devices):
        print(f"\n⚠️  Device {test_device_id} not found in device list")
        if devices:
            test_device_id = devices[0].get('id')
            print(f"   Using first available device: {test_device_id}")

    if test_device_id:
        test_device_status(client, test_device_id)

    print("\n" + "=" * 50)
    print("✅ Test suite completed")
    print("=" * 50)


if __name__ == '__main__':
    main()