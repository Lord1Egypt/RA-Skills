# Device Message Subscription

Real-time WebSocket subscription for Tuya device events. Enables monitoring property changes (brightness, switch state, temperature, etc.) and online/offline transitions as they happen.

> **Server-side only.** The WebSocket client must run on a backend server. Never connect from a browser or mobile app. To push real-time data to a frontend, subscribe server-side and relay via SSE, your own WebSocket, or polling.

**Dependency:** `pip install websockets` (Python 3.7+)

---

## Authentication & Connection

The WebSocket client reuses the same `TUYA_API_KEY` used by the REST API (`tuya_api.py`). No separate credentials are needed.

The WebSocket URI is **auto-detected** from the API key prefix, matching the same convention as the REST base URL:

| API Key Prefix | Region | WebSocket URI |
|---------------|--------|---------------|
| `AY` | China | `wss://wsmsgs.tuyacn.com` |
| `AZ` | US West | `wss://wsmsgs.iot-wus.com` |
| `EU` | Central Europe | `wss://wsmsgs.iot-eu.com` |
| `IN` | India | `wss://wsmsgs.iot-ap.com` |
| `UE` | US East | `wss://wsmsgs.iot-eus.com` |
| `WE` | Western Europe | `wss://wsmsgs.iot-weu.com` |
| `SG` | Singapore | `wss://wsmsgs.iot-sea.com` |

You can pass `uri` explicitly to override if needed.

---

## Client API Summary

| Capability | Usage |
|-----------|-------|
| Register property change handler | `@client.on_property_change` |
| Register online/offline handler | `@client.on_online_status` |
| Register raw message handler | `@client.on_raw_message` |
| Connect (blocking, auto-reconnect) | `await client.connect()` |
| Graceful stop | `client.stop()` |
| Format timestamp | `TuyaDeviceMQClient.format_timestamp(ts_ms)` |

Fatal close codes that stop reconnection: 1002, 1003, 1008, 1011.

Server error detection: any frame with `error`, `errorMsg`, `errorCode` (non-SUCCESS), or `success: false`.

---

## Message Format

All WebSocket messages are JSON objects with two top-level fields:

```json
{
  "data": { ... },
  "eventType": "devicePropertyChange" | "onlineStatusChange"
}
```

### devicePropertyChange

Pushed when one or more device property values change.

```json
{
  "data": {
    "devId": "36040531cc50e35ee60d",
    "status": [
      { "code": "led_switch", "value": true, "time": 1773668532000 },
      { "code": "bright_value", "value": 255, "time": 1773668532000 }
    ]
  },
  "eventType": "devicePropertyChange"
}
```

| Field | Type | Description |
|-------|------|-------------|
| data.devId | String | Device ID (matches `device_id` in REST API) |
| data.status | Array | One or more property changes in this event |
| data.status[].code | String | Property dp code (matches Thing Model `code`) |
| data.status[].value | Any | New value — type depends on the property's typeSpec |
| data.status[].time | Long | Change timestamp (milliseconds) |

#### Value formats by typeSpec

| typeSpec.type | Format | Example |
|---------------|--------|---------|
| bool | `true` / `false` | `"code": "switch_led", "value": true` |
| value | Integer | `"code": "bright_value", "value": 255` |
| enum | String within range | `"code": "work_mode", "value": "scene_3"` |
| string | String | `"code": "flash_scene_3", "value": "ffff5001ff0000"` |

#### Common property codes

| Code | Meaning | Value Type | Example Values |
|------|---------|------------|----------------|
| led_switch / switch_led | Light switch | bool | true, false |
| switch | Generic switch | bool | true, false |
| bright_value | Brightness | value | 10-1000 |
| temp_value | Color temperature | value | 0-1000 |
| work_mode | Working mode | enum | "white", "colour", "scene_1" |
| temp_set | Target temperature (AC) | value | 16-30 |
| mode | AC mode | enum | "auto", "cold", "hot" |
| doorcontact_state | Door/window sensor | bool | true (open), false (closed) |
| pir | Motion detection | enum | "pir" (motion detected) |

Actual codes depend on each device's Thing Model.

### onlineStatusChange

Pushed when a device connects to or disconnects from the network.

```json
{
  "data": {
    "devId": "6c8b3a57470efd4d9cun7h",
    "status": "online",
    "time": 1773668467323
  },
  "eventType": "onlineStatusChange"
}
```

| Field | Type | Description |
|-------|------|-------------|
| data.devId | String | Device ID |
| data.status | String | `"online"` or `"offline"` |
| data.time | Long | Event timestamp (milliseconds) |

### Mapping to REST API

| Message Field | REST API Equivalent | Query Method |
|--------------|---------------------|--------------|
| data.devId | device_id | `GET /v1.0/end-user/devices/{device_id}/detail` |
| status[].code | Thing Model property code | `GET /v1.0/end-user/devices/{device_id}/model` |
| status[].value | Current property value | Also in device detail `properties` field |

---

## Usage

### Quick Start

```python
import asyncio
import os
import sys
sys.path.insert(0, "{baseDir}/scripts")
from tuya_device_mq_client import TuyaDeviceMQClient

async def main():
    client = TuyaDeviceMQClient(api_key=os.environ["TUYA_API_KEY"])

    @client.on_property_change
    async def on_prop(device_id, properties):
        for prop in properties:
            t = TuyaDeviceMQClient.format_timestamp(prop["time"])
            print(f"[{t}] Device {device_id}: {prop['code']} = {prop['value']}")

    @client.on_online_status
    async def on_status(device_id, status, timestamp_ms):
        t = TuyaDeviceMQClient.format_timestamp(timestamp_ms)
        print(f"[{t}] Device {device_id} is now {status}")

    await client.connect()

asyncio.run(main())
```

### Filtering Specific Devices

```python
client = TuyaDeviceMQClient(
    api_key=os.environ["TUYA_API_KEY"],
    device_ids=["device_id_1", "device_id_2"],
)
```

### Property Change with Human-Readable Values

```python
def format_property_value(code: str, value) -> str:
    """Format property values into human-readable descriptions."""
    bool_codes = {"led_switch", "switch_led", "switch", "doorcontact_state"}
    if code in bool_codes:
        if code == "doorcontact_state":
            return "open" if value else "closed"
        return "on" if value else "off"

    mode_labels = {
        "white": "white mode", "colour": "color mode",
        "auto": "auto mode", "cold": "cooling mode", "hot": "heating mode",
    }
    if isinstance(value, str) and value in mode_labels:
        return mode_labels[value]

    return str(value)

@client.on_property_change
async def handle(device_id, properties):
    for prop in properties:
        t = TuyaDeviceMQClient.format_timestamp(prop["time"])
        readable = format_property_value(prop["code"], prop["value"])
        print(f"[{t}] Device {device_id} | {prop['code']}: {prop['value']} ({readable})")
```

### Online Status Monitor with Counters

```python
from collections import defaultdict

stats: dict[str, dict[str, int]] = defaultdict(lambda: {"online": 0, "offline": 0})

@client.on_online_status
async def handle(device_id, status, timestamp_ms):
    t = TuyaDeviceMQClient.format_timestamp(timestamp_ms)
    stats[device_id][status] += 1
    print(f"[{t}] Device {device_id}: {status}")
    s = stats[device_id]
    print(f"         Total: online {s['online']} times, offline {s['offline']} times")
```

### Event-Driven Automation with Throttling

Use case: "When the door sensor opens, turn on the hallway light."

```python
import time
import sys
sys.path.insert(0, "{baseDir}/scripts")
from tuya_device_mq_client import TuyaDeviceMQClient
from tuya_api import TuyaAPI

# Configuration
TRIGGER_DEVICE_ID = "your_trigger_device_id"  # e.g. door sensor
TRIGGER_CODE = "doorcontact_state"
TRIGGER_VALUE = True  # door opened

ACTION_DEVICE_ID = "your_action_device_id"  # e.g. hallway light
ACTION_PROPERTIES = {"switch_led": True}

NOTIFICATION_COOLDOWN_SECONDS = 30 * 60  # 30 minutes

last_notification_time: dict[str, float] = {}

def should_notify(event_key: str) -> bool:
    """Check whether a notification should be sent (throttle control)."""
    now = time.time()
    last_time = last_notification_time.get(event_key, 0)
    if now - last_time >= NOTIFICATION_COOLDOWN_SECONDS:
        last_notification_time[event_key] = now
        return True
    return False

api = TuyaAPI()

client = TuyaDeviceMQClient(
    api_key=os.environ["TUYA_API_KEY"],
    device_ids=[TRIGGER_DEVICE_ID],
)

@client.on_property_change
async def handle(device_id, properties):
    for prop in properties:
        if prop["code"] == TRIGGER_CODE and prop["value"] == TRIGGER_VALUE:
            # Execute device control via REST API
            api.issue_properties(ACTION_DEVICE_ID, ACTION_PROPERTIES)
            print(f"Automation triggered: turned on {ACTION_DEVICE_ID}")

            # Throttled notification
            event_key = f"{device_id}:{TRIGGER_CODE}"
            if should_notify(event_key):
                api.send_push("Automation Triggered", "Door opened — hallway light turned on.")
```

---

## Constraints

- **Server-side only** — credentials must never reach the frontend.
- **Notification throttling is mandatory** — property events fire frequently; minimum 30-minute cooldown for notifications.
- **Same API key** — uses `TUYA_API_KEY`, same as the REST API. No separate WebSocket credentials needed. URI auto-detected from key prefix for all 7 data centers.
- **Complementary to device control** — this handles real-time events; use `tuya_api.py` for device queries and commands.
