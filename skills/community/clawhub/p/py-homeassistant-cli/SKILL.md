---
name: py-homeassistant-cli
description: >
  Tiny and short Python CLI tool to control Home Assistant devices and automations via the REST API. 
  No external dependencies — uses only Python 3.6+ standard library.
license: MIT
homepage: https://github.com/xwings/py-homeassistant-cli
compatibility: Requires Python 3.6+. Network access to Home Assistant instance.
metadata: {"author": "xwings", "openclaw": { env: ["HA_URL", "HA_TOKEN"],"bins": ["python3 {baseDir}/scripts/homeassistant-cli.py"]}}
---

# Home Assistant Skill

Control smart home devices via the Home Assistant REST API using the Python CLI tool at `{baseDir}/scripts/homeassistant-cli.py`. No external dependencies — uses only Python standard library.

## Setup

Configure via environment variables or command-line arguments (args take priority):

```bash
# Optional: Environment variables
export HA_URL="http://10.0.0.10:8123"
export HA_TOKEN="your_long_lived_access_token"

# pass via args (overrides env vars)
python3 {baseDir}/scripts/homeassistant-cli.py --server http://10.0.0.10:8123 --token YOUR_TOKEN check
```

Use `--help` on any command for details: `python3 {baseDir}/scripts/homeassistant-cli.py light --help`

## Safety Rules

**Always confirm with the user before:** locking/unlocking **locks**, arming/disarming **alarm panels**, opening/closing **garage doors** or **gates**, disabling **security automations**.

## Command Reference

All commands follow: `python3 {baseDir}/scripts/homeassistant-cli.py [--server URL] [--token TOKEN] <command> [args]`

### Discovery & Status

```bash
check                                          # Check API connectivity
entities                                       # List all entities
entities --domain light                        # List entities by domain (light, switch, sensor, etc.)
state <entity_id>                              # Get full entity state JSON
areas                                          # List all areas
area-entities <area> [--domain light]          # Entities in an area, optionally filtered
area-of <entity_id>                            # Find which area an entity belongs to
floors                                         # List all floors and their areas
services [--domain light]                      # List available services
dashboard                                      # Quick overview: lights on, doors, temps, locks, presence
presence [--trackers]                          # Who is home (--trackers for device trackers)
weather [--forecast daily|hourly] [-e entity]  # Current weather or forecast
```

### Device Control

```bash
switch <turn_on|turn_off|toggle> <entity_id>
light <turn_on|turn_off> <entity_id> [--brightness 80] [--rgb 255,150,50] [--color-temp 300]
fan <turn_on|turn_off> <entity_id> [--percentage 50]
cover <open|close|set_position> <entity_id> [--position 50]
lock <lock|unlock> <entity_id>
media <play_pause|volume> <entity_id> [--level 0.5]
vacuum <start|dock> <entity_id>
climate <state|set_temp|set_mode> <entity_id> [--temperature 72] [--mode auto]
alarm <arm_home|disarm> <entity_id> [--code 1234]
scene <entity_id>
```

### Automations & Scripts

```bash
automation <list|trigger|enable|disable> [entity_id]
script <list|run> [entity_id] [--variables '{"key": "value"}']
```

### Notifications

```bash
notify list                                                    # List notification targets
notify send <service> "message" [--title "title"]              # Send notification
```

### Input Helpers

```bash
input boolean <entity_id>                   # Toggle
input number <entity_id> <value>            # Set number
input select <entity_id> "option"           # Set selection
input text <entity_id> "value"              # Set text
input datetime <entity_id> "07:30:00"       # Set time
```

### Calendar & TTS

```bash
calendar list                                              # List calendars
calendar events <entity_id> [--days 14]                    # Upcoming events
tts <tts_entity> <media_player_entity> "message"           # Text-to-speech
```

### Templates, History & Logbook

```bash
template '{{ states.light | list | count }} lights'                                    # Evaluate Jinja2
history <entity_id> [--start ISO8601] [--end ISO8601]                                  # State history
logbook [--entity entity_id] [--limit 20]                                              # Logbook entries
```

Template functions: `states()`, `is_state()`, `state_attr()`, `areas()`, `area_entities()`, `area_name()`, `floors()`, `floor_areas()`, `labels()`, `label_entities()`, `devices()`, `device_entities()`, `now()`, `relative_time()`.

### Generic Service Call

```bash
service <domain> <service> --data '{"entity_id": "light.living_room"}'

# Batch: pass array of entity_ids
service light turn_off --data '{"entity_id": ["light.room1", "light.room2"]}'
```

## Tesla

Entities: `sensor.mao_dou_battery`, `device_tracker.mao_dou_location_tracker`, `device_tracker.mao_dou_destination_location_tracker`, `automation.tesla_battery_below_20`

```bash
tesla battery        # Battery level
tesla location       # GPS coordinates, heading, speed
tesla destination    # Destination location
tesla automations    # List Tesla-related entities
```

## Entity Domains

| Domain | Examples | Domain | Examples |
|--------|----------|--------|----------|
| `switch.*` | Smart plugs | `light.*` | Lights (Hue, LIFX) |
| `climate.*` | Thermostats, AC | `cover.*` | Blinds, garage doors |
| `lock.*` | Smart locks | `fan.*` | Fans, ventilation |
| `media_player.*` | TVs, speakers | `vacuum.*` | Robot vacuums |
| `alarm_control_panel.*` | Security systems | `scene.*` | Pre-configured scenes |
| `script.*` | Action sequences | `automation.*` | Automations |
| `sensor.*` | Temp, humidity, power | `binary_sensor.*` | Motion, door/window |
| `person.*` | Presence tracking | `device_tracker.*` | Device locations |
| `weather.*` | Weather/forecasts | `calendar.*` | Calendar events |
| `notify.*` | Notification targets | `tts.*` | Text-to-speech |
| `input_boolean.*` | Virtual toggles | `input_number.*` | Numeric sliders |
| `input_select.*` | Dropdown selectors | `input_text.*` | Text inputs |
| `input_datetime.*` | Date/time inputs | | |

## HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad request (malformed JSON) |
| 401 | Unauthorized (bad/missing token) |
| 404 | Entity or endpoint not found |
| 503 | HA starting up or unavailable |

## Notes

- Long-lived tokens don't expire — store securely
- Test entity IDs with `entities --domain` first
- Use `service` command for any operation not covered by dedicated commands
- Service calls return JSON arrays of affected entity states; errors print to stderr
