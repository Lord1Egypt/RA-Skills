# API Reference

Base URL: `http://ycznwl.local/api/v1` (default)

All requests require: `Authorization: Bearer <token>`

All responses use format:
```json
{ "code": 200, "data": { ... }, "message": "ok" }
```

Error responses:
```json
{ "code": 400, "data": null, "message": "error description" }
```

---

## Device Endpoints

### List All Devices

```
GET /devices
```

Returns **all** devices in a single response (no pagination). See [devices.md](devices.md) for response format.

### Get Single Device

```
GET /devices/:id
```

`:id` is the numeric device ID (not UUID).

### Control Device

```
POST /devices/:id/control
```

`:id` is the numeric device ID.

```json
{
  "action": "turn_on",
  "params": {}
}
```

See [devices.md](devices.md) for valid action/params combinations per device type.

---

## Scene Endpoints

Scenes are reusable groups of device actions. Each scene auto-creates a virtual device
(see [devices.md](devices.md) § Virtual Scene Devices).

### List Scenes

```
GET /scenes
```

Query params:
- `enabled` (string, optional) — `"true"` or `"false"` to filter

**Response**:
```json
{
  "scenes": [
    {
      "id": 1,
      "uuid": "a1b2c3d4-...",
      "name": "Good Night",
      "description": "Turn off all lights, close curtains",
      "icon": "moon",
      "color": "#6366F1",
      "actions": [
        {
          "id": "act1",
          "device_uuid": "light-uuid",
          "device_name": "Living Room Light",
          "action": "turn_off",
          "params": {},
          "delay": 0
        }
      ],
      "knx_bind_address": "",
      "knx_bind_dpt": "",
      "knx_scene_id": null,
      "device_uuid": "scene-a1b2c3d4-...",
      "enabled": true,
      "sort_order": 0,
      "exec_total": 42,
      "exec_success": 40,
      "exec_fail": 2,
      "last_exec_at": "2026-04-07T10:30:00Z",
      "created_at": "2026-03-01T08:00:00Z",
      "updated_at": "2026-04-07T10:30:00Z"
    }
  ],
  "total": 1
}
```

### Get Single Scene

```
GET /scenes/:uuid
```

### Create Scene

```
POST /scenes
```

```json
{
  "name": "Good Night",
  "description": "Turn off all lights",
  "icon": "moon",
  "color": "#6366F1",
  "actions": [
    {
      "id": "a1",
      "device_uuid": "light-uuid",
      "device_name": "Living Room Light",
      "action": "turn_off",
      "params": {},
      "delay": 0
    },
    {
      "id": "a2",
      "device_uuid": "curtain-uuid",
      "device_name": "Curtain",
      "action": "close",
      "params": {},
      "delay": 500
    }
  ],
  "enabled": true
}
```

Only `name` is required. Returns the scene object with server-generated `uuid` and
auto-created `device_uuid`.

**Optional KNX binding fields** (for scenes triggered by physical KNX panels):
- `knx_bind_address` — KNX group address (e.g. `"1/2/3"`)
- `knx_bind_dpt` — KNX DPT (e.g. `"18.001"`)
- `knx_scene_id` — KNX scene number (0–63)

### Update Scene

```
PUT /scenes/:uuid
```

Partial update — include only fields to change:
```json
{
  "name": "Updated Name",
  "enabled": false,
  "actions": [ ... ]
}
```

### Delete Scene

```
DELETE /scenes/:uuid
```

Also removes the associated virtual device.

### Execute Scene

```
POST /scenes/:uuid/execute
```

Runs all configured device actions. Returns execution result:
```json
{
  "success": true,
  "actions_executed": 3,
  "actions_failed": 0,
  "duration_ms": 150,
  "errors": []
}
```

Error tolerance: if an action fails, remaining actions still execute.

### Toggle Scene Enabled/Disabled

```
POST /scenes/:uuid/toggle
```

Returns:
```json
{ "uuid": "...", "enabled": false }
```

### Update Sort Order

```
PUT /scenes/sort
```

```json
{
  "order": [
    { "uuid": "scene-uuid-1", "sort_order": 0 },
    { "uuid": "scene-uuid-2", "sort_order": 1 }
  ]
}
```

### List Execution Logs

```
GET /scenes/logs?scene_uuid=xxx&limit=50&offset=0
```

Query params:
- `scene_uuid` (string, optional) — filter by scene
- `limit` (int, default 50)
- `offset` (int, default 0)

---

## Automation Endpoints

### Get System Limits

```
GET /automation/limits
```

Returns validation boundaries (max nodes, max timeout, etc.).

### List Workflows

```
GET /automation/workflows?limit=100&offset=0
```

Query params:
- `limit` (int, default 20, max 100)
- `offset` (int, default 0)
- `status` (string, optional) — filter by status: `draft`, `ready`, `active`, `error`

### Create Workflow (empty)

```
POST /automation/workflows
```

```json
{
  "name": "My Workflow",
  "description": "optional description"
}
```

Creates an empty workflow in `draft` state. Returns the full workflow object.

### Import Workflow (recommended for agents)

```
POST /automation/workflows/import
```

This is the **preferred** endpoint for agents creating workflows. It accepts a complete
workflow definition and handles UUID remapping, default value application, and validation.

**Request body**:
```json
{
  "schema_version": 1,
  "workflow": {
    "name": "Required — workflow name",
    "description": "Optional, default ''",
    "icon": "Optional, default 'zap'",
    "color": "Optional, default '#3B82F6'",
    "category": "Optional, default 'custom'",
    "tags": [],
    "exec_mode": "Optional: single|parallel|queue|restart, default 'single'",
    "max_parallel": 1,
    "debounce_ms": 0,
    "cooldown_ms": 0,
    "timeout_s": 300,
    "retry_max": 0,
    "retry_interval_s": 10,
    "flow_data": {
      "triggers": [ ... ],
      "nodes": [ ... ],
      "edges": [ ... ]
    }
  }
}
```

**Only `name` and `flow_data` (with at least one trigger) are required.**
All other fields use defaults when omitted.

**Server behavior**:
1. Remaps ALL UUIDs in triggers, nodes, and edges to new server-generated UUIDs
2. Preserves edge source/target relationships using a UUID mapping table
3. Applies default values for omitted optional fields
4. Creates workflow in `draft` status, `enabled = false`

**Response**: Full workflow object with server-assigned UUID and remapped flow_data.

> **Security — Review before enabling**: Before calling `/validate` and `/enable`, inspect
> the imported workflow JSON for off-LAN HTTP destinations, MQTT brokers outside the trusted
> LAN, webhook triggers, or embedded secrets. Only import workflows from sources you trust.

> **IMPORTANT — Verify import response**: After import, check the response body to confirm
> `node_subtype` is non-empty for all nodes. If it is empty `""`, you likely used the wrong
> field name (`sub_type` instead of `node_subtype`). Nodes use `node_subtype`; devices use
> `sub_type`. This is a common mistake.

> **IMPORTANT — Validate after import**: Always call `/validate` after import, and check
> BOTH `valid` AND `errors` fields. The endpoint may return `valid: true` with non-empty
> `errors` (e.g. for node config issues). Only proceed to enable if `errors` is null/empty.

### Get Workflow Detail

```
GET /automation/workflows/:uuid
```

Returns the complete workflow including flow_data with all triggers, nodes, and edges.

### Update Workflow

```
PUT /automation/workflows/:uuid
```

```json
{
  "workflow": {
    "name": "Updated Name",
    "timeout_s": 120
  },
  "triggers": [ ... ],
  "nodes": [ ... ],
  "edges": [ ... ]
}
```

The `workflow` object supports partial updates — only include fields you want to change.
`triggers`, `nodes`, `edges` are the complete new flow_data arrays (replacing existing).

**Important**: When editing, keep existing UUIDs for unchanged elements. Only generate
new UUIDs for newly added triggers/nodes/edges.

> **⚠ Update vs Import — different body structure**: The Update endpoint wraps
> `triggers`/`nodes`/`edges` at the top level alongside `workflow`. The Import endpoint
> nests them inside `workflow.flow_data`. Do not mix these formats — using the import
> structure in an update request will silently discard your flow changes.

### Delete Workflow

```
DELETE /automation/workflows/:uuid
```

### Clone Workflow

```
POST /automation/workflows/:uuid/clone
```

Creates a copy of the workflow with new UUIDs and "(Copy)" appended to the name.

### Validate Workflow

```
POST /automation/workflows/:uuid/validate
```

Runs server-side validation on the workflow's flow_data and configuration.

**Optional body** (for including config validation):
```json
{
  "timeout_s": 300,
  "exec_mode": "single",
  "max_parallel": 1
}
```

**Response**:
```json
{
  "valid": true,
  "errors": []
}
```

Or with errors:
```json
{
  "valid": false,
  "errors": [
    {
      "code": "trigger_config_incomplete",
      "message": "Device event trigger 'Temp' is missing device UUID",
      "node_uuid": "abc123",
      "field": "device_uuid"
    }
  ]
}
```

### Enable Workflow

```
POST /automation/workflows/:uuid/enable
```

Activates the workflow. Requires the workflow to pass validation.
Returns error if validation fails.

### Disable Workflow

```
POST /automation/workflows/:uuid/disable
```

Deactivates the workflow. Running executions are not cancelled.

### Execute Workflow (manual trigger)

```
POST /automation/workflows/:uuid/execute
```

Manually fires the workflow as if the manual trigger was activated.

---

## Execution Endpoints

### List Executions

```
GET /automation/executions?workflow_uuid=xxx&limit=20&offset=0
```

Query params:
- `workflow_uuid` (string, optional) — filter by workflow
- `status` (string, optional) — filter by status: `pending`, `running`, `completed`, `failed`, `cancelled`, `timeout`
- `limit` (int, default 20)
- `offset` (int, default 0)

### Get Execution Detail

```
GET /automation/executions/:uuid
```

### Get Execution Logs

```
GET /automation/executions/:uuid/logs
```

Returns per-node execution logs with timing information.

### Cancel Execution

```
POST /automation/executions/:uuid/cancel
```

Cancels a running execution.

---

## Sun Times Endpoints


### Get Today's Sun Times

```
GET /system/sun-times
```

Query params:
- `date` (string, optional) — Date in `YYYY-MM-DD` format. Default: today
- `tz` (string, optional) — Timezone override (e.g. `"Asia/Shanghai"`)

**Response**:
```json
{
  "latitude": 31.2304,
  "longitude": 121.4737,
  "date": "2025-04-24",
  "sunrise": "2025-04-24T05:23:00+08:00",
  "sunset": "2025-04-24T18:31:00+08:00",
  "timezone": "Asia/Shanghai"
}
```

---

## Edge Format

Edges connect triggers to nodes and nodes to nodes.

```json
{
  "uuid": "e1",
  "source_uuid": "t1",
  "source_type": "trigger",
  "source_handle": "output",
  "target_uuid": "n1",
  "target_handle": "input",
  "enabled": true
}
```

| Field | Description |
|-------|-------------|
| `source_uuid` | UUID of the source trigger or node |
| `source_type` | `"trigger"` if source is a trigger, `"node"` if source is a node |
| `source_handle` | `"output"` for triggers and action/delay/transform nodes. `"true"` or `"false"` for condition/logic nodes |
| `target_uuid` | UUID of the target node |
| `target_handle` | Always `"input"` |

### Edge routing rules

1. **Trigger → Node**: `source_type: "trigger"`, `source_handle: "output"`, `target_handle: "input"`
2. **Condition → Node (true branch)**: `source_type: "node"`, `source_handle: "true"`, `target_handle: "input"`
3. **Condition → Node (false branch)**: `source_type: "node"`, `source_handle: "false"`, `target_handle: "input"`
4. **Logic → Node (true branch)**: `source_type: "node"`, `source_handle: "true"`, `target_handle: "input"`
5. **Logic → Node (false branch)**: `source_type: "node"`, `source_handle: "false"`, `target_handle: "input"`
6. **Action → Node**: `source_type: "node"`, `source_handle: "output"`, `target_handle: "input"`
7. **Delay → Node**: `source_type: "node"`, `source_handle: "output"`, `target_handle: "input"`
8. **Transform → Node**: `source_type: "node"`, `source_handle: "output"`, `target_handle: "input"`
