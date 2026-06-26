#!/usr/bin/env python3
"""Read Xiaomi LYWSD03MMC BLE sensor and publish readings via SmartClaws CLI.

Requirements: pip install bleak

Usage:
    python3 ble-publisher.py --address <BLE-MAC-or-UUID> --device <smartclaws-device-name>

To find your sensor's BLE address, run:
    python3 -c "import asyncio; from bleak import BleakScanner; asyncio.run(BleakScanner.discover())"
    # Look for devices named "LYWSD03MMC"
"""

import argparse
import asyncio
import json
import subprocess
import sys
from datetime import datetime, timezone

from bleak import BleakClient

# Xiaomi LYWSD03MMC temperature/humidity GATT characteristic
DATA_CHAR = "ebe0ccc1-7a0a-4b0c-8a1a-6ff2997da3a6"

SMARTCLAWS = "smartclaws"


def parse_reading(data: bytes) -> dict:
    """Parse raw BLE data into temperature, humidity, and voltage."""
    temp = int.from_bytes(data[0:2], "little", signed=True) / 100
    humidity = data[2]
    voltage = int.from_bytes(data[3:5], "little") / 1000
    return {"temp": temp, "humidity": humidity, "voltage": voltage}


def publish(device: str, topic: str, payload: dict) -> bool:
    """Publish a reading to SmartClaws via CLI."""
    result = subprocess.run(
        [
            SMARTCLAWS, "publish",
            "--device", device,
            "--topic", topic,
            "--data", json.dumps(payload),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"  publish error: {result.stderr.strip()}", file=sys.stderr)
        return False
    for line in result.stdout.strip().splitlines():
        print(f"  {line}")
    return True


async def run(address: str, device: str, interval: float, max_retries: int):
    retries = 0
    while True:
        try:
            print(f"Connecting to {address}...")
            async with BleakClient(address) as client:
                print(f"Connected. Reading every {interval}s, publishing to '{device}'.\n")
                retries = 0
                while True:
                    data = await client.read_gatt_char(DATA_CHAR)
                    reading = parse_reading(data)
                    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
                    print(f"[{ts}] {reading['temp']}C / {reading['humidity']}% / {reading['voltage']}V")
                    publish(device, "sensor", reading)
                    if interval <= 0:
                        break
                    await asyncio.sleep(interval)
            if interval <= 0:
                break
        except KeyboardInterrupt:
            print("\nStopped.")
            break
        except Exception as e:
            retries += 1
            if 0 < max_retries < retries:
                print(f"Max retries ({max_retries}) exceeded. Exiting.", file=sys.stderr)
                sys.exit(1)
            wait = min(retries * 5, 30)
            print(f"BLE error: {e}. Reconnecting in {wait}s... (retry {retries})", file=sys.stderr)
            await asyncio.sleep(wait)


def main():
    parser = argparse.ArgumentParser(description="Read BLE sensor and publish to SmartClaws")
    parser.add_argument("--address", required=True, help="BLE device address (MAC or UUID)")
    parser.add_argument("--device", required=True, help="SmartClaws device name")
    parser.add_argument("--interval", type=float, default=60, help="Seconds between readings (0 = single read)")
    parser.add_argument("--max-retries", type=int, default=0, help="Max BLE reconnect retries (0 = unlimited)")
    args = parser.parse_args()
    asyncio.run(run(args.address, args.device, args.interval, args.max_retries))


if __name__ == "__main__":
    main()
