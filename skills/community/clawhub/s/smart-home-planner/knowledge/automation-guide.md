# Local Automation Guide

## Overview

Run smart home automations locally via mijia-api polling, without relying on Mi Home cloud automations.

**Two modes:** Standalone (lightweight) or AppDaemon (framework).

## Quick Start

```bash
# 1. Install deps
pip install mijiaAPI pyyaml

# 2. Login to mijia-api (if not done)
python3 -c "from mijiaAPI import mijiaAPI; api = mijiaAPI(); api.login()"

# 3. Discover devices
python3 automation/run_automations.py --discover

# 4. Edit config
#    automation/conf/devices.yaml — map DIDs to entity_ids
#    automation/conf/automations.yaml — define rules

# 5. Run
python3 automation/run_automations.py --config automation/conf
```

## Standalone Mode (Recommended)

Single Python script, no framework dependency.

```bash
python3 automation/run_automations.py --config automation/conf
```

Features:
- Smart polling (10s when occupied, 60s when empty)
- HA-compatible YAML rule format
- `--discover` flag for device listing
- ~20-50MB RAM

## AppDaemon Mode

Full framework with plugin system and web UI.

```bash
# Install
pip install appdaemon

# Setup plugin
cp automation/plugins/mijia/* <appdaemon_plugins_dir>/mijia/

# Run
appdaemon -c automation/conf/
```

**Critical naming conventions:**
- Plugin file: `mijiaplugin.py` (NOT `mijia_plugin.py`)
- Class name: `MijiaPlugin`
- Config: use `devices_file: devices.yaml` (NOT `!include`)

**Required plugin methods:**
- `get_namespace()` → str
- `get_updates()` → async coroutine (main polling loop)
- `stop()`
- `get_complete_state()` → dict
- `get_metadata()` → dict
- `utility()` → called every second

## YAML Automation Format

HA-compatible format:

```yaml
- id: my_automation
  alias: "My Automation"
  trigger:
    - platform: state
      entity_id: "sensor.my_sensor"
      to: "on"
  condition:
    - condition: time
      after: "08:00:00"
      before: "23:00:00"
  action:
    - service: scene.turn_on
      target:
        entity_id: "scene.my_scene"
  mode: single
```

### Triggers

| Platform | Fields | Description |
|----------|--------|-------------|
| `state` | entity_id, from, to, for | State change |
| `numeric_state` | entity_id, above, below | Numeric threshold |
| `time` | at | Daily at time |

### Conditions

| Type | Fields | Description |
|------|--------|-------------|
| `state` | entity_id, state | Check current state |
| `time` | after, before | Time range |
| `and` | conditions[] | All true |
| `or` | conditions[] | Any true |
| `not` | conditions[] | None true |

### Actions

| Service | Data | Description |
|---------|------|-------------|
| `light.turn_on` | target.entity_id | Turn on light |
| `light.turn_off` | target.entity_id | Turn off light |
| `switch.turn_on` | target.entity_id | Turn on switch |
| `switch.turn_off` | target.entity_id | Turn off switch |
| `scene.turn_on` | target.entity_id | Run scene |
| `mijia.set_property` | did, siid, piid, value | Direct property |
| `mijia.run_action` | did, siid, aiid, params | Direct action |

### Modes

| Mode | Behavior |
|------|----------|
| `single` | Skip if already running |
| `restart` | Cancel previous, start new |
| `queued` | Queue and run sequentially |

## Device Registry (devices.yaml)

Map Mijia DIDs to HA-style entity_ids:

```yaml
sensors:
  - entity_id: "sensor.occupy_living_room"
    name: "客厅人体传感器"
    did: "1100470123"
    model: "zywjw.sensor_occupy.c01"
    siid: 2
    piid: 1
    type: "occupancy"
```

Use `--discover` to list all devices with DIDs.

## Smart Polling

- Occupancy detected → poll every 10s
- No occupancy → poll every 60s
- Based on occupancy_sensors list in config

## Running as Service

### macOS (launchd)

```xml
<!-- ~/Library/LaunchAgents/com.mijia.automation.plist -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.mijia.automation</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/python3</string>
        <string>/path/to/automation/run_automations.py</string>
        <string>--config</string>
        <string>/path/to/conf</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
```

```bash
launchctl load ~/Library/LaunchAgents/com.mijia.automation.plist
```

### Linux (systemd)

```ini
# /etc/systemd/system/mijia-automation.service
[Unit]
Description=Mijia Automation Engine
After=network.target

[Service]
Type=simple
User=your_user
ExecStart=/usr/bin/python3 /path/to/automation/run_automations.py --config /path/to/conf
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| `auth invalid` | Token expired | Re-run `api.login()` |
| `No devices` | Empty devices.yaml | Run `--discover`, update yaml |
| `Not triggering` | Wrong entity_id | Check devices.yaml mapping |
| `Poll too slow` | Low frequency | Configure occupancy_sensors |
| AppDaemon `No module` | Wrong filename | Must be `mijiaplugin.py` |
| AppDaemon `no get_namespace` | Missing method | Add `get_namespace()` method |
| `429` / rate limited | Too many API calls | Back off and reduce polling frequency |
| YAML parse error | Invalid config | Fix syntax before retrying |
| Permission denied | Read-only target | Generate files locally and deploy manually |

## Safety Notes

- Do not auto-arm or auto-unlock anything that can create a safety problem without an explicit user-approved fallback.
- If motion or door sensors misfire, prefer temporarily disabling the scene over forcing aggressive polling.
