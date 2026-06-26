# USB Relay & Light Sensor Skills - Usage Guide

Complete guide for installing and using the USB Relay Control and Light Sensor Reader skills with AI agents.

## Quick Start

Already have system configured? Here's the fastest way to get started:

```bash
# 1. Install ClawHub CLI
npm install -g clawhub

# 2. Login
npx clawhub login

# 3. Install skills
npx clawhub install control-usb-relay
npx clawhub install usb-light-sensor-reader

# 4. Install NanoBot
pip3 install nanobot-ai

# 5. Configure NanoBot
nanobot init

# 6. Start using with AI
nanobot start
```

Then tell NanoBot: *"Use the control-usb-relay skill to turn on the device"*

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Hardware Setup](#hardware-setup)
4. [Using with AI Agents](#using-with-ai-agents)
5. [Usage Examples](#usage-examples)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### System Requirements

- **OS:** Linux (Ubuntu, Debian, Fedora, etc.)
- **Python:** 3.8 or higher
- **Hardware:** USB relay module and/or USB light sensor
- **Permissions:** User must be in `dialout` group for serial port access

### Hardware Requirements

| Device | Port | Description |
|--------|------|-------------|
| USB Relay | `/dev/ttyUSB1` | 1-channel or multi-channel relay module |
| USB Light Sensor | `/dev/ttyUSB0` | BH1750 or similar lux sensor |

---

## Installation

### Step 1: Install Node.js (if not installed)

```bash
# Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verify installation
node --version
npm --version
```

### Step 2: Install ClawHub CLI

```bash
# Install globally via npm
npm install -g clawhub

# Or use npx without global installation
npx clawhub --version
```

### Step 3: Login to ClawHub

```bash
# Login (opens browser for authentication)
npx clawhub login

# Verify login
npx clawhub whoami
```

### Step 4: Install Python Dependencies

```bash
# Install pyserial for USB communication
pip3 install pyserial

# Or for specific user
pip3 install --user pyserial
```

### Step 5: Configure Serial Port Permissions

```bash
# Add user to dialout group
sudo usermod -a -G dialout $USER

# Apply changes (logout and login, or reboot)
# Verify with:
groups $USER
```

### Step 6: Install the Skills

```bash
# Create skills directory (if not exists)
mkdir -p skills
cd skills

# Install USB Relay Control skill
npx clawhub install control-usb-relay

# Install USB Light Sensor Reader skill
npx clawhub install usb-light-sensor-reader

# List installed skills
npx clawhub list
```

### Step 7: Install NanoBot

```bash
# Clone NanoBot repository
git clone https://github.com/nanobot-ai/nanobot.git
cd nanobot

# Install dependencies
pip3 install -r requirements.txt

# Or install via pip
pip3 install nanobot-ai

# Verify installation
nanobot --version
```

#### NanoBot Configuration

After installation, configure NanoBot to use your skills:

```bash
# Initialize NanoBot configuration
nanobot init

# Or manually create config file
mkdir -p ~/.nanobot
```

Create `~/.nanobot/config.yaml`:

```yaml
skills:
  directory: ~/nanobot_demo/nanobot_deom/skills
  enabled:
    - control-usb-relay
    - usb-light-sensor-reader

hardware:
  relay_port: /dev/ttyUSB1
  sensor_port: /dev/ttyUSB0

model:
  provider: openai  # or anthropic, qwen, etc.
  api_key: your-api-key-here
```

#### Starting NanoBot

```bash
# Start NanoBot interactive mode
nanobot start

# Or run with specific config
nanobot run --config ~/.nanobot/config.yaml
```

---

## Hardware Setup

### Connecting USB Relay

1. Connect the USB relay module to USB port (typically appears as `/dev/ttyUSB1`)
2. Connect devices to relay terminals (NO, COM, NC)
3. Verify connection:
   ```bash
   ls -l /dev/ttyUSB*
   ```

### Connecting USB Light Sensor

1. Connect the light sensor module to USB port (typically appears as `/dev/ttyUSB0`)
2. Ensure sensor is exposed to light source
3. Verify connection:
   ```bash
   ls -l /dev/ttyUSB*
   ```

### Testing Hardware

```bash
# Test relay
cd skills/control-usb-relay
python3 relay.py

# Test sensor
cd skills/usb-light-sensor-reader
python3 sensor.py
```

---

## Using with AI Agents

### Supported AI Agents

These skills work with any AI agent that supports ClawHub skills:

- **NanoBot** - Lightweight AI assistant (recommended for hardware control)
- **OpenCLAW** - Open-source AI agent framework
- **Qwen Code** - AI coding assistant
- **Cursor** - AI-powered IDE
- **Windsurf** - AI development environment

### NanoBot Integration

After installing NanoBot (Step 7), the skills are automatically available.

### Prompting AI Agents

When working with AI agents, use clear prompts that reference the skills:

#### Example Prompts

**For Relay Control:**
```
Use the control-usb-relay skill to turn on the connected device.
```

**For Sensor Reading:**
```
Read the current light level using the usb-light-sensor-reader skill.
```

**For Automation:**
```
Create an automation that turns on the relay when the light sensor detects 
darkness (below 100 lux) and turns it off when it's bright (above 500 lux).
```

---

## Usage Examples

### Example 1: Basic Relay Control

**Prompt:**
```
Turn on the USB relay to power the connected device.
```

**Expected AI Action:**
```python
from relay import Relay

relay = Relay(port='/dev/ttyUSB1')
if relay.connect():
    relay.turn_on()
    print("Relay turned ON")
    relay.disconnect()
```

### Example 2: Reading Light Sensor

**Prompt:**
```
Check the current ambient light level in the room.
```

**Expected AI Action:**
```python
from sensor import Sensor

sensor = Sensor(port='/dev/ttyUSB0')
if sensor.connect():
    lux = sensor.read_lux()
    print(f"Current light level: {lux:.2f} lux")
    sensor.disconnect()
```

### Example 3: Automated Light Control

**Prompt:**
```
Set up automatic light control - turn on the lamp when it gets dark 
and turn it off when it's bright enough.
```

**Expected AI Action:**
```python
from sensor import Sensor
from relay import Relay
import time

sensor = Sensor(port='/dev/ttyUSB0')
relay = Relay(port='/dev/ttyUSB1')

sensor.connect()
relay.connect()

try:
    while True:
        lux = sensor.read_lux()
        print(f"Light: {lux:.2f} lux")
        
        if lux < 100:  # Dark
            if not relay.is_on():
                relay.turn_on()
                print("Turning ON light")
        elif lux > 500:  # Bright
            if relay.is_on():
                relay.turn_off()
                print("Turning OFF light")
        
        time.sleep(5)
except KeyboardInterrupt:
    sensor.disconnect()
    relay.disconnect()
```

### Example 4: Status Check

**Prompt:**
```
Check if the relay is currently on and what the light level is.
```

**Expected AI Action:**
```python
from sensor import Sensor
from relay import Relay

sensor = Sensor()
relay = Relay()

sensor.connect()
relay.connect()

print(f"Relay status: {'ON' if relay.is_on() else 'OFF'}")
print(f"Light level: {sensor.read_lux():.2f} lux")

sensor.disconnect()
relay.disconnect()
```

### Example 5: Scheduled Operation

**Prompt:**
```
Create a schedule to turn on the device for 30 minutes every evening 
when the light level drops below 150 lux.
```

**Expected AI Action:**
```python
from sensor import Sensor
from relay import Relay
import time
from datetime import datetime

sensor = Sensor(port='/dev/ttyUSB0')
relay = Relay(port='/dev/ttyUSB1')

sensor.connect()
relay.connect()

evening_start = 18  # 6 PM
evening_end = 23    # 11 PM
duration_minutes = 30
device_on = False

try:
    while True:
        now = datetime.now()
        hour = now.hour
        
        # Check if within evening hours
        if evening_start <= hour <= evening_end:
            lux = sensor.read_lux()
            
            # Turn on if dark and not already on
            if lux < 150 and not device_on:
                relay.turn_on()
                device_on = True
                print(f"Device ON at {now.strftime('%H:%M')}")
                start_time = time.time()
            
            # Turn off after duration
            if device_on:
                elapsed = (time.time() - start_time) / 60
                if elapsed >= duration_minutes:
                    relay.turn_off()
                    device_on = False
                    print(f"Device OFF after {duration_minutes} minutes")
        
        time.sleep(30)  # Check every 30 seconds
except KeyboardInterrupt:
    if device_on:
        relay.turn_off()
    sensor.disconnect()
    relay.disconnect()
```

---

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| `Permission denied` | User not in dialout group | `sudo usermod -a -G dialout $USER`, then logout/login |
| `Connection failed` | Wrong port or device not connected | Check `ls /dev/ttyUSB*` and verify connections |
| `No click sound` | Wrong protocol or external power needed | Verify relay protocol and check power supply |
| `Returns None` | Sensor warming up | Wait 1-2 seconds after connect() |
| `Port busy` | Another process using port | Kill other processes: `lsof /dev/ttyUSB0` |

### Diagnostic Commands

```bash
# Check USB devices
lsusb

# Check serial ports
ls -l /dev/ttyUSB*

# Check port usage
lsof /dev/ttyUSB0
lsof /dev/ttyUSB1

# Check user groups
groups $USER

# Test serial communication
python3 -c "import serial; print(serial.tools.list_ports.comports())"
```

### Getting Help

```bash
# View skill documentation
npx clawhub inspect control-usb-relay
npx clawhub inspect usb-light-sensor-reader

# Update skills
npx clawhub update control-usb-relay
npx clawhub update usb-light-sensor-reader

# Reinstall skills
npx clawhub uninstall control-usb-relay
npx clawhub install control-usb-relay
```

---

## Quick Reference

### Relay Commands

| Action | Method | Protocol |
|--------|--------|----------|
| Turn ON | `relay.turn_on()` | `A0 01 01 A2` |
| Turn OFF | `relay.turn_off()` | `A0 01 00 A1` |
| Toggle | `relay.toggle()` | Auto-detects state |
| Check status | `relay.is_on()` | Returns bool |

### Sensor Commands

| Action | Method | Threshold |
|--------|--------|-----------|
| Read light | `sensor.read_lux()` | Returns float |
| Check dark | `sensor.is_dark(100)` | Default: < 100 lux |
| Check bright | `sensor.is_bright(500)` | Default: > 500 lux |
| Raw reading | `sensor.read_raw()` | No filter |

---

## Additional Resources

- [ClawHub Documentation](https://clawhub.ai/docs)
- [NanoBot Documentation](https://nanobot.ai/docs)
- [NanoBot GitHub](https://github.com/nanobot-ai/nanobot)
- [OpenCLAW GitHub](https://github.com/openclaw/openclaw)
- [pyserial Documentation](https://pyserial.readthedocs.io/)

---

*Last updated: 2026-03-17*
*Skills version: 1.0.1*
