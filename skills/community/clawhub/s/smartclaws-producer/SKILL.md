---
name: smartclaws-producer
description: >
  Set up IoT sensors and publish data to SKALE blockchain via SmartClaws.
  Use when: setting up smartclaws, registering devices, connecting sensors,
  publishing temperature/humidity/IoT measurements, writing sensor scripts.
metadata:
  openclaw:
    emoji: "\U0001F4E1"
    homepage: https://github.com/skalenetwork/smartclaws
    requires:
      bins: ["python3"]
      anyBins: ["curl", "wget"]
---

# SmartClaws Producer

Publish IoT sensor data to the SKALE blockchain using the SmartClaws protocol. This skill handles the full producer pipeline: installing the CLI, initializing a wallet, registering devices, writing sensor-reading scripts, and publishing data on-chain.

## Real Hardware Rule

When the user asks to set up a sensor or publish real-world measurements, assume they mean a real hardware device unless they explicitly say they want a simulation, mock, or pipeline test.

Before writing any publisher script, first determine:

* the exact sensor model / part number
* how it connects to the host (BLE, USB serial, Wi-Fi, MQTT, GPIO/I2C/SPI, etc.)
* whether pairing or driver setup is required
* what library, CLI, or protocol is needed to read the sensor

If the exact sensor model or connection method is unknown, ask the user before proceeding.

Do not generate fake/mock sensor data for a real setup request.
Only use a mock publisher when the user explicitly requests testing, simulation, or pipeline validation without real hardware.

## Installation

Check if the CLI is available:

```bash
smartclaws --version
```

If not installed, download the binary for the current platform:

```bash
PLATFORM="$(uname -s | tr '[:upper:]' '[:lower:]')-$(uname -m | sed 's/aarch64/arm64/')"
curl -fL -o /usr/local/bin/smartclaws \
  "https://github.com/skalenetwork/smartclaws/releases/latest/download/smartclaws-${PLATFORM}"
chmod +x /usr/local/bin/smartclaws
```

If `/usr/local/bin` requires root, use `~/.local/bin/smartclaws` instead and ensure it's on PATH.

Verify: `smartclaws --version` should print the version number.

## Setup

### 1. Initialize

```bash
smartclaws init
```

This creates `~/.smartclaws/` with config and a wallet. Expected output:

```
Config created at ~/.smartclaws/config.json
  Network:   SKALE Sandbox
  RPC URL:   https://base-sepolia-testnet.skalenodes.com/v1/vigilant-snappy-arcturus
  Chain ID:  196243392
  Contract:  0x18B62f70ddaA2666FA5933a7b6Ff3943e69ca690
  Wallet:    0xAbC123... (generated)
```

If config already exists, it prints the current config without overwriting.

### 2. Show wallet address and fund it

After init, show the wallet address to the user:

```bash
smartclaws wallet info
```

Expected output:

```
Address: 0xAbC123...
Balance: 0 sFUEL
```

**Important:** The user must fund this wallet with sFUEL before proceeding. Show the wallet address to the user and ask them to fund it (e.g., via the SKALE faucet or by transferring sFUEL from another wallet). Registration and publishing will fail without sFUEL.

Wait for the user to confirm the wallet is funded, then verify:

```bash
smartclaws wallet info
```

The balance should now be greater than 0.

### 3. Register device group

```bash
smartclaws register
```

Creates a device group on-chain (one per machine). Requires a funded wallet. Expected output:

```
Registering device group 'swift-falcon'...
Device group registered:
  Name:     swift-falcon
  Address:  0xDEF456...
  Tx:       0x789...
```

This only needs to run once. Subsequent calls fail with: `Device group already registered: 0x...`

### 3. Check wallet

```bash
smartclaws wallet info
```

Shows wallet address and sFUEL balance. SKALE testnet transactions are zero-gas, but a small sFUEL balance is needed.

## Device Registration

Register a device to get dedicated on-chain channels:

```bash
smartclaws device register --name <device-name>
```

Choose a descriptive name (e.g., `temp-sensor`, `humidity-monitor`). Expected output:

```
Registering device 'temp-sensor'...
Device registered:
  Name:      temp-sensor
  Contract:  0x111...
  Outgoing:  0x222...
  Incoming:  0x333...
  Tx:        0x444...
```

**Important:** Save the `Outgoing` channel address. The reader on another machine will need it to access this device's data.

List registered devices: `smartclaws device list`

## Writing Sensor Scripts

Before writing a publisher script:

1. Identify the exact sensor model and connection type.
2. If the model or protocol is missing, ask the user.
3. Look up the sensor's pairing / reading instructions.
4. Determine the required Python package, system dependency, permissions, and read method.
5. Only then write a hardware-specific publisher script.

Never substitute mock data unless the user explicitly asks for a simulation or test publisher.

When the user has provided their sensor details, write a Python script that:

1. Imports the appropriate sensor library (install with pip if needed)
2. Reads sensor data in a function
3. Calls `smartclaws publish` via subprocess in a loop
4. Handles errors with retry logic

Save scripts to `~/.smartclaws/scripts/<device-name>-publisher.py`.

### Script Structure

Every publisher script follows this pattern:

```python
#!/usr/bin/env python3
"""Publish <sensor-type> readings to SmartClaws."""

import json
import subprocess
import sys
import time

SMARTCLAWS = "smartclaws"
DEVICE = "<device-name>"
TOPIC = "<topic>"
INTERVAL = 30  # seconds


def read_sensor():
    """Read sensor and return payload dict."""
    # --- sensor-specific code here ---
    return {"temp": 22.5, "humidity": 55}


def publish(payload):
    result = subprocess.run(
        [SMARTCLAWS, "publish", "--device", DEVICE, "--topic", TOPIC,
         "--data", json.dumps(payload)],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"publish error: {result.stderr.strip()}", file=sys.stderr)
        return False
    return True


def main():
    print(f"Publishing {TOPIC} every {INTERVAL}s for device '{DEVICE}'")
    while True:
        try:
            payload = read_sensor()
            publish(payload)
            print(f"  {payload}")
        except Exception as e:
            print(f"read error: {e}", file=sys.stderr)
        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
```

### Example: BLE Temperature Sensor (Xiaomi LYWSD03MMC)

Requires: `pip install bleak`

The read\_sensor function uses BLE GATT characteristic `ebe0ccc1-7a0a-4b0c-8a1a-6ff2997da3a6`. The data bytes decode as:

* bytes 0-1: temperature (little-endian signed int16, divide by 100)
* byte 2: humidity (uint8, percentage)
* bytes 3-4: voltage (little-endian uint16, divide by 1000)

See the full working example at `examples/ble-publisher.py` bundled with this skill.

## If the User Says "Set Up a Temperature Sensor"

Do not assume a mock sensor. Ask a short clarifying question such as:

* "What's the exact sensor model?"
* "How does it connect to this machine: BLE, USB, Wi-Fi, or GPIO/I2C?"

Only after receiving the hardware details should you write the publisher script.

If the user explicitly says they want a mock/test/simulated sensor, then use the mock publisher above.

## Common Mistake to Avoid

**Wrong:** User asks to set up a real sensor, and the agent immediately creates a fake/mock publisher with simulated data.

**Right:** Ask for the sensor model and connection method first, then write a hardware-specific publisher.

## Publishing Data

Single publish command:

```bash
smartclaws publish --device <name> --topic <topic> --data '{"temp": 22.5}'
```

Expected output:

```
Published to temp-sensor/temperature
  Tx:     0x555...
  Status: success
```

Every message is wrapped in a SmartClaws envelope:

```json
{
  "v": 1,
  "ts": 1711324800,
  "dev": "temp-sensor",
  "topic": "temperature",
  "p": {"temp": 22.5}
}
```

The CLI handles envelope encoding, wallet signing, and on-chain submission automatically.

## Running as a Service

For persistent publishing, create a systemd user service:

```bash
mkdir -p ~/.config/systemd/user

cat > ~/.config/systemd/user/smartclaws-<device-name>.service << 'EOF'
[Unit]
Description=SmartClaws publisher for <device-name>

[Service]
ExecStart=/usr/bin/python3 %h/.smartclaws/scripts/<device-name>-publisher.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=default.target
EOF

systemctl --user daemon-reload
systemctl --user enable --now smartclaws-<device-name>
```

Check status: `systemctl --user status smartclaws-<device-name>`
View logs: `journalctl --user -u smartclaws-<device-name> -f`
Stop: `systemctl --user stop smartclaws-<device-name>`

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `Not initialized. Run 'smartclaws init' first.` | No ~/.smartclaws/config.json | Run `smartclaws init` |
| `No device group registered.` | Haven't registered yet | Run `smartclaws register` |
| `Device 'X' is already registered.` | Duplicate name | Use a different name or check `smartclaws device list` |
| `Device 'X' not found.` | Wrong device name for publish | Check `smartclaws device list` |
| `Invalid JSON payload.` | Malformed --data argument | Ensure valid JSON, e.g. `'{"temp": 22.5}'` |
| BLE permission denied | Linux BLE requires capabilities | `sudo setcap cap_net_raw+eip $(which python3)` |
| BLE connection timeout | Sensor out of range or asleep | Move closer, retry. BLE range is ~10m |
