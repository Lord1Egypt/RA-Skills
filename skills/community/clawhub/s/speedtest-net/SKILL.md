---
name: speedtest-net
description: >
  Measure internet network speed (download, upload, ping) using speedtest-cli (Speedtest.net).
  Use when: user asks to "check speed", "run speedtest", "test network speed",
  "measure bandwidth", "check internet speed", or any request to test/download/upload
  speed of the host connection. Requires speedtest-cli pre-installed (see setup.md).
---

# Speedtest.net

## Quick Usage

```bash
python3 scripts/speedtest.py [--json] [--server SERVER_ID] [--timeout SECONDS]
```

### Flags

| Flag | Default | Description |
|------|---------|-------------|
| `--json` | off | Output raw JSON (download/upload/ping + server info) |
| `--server` | auto | Force a specific Speedtest server ID |
| `--timeout` | 120 | Max seconds to wait for the test |

### Plain text output (default)

```
Ping: 45.12 ms
Download: 120.45 Mbit/s
Upload: 25.33 Mbit/s
```

### JSON output (`--json`)

Returns structured data including server name/location, ISP, and IP.

## Prerequisites

`speedtest-cli` must be installed before using this skill. See **[setup.md](setup.md)** for installation instructions.

If the script reports `speedtest-cli not found`, do **not** attempt automatic installation — direct the user to setup.md and let them install it manually.

## Notes

- Tests connect to the nearest Ookla/Speedtest server by default.
- Results vary by server distance, network congestion, and host resources.
- For repeated monitoring, schedule via cron with JSON output and log results.
