# Scene Reference

## What is a Scene?

A scene is a reusable collection of device actions that execute together as a group.
When triggered, the system runs all actions in order (respecting per-action delays).
If an intermediate action fails, remaining actions still execute (error tolerance).

Each scene auto-creates a **virtual device** (`protocol: "scene"`) that allows it to
be controlled through the standard device control API and used in automation workflows.

---

## Scene Data Model

```json
{
  "id": 1,
  "uuid": "a1b2c3d4-e5f6-...",
  "name": "Good Night",
  "description": "Turn off all lights and close curtains",
  "icon": "moon",
  "color": "#6366F1",
  "actions": [ ... ],
  "knx_bind_address": "",
  "knx_bind_dpt": "",
  "knx_scene_id": null,
  "device_uuid": "scene-a1b2c3d4-e5f6-...",
  "enabled": true,
  "sort_order": 0,
  "exec_total": 42,
  "exec_success": 40,
  "exec_fail": 2,
  "last_exec_at": "2026-04-07T10:30:00Z",
  "created_at": "2026-03-01T08:00:00Z",
  "updated_at": "2026-04-07T10:30:00Z"
}
```

### Core Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `name` | string | **yes** | — | Scene name (max 100 chars) |
| `description` | string | no | `""` | Description (max 500 chars) |
| `icon` | string | no | `"home"` | Icon identifier (Material/Lucide name, e.g. `"moon"`, `"sun"`, `"play"`) |
| `color` | string | no | `"#3B82F6"` | Hex color for UI display |
| `actions` | array | no | `[]` | Device actions to execute (see below) |
| `enabled` | bool | no | `true` | Whether the scene can be executed |

### KNX Binding Fields (optional)

These fields bind a scene to a physical KNX scene controller so that
pressing a button on the KNX panel triggers the software scene.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `knx_bind_address` | string | no | KNX group address to listen on (e.g. `"1/2/3"`) |
| `knx_bind_dpt` | string | no | KNX DPT for value parsing. Use `"18.001"` (Scene Control) for KNX scene panels |
| `knx_scene_id` | int\|null | no | Scene number (0–63) from the KNX panel. `null` = not bound |

**DPT 18.001 (Scene Control)**: This is a call-only KNX datapoint — the gateway
receives scene activation commands from KNX panels but does not learn/store scenes
on the KNX side. When a KNX panel sends scene number N to the bound address,
the gateway matches `knx_scene_id == N` and executes the scene's actions.

**Example — bind scene to KNX wall panel**:
```json
{
  "name": "Living Room Evening",
  "knx_bind_address": "1/7/0",
  "knx_bind_dpt": "18.001",
  "knx_scene_id": 3,
  "actions": [ ... ]
}
```
When the KNX panel sends scene 3 to group address `1/7/0`, this scene executes.

### Auto-Generated Fields (read-only)

| Field | Description |
|-------|-------------|
| `uuid` | Server-generated UUID for the scene |
| `device_uuid` | UUID of the auto-created virtual device (`scene-<uuid>`) |
| `sort_order` | Display order in the UI |
| `exec_total` | Total execution count |
| `exec_success` | Successful execution count |
| `exec_fail` | Failed execution count |
| `last_exec_at` | Timestamp of last execution |

---

## Actions Array

The `actions` field is a JSON array of device actions. Each action represents one
command to send to a device.

### Action Structure

```json
{
  "id": "a1",
  "device_uuid": "light-living-room-uuid",
  "device_name": "Living Room Light",
  "action": "turn_off",
  "params": {},
  "delay": 0
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | **yes** | Unique action ID within the scene (e.g. `"a1"`, `"a2"`) |
| `device_uuid` | string | **yes** | UUID of the target device (from `GET /devices`) |
| `device_name` | string | **yes** | Display name of the device (for UI rendering) |
| `action` | string | **yes** | Device action name — must match device capability (see [devices.md](devices.md)) |
| `params` | object | **yes** | Action parameters — must match action schema (see [devices.md](devices.md)) |
| `delay` | int | no | Delay in milliseconds before executing this action. `0` = immediate |

### Action/Params Reference by Device Type

Actions and params must exactly match what the device supports. Always cross-reference
with [devices.md](devices.md). Common patterns:

| Device Type | Action | Params | Example |
|-------------|--------|--------|---------|
| `light` | `turn_on` | `{}` | Turn on a light |
| `light` | `turn_off` | `{}` | Turn off a light |
| `light_dimmer` | `set_brightness` | `{ "brightness": 50 }` | Set to 50% (auto powers light on) |
| `light_tunable` | `set_color_temperature` | `{ "color_temperature": 3000 }` | Set warm white (range 1000–10000 K, see [devices.md](devices.md)) |
| `light_rgb` | `set_color` | `{ "color": "#FF8800" }` | Set hex color (NOT `hue`/`saturation`) |
| `curtain` | `close` | `{}` | Close curtain |
| `curtain` | `set_position` | `{ "position": 50 }` | Half open |
| `blind` | `set_slat_position` | `{ "slat_position": 45 }` | Tilt slats |
| `ac` | `set_mode` | `{ "mode": "cool" }` | Cooling mode |
| `ac` | `set_target_temperature` | `{ "target_temperature": 24 }` | Set to 24°C |
| `ac` | `set_fan_speed_mode` | `{ "fan_speed_mode": "high" }` | AC default enum: `auto/low/medium/high` |
| `fan` | `set_fan_speed` | `{ "fan_speed": 70 }` | 70% speed |
| `fan` | `set_fan_speed_mode` | `{ "fan_speed_mode": "level2" }` | Fan default enum: `level1/level2/level3` (NOT `low/high` — see [devices.md](devices.md#fan_speed--fan-speed-control)) |
| `switch` | `turn_off` | `{}` | Turn off outlet |
| `lock` | `lock` | `{}` | Lock door |

### Execution Behavior

1. Actions execute **sequentially** in array order
2. Each action's `delay` is waited **before** that action executes
3. **Error tolerance**: If an action fails (device offline, invalid params), execution
   continues with the next action. The final result reports both `actions_executed` and
   `actions_failed`
4. Disabled scenes (`enabled: false`) cannot be executed — the API returns an error

### Example — Complete "Good Night" Scene

```json
{
  "name": "Good Night",
  "description": "Prepare house for sleep",
  "icon": "moon",
  "color": "#6366F1",
  "actions": [
    {
      "id": "a1",
      "device_uuid": "light-living-uuid",
      "device_name": "Living Room Light",
      "action": "turn_off",
      "params": {},
      "delay": 0
    },
    {
      "id": "a2",
      "device_uuid": "light-bedroom-uuid",
      "device_name": "Bedroom Light",
      "action": "set_brightness",
      "params": { "brightness": 10 },
      "delay": 0
    },
    {
      "id": "a3",
      "device_uuid": "curtain-living-uuid",
      "device_name": "Living Room Curtain",
      "action": "close",
      "params": {},
      "delay": 500
    },
    {
      "id": "a4",
      "device_uuid": "ac-bedroom-uuid",
      "device_name": "Bedroom AC",
      "action": "set_target_temperature",
      "params": { "target_temperature": 26 },
      "delay": 0
    },
    {
      "id": "a5",
      "device_uuid": "ac-bedroom-uuid",
      "device_name": "Bedroom AC",
      "action": "set_mode",
      "params": { "mode": "fan_only" },
      "delay": 0
    },
    {
      "id": "a6",
      "device_uuid": "lock-front-uuid",
      "device_name": "Front Door Lock",
      "action": "lock",
      "params": {},
      "delay": 1000
    }
  ],
  "enabled": true
}
```

---

## Execution Result

When a scene is executed (via `POST /scenes/:uuid/execute`, automation `scene_exec`
node, or device control `activate_scene`), the response includes:

```json
{
  "success": true,
  "actions_executed": 6,
  "actions_failed": 0,
  "duration_ms": 1650,
  "errors": []
}
```

| Field | Type | Description |
|-------|------|-------------|
| `success` | bool | `true` if all actions succeeded, `false` if any failed |
| `actions_executed` | int | Number of actions that completed successfully |
| `actions_failed` | int | Number of actions that failed |
| `duration_ms` | int | Total execution time in milliseconds (including delays) |
| `errors` | array | Error messages from failed actions |

---

## Execution Logs

Each execution is recorded in the execution log. Query via:

```
GET /scenes/logs?scene_uuid=xxx&limit=50&offset=0
```

Log entry format:
```json
{
  "id": 1,
  "scene_uuid": "a1b2c3d4-...",
  "scene_name": "Good Night",
  "source": "manual",
  "success": true,
  "duration_ms": 1650,
  "actions_executed": 6,
  "actions_failed": 0,
  "error_message": "",
  "created_at": "2026-04-08T23:00:00Z"
}
```

| Source | Description |
|--------|-------------|
| `manual` | Triggered from the web UI or `POST /scenes/:uuid/execute` |
| `knx` | Triggered by a KNX panel via the bound address |
| `automation` | Triggered from an automation workflow (`scene_exec` node) |

---

## Virtual Scene Device

Each scene automatically creates a virtual device that appears in `GET /devices`:

| Property | Value |
|----------|-------|
| `uuid` | `scene-<scene_uuid>` |
| `type` | `scene` |
| `sub_type` | `scene` |
| `protocol` | `scene` |
| `instance_name` | `scene` |
| `is_online` | always `true` |
| `capabilities` | `["scene"]` |

Virtual scene devices support one action:

| Action | Description |
|--------|-------------|
| `activate_scene` | Execute the scene (same as `POST /scenes/:uuid/execute`) |

Scene enable/disable is managed via the dedicated API (`POST /scenes/:uuid/toggle`), not through device control.

This allows scenes to be triggered through the standard device control API:
```
POST /devices/:id/control
{ "action": "activate_scene", "params": {} }
```

And used in automation workflows via `device_control` nodes (though `scene_exec` is preferred).
