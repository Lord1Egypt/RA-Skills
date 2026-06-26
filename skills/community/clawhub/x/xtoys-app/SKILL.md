---
name: xtoys-app
version: 1.1.0
description: |
  Control xtoys.app devices via webhook.
  Supports precise control of various body parts for remote intimate device control.
license: MIT
homepage: https://xtoys.app
repository: https://github.com/himeteam/xtoys
metadata:
  author: himeteam
  tags: ["iot", "webhook", "device-control"]
  requirements:
    - python3
    - requests
    - urllib3
---

# Xtoys.app Webhook Skill v1.1.0

Remote control xtoys.app connected devices via webhook API.

## Configuration

Three configuration methods supported (priority from high to low):

### 1. Environment Variable (Recommended)
```bash
export XTOYS_WEBHOOK_ID="your-webhook-id-here"
```

### 2. Command Line Parameter
```bash
python3 scripts/xtoys_control.py --webhook-id xxx --action left_nipple --level 50
```

### 3. Configuration File
Set in `config.json`:
```json
{
  "webhook_id": "your-webhook-id-here"
}
```

Get your Webhook ID:
1. Open xtoys.app
2. Go to Settings → Webhook
3. Copy Webhook ID

## Usage

### Command Line

```bash
# Control specific body part
python3 scripts/xtoys_control.py --action left_nipple --level 50

# Stop current stimulation
python3 scripts/xtoys_control.py --action stop

# List supported actions
python3 scripts/xtoys_control.py --list

# Test connection
python3 scripts/xtoys_control.py --test

# Use environment variable
XTOYS_WEBHOOK_ID=xxx python3 scripts/xtoys_control.py --action clitoris --level 80

# Show verbose logs
python3 scripts/xtoys_control.py --action left_nipple --level 30 --verbose
```

### As Tool Call

```python
from scripts.xtoys_control import XtoysController

# Method 1: Using context manager (recommended)
with XtoysController("your-webhook-id") as controller:
    controller.send_command("left_nipple", 50)  # 50% intensity
    controller.send_command("clitoris", 80)      # 80% intensity
    controller.stop()  # Stop current

# Method 2: Manual management
controller = XtoysController("your-webhook-id")
try:
    controller.send_command("both_nipples", 50)
finally:
    controller.close()

# Method 3: Using environment variable
import os
os.environ["XTOYS_WEBHOOK_ID"] = "your-webhook-id"
with XtoysController() as controller:
    controller.send_command("vagina", 50)

# Batch operations
commands = [
    {"action": "left_nipple", "level": 30},
    {"action": "right_nipple", "level": 30},
    {"action": "clitoris", "level": 50},
]
results = controller.send_batch(commands)
```

## Supported Actions (Body Parts)

> **Note:** xtoys can only operate one body part at a time. When switching parts, the previous part will automatically be set to 0.

### Body Parts (Individual intensity control)
- `left_nipple` - Left nipple
- `right_nipple` - Right nipple
- `both_nipples` - Both nipples
- `left_breast` - Left breast
- `right_breast` - Right breast
- `both_breasts` - Both breasts
- `clitoris` - Clitoris
- `vagina` - Vagina
- `anus` - Anus

### Special Commands
- `stop` - Stop current stimulation
- `pause` - Pause current stimulation (same as stop)

## Level (Intensity)

- Range: 0 - 100
- **0 = Stop the body part**
- 100 = Maximum intensity

## How It Works

1. **Single Part Limitation**: xtoys can only stimulate one body part at a time
2. **Auto-switching**: When setting a new part, the previous part is automatically stopped
3. **Stop**: Use `stop` or set any part's `level` to 0

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `XTOYS_WEBHOOK_ID` | Webhook ID | `abc123` |
| `XTOYS_LOG_LEVEL` | Log level | `DEBUG`, `INFO`, `WARNING`, `ERROR` |

## Example Scenarios

```bash
# Gradual increase
for i in 10 30 50 70 100; do
  python3 scripts/xtoys_control.py --action left_nipple --level $i
  sleep 2
done

# Random fluctuation
python3 scripts/xtoys_control.py --action clitoris --level $((RANDOM % 100))

# Use in scripts
export XTOYS_WEBHOOK_ID="your-webhook-id"
python3 scripts/xtoys_control.py --action left_nipple --level 30
python3 scripts/xtoys_control.py --action clitoris --level 50
python3 scripts/xtoys_control.py --stop
```

## Safety Guidelines

- Always ensure remote control is consensual
- Use safeword mechanism
- Avoid prolonged high-intensity use
- Start with low intensity for first-time use
- Keep webhook ID confidential, do not share publicly

## Dependencies

```bash
pip install requests urllib3
```

## Changelog

### v1.1.0
- Fixed "estim" leading space issue
- Added environment variable support (`XTOYS_WEBHOOK_ID`)
- Improved error handling and logging system
- Added connection pooling and auto-retry
- Added batch operation support
- Added connection test feature
- Added context manager (`with` statement) support

### v1.0.0
- Initial release
- Basic webhook control functionality
