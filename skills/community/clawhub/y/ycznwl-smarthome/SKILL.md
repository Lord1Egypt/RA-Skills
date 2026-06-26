---
name: ycznwl-smarthome
description: >-
  Create, edit, validate, and manage KNX Gateway automation workflows and scenes
  via REST API. Covers device listing, device control, scene CRUD/execution,
  workflow CRUD, import/export, trigger/node configuration, and workflow lifecycle
  (enable/disable/execute). Use when building or modifying automations, generating
  workflows for import, creating/executing scenes, or controlling devices
  programmatically. Use when the user says "create automation", "build workflow",
  "control device", "automation API", "create scene", or "execute scene".
version: 1.0.6
compatibility: Requires network access to a user-provided KNX Gateway on a trusted LAN or VPN.
metadata:
  openclaw:
    requires:
      env:
        - KNX_TOKEN
    primaryEnv: KNX_TOKEN
    always: false
    homepage: https://github.com/tmpbin/knx-gateway-skills
---

# YCZNWL KNX Gateway Automation Agent Skill

## Connection

| Parameter | Default | Description |
|-----------|---------|-------------|
| Base URL  | `http://ycznwl.local/api/v1` | Default mDNS address — use as-is unless the user provides their own gateway address or IP |
| Auth      | `Authorization: Bearer ${KNX_TOKEN}` | See token instructions below |
| Encoding  | `UTF-8` | The gateway accepts and emits UTF-8 only. Always send `Content-Type: application/json; charset=utf-8` and decode responses as UTF-8. Names, descriptions, room names, action names, and any free-text fields may contain Chinese characters and **must** be transmitted/parsed as UTF-8. Do not URL-encode JSON payloads or wrap them in an extra encoding layer. |

### Getting an API Token

1. Open the KNX Gateway web UI
2. Click your avatar (top-right) → **Get API Token**
3. Copy the token

**Safe token handling**:
- Store the token in your platform's secret store or a local environment variable (`export KNX_TOKEN=...`) — never paste it directly into a chat conversation, as conversation logs may be persisted
- Reference it in requests via the environment variable, not inline
- Never hardcode the token in shared scripts or commit it to version control

This skill's only required credential is `KNX_TOKEN`. Optional workflow nodes that
send data outside the gateway or trusted LAN must be configured only after an
explicit user request and endpoint review. Do not introduce hardcoded secrets
into skill files or workflow examples.

Default safety policy: keep automations local to the gateway and trusted LAN.
Only author or enable off-LAN HTTP, MQTT, webhook, or email integrations when
the user explicitly asks for that integration and approves the exact endpoint.

## Reference Documents

This skill is organized into progressive reference files. Read them in order when you
need detailed information:

| File | Content |
|------|---------|
| [ref/devices.md](ref/devices.md) | Device types, subtypes, capabilities, actions, params |
| [ref/scenes.md](ref/scenes.md) | **Scene data model, actions structure, KNX binding, execution behavior** |
| [ref/triggers.md](ref/triggers.md) | Trigger types and their exact configuration (incl. `sun_event` with offset scheduling) |
| [ref/nodes.md](ref/nodes.md) | Node types, subtypes (incl. `scene_exec`, `schedule_match` with sunrise/sunset boundaries), config structs, validation rules |
| [ref/api.md](ref/api.md) | Complete REST API endpoint reference (devices, scenes, automation, system location/sun times) |
| [ref/examples.md](ref/examples.md) | Realistic, validated workflow examples (incl. scene-based) |

## Quick Start — Agent Workflow

### Creating a new scene

1. **Discover devices**: `GET /devices` → note `uuid`, `name`, `type`, `capabilities`, and `room_id` (resolve via `GET /rooms`)
2. **Build actions array**: Each action targets a device:
   ```json
   {
     "id": "a1",
     "device_uuid": "light-uuid",
     "device_name": "Living Room Light",
     "action": "turn_off",
     "params": {},
     "delay": 0
   }
   ```
   - `action` + `params` must match the device's capability (see [ref/devices.md](ref/devices.md))
   - `delay` is in milliseconds (0 = immediate, 500 = 0.5s delay before this action)
   - `id` is a unique string per action (e.g. `"a1"`, `"a2"`)

#### Scene authoring best practices

- **Brightness implies power on (dimmable lights only)**: For lights with brightness control
  (`light_dimmer`, `light_tunable`, `light_rgb`), sending `set_brightness` with `brightness > 0`
  automatically powers the light on at the firmware/handler level. **Do not emit a separate
  `turn_on` action before `set_brightness`** — it adds latency and a redundant KNX telegram.
  Sending `set_brightness` with `brightness: 0` will likewise turn the light off. Use an explicit
  `turn_on` / `turn_off` only when the device has no brightness capability.
- **Multi-room scenes — prefix `device_name` with the room name**: When a scene spans multiple
  rooms, prepend the room name to the action's display name so the execution log and UI are
  readable. Example: `"device_name": "客厅·主灯"` instead of just `"主灯"`. Single-room scenes
  may keep the bare device name. The room name comes from `GET /rooms` joined on `device.room_id`.
  This applies to both scene actions (`actions[].device_name`) and any `name` you set on
  automation `device_control` / `scene_exec` action nodes.
- **Color temperature range**: Devices can be configured for any range within `1000–10000 K`
  with a configurable step. The backend clamps & step-aligns values automatically — but pass
  reasonable values that the user has actually configured for the device.

3. **Create**: `POST /scenes` with `name`, `actions`, optional `icon`, `color`, `description`, `enabled`
4. **Test**: `POST /scenes/:uuid/execute` → verify execution result

### Editing an existing scene

1. **Get current state**: `GET /scenes/:uuid`
2. **Update**: `PUT /scenes/:uuid` with partial fields:
   ```json
   {
     "name": "Updated Scene Name",
     "actions": [ ... ],
     "enabled": true
   }
   ```
   Only include fields you want to change. The `actions` array replaces the existing one entirely.
3. **Test**: `POST /scenes/:uuid/execute`

### Managing scenes

| Operation | Method | Endpoint |
|-----------|--------|----------|
| List all scenes | `GET` | `/scenes` (optional `?enabled=true`) |
| Get scene | `GET` | `/scenes/:uuid` |
| Create | `POST` | `/scenes` |
| Update | `PUT` | `/scenes/:uuid` |
| Delete | `DELETE` | `/scenes/:uuid` |
| Execute | `POST` | `/scenes/:uuid/execute` |
| Toggle enabled | `POST` | `/scenes/:uuid/toggle` |
| Reorder | `PUT` | `/scenes/sort` |
| View logs | `GET` | `/scenes/logs?scene_uuid=xxx` |

See [ref/api.md](ref/api.md) for full request/response details.

### Using scenes in automations

Scenes can be triggered from automation workflows in two ways:
- **`scene_exec` node** (recommended): `{ "node_subtype": "scene_exec", "config": { "scene_uuid": "..." } }`
- **`device_control` node** with virtual device: `{ "config": { "device_uuid": "scene-<scene_uuid>", "action": "activate_scene" } }`

See [ref/examples.md](ref/examples.md) Examples 7 & 8 for complete workflow payloads.

### Creating a new automation

1. **Discover devices**: `GET /devices` → note `uuid`, `type`, `sub_type`, `capabilities`
2. **Discover scenes** (if needed): `GET /scenes` → note scene `uuid` for `scene_exec` nodes
3. **Build import JSON** using the format documented in [ref/api.md](ref/api.md) section "Import"
4. **Import**: `POST /automation/workflows/import` → returns new workflow with server-generated UUIDs
5. **Validate**: `POST /automation/workflows/:uuid/validate`
6. **Enable**: `POST /automation/workflows/:uuid/enable`

### Manually executing an automation — REQUIRES a manual trigger

`POST /automation/workflows/:uuid/execute` can only fire **enabled** triggers of type
`manual`. If the workflow has no manual trigger (e.g. only `device_event`, `cron`,
`sun_event`, `knx_group_event`, or `webhook` triggers), the call returns
`no enabled manual trigger found in workflow ...` and nothing executes.

**Rule**: If the user wants the workflow to be runnable on demand from the UI or via the
API (e.g. a "test" button, a chatbot command, a script), include at least one
`{ "trigger_type": "manual", "enabled": true }` trigger in the import JSON. You may combine
it with other triggers — they remain independent.

```json
{
  "triggers": [
    { "uuid": "t-manual", "trigger_type": "manual", "enabled": true, "config": {} },
    { "uuid": "t-cron",   "trigger_type": "cron",   "enabled": true, "config": { "expression": "0 7 * * *" } }
  ]
}
```

A workflow without a manual trigger still runs automatically when its other triggers fire —
it just cannot be invoked through `POST /workflows/:uuid/execute`.

### Editing an existing automation

1. **Get current state**: `GET /automation/workflows/:uuid`
2. **Modify** triggers/nodes/edges — keep existing UUIDs for unchanged elements, generate new UUIDs for additions
3. **Save**: `PUT /automation/workflows/:uuid`
4. **Validate**: `POST /automation/workflows/:uuid/validate`

## Security Notes

- **Imported workflows**: Always inspect imported workflow JSON before enabling. Look for
  unexpected off-LAN HTTP requests, MQTT brokers outside the trusted LAN, or webhook
  triggers exposed beyond the gateway network. Only import workflows from sources you trust.
- **Network egress**: Prefer gateway-local and LAN-local workflows. HTTP request,
  MQTT publish, webhook, and email integrations are advanced gateway features; use them
  only when the user explicitly asks and the destination is reviewed.
- **Webhook triggers**: Exposing a webhook URL can make the gateway reachable from outside
  its normal network. Use only when network exposure is deliberate and the token is kept secret.
- **Base URL**: Verify the gateway address resolves to your local network before running
  any control commands.

## Critical Rules

1. **Device actions are NOT generic "set" or "toggle"**. Each device type has specific
   actions. Always check [ref/devices.md](ref/devices.md) for the exact action name and
   required params for each device type/subtype combination.

2. **UUIDs on import are placeholders**. The server remaps ALL UUIDs. Use simple
   placeholder values like `"t1"`, `"n1"`, `"e1"` — the server will replace them with
   real UUIDs.

3. **Imported workflows start in `draft` + `disabled` state**. Always validate then
   enable after import.

4. **Node configs are strictly typed**. A `device_control` node with wrong params will
   fail at execution time even if import succeeds. Always match action + params to the
   device's capability.

5. **Edge handle names**: Triggers use `source_handle: "output"`. Condition/logic nodes
   use `"true"` and `"false"` as source_handle. Action, delay, and transform nodes use
   `source_handle: "output"`. All target handles are `"input"`.

6. **`source_type` in edges**: Use `"trigger"` when source is a trigger UUID, use
   `"node"` when source is any node UUID.

## Common Pitfalls (MUST READ)

### Pitfall 1: `node_subtype` vs `sub_type` — DIFFERENT fields!

- **Devices** use `sub_type` (e.g. `"sub_type": "light_dimmer"`)
- **Nodes** use `node_subtype` (e.g. `"node_subtype": "device_control"`)
- If you use `sub_type` in a node definition, it will be **silently ignored**. The node
  will have an empty subtype and validation will report "未知节点类型 action:" (unknown
  node type). **Always use `node_subtype` for nodes.**

### Pitfall 2: Validate response — check `errors` array, NOT just `valid`

The `/validate` endpoint may return `"valid": true` even when `errors` is non-empty.
Node config errors (e.g. missing subtype, wrong params) appear in `errors` but do not
flip `valid` to false. **Always check the `errors` array is null or empty.**

```
✗ BAD:  if response.data.valid == true → proceed
✓ GOOD: if response.data.valid == true AND response.data.errors is null/empty → proceed
```

### Pitfall 3: After import, verify the response data

Always inspect the import response body. Confirm that:
- `node_subtype` fields are non-empty for action nodes
- `source_handle` / `target_handle` have the expected values
- `config` objects contain the correct action/params

If any field is missing or empty, the import JSON had a wrong field name.

## System Limits

| Limit | Value |
|-------|-------|
| Max workflows | 200 |
| Max nodes per flow | 50 |
| Max edges per flow | 200 |
| Max triggers per workflow | 5 |
| Timeout range | 5–3600 seconds |
| Max parallel | 10 |
| Max retry count | 5 |
| Max name length | 128 chars |
| Max description length | 1024 chars |

Retrieve current limits: `GET /automation/limits`
