#!/usr/bin/env python3
"""Publish simulated temperature data to SmartClaws for testing without hardware."""

import json
import math
import random
import subprocess
import sys
import time

SMARTCLAWS = "smartclaws"
DEVICE = "mock-sensor"
TOPIC = "sensor"
INTERVAL = 10  # seconds

# Simulation parameters
BASE_TEMP = 22.0  # base temperature in Celsius
AMPLITUDE = 3.0  # sine wave amplitude
PERIOD = 600  # full cycle in seconds (10 minutes)
NOISE = 0.3  # random noise amplitude
BASE_HUMIDITY = 55  # base humidity percentage


def read_sensor():
    """Generate simulated temperature and humidity readings."""
    t = time.time()
    temp = BASE_TEMP + AMPLITUDE * math.sin(2 * math.pi * t / PERIOD)
    temp += random.uniform(-NOISE, NOISE)
    humidity = BASE_HUMIDITY + random.randint(-5, 5)
    return {"temp": round(temp, 2), "humidity": humidity}


def publish(payload):
    result = subprocess.run(
        [
            SMARTCLAWS, "publish",
            "--device", DEVICE,
            "--topic", TOPIC,
            "--data", json.dumps(payload),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"publish error: {result.stderr.strip()}", file=sys.stderr)
        return False
    return True


def main():
    print(f"Mock publisher: {TOPIC} every {INTERVAL}s for device '{DEVICE}'")
    print(f"Simulating: {BASE_TEMP}C +/- {AMPLITUDE}C sine wave, period {PERIOD}s\n")
    while True:
        try:
            payload = read_sensor()
            ok = publish(payload)
            status = "ok" if ok else "FAILED"
            print(f"  [{status}] temp={payload['temp']}C humidity={payload['humidity']}%")
        except KeyboardInterrupt:
            print("\nStopped.")
            break
        except Exception as e:
            print(f"error: {e}", file=sys.stderr)
        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
