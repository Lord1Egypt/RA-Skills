# IPC Event Receiving (Guardian Mode Foundation)

Alarm/event subscription, snapshot linkage, and on-disk event store — exposed as the single MCP tool `manage_camera_events` by `scripts/mcp_server.py`

> **MCP-only:** All tools below are invoked exclusively through the MCP server (`scripts/mcp_server.py`). Never import this module directly or write standalone scripts to call these functions.

> **J/O-class not supported:** alarm event monitoring uses the Skyworth private protocol and is unavailable on JCP or O-class cameras (`protocol_type="J"`/`"O"`). All actions (`start` / `stop` / `poll` / `wait`) for a J/O-class `camera_name` return immediately with a clear message — not a timeout or malfunction.

---

## Architecture

**Single event source — XPAI private protocol**:

1. **XPAI private protocol** — alarm messages are pushed **over a persistent RTSP session**: after `DESCRIBE` / `SETUP` / `PLAY` with the private alarm User-Agent, the device reports alarm JSON (~94 bytes) on interleaved channel `0x65`. Any non-200 handshake step aborts into a reconnect backoff (2 s → 30 s exponential cap). The listener status exposes `rtsp_session` and `last_error`, so failed handshakes are visible instead of silently half-open.

**Listening endpoint:** the alarm session is opened on the main stream path from `config.yaml` (`CameraConfig.rtsp_path` — `/md0_0` on SK devices, the alarm stream; sub stream is `/md0_1`). The in-memory connection dict supplies only ip/port/credentials, never endpoints.

**Alarm codes → normalized topics:**

| `alm` | Topic | Meaning | | `alm` | Topic | Meaning |
|-------|-------|---------|-|-------|-------|---------|
| `MD` | `motion` | Motion detection | | `VS` | `tamper` | Tamper detection |
| `HD` | `human` | Human detection | | `VD` | `vehicle` | Vehicle detection |
| `VGR` | `region_intrusion` | Region intrusion | | `HTD` | `high_temp` | High temperature |
| `VGL` | `line_crossing` | Line crossing | | `LTD` | `low_temp` | Low temperature |

**Deduplication:** events with the same `(camera, normalized topic)` within the debounce window (default 5 s) are merged into one record. **Snapshots are sampled, not triggered:** at most one snapshot per camera per fixed 30 s interval — every alarm is recorded, but the picture is a sample. Snapshot capture runs on a background thread with a pre-generated path and never blocks the listening loop (a synchronous snapshot once stalled the alarm socket and the device killed the session after its 30 s send timeout).

**On-disk event store:** after processing (raw protocol fields are dropped; a schema 1.0 JSON line is produced), the event is appended to `events/camera_events.txt`. The in-memory queue is only a hot cache; `poll` / `wait` always read the disk store, so backlog survives MCP server restarts and is readable from fresh sessions. **Schema, paths, write semantics, and the consumer contract** are defined in [references/EVENT_INTEGRATION.md](../EVENT_INTEGRATION.md) — read that file when writing any external consumer (other skills, forwarders, dashboards).

**Monitor intent persistence & auto-resume:** listener threads live inside the MCP server process and die when the host recycles it. To survive that, `start` persists the monitoring intent to `events/monitor_state.json` and `stop` clears it. On server startup and at every `poll` / `wait` entry, persisted intents are re-armed for cameras whose listener is not running. No new authorization surface: only listeners the user enabled and never stopped are restored.

---

## `manage_camera_events(action, camera_name=None, debounce_seconds=5.0, limit=100, timeout_seconds=60)`

**The single MCP entry point for all event operations** — the `action` parameter switches the working mode.

| `action` | Mode | Returns | Relevant parameters |
|----------|------|---------|--------------------|
| `start` | Start the background listener | `EventMonitorResult` | `camera_name` (required), `debounce_seconds` |
| `stop` | Stop the listener | `EventMonitorResult` | `camera_name` (required) |
| `poll` | Read unconsumed events, advance cursor | `PendingEventsResult` | `camera_name` (optional filter), `limit` |
| `wait` | Long-poll block for new events | `PendingEventsResult` | `camera_name` (optional filter), `timeout_seconds` |

---

### `action="start"`

Start the background event listener for a camera. **Requires explicit user confirmation before calling** — this is the only action in the skill that spawns a background thread.

| Aspect | Detail |
|--------|--------|
| **Safety** | Explicit Prompt — background thread starts only after user enablement; behavior limited to alarm subscription + writes into `snapshots/` and `events/` whitelist paths |
| **Returns** | `EventMonitorResult` (see field table below) |
| **Parameters** | `camera_name`: camera identifier (must be registered or connected). `debounce_seconds`: dedup window (snapshot sampling is a fixed 30 s interval, independent of this value). |
| **Agent behavior** | `success=True` means the listener thread started; the RTSP handshake result surfaces later in the `monitors` status returned by `poll` / `wait` (`rtsp_session`, `last_error`). If start fails outright, relay `error_message`. |

**EventMonitorResult return fields:**

| Field | Type | Description |
|-------|------|-------------|
| `success` | bool | Whether the operation succeeded |
| `camera_name` | string | Camera identifier |
| `running` | bool | Whether the listener is now running |
| `active_channels` | list[string] | Active protocol channels (`["private"]` once the RTSP alarm session is fully established) |
| `error_message` | string | Failure reason (empty on success) |

---

### `action="stop"`

Stop the listener and close the RTSP alarm session. Also clears the persisted monitoring intent — the listener will **not** auto-resume after future process restarts.

| Aspect | Detail |
|--------|--------|
| **Safety** | No special constraints |
| **Returns** | `EventMonitorResult` (`running=False` after stop) |
| **Parameters** | `camera_name`: camera identifier. |

---

### `action="poll"`

Return unconsumed events (with snapshot paths) and advance the persisted per-camera cursor.

| Aspect | Detail |
|--------|--------|
| **Safety** | No special constraints (reads store + writes cursor file) |
| **Returns** | `PendingEventsResult` (see field table below) |
| **Parameters** | `camera_name`: filter to one camera; omitting consumes all cameras' backlog. `limit`: max events per call (default 100). |
| **Agent behavior** | Works from a fresh session with a freshly started MCP server (reads the disk store; also auto-resumes any persisted-but-dead listeners). For each event, read the `snapshot_path` image, analyze, and report. `remaining > 0` means the backlog was truncated by `limit` — call again. |

**PendingEventsResult return fields:**

| Field | Type | Description |
|-------|------|-------------|
| `success` | bool | Whether the operation succeeded |
| `events` | list | List of `CameraEvent` objects (see field table below) |
| `remaining` | int | Number of unconsumed events still in the store |
| `monitors` | dict | Status of each listener (keyed by camera name): `running`, `channels`, `rtsp_session`, `last_error`, `emitted`, `suppressed`, `debounce_seconds` |
| `error_message` | string | Failure reason (empty on success) |

**CameraEvent fields** (each item in `events`):

| Field | Type | Description |
|-------|------|-------------|
| `schema_version` | string | Fixed `"1.0"` |
| `event_id` | string | `{YYYYMMDD_HHMMSS}_{camera_id}_{event_type}` — idempotent dedup key |
| `event_type` | string | Normalized type: `motion` / `human` / `vehicle` / `tamper` / `region_intrusion` / `line_crossing` / `high_temp` / `low_temp` |
| `camera_id` | string | Camera registration name (key in config.yaml) |
| `camera_name` | string | Display name (defaults to `camera_id` when no separate display name) |
| `timestamp` | string | ISO 8601 with local timezone (e.g. `"2026-07-29T09:30:00+08:00"`) |
| `severity` | string | `info` / `warning` / `critical` |
| `title` | string | Ready-to-use notification title |
| `message` | string | Ready-to-use notification body |
| `label` | string or null | Target class (person/car/truck…); `null` when unavailable |
| `confidence` | float or null | Confidence score 0–1; `null` when protocol doesn't provide it |
| `snapshot_path` | string | Absolute snapshot path; **may be empty** (sampled at a fixed 30 s interval, captured asynchronously — a missing file means the background capture failed) |
| `tags` | list[string] | Currently always `["guardian"]` |

---

### `action="wait"`

Long-poll blocking wait: returns immediately when an event arrives (and consumes it), or returns an empty list at timeout (`success=True` either way).

| Aspect | Detail |
|--------|--------|
| **Safety** | No special constraints |
| **Returns** | `PendingEventsResult` (same structure as `poll`; events empty on timeout) |
| **Parameters** | `camera_name`: optional filter. `timeout_seconds`: default 60, **capped at 60** to stay under typical MCP client stdio tool timeouts. |
| **Agent behavior** | For continuous in-session guarding, loop this call — never expect a single long block. On each non-empty return: read snapshots, analyze, report, then continue the loop until the user stops. |
