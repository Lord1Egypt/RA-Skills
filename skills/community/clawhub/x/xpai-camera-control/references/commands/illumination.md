# Illumination Mode Control

Camera illumination mode query and adjustment — exposed as the single MCP tool `manage_illumination` by `scripts/mcp_server.py`

> **MCP-only:** All tools below are invoked exclusively through the MCP server (`scripts/mcp_server.py`). Never import this module directly or write standalone scripts to call these functions.

**Prerequisite:** Camera must be connected via `connect_device()` and present in the server's connection state (or have cached credentials in `config.yaml`).

> **J/O-class not supported:** this capability uses the Skyworth private protocol and is unavailable on JCP or O-class cameras (`protocol_type="J"`/`"O"`). Calls return immediately with `error_code="UNSUPPORTED_PROTOCOL"` and a clear message — not a timeout or malfunction.

---

## Architecture

Illumination control uses the **XPAI Private Protocol only** (TCP channel, port 9010, dynamic-token HTTP): capability query, read settings, write settings — handled internally by the tool.

This protocol exposes **2 controllable parameters**:

**Day/Night mode** (`daynightmode`):

| Value | Mode | Description |
|-------|------|-------------|
| 0 | Day mode | Day mode (lights off) |
| 1 | Night mode | Night mode (lights on) |
| 2 | Auto mode | Auto (sensor-driven) |
| 3 | Timer mode | Timer (scheduled on/off) |
| 4 | Smart mode | Smart (AI-driven) |

**Fill light mode** (`filllightmode`):

| Value | Mode | Description |
|-------|------|-------------|
| 0 | Full-color mode | Full-color (white light) |
| 1 | Infrared mode | Infrared (IR) |
| 2 | Smart night vision | Smart night vision (auto-switch) |

Both parameters accept either the integer value or a string alias (`day`/`night`/`auto`/`timer`/`smart` for daynightmode, `color`/`ir`/`smart` for filllightmode, plus the Chinese aliases 白天/夜晚/自动/定时/智能 and 全彩/红外/智能夜视).

> The remaining firmware fields (white-light brightness, IR brightness, sensitivity values, timer schedule, etc.) are not exposed — they are read as part of the baseline and passed through unchanged on write (most devices only support the two modes above).

**Set behavior:** the device requires the **full parameter set** when writing. The tool handles this internally — it first reads current settings, merges only the user-specified parameters, then sends the complete set. The Agent only needs to pass the parameters it wants to change.

---

## `manage_illumination(camera_name, action, **params) -> FilllightQueryResult | FilllightSetResult`

**The single MCP entry point for all illumination operations.**

| `action` | Mode | Returns |
|----------|------|---------|
| `get` | Query capability & current settings | `FilllightQueryResult` |
| `set` | Set illumination parameters | `FilllightSetResult` |

---

### `action="get"`

Query the device's illumination capability and all current settings.

| Aspect | Detail |
|--------|--------|
| **Safety** | None (read-only query) |
| **Parameters** | `camera_name` only |
| **Agent behavior** | Report `capabilities` and `current` to the user. If `capabilities` is empty, the device does not support illumination control. |

**Returns** `FilllightQueryResult` with:
- `channel`: protocol channel used (`"sk"`)
- `capabilities`: list of parameter descriptions with ranges and current values (e.g. `[{"name": "daynightmode", "label": "Light setting (day/night mode)", "type": "int", "min": 0, "max": 4, "current": 2, "current_text": "Auto mode", "options": {...}}, ...]`)
- `current`: current values of the exposed parameters only (e.g. `{"daynightmode": 2, "filllightmode": 1}`)

---

### `action="set"`

Change one or more illumination parameters. **Requires explicit user confirmation.**

| Aspect | Detail |
|--------|--------|
| **Safety** | Explicit Prompt — hardware setting change; confirm with the user |
| **Parameters** | `camera_name` + any subset of the 2 illumination parameters |
| **Agent behavior** | Call `get` first to retrieve `capabilities` and validate parameter ranges, then call `set` with only the parameters the user wants to change. Report `updated` fields after change. |

**All settable parameters** (all optional — specify only what you want to change):

| Parameter | Type | Range |
|-----------|------|-------|
| `daynightmode` | int / string alias | 0–4 |
| `filllightmode` | int / string alias | 0–2 |

---

## FilllightQueryResult return fields

| Field | Type | Description |
|-------|------|-------------|
| `ok` | bool | Whether the operation succeeded |
| `camera` | string | Camera name |
| `channel` | string | Protocol channel used (`"sk"`) |
| `capabilities` | list | Parameter capability descriptions (name, label, type, min/max, current value, current_text, options) |
| `current` | dict | Current values of the exposed parameters only |
| `error_code` | string | Error code on failure |
| `message` | string | Human-readable status message |
| `hint` | string | Suggested next step on failure |

## FilllightSetResult return fields

| Field | Type | Description |
|-------|------|-------------|
| `ok` | bool | Whether the operation succeeded |
| `camera` | string | Camera name |
| `channel` | string | Protocol channel used (`"sk"`) |
| `updated` | dict | Fields that were changed, with post-write readback values |
| `current` | dict | Current values of the exposed parameters only after the change |
| `verified` | bool | Whether the change was confirmed by readback (SK channel always reads back) |
| `error_code` | string | Error code on failure |
| `message` | string | Human-readable status message |
| `hint` | string | Suggested next step on failure |

---

## Error codes

| `error_code` | Cause |
|--------------|-------|
| `DEVICE_UNREACHABLE` | SK TCP 9010 unreachable — verify camera is online; retry after 2-3 s (transient port flapping) |
| `OPTION_QUERY_FAILED` | Capability query rejected by device |
| `CURRENT_QUERY_FAILED` | Current-value query rejected by device |
| `SET_FAILED` | Device rejected the write command |
| `PARAM_NOT_SUPPORTED` | Requested parameter not supported by this camera |
| `PARAM_OUT_OF_RANGE` | Parameter value outside allowed range |
| `INVALID_PARAM_TYPE` | Wrong type for parameter (e.g. unrecognized string alias) |
| `NO_PARAMS` | No parameters were passed to set |
