---
name: USB Light Sensor Reader
slug: usb-light-sensor-reader
version: 1.0.2
description: Read light intensity from USB sensors with real-time monitoring, filtering, and threshold detection.
metadata: {"clawdbot":{"emoji":"☀️","requires":{"bins":["python3"]},"os":["linux"]}}
---

## When to Use

User wants to read light intensity (lux) from USB-connected light sensor or check ambient light levels.

## Core Rules

1. **Verify Hardware First** — Confirm sensor is at `/dev/ttyUSB0` and user is in `dialout` group.

2. **Always Initialize** — Call `sensor.connect()` before reading. Waits 1s for warmup.

3. **Use Filtered Data** — `read_lux()` returns 5-sample moving average. Use `read_raw()` for unfiltered values.

4. **Default Thresholds** — Dark: < 100 lux, Bright: > 500 lux. Adjust based on environment.

5. **Disconnect on Exit** — Always call `sensor.disconnect()` to release serial port.

## Data Storage

No persistent storage. Sensor data read in real-time from serial port.

## External Endpoints

| Endpoint | Purpose |
|----------|---------|
| `/dev/ttyUSB0` | Serial read |

## Quick Reference

| Topic | File |
|-------|------|
| Setup & examples | `setup.md` |
| Troubleshooting | `setup.md` |

## Security Notes

- Declares external hardware dependency (USB sensor)
- No network access or environment variables required
