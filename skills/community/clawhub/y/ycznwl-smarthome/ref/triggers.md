# Trigger Reference

Triggers are the entry points of a workflow. Each workflow can have 1–5 triggers.
Triggers live in `flow_data.triggers[]`.

## Common Trigger Fields

Every trigger has these fields:

```json
{
  "uuid": "placeholder-remapped-on-import",
  "trigger_type": "<type>",
  "label": "Human-readable name",
  "enabled": true,
  "pos_x": 100,
  "pos_y": 200
}
```

## Compare Operators

Used by `device_event` and `knx_group_event` triggers:

| Operator | Meaning | Works on |
|----------|---------|----------|
| `changed` | Value changed (any change fires) | Any |
| `eq` | Equal | Numbers, strings |
| `ne` | Not equal | Numbers, strings |
| `gt` | Greater than | Numbers |
| `lt` | Less than | Numbers |
| `gte` | Greater than or equal | Numbers |
| `lte` | Less than or equal | Numbers |
| `is_true` | Truthy check (not 0, not false, not empty) | Booleans, numbers |
| `is_false` | Falsy check (0, false, empty, null) | Booleans, numbers |

**Important**: For boolean device properties (like `power`, `motion`, `contact`), the
value is normalized before comparison. `true`/`1`/`"true"` → `1`, `false`/`0`/`"false"` → `0`.
So `gte` with value `"1"` and `is_true` both correctly match "on" / "true" states.

---

## 1. manual — Manual Trigger

Fires when a user clicks "Execute" in the UI or calls the execute API.

**Extra fields**: none

```json
{
  "uuid": "t1",
  "trigger_type": "manual",
  "label": "Manual Run",
  "enabled": true,
  "pos_x": 100, "pos_y": 200
}
```

---

## 2. device_event — Device State Change

Fires when a device property changes and the compare condition is met.

**Extra fields**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `device_uuid` | string | yes | UUID of the device to monitor |
| `device_property` | string | yes | Property name to watch (e.g. `power`, `temperature`, `brightness`) |
| `compare_op` | string | yes | Compare operator (see table above) |
| `compare_value` | string | for most ops | Compare threshold. Not needed for `changed`, `is_true`, `is_false` |

**Trigger data available at runtime**:
- `trigger.device_uuid` — the device UUID
- `trigger.property` — the property name
- `trigger.old_value` — previous value
- `trigger.new_value` — new value
- `trigger.device_status` — full device status map

```json
{
  "uuid": "t1",
  "trigger_type": "device_event",
  "label": "Temperature Above 25",
  "enabled": true,
  "device_uuid": "sensor-uuid-here",
  "device_property": "temperature",
  "compare_op": "gte",
  "compare_value": "25",
  "pos_x": 100, "pos_y": 200
}
```

### Common device_event patterns

**Light turned on**:
```json
{
  "device_uuid": "light-uuid",
  "device_property": "power",
  "compare_op": "is_true",
  "compare_value": ""
}
```

**Motion detected**:
```json
{
  "device_uuid": "motion-sensor-uuid",
  "device_property": "motion",
  "compare_op": "is_true",
  "compare_value": ""
}
```

**Temperature dropped below 18°C**:
```json
{
  "device_uuid": "temp-sensor-uuid",
  "device_property": "temperature",
  "compare_op": "lt",
  "compare_value": "18"
}
```

**Any brightness change**:
```json
{
  "device_uuid": "dimmer-uuid",
  "device_property": "brightness",
  "compare_op": "changed",
  "compare_value": ""
}
```

---

## 3. cron — Scheduled Trigger

Fires on a cron schedule. Supports standard 5-field cron (minute, hour, day, month, weekday)
and 6-field cron with seconds.

**Extra fields**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `cron_expr` | string | yes | Cron expression |

```json
{
  "uuid": "t1",
  "trigger_type": "cron",
  "label": "Every Day 8AM",
  "enabled": true,
  "cron_expr": "0 8 * * *",
  "pos_x": 100, "pos_y": 200
}
```

### Cron expression examples

| Expression | Meaning |
|-----------|---------|
| `* * * * *` | Every minute |
| `0 8 * * *` | Daily at 8:00 AM |
| `0 8 * * 1-5` | Weekdays at 8:00 AM |
| `0 0 1 * *` | First day of month at midnight |
| `*/5 * * * *` | Every 5 minutes |
| `0 18 * * 0,6` | Weekends at 6:00 PM |
| `0 0 8 * * *` | 6-field: Daily at 8:00:00 AM (with seconds) |

---

## 4. knx_group_event — KNX Group Telegram

Fires when a KNX group write/read/response matches the configured addresses.

**Extra fields**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `knx_addresses` | string[] | yes | List of KNX group addresses to monitor (e.g. `["1/2/3"]`) |
| `knx_event_types` | string[] | no | Event types to filter: `"write"`, `"read"`, `"response"`. Empty = all |
| `knx_dpt` | string | no | KNX DPT for value parsing (e.g. `"1.001"`, `"9.001"`, `"5.001"`) |
| `compare_op` | string | no | Compare operator for parsed value |
| `compare_value` | string | no | Compare threshold |

**Trigger data available at runtime**:
- `trigger.knx_address` — the matching group address
- `trigger.knx_command` — the command type (write/read/response)
- `trigger.knx_dpt` — the DPT used for parsing
- `trigger.knx_value` — the parsed value
- `trigger.knx_source` — the source KNX address

```json
{
  "uuid": "t1",
  "trigger_type": "knx_group_event",
  "label": "KNX Switch Input",
  "enabled": true,
  "knx_addresses": ["1/2/3"],
  "knx_event_types": ["write"],
  "knx_dpt": "1.001",
  "compare_op": "is_true",
  "compare_value": "",
  "pos_x": 100, "pos_y": 200
}
```

### Common KNX DPT types

| DPT | Type | Description | Value range |
|-----|------|-------------|-------------|
| `1.001` | Boolean (Switch) | On/Off | 0 or 1 |
| `1.002` | Boolean | True/False | 0 or 1 |
| `1.008` | Boolean (Up/Down) | Up/Down | 0 or 1 |
| `5.001` | 8-bit unsigned (Percentage) | 0–100% | 0–100 |
| `5.010` | 8-bit unsigned (Counter) | Pulse counter | 0–255 |
| `9.001` | 2-byte float (Temperature) | Temperature °C | -273 to 670760 |
| `9.004` | 2-byte float (Illuminance) | Lux | 0–670760 |
| `9.007` | 2-byte float (Humidity) | Humidity % | 0–670760 |
| `14.056` | 4-byte float (Power) | Watts | float |

---

## 5. sun_event — Sunrise/Sunset

Fires at sunrise or sunset, calculated from the system's geographic location
(latitude/longitude). Supports an optional minute offset for triggering before
or after the actual event.


**Scheduling behavior**:
- **Zero offset** (`sun_offset_min: 0` or omitted): triggered by the system
  monitor's sunrise/sunset event bus (accurate to ~30 seconds).
- **Non-zero offset**: uses per-trigger timer scheduling — computes the exact
  next fire time daily based on astronomical data, re-schedules automatically
  after each firing and when the system location changes.

**Extra fields**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `sun_event` | string | yes | `"sunrise"` or `"sunset"` |
| `sun_offset_min` | int | no | Offset in minutes (negative = before, positive = after). Range: -720 to 720. Default: 0 |

**Trigger data available at runtime**:
- `trigger.new_value` — `"sunrise"` or `"sunset"`
- `trigger.source` — `"system"`

```json
{
  "uuid": "t1",
  "trigger_type": "sun_event",
  "label": "30 min before sunset",
  "enabled": true,
  "sun_event": "sunset",
  "sun_offset_min": -30,
  "pos_x": 100, "pos_y": 200
}
```

**Example — at sunrise (no offset)**:
```json
{
  "uuid": "t1",
  "trigger_type": "sun_event",
  "label": "Sunrise",
  "enabled": true,
  "sun_event": "sunrise",
  "pos_x": 100, "pos_y": 200
}
```

---

## 6. webhook — Inbound HTTP Trigger

Fires when the workflow's webhook URL is called by an approved client.

Use webhook triggers only when the user explicitly wants inbound HTTP access to
the gateway workflow. Keep the token in the gateway configuration or secret store;
do not place a real token in documentation or shared workflow examples.

**Extra fields**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `webhook_token` | string | yes | Secret token for the webhook URL |

```json
{
  "uuid": "t1",
  "trigger_type": "webhook",
  "label": "Inbound Trigger",
  "enabled": true,
  "webhook_token": "WEBHOOK_TOKEN_PLACEHOLDER",
  "pos_x": 100, "pos_y": 200
}
```

**Trigger data available at runtime**:
- `trigger.webhook_payload` — the JSON body sent to the webhook
