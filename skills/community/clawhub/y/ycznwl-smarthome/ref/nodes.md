# Node Reference

Nodes are the processing elements of a workflow. Each node lives in `flow_data.nodes[]`.

> **CRITICAL**: The node subtype field is `"node_subtype"`, NOT `"sub_type"`.
> Devices use `sub_type`, but nodes use `node_subtype`. Mixing them up will silently
> drop the subtype, causing validation failures like "未知节点类型 action:".

## Common Node Fields

```json
{
  "uuid": "placeholder-remapped-on-import",
  "node_type": "<type>",
  "node_subtype": "<subtype>",
  "label": "Human-readable name",
  "config": { ... },
  "enabled": true,
  "pos_x": 400,
  "pos_y": 200,
  "width": 0,
  "collapsed": false,
  "notes": ""
}
```

Only `uuid`, `node_type`, `node_subtype`, `label`, `config`, `enabled`, `pos_x`, `pos_y`
are required for import.

## ValueRef Structure

Several node configs use `ValueRef` to reference dynamic values:

```json
{
  "source": "<source_type>",
  "value": "<reference>"
}
```

| Source | Value format | Description |
|--------|-------------|-------------|
| `literal` | Any string | A hardcoded value, e.g. `"25"`, `"hello"` |
| `trigger` | Property path | Reference to trigger data, e.g. `"new_value"`, `"knx_value"` |
| `device` | `<uuid>.<property>` | Current value of a device property, e.g. `"abc123.temperature"` |
| `node_output` | `<node_uuid>` | Output of a previously executed node — **requires the server-assigned UUID**; only usable when editing an existing workflow (get UUIDs via `GET /automation/workflows/:uuid`), not in import payloads where UUIDs are placeholders |
| `variable` | `<key>` | A workflow variable set by `set_variable` node |

---

## Condition Nodes (`node_type: "condition"`)

Condition nodes evaluate to `true` or `false`. They have two output handles.

### device_state — Check Device Property

Checks the current value of a device property against a threshold.

**Config (`CfgDeviceState`)**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `device_uuid` | string | yes | UUID of the device |
| `property` | string | yes | Property to check (e.g. `power`, `temperature`, `brightness`) |
| `operator` | string | yes | Compare operator: `eq`, `ne`, `gt`, `lt`, `gte`, `lte`, `is_true`, `is_false` |
| `value` | string | depends | Compare threshold (not needed for `is_true`/`is_false`) |

**Output handles**: `true`, `false`

**Example — is light on?**:
```json
{
  "uuid": "n1",
  "node_type": "condition",
  "node_subtype": "device_state",
  "label": "Is Light On",
  "config": {
    "device_uuid": "light-uuid",
    "property": "power",
    "operator": "is_true",
    "value": ""
  },
  "enabled": true,
  "pos_x": 300, "pos_y": 200
}
```

**Example — temperature above 26°C?**:
```json
{
  "config": {
    "device_uuid": "temp-sensor-uuid",
    "property": "temperature",
    "operator": "gt",
    "value": "26"
  }
}
```

### numeric_compare — Compare Two Values

Compares two dynamic values using ValueRef.

**Config (`CfgNumericCompare`)**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `left` | ValueRef | yes | Left operand |
| `operator` | string | yes | `eq`, `ne`, `gt`, `lt`, `gte`, `lte` |
| `right` | ValueRef | yes | Right operand |

**Output handles**: `true`, `false`

**Example — trigger value > 50?**:
```json
{
  "config": {
    "left": { "source": "trigger", "value": "new_value" },
    "operator": "gt",
    "right": { "source": "literal", "value": "50" }
  }
}
```

### schedule_match — Time Window Check

Checks if the current time falls within a specified schedule. Each boundary (from/to)
can independently be a fixed clock time or a sun event (sunrise/sunset) with an offset.

**Config (`CfgScheduleMatch`)**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `days` | int[] | no | Days of week: 0=Sun, 1=Mon, ..., 6=Sat. Empty = all days |
| `from_type` | string | no | `"fixed"`, `"sunrise"`, or `"sunset"`. Default: `"fixed"` |
| `from` | string | no | Start time `"HH:MM"` (24h). Only used when `from_type` is `"fixed"`. Empty = 00:00 |
| `from_offset_min` | int | no | Offset in minutes for sun events (-720 to 720). Negative = before, positive = after |
| `to_type` | string | no | `"fixed"`, `"sunrise"`, or `"sunset"`. Default: `"fixed"` |
| `to` | string | no | End time `"HH:MM"` (24h). Only used when `to_type` is `"fixed"`. Empty = 23:59 |
| `to_offset_min` | int | no | Offset in minutes for sun events (-720 to 720) |
| `timezone` | string | no | Timezone, e.g. `"Asia/Shanghai"`. Empty = system default |

**Output handles**: `true`, `false`

**Note**: Sun-based boundaries require system geographic location to be configured
(via Settings → Location Config). If location is not configured, validation will report
a `system_location` error. Cross-midnight windows (e.g. sunset → sunrise) are supported.

**Example — weekdays 9AM to 6PM (fixed)**:
```json
{
  "config": {
    "days": [1, 2, 3, 4, 5],
    "from_type": "fixed",
    "from": "09:00",
    "to_type": "fixed",
    "to": "18:00"
  }
}
```

**Example — sunrise to sunset (daytime only)**:
```json
{
  "config": {
    "from_type": "sunrise",
    "to_type": "sunset"
  }
}
```

**Example — 30 min before sunset to sunrise (night mode with offset)**:
```json
{
  "config": {
    "from_type": "sunset",
    "from_offset_min": -30,
    "to_type": "sunrise"
  }
}
```

**Example — mixed: fixed start, end at sunset**:
```json
{
  "config": {
    "from_type": "fixed",
    "from": "08:00",
    "to_type": "sunset",
    "to_offset_min": -15
  }
}
```

---

## Action Nodes (`node_type: "action"`)

Action nodes perform operations. They have one output handle: `output`.

### device_control — Control a Device

Sends a control command to a device.

**Config (`CfgDeviceControl`)**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `device_uuid` | string | yes | UUID of the device to control |
| `action` | string | yes | Action name (see [devices.md](devices.md) for valid actions per device type) |
| `params` | object | no | Action parameters (see [devices.md](devices.md) for params per action) |

**CRITICAL**: The `action` and `params` must exactly match the device's capability.
Do NOT use generic names like `"set"` or `"switch"`. Use the exact action names from
[devices.md](devices.md).

**Example — turn on a light**:
```json
{
  "uuid": "n1",
  "node_type": "action",
  "node_subtype": "device_control",
  "label": "Turn On Light",
  "config": {
    "device_uuid": "light-uuid-here",
    "action": "turn_on",
    "params": {}
  },
  "enabled": true,
  "pos_x": 500, "pos_y": 200
}
```

**Example — set brightness to 50%**:
```json
{
  "config": {
    "device_uuid": "dimmer-uuid",
    "action": "set_brightness",
    "params": { "brightness": 50 }
  }
}
```

**Example — close curtain**:
```json
{
  "config": {
    "device_uuid": "curtain-uuid",
    "action": "close",
    "params": {}
  }
}
```

**Example — set AC to cool mode at 24°C**:
Two separate nodes needed — one for mode, one for temperature:
```json
{
  "config": {
    "device_uuid": "ac-uuid",
    "action": "set_mode",
    "params": { "mode": "cool" }
  }
}
```
```json
{
  "config": {
    "device_uuid": "ac-uuid",
    "action": "set_target_temperature",
    "params": { "target_temperature": 24 }
  }
}
```

**Example — using template in params** (resolve trigger value at runtime):
```json
{
  "config": {
    "device_uuid": "dimmer-uuid",
    "action": "set_brightness",
    "params": { "brightness": "{{trigger.new_value}}" }
  }
}
```

### notify — Send Notification

Sends a system notification or email.

**Config (`CfgNotify`)**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `channel` | string | yes | `"system"` or `"email"` |
| `title` | string | no | Notification title (default: "KNX Gateway" for email) |
| `body` | string | yes | Notification body (supports templates like `{{trigger.new_value}}`) |
| `level` | string | no | For system: `"info"`, `"warning"`, `"error"`. Default: `"info"` |
| `smtp_host` | string | for email | SMTP server address (e.g. `"smtp.exmail.qq.com"`) |
| `smtp_port` | int | for email | SMTP port (e.g. `587` for STARTTLS, `465` for SSL) |
| `smtp_user` | string | for email | SMTP login username |
| `smtp_pass` | string | for email | SMTP login password |
| `smtp_ssl` | bool | no | Use implicit TLS/SSL (port 465). Default: false (STARTTLS) |
| `email_to` | string | for email | Recipient email address |

**Example — system notification**:
```json
{
  "config": {
    "channel": "system",
    "body": "Temperature exceeded threshold: {{trigger.new_value}}°C",
    "level": "warning"
  }
}
```

> **Security**: Email notifications transmit notification content to an external SMTP
> server. Store SMTP credentials in environment variables rather than hardcoding them
> in the workflow config.

**Example — email notification**:
```json
{
  "config": {
    "channel": "email",
    "title": "Temperature Alert",
    "body": "Current temperature is {{trigger.new_value}}°C",
    "smtp_host": "smtp.example.com",
    "smtp_port": 587,
    "smtp_user": "user@example.com",
    "smtp_pass": "SMTP_PASSWORD_PLACEHOLDER",
    "smtp_ssl": false,
    "email_to": "admin@example.com"
  }
}
```

### mqtt_publish — Publish MQTT Message

Publishes a message to an MQTT broker.

> **Security**: If `broker_uri` points outside the trusted LAN, device data is transmitted over
> the network. Use TLS (`ssl://`) for non-local brokers and avoid `tls_skip_verify: true`
> in production.

**Config (`CfgMqttPublish`)**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `topic` | string | yes | MQTT topic |
| `payload` | string | yes | Message payload (supports templates) |
| `broker_uri` | string | no | Broker URI (default: `tcp://localhost:1883`). Supports `tcp://`, `ssl://`, `tls://` |
| `username` | string | no | MQTT auth username |
| `password` | string | no | MQTT auth password |
| `tls_skip_verify` | bool | no | Skip TLS certificate verification |
| `qos` | int | no | QoS level: 0, 1, or 2. Default: 0 |
| `retain` | bool | no | Retain message. Default: false |

**Example — publish to local broker**:
```json
{
  "config": {
    "topic": "home/living-room/temperature",
    "payload": "{{trigger.new_value}}"
  }
}
```

### http_request — HTTP Request

Makes an HTTP request to a reviewed URL.

> **Security**: This node sends data outside the local network. Verify the target URL and
> any included headers or body content before enabling the workflow. Do not use URLs from
> untrusted workflow sources.

**Config (`CfgHttpRequest`)**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `method` | string | yes | HTTP method: `GET`, `POST`, `PUT`, `DELETE` |
| `url` | string | yes | Target URL |
| `headers` | object | no | Key-value header pairs |
| `body` | string | no | Request body (supports templates) |
| `timeout_s` | int | no | Request timeout in seconds. Default: 30 |

**Example**:
```json
{
  "config": {
    "method": "POST",
    "url": "http://lan-notifier.local/api/events",
    "headers": { "Content-Type": "application/json" },
    "body": "{\"temperature\": {{trigger.new_value}}}",
    "timeout_s": 10
  }
}
```

### knx_send — Send KNX Telegram

Sends one or more KNX group write/response telegrams.

**Config (`CfgKnxSend`)**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `targets` | array | yes | Array of KNX send targets |

Each target:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `address` | string | yes | KNX group address (e.g. `"1/2/3"`) |
| `command_type` | string | yes | `"write"` or `"response"` |
| `dpt` | string | yes | KNX DPT (e.g. `"1.001"`, `"5.001"`, `"9.001"`) |
| `value` | ValueRef | yes | Value to send |

**Example — turn on KNX switch**:
```json
{
  "config": {
    "targets": [{
      "address": "1/1/1",
      "command_type": "write",
      "dpt": "1.001",
      "value": { "source": "literal", "value": "1" }
    }]
  }
}
```

**Example — set KNX dimmer to trigger value**:
```json
{
  "config": {
    "targets": [{
      "address": "1/2/1",
      "command_type": "write",
      "dpt": "5.001",
      "value": { "source": "trigger", "value": "new_value" }
    }]
  }
}
```

### scene_exec — Execute a Scene

Executes a scene by UUID. Runs all device actions configured in the scene,
with error tolerance (partial failures do not block remaining actions).

**Config (`CfgSceneExec`)**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `scene_uuid` | string | yes | UUID of the scene to execute (from `GET /scenes`) |

**Output**: Returns execution result with success/failure counts.

**Output data**:
```json
{
  "scene_uuid": "a1b2c3d4-...",
  "success": true,
  "actions_executed": 5,
  "actions_failed": 0,
  "duration_ms": 320
}
```

**Example**:
```json
{
  "uuid": "n1",
  "node_type": "action",
  "node_subtype": "scene_exec",
  "label": "Run Good Night Scene",
  "config": {
    "scene_uuid": "SCENE_UUID_GOOD_NIGHT"
  },
  "enabled": true,
  "pos_x": 500, "pos_y": 200
}
```

> **scene_exec vs device_control for scenes**: Both can trigger a scene.
> - `scene_exec` takes a `scene_uuid` directly — simpler, purpose-built.
> - `device_control` with a virtual scene device UUID + `action: "activate_scene"` works
>   identically but uses the generic device control path.
> Prefer `scene_exec` in automation workflows for clarity.

### set_variable — Set Workflow Variable

Stores a value in the workflow execution context for use by downstream nodes.

> **Note**: `set_variable` is categorized as an `action` node type but does not control any device.
> The stored value is accessible downstream via the `{{var.<key>}}` template or `{ "source": "variable", "value": "<key>" }` ValueRef.

**Config (`CfgSetVariable`)**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `key` | string | yes | Variable name |
| `value` | ValueRef | yes | Value to store |

**Example**:
```json
{
  "config": {
    "key": "threshold",
    "value": { "source": "literal", "value": "25" }
  }
}
```

---

## Logic Nodes (`node_type: "logic"`)

Logic nodes combine boolean inputs from upstream condition nodes.
They require at least 2 incoming edges from condition nodes (NOT directly from triggers).

**Output handles**: `true`, `false`

### and — All Inputs True

```json
{
  "uuid": "n1",
  "node_type": "logic",
  "node_subtype": "and",
  "label": "All Conditions",
  "config": {},
  "enabled": true,
  "pos_x": 500, "pos_y": 200
}
```

### or — Any Input True

```json
{
  "uuid": "n1",
  "node_type": "logic",
  "node_subtype": "or",
  "label": "Any Condition",
  "config": {},
  "enabled": true,
  "pos_x": 500, "pos_y": 200
}
```

**Validation rule**: Logic nodes must NOT directly receive edges from triggers. Always
place a condition node between a trigger and a logic node.

---

## Delay Nodes (`node_type: "delay"`)

Delay nodes pause execution for a specified duration.

**Output handle**: `output`

### fixed_delay — Fixed Wait

**Config (`CfgFixedDelay`)**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `seconds` | int | yes | Delay duration in seconds. Must not exceed `workflow.timeout_s` |

```json
{
  "uuid": "n1",
  "node_type": "delay",
  "node_subtype": "fixed_delay",
  "label": "Wait 10s",
  "config": { "seconds": 10 },
  "enabled": true,
  "pos_x": 400, "pos_y": 200
}
```

**Validation rule**: `seconds` must be ≤ the workflow's `timeout_s`.

---

## Transform Nodes (`node_type: "transform"`)

Transform nodes modify data flowing through the workflow.

**Output handle**: `output`

### value_map — Map Values

Maps input values to output values using a lookup table.

**Config (`CfgValueMap`)**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `input` | ValueRef | yes | Input value to look up |
| `mapping` | object | yes | Key-value mapping `{ "input": "output" }` |
| `default` | string | no | Default output if no mapping matches |
| `output_key` | string | yes | Name for the output variable |

**Example — map motion to actions**:
```json
{
  "config": {
    "input": { "source": "trigger", "value": "new_value" },
    "mapping": {
      "true": "occupied",
      "false": "vacant"
    },
    "default": "unknown",
    "output_key": "room_status"
  }
}
```

The mapped result is stored as a workflow variable. Access it in downstream nodes:
- Template syntax: `{{var.room_status}}`
- ValueRef: `{ "source": "variable", "value": "room_status" }`

---

## Template Syntax

String values in node configs support Go template syntax for dynamic values:

| Template | Resolves to |
|----------|-------------|
| `{{trigger.new_value}}` | New value from trigger event |
| `{{trigger.old_value}}` | Previous value |
| `{{trigger.device_uuid}}` | Trigger device UUID |
| `{{trigger.device_name}}` | Trigger device name |
| `{{trigger.property}}` | Trigger property name |
| `{{trigger.knx_value}}` | KNX trigger parsed value |
| `{{trigger.knx_address}}` | KNX trigger group address |
| `{{var.key_name}}` | Workflow variable |

Templates work in: `body`, `payload`, `url`, `params` string values, and ValueRef `value` fields.
