# py-homeassistant-cli

A Python CLI tool to control Home Assistant devices and automations via the REST API. No external dependencies — uses only Python 3.6+ standard library.

## Setup

1. Get a long-lived access token from Home Assistant (Profile → Long-Lived Access Tokens)

2. Configure via environment variables or command-line arguments:

```bash
# Optional: Environment variables
export HA_URL="http://10.0.0.10:8123"
export HA_TOKEN="your_long_lived_access_token"

# Or pass via args (overrides env vars)
python3 scripts/homeassistant-cli.py --server http://10.0.0.10:8123 --token YOUR_TOKEN check
```

3. Verify connectivity:

```bash
python3 scripts/homeassistant-cli.py check
```

## Usage

```
python3 scripts/homeassistant-cli.py [--server URL] [--token TOKEN] <command> [args]
```

Use `--help` on any command for details:

```bash
python3 scripts/homeassistant-cli.py --help
python3 scripts/homeassistant-cli.py light --help
```

## Commands

| Command | Description |
|---------|-------------|
| `check` | Check API connectivity |
| `entities` | List entities (`--domain light` to filter) |
| `state` | Get entity state |
| `areas` / `floors` | List areas and floors |
| `area-entities` / `area-of` | Area-entity lookups |
| `dashboard` | Quick overview of active devices |
| `switch` | Turn on/off/toggle switches |
| `light` | Control lights (brightness, RGB, color temp) |
| `climate` | Thermostat state, temperature, HVAC mode |
| `cover` | Open/close blinds, garage doors |
| `lock` | Lock/unlock |
| `fan` | Fan on/off with speed |
| `media` | Play/pause, volume |
| `vacuum` | Start cleaning / return to dock |
| `alarm` | Arm/disarm alarm panel |
| `scene` | Activate a scene |
| `automation` | List/trigger/enable/disable automations |
| `script` | List/run scripts with variables |
| `notify` | List targets or send notifications |
| `presence` | Who is home / device trackers |
| `weather` | Current weather or forecast |
| `input` | Control input helpers (boolean, number, select, text, datetime) |
| `calendar` | List calendars / upcoming events |
| `tts` | Text-to-speech |
| `services` | List available HA services |
| `service` | Call any HA service (generic) |
| `template` | Evaluate Jinja2 templates |
| `history` | Entity state history |
| `logbook` | View logbook entries |
| `tesla` | Tesla battery, location, automations |

## Examples

```bash
# List all lights and their states
python3 scripts/homeassistant-cli.py entities --domain light

# Turn on living room light at 80% brightness
python3 scripts/homeassistant-cli.py light turn_on light.living_room --brightness 80

# Set thermostat to 72 degrees
python3 scripts/homeassistant-cli.py climate set_temp climate.thermostat --temperature 72

# Quick dashboard of active devices
python3 scripts/homeassistant-cli.py dashboard

# Send a notification
python3 scripts/homeassistant-cli.py notify send mobile_app_phone "Front door opened" --title "Alert"

# Call any service with custom data
python3 scripts/homeassistant-cli.py service light turn_off --data '{"entity_id": ["light.room1", "light.room2"]}'
```

## License

MIT
