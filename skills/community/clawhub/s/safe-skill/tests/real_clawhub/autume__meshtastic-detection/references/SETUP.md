# Meshtastic Detection — Setup Guide

## Hardware Requirements

| Item | Notes |
|------|-------|
| Meshtastic node | Connected to host via USB |
| USB cable | Data-capable (not charge-only) |
| Host machine | macOS / Linux with Python 3.10+ |

> Both the local module and remote sensor device must be configured on the
> same Meshtastic channel and frequency region. The remote device must have
> **Detection Sensor Settings** configured (GPIO pin monitoring).

## Step 1: Connect Hardware

1. Connect the Meshtastic module to the host via USB.
2. Verify the device shows up:

```bash
# macOS
ls /dev/cu.usb*

# Linux
ls /dev/ttyACM* /dev/ttyUSB*
```

3. (Linux only) Ensure your user has serial port access:

```bash
sudo usermod -a -G dialout $USER
# Log out and back in
```

## Step 2: Install Python Dependencies

```bash
cd meshtastic-detection

# Create virtual environment — requires Python 3.10+
# macOS ships Python 3.9 as default; use a newer version explicitly:
python3.12 -m venv venv    # or python3.11, python3.13
source venv/bin/activate

# Verify version (must be 3.10+)
python --version

# Install dependencies
pip install -r requirements.txt
```

> **macOS note:** If you see `pyobjc-core` build errors, you're using Python 3.9.
> Delete the venv and recreate with `python3.12 -m venv venv`.

## Step 3: Test the Connection

```bash
python -c "
import meshtastic
import meshtastic.serial_interface
iface = meshtastic.serial_interface.SerialInterface('/dev/cu.usbmodem1CDBD4A896441')
info = iface.getMyNodeInfo()
user = info.get('user', {})
print(f'Connected: {user.get(\"longName\", \"unknown\")} ({user.get(\"id\", \"?\")})')
iface.close()
"
```

Replace the serial port path with your actual device path from Step 1.

## Step 4: Configure

Edit `CONFIG.md` in the project root:

1. Set `serial_port` to your device path
2. Set notification channel to `feishu`

## Step 5: Test the Receiver

Run the receiver manually to verify it captures detection events:


```bash
python scripts/usb_receiver.py --port /dev/cu.usbmodem1CDBD4A896441
```

You should see:
```
Meshtastic USB Receiver
  Serial port: /dev/cu.usbmodem1CDBD4A896441
  Data dir:    ./data
Connecting to /dev/cu.usbmodem1CDBD4A896441...
Connected: YourNodeName (!abc12345)
Receiver running. Data dir: data | Existing records: 0
```

Trigger the Detection Sensor on the remote device (GPIO pin HIGH). You should see:
```
[DETECTION_SENSOR_APP] from !xxx (ch0): alert detected
Stored: type=detection, portnum=DETECTION_SENSOR_APP (total: 1)
```

Use `--debug` to see ALL incoming packets (including ones that are filtered out):
```bash
python scripts/usb_receiver.py --port /dev/cu.usbmodem1CDBD4A896441 --debug
```

## Step 6: Test the Event Monitor

```bash
python scripts/event_monitor.py
```

Should output JSON with `alert_count > 0` if there are new detections since last check.

## Step 7: Set Up OpenClaw Cron (feishu alerts)

Create the cron job via OpenClaw CLI or through conversation:

```bash
openclaw cron add \
  --name "sensor-monitor" \
  --every 1m \
  --session isolated \
  --timeout-seconds 60 \
  --message "Run this command and report the output: cd /Users/odensu/.openclaw/skills/meshtastic-detection && ./venv/bin/python scripts/event_monitor.py — If alert_count > 0, tell me how many alerts, the latest sender and time. If alert_count is 0, reply: 暂无新告警。" \
  --announce \
  --channel feishu \
  --to <your-feishu-open-id>
```

Verify it works:
```bash
openclaw cron list
openclaw cron run <job-id>
openclaw cron runs --id <job-id>
```

## Step 8 (Optional): Install as systemd Service

For Linux servers that need the receiver running permanently:

1. Copy the service template:

```bash
sudo cp references/meshtastic-detection.service /etc/systemd/system/
```

2. Edit the service file to match your paths:

```bash
sudo nano /etc/systemd/system/meshtastic-detection.service
```

Update:
- `WorkingDirectory` — path to the `meshtastic-detection` directory
- `ExecStart` — path to the Python venv and script
- `User` — your username

3. Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable meshtastic-detection
sudo systemctl start meshtastic-detection
```

4. Check status:

```bash
sudo systemctl status meshtastic-detection
sudo journalctl -u meshtastic-detection -f
```

## Troubleshooting

### Serial port not found

```bash
# macOS
ls /dev/cu.usb*

# Linux
ls /dev/tty{ACM,USB}* 2>/dev/null
```

### Permission denied on serial port (Linux)

```bash
sudo usermod -a -G dialout $USER
# Then log out and back in
```

### Only one process can use the serial port

If you get "Resource temporarily unavailable":

```bash
# macOS
lsof /dev/cu.usbmodem*

# Linux
sudo fuser /dev/ttyACM0

# Stop the systemd service if running
sudo systemctl stop meshtastic-detection
```

### Receiver connects but no detection events

- Only `DETECTION_SENSOR_APP` messages are captured (TEXT_MESSAGE_APP is ignored)
- Confirm the remote device has **Detection Sensor Settings** configured
- Both devices must be on the same channel with the same encryption key
- Run with `--debug` to see all packets

### Cron job fails

```bash
# Check status
openclaw cron list

# Check error details
openclaw cron runs --id <job-id>

# Common fixes:
openclaw cron edit <id> --timeout-seconds 60        # increase timeout
openclaw cron edit <id> --to <feishu-open-id>        # set delivery target
```
