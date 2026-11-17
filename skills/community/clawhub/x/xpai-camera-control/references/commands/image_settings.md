# Image Settings

Camera image parameter query and adjustment — exposed as the single MCP tool `manage_image_settings` by `scripts/mcp_server.py`

> **MCP-only:** All tools below are invoked exclusively through the MCP server (`scripts/mcp_server.py`). Never import this module directly or write standalone scripts to call these functions.

**Prerequisite:** Camera must be connected via `connect_device()` and present in the server's connection state (or have cached credentials in `config.yaml`).

> **J/O-class not supported:** this capability uses the Skyworth private protocol and is unavailable on JCP or O-class cameras (`protocol_type="J"`/`"O"`). Calls return immediately with `error_code="UNSUPPORTED_PROTOCOL"` and a clear message — not a timeout or malfunction.

---

## Architecture

Image settings use the **XPAI private protocol only** (TCP channel; same pattern as Illumination — no ONVIF fallback, because ONVIF Imaging covers only the 4 continuous parameters and cannot do `flip`).

### XPAI Private Protocol (TCP channel)

The private protocol provides full image control via vendor-specific TCP commands (capability query, read settings, write settings — handled internally by the tool).

This protocol exposes **5 controllable parameters**:

**Continuous parameters:**

| Parameter | Type | Typical Range | Description |
|-----------|------|---------------|-------------|
| `brightness` | int | device-reported | Brightness |
| `contrast` | int | device-reported | Contrast |
| `saturation` | int | device-reported | Color saturation |
| `sharpness` | int | device-reported | Sharpness |

**Multi-level enum parameters:**

| Parameter | Type | Values | Description |
|-----------|------|--------|-------------|
| `flip` | int | 0–3 | Image flip: 0=normal, 1=diagonal, 2=horizontal, 3=vertical |

> The remaining firmware fields (`whitebalance`, `wdr`, `face_mode`, `plate_mode`, `default`) are not exposed — they are read as part of the baseline and passed through unchanged on write.

**Set behavior:** the device requires the **full parameter set** when writing. The tool handles this internally — it first reads current settings, merges only the user-specified parameters, then sends the complete set. The Agent only needs to pass the parameters it wants to change.

---

## `manage_image_settings(camera_name, action, **params) -> ImageQueryResult | ImageSetResult`

**The single MCP entry point for all image settings operations.**

| `action` | Mode | Returns |
|----------|------|---------|
| `get` | Query capability & current settings | `ImageQueryResult` |
| `set` | Set image parameters | `ImageSetResult` |

---

### `action="get"`

Query the device's image parameter capabilities and all current values.

| Aspect | Detail |
|--------|--------|
| **Safety** | None (read-only query) |
| **Parameters** | `camera_name` only |
| **Agent behavior** | Report capabilities (with ranges and current values) to the user. If capabilities is empty, the device does not support image settings. |

**Returns** `ImageQueryResult` with:
- `channel`: `"sk"` (protocol channel used)
- `capabilities`: list of parameter descriptions with ranges and current values (e.g. `[{"name": "brightness", "type": "int", "specs": {"min": "1", "max": "255"}, "current": 128, "current_text": "128"}, ...]`)
- `current`: raw dict of all current parameter values from the device

---

### `action="set"`

Change one or more image parameters. **Requires explicit user confirmation.**

| Aspect | Detail |
|--------|--------|
| **Safety** | Explicit Prompt — hardware setting change; confirm with the user |
| **Parameters** | `camera_name` + any subset of the image parameters |
| **Agent behavior** | Call `get` first to retrieve capabilities and validate parameter ranges, then call `set` with only the parameters the user wants to change. Report `updated` fields and `current` full state after change. |

**All settable parameters** (all optional — specify only what you want to change):

| Parameter | Type | Range |
|-----------|------|-------|
| `brightness` | int | device-reported |
| `contrast` | int | device-reported |
| `saturation` | int | device-reported |
| `sharpness` | int | device-reported |
| `flip` | int | 0–3 (0=normal, 1=diagonal, 2=horizontal, 3=vertical) |

---

## ImageQueryResult return fields

| Field | Type | Description |
|-------|------|-------------|
| `ok` | bool | Whether the operation succeeded |
| `camera` | string | Camera name |
| `channel` | string | `"sk"` |
| `capabilities` | list | Parameter capability descriptions (name, type, specs with min/max, current value, current_text) |
| `current` | dict | Raw device current parameter values |
| `error_code` | string | Error code on failure |
| `message` | string | Human-readable status message |
| `hint` | string | Suggested next step on failure |

## ImageSetResult return fields

| Field | Type | Description |
|-------|------|-------------|
| `ok` | bool | Whether the operation succeeded |
| `camera` | string | Camera name |
| `channel` | string | `"sk"` |
| `updated` | dict | Fields that were changed, with post-write readback values |
| `current` | dict | Full current parameter state after the change |
| `error_code` | string | Error code on failure |
| `message` | string | Human-readable status message |
| `hint` | string | Suggested next step on failure |

---

## Error codes

| `error_code` | Cause |
|--------------|-------|
| `DEVICE_UNREACHABLE` | SK TCP 9010 unreachable — verify camera is online |
| `OPTION_QUERY_FAILED` | Capability query rejected by device |
| `CURRENT_QUERY_FAILED` | Current-value query rejected by device |
| `SET_FAILED` | Device rejected the write command |
| `PARAM_NOT_SUPPORTED` | Requested parameter not supported by this camera model |
| `PARAM_OUT_OF_RANGE` | Parameter value outside allowed range |
| `INVALID_PARAM_TYPE` | Wrong type for parameter (e.g. string instead of int) |
| `NO_PARAMS` | No parameters were passed to set |
