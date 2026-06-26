---
name: smartclaws-reader
description: >
  Read and analyze IoT sensor data from SKALE blockchain via SmartClaws.
  Use when: querying sensor readings, asking about temperature or other
  measurements, analyzing trends, checking thresholds, reading on-chain IoT data.
metadata:
  openclaw:
    emoji: "\U0001F4CA"
    homepage: https://github.com/skalenetwork/smartclaws
    requires:
      anyBins: ["curl", "wget"]
---

# SmartClaws Reader

Read and analyze IoT sensor data published to the SKALE blockchain via the SmartClaws protocol. This skill handles reading on-chain data, parsing sensor readings, and answering natural-language questions about measurements.

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

## Setup

Initialize the CLI (creates config and wallet):

```bash
smartclaws init
```

Expected output:

```
Config created at ~/.smartclaws/config.json
  Network:   SKALE Sandbox
  RPC URL:   https://base-sepolia-testnet.skalenodes.com/v1/vigilant-snappy-arcturus
  Chain ID:  196243392
  Contract:  0x18B62f70ddaA2666FA5933a7b6Ff3943e69ca690
  Wallet:    0xAbC123... (generated)
```

After init, show the wallet address to the user:

```bash
smartclaws wallet info
```

The reader machine does not need to run `smartclaws register` — it only reads data, it doesn't own devices. The wallet does not need sFUEL for read-only operations.

## Channel Address

To read data, you need the **channel address** from the producer. This is the `Outgoing` address printed when the producer registered the device. Ask the user for this address if not already known.

Example channel address: `0x222333444555666777888999AAABBBCCCDDDEEEF`

## Reading Data

### Latest reading

```bash
smartclaws read --channel <address> --limit 1 --json
```

### Multiple recent readings

```bash
smartclaws read --channel <address> --limit 20 --json
```

### Read from specific offset

```bash
smartclaws read --channel <address> --offset 5 --limit 10 --json
```

### Human-readable output (no --json)

```bash
smartclaws read --channel <address> --limit 5
```

Outputs:

```
Messages: 42 total (offsets 0..41)
Reading: 37..41

[37] 2026-03-28T10:00:00.000Z temp-sensor/temperature {"temp":22.1,"humidity":55}
[38] 2026-03-28T10:00:30.000Z temp-sensor/temperature {"temp":22.3,"humidity":54}
[39] 2026-03-28T10:01:00.000Z temp-sensor/temperature {"temp":22.5,"humidity":54}
[40] 2026-03-28T10:01:30.000Z temp-sensor/temperature {"temp":22.4,"humidity":55}
[41] 2026-03-28T10:02:00.000Z temp-sensor/temperature {"temp":22.6,"humidity":53}
```

## JSON Output Schema

When using `--json`, the output structure is:

```json
{
  "device": null,
  "channel": "0x222...",
  "total": 42,
  "oldest": 0,
  "latest": 41,
  "messages": [
    {
      "offset": 41,
      "v": 1,
      "ts": 1711612920,
      "dev": "temp-sensor",
      "topic": "temperature",
      "p": {
        "temp": 22.6,
        "humidity": 53
      }
    }
  ]
}
```

Field reference:

* `device`: device name (null when using --channel instead of --device)
* `channel`: the on-chain channel address
* `total`: total number of messages in the channel
* `oldest` / `latest`: offset range of available messages
* `messages[].v`: envelope version (always 1)
* `messages[].ts`: Unix timestamp in seconds
* `messages[].dev`: device name set by the producer
* `messages[].topic`: message topic (e.g., "temperature", "sensor")
* `messages[].p`: the payload object with sensor values

## Data Truthfulness

When answering questions about sensor readings, do not imply that test/mock data is real device data. If the producer was configured with a mock/test publisher, be explicit that the readings are simulated.

## Answering Data Questions

### "What's the current temperature?"

```bash
smartclaws read --channel <address> --limit 1 --json
```

Parse the output, extract `messages[0].p.temp` (or the relevant field). Report the value and convert `messages[0].ts` to a human-readable timestamp.

Example response: "The current temperature is 22.6C, recorded at 10:02 AM UTC."

### "What was the average temperature today / in the last N hours?"

```bash
smartclaws read --channel <address> --limit 200 --json
```

Read a large batch, then filter by timestamp and compute the mean:

```python
import json, subprocess, time

result = subprocess.run(
    ["smartclaws", "read", "--channel", "<address>", "--limit", "200", "--json"],
    capture_output=True, text=True
)
data = json.loads(result.stdout)

cutoff = time.time() - 3600  # last hour
temps = [m["p"]["temp"] for m in data["messages"] if m["ts"] >= cutoff]

if temps:
    avg = sum(temps) / len(temps)
    print(f"Average: {avg:.1f}C over {len(temps)} readings")
else:
    print("No readings in the requested period")
```

### "Has the temperature gone above X?"

Read recent messages and check for threshold crossings:

```python
threshold = 28.0
above = [m for m in data["messages"] if m["p"]["temp"] > threshold]
if above:
    peak = max(above, key=lambda m: m["p"]["temp"])
    print(f"Yes, reached {peak['p']['temp']}C at {peak['ts']}")
else:
    print(f"No, all readings are at or below {threshold}C")
```

### "Show the trend" / "Describe what's happening"

Read a window of data and compute basic statistics:

```python
temps = [m["p"]["temp"] for m in data["messages"]]
if len(temps) >= 2:
    direction = "rising" if temps[-1] > temps[0] else "falling" if temps[-1] < temps[0] else "stable"
    print(f"Trend: {direction}")
    print(f"  Min: {min(temps):.1f}C, Max: {max(temps):.1f}C, Avg: {sum(temps)/len(temps):.1f}C")
    print(f"  From {temps[0]:.1f}C to {temps[-1]:.1f}C over {len(temps)} readings")
```

## Multiple Sensors

If the channel carries data from multiple devices or topics, filter by the `dev` and `topic` fields in the envelope before analysis:

```python
# Filter for a specific device
sensor_data = [m for m in data["messages"] if m["dev"] == "temp-sensor"]

# Filter for a specific topic
temp_data = [m for m in data["messages"] if m["topic"] == "temperature"]
```

## Reading from a Local Device

If the device was registered on this machine (both producer and reader on same machine), you can use `--device` instead of `--channel`:

```bash
smartclaws read --device temp-sensor --limit 1 --json
```

This looks up the channel address from `~/.smartclaws/devices/temp-sensor.json` automatically.

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `Not initialized. Run 'smartclaws init' first.` | No config | Run `smartclaws init` |
| `Provide --device or --channel.` | Neither flag given | Add `--channel <addr>` or `--device <name>` |
| `No messages.` | Channel is empty | Producer hasn't published yet, or wrong channel |
| Contract revert on read | Invalid channel address | Verify the address with the producer |
| RPC connection error | Network issue | Check internet connection; verify RPC URL in config |
