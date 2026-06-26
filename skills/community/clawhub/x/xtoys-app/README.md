# Xtoys.app Webhook Controller

[![GitHub](https://img.shields.io/badge/GitHub-himeteam/xtoys-blue)](https://github.com/himeteam/xtoys)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-blue)](https://python.org)

A webhook controller for [xtoys.app](https://xtoys.app) devices. Control intimate devices remotely via webhook API.

## Features

- Precise control of multiple body parts
- Intensity control: 0-100
- Batch operation support
- Connection pooling with automatic retry
- Environment variable and configuration file support
- Complete logging system

## Installation

```bash
git clone https://github.com/himeteam/xtoys.git
```

## Configuration

### 1. Get Your Webhook ID

1. Open [xtoys.app](https://xtoys.app)
2. Go to Settings → Webhook
3. Copy your Webhook ID

### 2. Set Configuration (Choose one)

**Environment Variable (Recommended):**
```bash
export XTOYS_WEBHOOK_ID="your-webhook-id"
```

**Configuration File:**
Edit `config.json`:
```json
{
  "webhook_id": "your-webhook-id"
}
```

**Command Line:**
```bash
python3 scripts/xtoys_control.py --webhook-id xxx --action left_nipple --level 50
```

## Usage

### Command Line

```bash
# Control left nipple
python3 scripts/xtoys_control.py --action left_nipple --level 50

# Control clitoris
python3 scripts/xtoys_control.py --action clitoris --level 80

# Stop current stimulation
python3 scripts/xtoys_control.py --stop

# List supported actions
python3 scripts/xtoys_control.py --list

# Test connection
python3 scripts/xtoys_control.py --test
```

### Python API

```python
from scripts.xtoys_control import XtoysController

# Using context manager (recommended)
with XtoysController("your-webhook-id") as controller:
    controller.send_command("left_nipple", 50)
    controller.send_command("clitoris", 80)
    controller.stop()

# Batch operations
commands = [
    {"action": "left_nipple", "level": 30},
    {"action": "right_nipple", "level": 30},
    {"action": "clitoris", "level": 50},
]
results = controller.send_batch(commands)
```

## Supported Actions

> **Note:** Xtoys can only operate one body part at a time. When switching parts, the previous part will automatically be set to 0.

### Body Parts

| Action | Description |
|--------|-------------|
| `left_nipple` | Left nipple |
| `right_nipple` | Right nipple |
| `both_nipples` | Both nipples |
| `left_breast` | Left breast |
| `right_breast` | Right breast |
| `both_breasts` | Both breasts |
| `clitoris` | Clitoris |
| `vagina` | Vagina |
| `anus` | Anus |

### Special Commands

| Action | Description |
|--------|-------------|
| `stop` | Stop current stimulation |
| `pause` | Pause current stimulation (same as stop) |

**How it works:**
- Xtoys can only stimulate one body part at a time
- When setting a new part, the previous part is automatically set to 0
- Use `stop` or set any part's `level` to 0 to stop

## Level (Intensity)

- Range: 0 - 100
- **0 = Stop the body part**
- 100 = Maximum intensity

## How It Works

1. **Single Part Limitation**: Xtoys can only stimulate one body part at a time
2. **Auto-switching**: When setting a new body part, the previous part is automatically stopped
3. **Stop**: Use `stop` command or set `level=0` to stop current stimulation

## Dependencies

```bash
pip install requests urllib3
```

## Safety Guidelines

- Always ensure remote control is consensual
- Use safeword mechanism
- Avoid prolonged high-intensity use
- Start with low intensity for first-time use
- Keep webhook ID confidential, do not share publicly

## As OpenClaw Skill

Install to OpenClaw:
```bash
# Clone to skills directory
git clone https://github.com/himeteam/xtoys.git ~/.openclaw/skills/xtoys-app
```

Or install from SkillHub:
```bash
clawhub install xtoys-app
```

## License

MIT License

## Links

- [Xtoys.app](https://xtoys.app)
- [OpenClaw](https://openclaw.ai)
- [ClawHub](https://clawhub.ai)
- [GitHub Repository](https://github.com/himeteam/xtoys)
