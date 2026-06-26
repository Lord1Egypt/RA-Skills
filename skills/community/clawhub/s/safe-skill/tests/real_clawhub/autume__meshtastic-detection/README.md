# meshtastic-detection

Meshtastic Detection Sensor alert receiver via LoRa -- USB serial, local JSONL storage, feishu notifications.

## Overview

An OpenClaw skill that connects to a Meshtastic LoRa device via USB to receive `DETECTION_SENSOR_APP` events from a remote sensor node. When the remote device's GPIO pin triggers (preset target detected), the event is stored locally and an alert is sent to feishu.

- **Receive** `DETECTION_SENSOR_APP` events over LoRa mesh (GPIO trigger)
- **Store** to local JSONL files (no database required)
- **Alert** immediately via feishu through OpenClaw cron
- **Query** through OpenClaw conversation or CLI

## Supported Platforms

| Platform | Serial port pattern | Service manager |
|----------|-------------------|-----------------|
| macOS | `/dev/cu.usbmodem*` | launchd (plist) |
| Linux x86/arm | `/dev/ttyUSB*`, `/dev/ttyACM*` | systemd |
| Raspberry Pi | `/dev/ttyUSB*`, `/dev/ttyACM*` | systemd |
| Docker | `/dev/ttyUSB*`, `/dev/ttyACM*` | entrypoint.sh + `nohup` / container CMD |

`setup.sh` auto-detects your platform (including Docker) and handles all differences.

## Architecture

```
Remote Sensor Device              Host Machine (macOS/Linux/RPi)
[GPIO Detection Sensor]           [Meshtastic Module via USB]
        |                                  |
        | LoRa radio                  usb_receiver.py (daemon)
        |                                  |
        └──────────────────────────────────┘
                                           |
                                    data/sensor_data.jsonl
                                           |
                              ┌────────────┼────────────┐
                              │            │            │
                        sensor_cli.py  event_monitor  OpenClaw cron
                        (query data)   (check new)    (feishu alert)
```

## Quick Start

```bash
# 1. One-click setup (auto-detects platform, Python, serial port)
./setup.sh

# 2. Start receiver (Ctrl+C to stop)
#    macOS:
./venv/bin/python scripts/usb_receiver.py --port /dev/cu.usbmodem1CDBD4A896441
#    Linux/RPi:
./venv/bin/python scripts/usb_receiver.py --port /dev/ttyUSB0
#    Docker (inside container):
./entrypoint.sh

# 3. Check for alerts (in another terminal)
./venv/bin/python scripts/event_monitor.py

# 4. Query historical data
./venv/bin/python scripts/sensor_cli.py latest
./venv/bin/python scripts/sensor_cli.py stats --since 1h
```

If you need Feishu alerts, follow the **"OpenClaw Cron Alert (feishu)"** section below to configure a cron job.

## Install as System Service

`setup.sh` automatically generates a service file for your platform. Follow the output instructions, or:

**Linux / Raspberry Pi (systemd):**
```bash
sudo cp meshtastic-detection.generated.service /etc/systemd/system/meshtastic-detection.service
sudo systemctl daemon-reload
sudo systemctl enable --now meshtastic-detection

# Check status
sudo systemctl status meshtastic-detection
sudo journalctl -u meshtastic-detection -f
```

**macOS (launchd):**
```bash
cp com.openclaw.meshtastic-detection.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.openclaw.meshtastic-detection.plist

# Uninstall
launchctl unload ~/Library/LaunchAgents/com.openclaw.meshtastic-detection.plist
```

**Docker (entrypoint.sh):**

There is no systemd inside the container. When `setup.sh` detects Docker, it generates `entrypoint.sh`, which contains a simple auto-restart loop.

Option 1: run in background inside an already running container
```bash
nohup ./entrypoint.sh > data/entrypoint.log 2>&1 &

# Tail logs
tail -f data/entrypoint.log
```

Option 2: use as the main container process (recommended, letting Docker manage restarts)

```yaml
# docker-compose.yml
services:
  meshtastic:
    image: your-image
    working_dir: /app/skills/meshtastic-detection
    command: ./entrypoint.sh
    restart: always
    privileged: true
    devices:
      - /dev/ttyACM0:/dev/ttyACM0
    volumes:
      - ./data:/app/skills/meshtastic-detection/data
```

## Components

| Component | Purpose |
|-----------|---------|
| `usb_receiver.py` | Long-running daemon: USB serial -> JSONL storage (DETECTION_SENSOR_APP only) |
| `event_monitor.py` | Incremental alert checker: reads new records since last check, outputs JSON |
| `sensor_cli.py` | CLI query tool: latest, query, stats, status |
| `SKILL.md` | OpenClaw skill definition (agent reads this) |
| `CONFIG.md` | User configuration (serial port, notification channel) |

## Data Format

Each detection record in `data/sensor_data.jsonl`:

```json
{"received_at": "2026-03-04T11:07:06+00:00", "sender": "!1dd29c50", "channel": "ch0", "portnum": "DETECTION_SENSOR_APP", "data": {"type": "detection", "text": "alert detected"}}
```

Only `DETECTION_SENSOR_APP` messages are captured. Every record = a GPIO trigger on the remote sensor.

## Log Rotation

`sensor_data.jsonl` is automatically rotated when it exceeds **5 MB**:

- Current file -> `sensor_data.jsonl.1` -> `sensor_data.jsonl.2` (oldest deleted)
- At most **2 archive files** are kept (total max ~15 MB on disk)
- `event_monitor` state is automatically reset after rotation
- `sensor_cli` reads across all archive files for complete query results

No manual cleanup needed.

## OpenClaw Cron Alert (feishu)

After configuration, the cron job will run `event_monitor.py` every minute; if there are new alerts, OpenClaw will push them to Feishu.

### 1. Create a cron job

From the project root, run the following (replace `<PROJECT_PATH>` with your real path, e.g. `/Users/you/.openclaw/skills/meshtastic-detection`, and `<your-feishu-open-id>` with your Feishu open_id):

```bash
openclaw cron add \
  --name "sensor-monitor" \
  --every 1m \
  --session isolated \
  --timeout-seconds 60 \
  --message "Run this command and report the output: cd <PROJECT_PATH> && ./venv/bin/python scripts/event_monitor.py — If alert_count > 0, tell me how many alerts there are, and the latest sender and time. If alert_count is 0, reply: No new alerts." \
  --announce \
  --channel feishu \
  --to <your-feishu-open-id>
```

Notes:
- `--every 1m`: run every 1 minute
- `--timeout-seconds 60`: per-run timeout in seconds (running the script + sending the message usually takes ~20–40 seconds)
- `--channel feishu`: send via Feishu
- `--to <open-id>`: Feishu receiver open_id (required, otherwise no messages are delivered)

### 2. Verify it works

```bash
# List all cron jobs
openclaw cron list

# Trigger once manually (replace <job-id> with the ID from the list)
openclaw cron run <job-id>

# View the run history for this job
openclaw cron runs --id <job-id>
```

If Feishu does not receive messages: check that `--to` is set to the correct Feishu user open_id; if it times out, increase `--timeout-seconds`.

### 3. Container cron job (JSON structure)

The following describes the equivalent configuration for `sensor-monitor`, for viewing, debugging, or recreating jobs in the container or platform.

**Project path in container** (differs from local):

- In container: `/home/node/.openclaw/workspace/skills/meshtastic-detection/`
- Local: `<PROJECT_PATH>` (e.g. `/Users/you/.openclaw/skills/meshtastic-detection`)

**Key JSON fields**:

| Field | Description |
|-------|-------------|
| `jobs[].name` | Job name, e.g. `sensor-monitor` |
| `jobs[].schedule.kind` | `"every"` = run at fixed interval |
| `jobs[].schedule.everyMs` | Interval in ms, e.g. `60000` = 1 minute |
| `jobs[].sessionTarget` | `"isolated"` = isolated session |
| `jobs[].payload.kind` | `"agentTurn"` = Agent executes the instruction |
| `jobs[].payload.message` | Full instruction for the Agent (see template below) |
| `jobs[].payload.timeoutSeconds` | Per-run timeout in seconds, e.g. `60` |
| `jobs[].delivery.mode` | `"silent"` = run only, no platform delivery; for Feishu, the message instructs the Agent to use the message tool |

**Recommended payload.message template** (Feishu alert + heartbeat):

```text
Run detection task: cd /home/node/.openclaw/workspace/skills/meshtastic-detection/ && ./venv/bin/python scripts/event_monitor.py

Based on the output:
- If alert_count > 0: Use the message tool to send an alert to Feishu (target: user:<feishu-open-id>), in this format:

🚨 **Meshtastic Detection Alert**
📊 **Count**: X new alert(s)
📡 **Source node**: sender_id
📍 **Latest time**: timestamp
📝 **Content**: alert text

- If alert_count = 0: Reply HEARTBEAT_OK (do not send a message)

Important: You must use the message tool with action=send to send the message to Feishu.
```

Replace `<feishu-open-id>` with the recipient's Feishu open_id (e.g. `ou_9b2c3a662d7a314f2d9a3a893f29cc3c`).

**state fields** (runtime status, read-only):

- `nextRunAtMs` / `lastRunAtMs`: Next/last run time (ms timestamp)
- `lastRunStatus`: `"ok"` or error message
- `lastDeliveryStatus` / `lastDeliveryError`: If platform delivery fails, check here; in the container, alerts often rely on the payload message instructing the Agent to use the message tool to send to Feishu.

## File Structure

```
meshtastic-detection/
├── _meta.json                    # ClawHub metadata
├── SKILL.md                      # AI agent instructions (with metadata gating)
├── CONFIG.md                     # User configuration
├── README.md                     # This file
├── setup.sh                      # One-click setup (macOS/Linux/RPi)
├── requirements.txt              # Python dependencies
├── .gitignore
├── scripts/
│   ├── usb_receiver.py           # USB serial daemon
│   ├── event_monitor.py          # Incremental alert monitor
│   └── sensor_cli.py             # Query CLI
├── data/                         # Runtime data (git-ignored)
│   ├── sensor_data.jsonl
│   ├── sensor_data.jsonl.1       # Archive
│   ├── sensor_data.jsonl.2       # Archive
│   ├── latest.json
│   └── monitor_state.json
├── docs/
│   └── OPENCLAW_SKILLS_GUIDE.md
└── references/
    ├── SETUP.md                  # Detailed installation guide
    ├── meshtastic-detection.service                # systemd template (Linux/RPi)
    ├── com.openclaw.meshtastic-detection.plist     # launchd template (macOS)
    └── entrypoint.sh                              # Docker entrypoint template
```

## Dependencies

- `meshtastic>=2.0` -- Meshtastic Python API
- `pypubsub` -- Pubsub for serial event handling
- Python 3.10+

| Platform | Install Python |
|----------|---------------|
| macOS | `brew install python@3.12` |
| Raspberry Pi | `sudo apt install python3.11 python3.11-venv` |
| Ubuntu/Debian | `sudo apt install python3.12 python3.12-venv` |

## Troubleshooting

**Docker: running setup.sh when ensurepip is unavailable / no root**
- `setup.sh` first tries to create a venv without pip and then installs pip via get-pip.py, **without relying on apt**, suitable for containers without root.
- If it still fails, use an image that already includes venv support (e.g. `python:3.11`), or run inside the image as root: `apt update && apt install -y python3.11-venv`.

**Docker serial access (/dev/ttyACM0 permission issues)**
- On the host, mount the device into the container:
  - `docker run --device /dev/ttyACM0:/dev/ttyACM0 ...`
  - Or in docker-compose:
    - `devices:`
      - `/dev/ttyACM0:/dev/ttyACM0`
- If you still get `Permission denied`, you can temporarily run a privileged container (recommended only for testing):
  - `docker run --privileged ...`
  - Or in docker-compose:`privileged: true`
- In production, a safer approach is to mount only the required devices and avoid using `privileged: true` long term.

**Raspberry Pi / Debian: ensurepip not available**
- `setup.sh` will auto-detect and install the missing `python3.X-venv` package via apt.
- If auto-install fails, run manually: `sudo apt install python3.11-venv` (replace `3.11` with your Python version).

**Raspberry Pi: serial port permission denied**
- Add your user to the `dialout` group: `sudo usermod -a -G dialout $USER`
- Log out and back in (or reboot) for the change to take effect.

**venv install fails with pyobjc-core error (macOS)**
- You're using Python 3.9 (macOS default). Recreate with `python3.12 -m venv venv`.

**Receiver runs but no detection events appear**
- Only `DETECTION_SENSOR_APP` messages are captured (not TEXT_MESSAGE_APP).
- Run with `--debug` to see all incoming packets.
- Confirm the remote device has Detection Sensor Settings configured (GPIO pin monitoring).
- Both devices must be on the same Meshtastic channel with the same encryption key.

**Cron job times out**
- Increase `timeoutSeconds` to 60 via `openclaw cron edit <id> --timeout-seconds 60`.

**Cron runs but feishu doesn't receive message**
- Set delivery target: `openclaw cron edit <id> --to <feishu-open-id>`.

**Serial port busy**
- Only one process can use the port.
- macOS: `lsof /dev/cu.usbmodem*`
- Linux/RPi: `lsof /dev/ttyUSB* /dev/ttyACM*`

## License

MIT
