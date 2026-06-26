---
name: tuya-cloud
description: Read sensor data and control Tuya IoT devices via Tuya Cloud API or local LAN. Use when the user wants to list devices, read temperature, humidity, soil moisture, battery or other sensor data, or send commands to switches and valves. Requires TUYA_ACCESS_ID, TUYA_ACCESS_SECRET, and optionally TUYA_API_ENDPOINT in .env.
license: MIT
metadata: {"openclaw":{"emoji":"🔌","primaryEnv":"TUYA_ACCESS_ID","requires":{"env":["TUYA_ACCESS_ID","TUYA_ACCESS_SECRET"],"bins":["python3"]}}}
---

# Tuya Cloud Controller

Read sensor data and control Tuya IoT devices via `scripts/tuya_controller.py`. Supports both Tuya Cloud API and direct local LAN control.

## Device registry

Known controllable devices are defined in `scripts/config.py` as `CONTROLLABLE_DEVICES` (OPTIONAL).  
**Always consult this list first if exist** to resolve a device name to its `device_id`.  
For valve devices the `valve` key gives the DP code ( e.g. `switch_1`) to use as the command `code`.  
Only call `tuya_list_devices` if the device is not listed in the config.

## Setup

Add credentials to `.env`:

```bash
TUYA_ACCESS_ID=your_access_id
TUYA_ACCESS_SECRET=your_access_secret
TUYA_API_ENDPOINT=https://openapi.tuyaeu.com  # default: tuyaus.com (US)
```

Regional endpoints: EU `tuyaeu.com` · US `tuyaus.com` · CN `tuyacn.com` · IN `tuyain.com`

Enable **IoT Core** service in your Tuya IoT Platform project, and grant devices controllable permission (read-only by default).

## Tools

### `tuya_list_devices`

List all Tuya devices linked to the cloud project.

```bash
python scripts/tuya_controller.py list_devices
python scripts/tuya_controller.py list_devices --output_format json --output_path devices.json
```

### `tuya_read_24h_avg`

Return the 24-hour average soil moisture (humidity) for a sensor, computed from its Tuya DP log history.

```bash
python scripts/tuya_controller.py read_24h_avg <device_id>
```

Output is a JSON object:

```json
{
  "avg_humidity": 34.2,   // mean of all va_humidity log entries over 24 h; null if no data
  "count": 47,            // number of log entries found
  "min_humidity": 28.0,
  "max_humidity": 41.0
}
```

If `count` is 0 all fields are `null` — this happens when the device has no log history yet or the Tuya logs API is rate-limited. The garden-irrigation skill falls back to the current reading in that case.

### `tuya_read_last_n`

Return the average soil moisture from the last N humidity readings, looking back up to 7 days. Preferred over `read_24h_avg` — avoids pagination-related rate limiting and gives a stable average regardless of time of day.

```bash
python scripts/tuya_controller.py read_last_n <device_id>
python scripts/tuya_controller.py read_last_n <device_id> --n 100
```

Output is the same JSON shape as `read_24h_avg`:

```json
{
  "avg_humidity": 59.3,
  "count": 50,
  "min_humidity": 46.0,
  "max_humidity": 66.0
}
```

If `count` is 0 all fields are `null` — rate-limited or no log history. The garden-irrigation skill falls back to the current reading in that case.

### `tuya_read_sensor`

Read all sensor data from a Tuya device (temperature, humidity, battery, motion, door state, switch state).

```bash
python scripts/tuya_controller.py read_sensor <device_id>
python scripts/tuya_controller.py read_sensor <device_id> --output_format text
```

`parse_sensor_data()` interprets raw API keys:

| Sensor | Raw keys | Notes |
|---|---|---|
| Temperature | `va_temperature`, `temp_current`, `temp_set` | Divided by 10 (e.g. 245 → 24.5°C) |
| Humidity | `va_humidity`, `humidity_value` | Percentage as-is |
| Battery | `battery_percentage`, `battery` | Good >80% / Medium >20% / Low ≤20% |
| Motion | `pir` | `"pir"` value = detected |
| Door | `doorcontact_state` | Boolean → Open/Closed |
| State | `state` | Boolean → On/Off |
| Soil moisture | `soil_moisture`, `humidity`, `va_humidity` | Percentage as-is |

### `tuya_control_device`

Send commands to a Tuya device (switch, valve, countdown timer). Pass a JSON array of `{"code", "value"}` pairs. Uses the IoT Core `/v1.0/iot-03/` endpoint, which supports Zigbee sub-devices.

```bash
# Turn switch/valve on or off
python scripts/tuya_controller.py control_device <device_id> '[{"code":"switch_1","value":true}]'
python scripts/tuya_controller.py control_device <device_id> '[{"code":"switch_2","value":false}]'

# Open valve for a fixed duration — send switch ON + countdown in ONE call
# countdown_1 / countdown_2 values are in MINUTES — do NOT multiply by 60
python scripts/tuya_controller.py control_device <device_id> '[{"code":"switch_1","value":true},{"code":"countdown_1","value":10}]'
```

> ⚠️ `countdown_1` / `countdown_2` are in **minutes**. `10` = 10 min, `60` = 1 hour.

#### Dual-channel valve devices

Some valve devices expose two independent channels (e.g. left and right outlet). Each channel has its own switch and countdown DP:

| Channel | Switch DP  | Countdown DP  |
|---------|------------|---------------|
| Left    | `switch_1` | `countdown_1` |
| Right   | `switch_2` | `countdown_2` |

Control each channel independently:

```bash
# Open left valve for 5 minutes
python scripts/tuya_controller.py control_device <device_id> '[{"code":"switch_1","value":true},{"code":"countdown_1","value":5}]'

# Open right valve for 10 minutes
python scripts/tuya_controller.py control_device <device_id> '[{"code":"switch_2","value":true},{"code":"countdown_2","value":10}]'

# Close right valve immediately
python scripts/tuya_controller.py control_device <device_id> '[{"code":"switch_2","value":false}]'
```

To register a dual-channel valve in `config.py`, add both channels as separate entries or use a list:

```python
# Option A: two entries (one per channel)
{'name': 'Greenhouse valve left',  'device_id': '<id>', 'valve': 'switch_1', 'countdown': 'countdown_1'},
{'name': 'Greenhouse valve right', 'device_id': '<id>', 'valve': 'switch_2', 'countdown': 'countdown_2'},
```

## Local LAN Tools

Control devices directly over the local network without cloud API calls. No credentials needed for scanning; `local_key` and `ip` required for read/control.

### `scan_local`

Scan the local network for Tuya devices via UDP broadcast.

```bash
python scripts/tuya_controller.py scan_local
python scripts/tuya_controller.py scan_local --timeout 10
python scripts/tuya_controller.py scan_local --enrich --output_format json   # add cloud names/local_keys (requires cloud credentials)
```

### `read_local`

Read device status directly over LAN (no cloud round-trip).

```bash
python scripts/tuya_controller.py read_local <device_id> <ip> <local_key>
python scripts/tuya_controller.py read_local <device_id> <ip> <local_key> --version 3.4
```

### `control_local`

Send commands to a device directly over LAN. Commands can use integer DP index (`dp`) or string DP name (`code`).

```bash
python scripts/tuya_controller.py control_local <device_id> <ip> <local_key> '[{"dp":1,"value":true}]'
python scripts/tuya_controller.py control_local <device_id> <ip> <local_key> '[{"code":"switch_1","value":true}]'
```

> Use integer `dp` for maximum compatibility. String `code` requires the device to support it.

## API Endpoints (internal)

- Device list: `GET /v1.0/iot-01/associated-users/devices`
- Device info: `GET /v1.0/devices/{device_id}`
- Device status: `GET /v1.0/iot-03/devices/{device_id}/status`
- Send commands: `POST /v1.0/iot-03/devices/{device_id}/commands`

## Dependencies

```bash
pip install tinytuya python-dotenv
```

## Troubleshooting

| Error | Fix |
|---|---|
| "Data center is not enabled" | Enable IoT Core in Tuya IoT Platform → Service API |
| "Permission denied" | Subscribe to IoT Core and enable Device Status Notification |
| Device offline | `online: false`; soil moisture returns `null` |
| Wrong endpoint | Match `TUYA_API_ENDPOINT` to your account region |
| Local scan finds nothing | Check firewall; UDP broadcast may be blocked on some networks |
| Local control fails for Zigbee devices | `read_local` / `control_local` CLI commands do not support Zigbee sub-devices. Use the Python API directly: `get_local_subdevice_status(gateway_id, gateway_ip, gateway_local_key, sub_device_id)` and `send_local_subdevice_commands(…)` in `tuya_controller.py` — these pass the sub-device ID as `cid` to the gateway. |
