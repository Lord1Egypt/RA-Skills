# Mijia API Guide (mijia-api)

## Overview

[mijia-api](https://github.com/Do1e/mijia-api) is a Python library that simulates the Mi Home app to call Xiaomi's cloud APIs. It authenticates via QR code scanning, then uses tokens to control devices remotely.

**Repository:** https://github.com/Do1e/mijia-api
**Stars:** 600+
**Language:** Python
**License:** GPL-3.0
**PyPI:** `mijiaAPI`

## Installation

```bash
pip install mijiaAPI
```

Dependencies installed automatically:
- `requests` — HTTP client
- `pycryptodome` — RC4 encryption
- `qrcode` + `pillow` — QR code generation for login
- `tzlocal` — Timezone detection

## Authentication

### First-Time Login

```python
from mijiaAPI import mijiaAPI

api = mijiaAPI()
api.login()  # Generates QR code in terminal
```

1. QR code appears in terminal
2. Open Mi Home app → scan QR code
3. Confirm login on phone
4. Token auto-saves to `~/.config/mijia-api/auth.json`

### Token Lifecycle

| Token | Duration | Auto-refresh |
|-------|----------|-------------|
| `serviceToken` | Short-lived | Yes (before each API call) |
| `passToken` | ~1 month | No (re-scan when expired) |

### Check Token Validity

```python
if api.available:
    print("Token is valid")
else:
    print("Token expired, need re-login")
    api.login()
```

### Re-authentication

When token expires (after ~1 month):
```python
api.login()  # New QR code scan
```

## Device Discovery

### List All Homes

```python
homes = api.get_homes_list()
for home in homes:
    print(f"Home: {home['name']}, ID: {home['id']}")
```

### List All Devices

```python
devices = api.get_devices_list()
for d in devices:
    print(f"{d['name']} ({d['model']}) - DID: {d['did']}")
```

### List Devices by Home

```python
devices = api.get_devices_list(home_id="xxx")
```

## Device Control

### High-Level API (mijiaDevice)

```python
from mijiaAPI import mijiaDevice

# By name
lamp = mijiaDevice(api, dev_name="Bedroom Lamp")

# By DID
lamp = mijiaDevice(api, did="xxx")

# Read properties
print(lamp.on)           # True/False
print(lamp.brightness)   # 0-100

# Set properties
lamp.on = True
lamp.brightness = 80
lamp.color_temperature = 4000

# Run action
lamp.run_action('toggle')
```

### Low-Level API (MIoT Spec)

```python
# Get properties
data = [{"did": "xxx", "siid": 2, "piid": 1}]
result = api.get_devices_prop(data)

# Set properties
data = [{"did": "xxx", "siid": 2, "piid": 1, "value": True}]
api.set_devices_prop(data)

# Run action
data = {"did": "xxx", "siid": 2, "aiid": 1, "in": []}
api.run_action(data)
```

### MIoT Spec Lookup

Each device model has a spec at `https://home.miot-spec.com/spec/{model}`

Example: `https://home.miot-spec.com/spec/yeelink.light.mbulb3`

The spec defines:
- `siid` — Service ID (e.g., light service = 2)
- `piid` — Property ID (e.g., brightness = 3, color temp = 5)
- `aiid` — Action ID (e.g., toggle = 1)
- Value ranges and types

## Scene Management

### List Scenes

```python
scenes = api.get_scenes_list()
for s in scenes:
    print(f"Scene: {s['name']}, ID: {s['scene_id']}")
```

### Run Scene

```python
api.run_scene(scene_id="xxx", home_id="yyy")
```

## Natural Language Control

Route commands through XiaoAi speaker:

```python
api.run("打开卧室灯")
api.run("把空调调到24度")
api.run("播放音乐")
```

## Batch Operations

Control multiple devices in one request:

```python
# Batch get
data = [
    {"did": "light1", "siid": 2, "piid": 1},
    {"did": "light2", "siid": 2, "piid": 1},
]
results = api.get_devices_prop(data)

# Batch set
data = [
    {"did": "light1", "siid": 2, "piid": 1, "value": True},
    {"did": "light2", "siid": 2, "piid": 1, "value": True},
]
api.set_devices_prop(data)
```

## CLI Usage

```bash
# List all devices
mijiaAPI -l

# Get device property
mijiaAPI get --dev_name "Bedroom Lamp" --prop_name "brightness"

# Set device property
mijiaAPI set --dev_name "Bedroom Lamp" --prop_name "brightness" --value 60

# List scenes
mijiaAPI --list_scenes

# Run scene
mijiaAPI --run_scene "Sleep Mode"

# Natural language
mijiaAPI --run "turn on the bedroom lamp"
```

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| `Token expired` | passToken expired after ~1 month | Re-run `api.login()` |
| `Device offline` | Device disconnected from network | Check Mi Home app, re-pair device |
| `Device not found` | Wrong name or device not in home | Check `get_devices_list()`, use exact name |
| `Permission denied` | Device shared, not owned | Use owner account |
| `AttributeError` on property | Property name not in device spec | Check miot-spec.com for available properties |
| QR code not appearing | Terminal doesn't support rendering | Use CLI tool instead of Python |

## Security Notes

- Auth tokens stored in `~/.config/mijia-api/auth.json`
- Tokens have Xiaomi account access — protect this file
- Use on trusted machines only
- Revoke access by changing Xiaomi account password
