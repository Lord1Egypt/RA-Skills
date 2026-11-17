# PTZ Control

Pan/tilt control with a **per-protocol backend** — exposed as MCP tools by `scripts/mcp_server.py`

The backend is selected by the camera's `protocol_type`: **SK-class** (`S`) uses the XPAI private protocol (vendor command via TCP channel); **JCP-class** (`J`) and third-party ONVIF-class (`O`) use **ONVIF only** (`ContinuousMove` / `Stop` on the ONVIF PTZ service, moving by normalized velocity vectors). Selection is handled internally — the Agent only sees the `protocol` field in the result (`"sky_private"` or `"onvif"`).

**J/O-class limits:** `degrees` mode is **not supported** on J-class or O-class cameras (ONVIF exposes normalized velocity vectors, not absolute angles); it returns an explicit unsupported message. Use `duration_seconds` for J/O-class movement.

> **MCP-only:** All tools below are invoked exclusively through the MCP server (`scripts/mcp_server.py`). Never import this module directly or write standalone scripts to call these functions.

**Prerequisite:** Camera must be connected via `connect_device()` and present in the server's connection state.

---

### `control_ptz(camera_name, direction: PTZDirection, speed: float = 0.5, duration_seconds: Optional[float] = None, degrees: Optional[float] = None) -> PTZMoveResult`

Directional movement of the PTZ head. Auto-stops after `duration_seconds` (defaults to 1.0 s when neither `duration_seconds` nor `degrees` is given). `duration_seconds` and `degrees` are mutually exclusive.

The tool uses timed movement and does not query the PTZ position or detect a physical travel limit.

| Aspect | Detail |
|--------|--------|
| **Safety** | Explicit Prompt |
| **Returns** | `PTZMoveResult` (see field table below) |
| **Parameters** | `direction`: `up`/`down`/`left`/`right`. Chinese aliases supported (上/下/左/右). `speed`: 0.1–1.0. `duration_seconds`: 0.1–10.0. `degrees`: rotation angle (SK-class only, converted at 1 s ≈ 34°; J/O-class returns an explicit unsupported notice) |

**PTZMoveResult return fields:**

| Field | Type | Description |
|-------|------|-------------|
| `success` | bool | Whether the move succeeded |
| `protocol` | string | Protocol actually used: `"onvif"` or `"sky_private"` |
| `error_message` | string | Failure reason (empty on success) |
| `requested_duration_seconds` | float | Duration the Agent requested |
| `actual_duration_seconds` | float | Duration used for the movement command |
| `degrees` | float | Requested angle in degrees mode (0 when unused) |
| `method` | string | Execution method: `"sk_time"` / `"sk_degrees"` / `"onvif_time"` |

---

### `stop_ptz(camera_name) -> PTZMoveResult`

Stop ongoing pan/tilt movement immediately.

| Aspect | Detail |
|--------|--------|
| **Safety** | None |
| **Returns** | `PTZMoveResult` (same structure as `control_ptz`) |
