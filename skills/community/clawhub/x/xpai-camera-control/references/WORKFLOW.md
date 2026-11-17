# Workflow Reference

Detailed workflow examples with MCP tool-call sequences. This file supplements the concise instructions in `SKILL.md`.

> **MCP-Only Interaction.** Every example below is an **MCP tool invocation** (tool name + JSON arguments) against the running `scripts/mcp_server.py` — **not** Python code to execute. Never import `scripts.toolkit` or write standalone scripts to reproduce these flows; doing so bypasses the skill's security constraints and the server's in-memory connection state. See [SKILL.md — MCP-Only Interaction](../SKILL.md#mcp-only-interaction-hard-rule).

Notation used below: `tool_name(arg1=value, arg2=value)` describes a single MCP tool call with its JSON arguments; `→` describes the returned result fields.

---

## Phase 0 — Session Init: Detailed Tool Calls

```text
0. If this is the first camera work after a long idle period (hours/days), or a previous
   connect/stream call failed on a camera that used to work:
   search_devices()
   → refreshes stale IPs in config.yaml (DHCP lease changes) and drops cameras that are gone
   then continue with the steps below

1. get_registered_cameras()
   → list of CameraConfig entries from config.yaml (name, ip, ports, credentials, device_class)

2. For each registered camera:
   connect_device(camera_name=<cam.name>)
   → success=true  : connected using cached credentials (auth_method reported)
   → success=false, status="failed", needs_password=true, error contains "cached credential connection failed":
      the tool has retried 3x and auto-removed the registration from config.yaml
      → fall through to Phase 1 to re-discover this device
   → success=false (other): note error_message, fall through to Phase 1 for this device

3. If config.yaml is empty or all connections failed → Phase 1
```

---

## Phase 1 — Discover Cameras: Detailed Tool Calls

`search_devices()` is the unified discovery tool — it automatically selects the best protocol(s) and returns normalized results.

```text
search_devices()
→ result.devices[]: ip, onvif_port, rtsp_port, device_class, model, manufacturer,
                    sn_code, discovery_method, sky_subtype, sky_name, sky_channels,
                    sky_mac, sky_hw_version, sky_sw_version, ...
```

- `discovery_method` tells you which protocol found each device (`"sky_discovery"` / `"jcp_discovery"` / `"ws_discovery"`)
- `sky_*` fields are populated for Skyworth devices, empty for others
- `device_class` is auto-classified via RTSP probe: `"password_required"` or `"direct_connect"`
- **Search writes config.yaml**: discovered reachable devices are registered (basic info only — no password), and registered entries that are neither discovered nor reachable are removed. Re-running `search_devices()` is the supported way to refresh IP changes, newly added cameras, and departed cameras.

For protocol-level details (multicast addresses, message formats), see [Discovery — How Discovery Works](commands/discovery.md#how-discovery-works-internal).

---

## Phase 2 — Connect & Authorize: Detailed Tool Calls

> **Pre-notice before a cloud-auth wait (required):** a cloud-authorization call blocks `connect_device` for up to 5 minutes until the user approves, and the request is pushed only to the phone App the camera is bound to. Before calling `connect_device` on a camera that may need cloud authorization (e.g. no cached password), tell the user to open the bound App and tap **Approve** when the request appears.

> **Password hint:** whenever asking the user for a camera password, mention that the password is printed on the camera's body label.

### Direct-connect camera (no password needed)

```text
connect_device(camera_name="study_camera")
→ tool probes RTSP → receives 200 OK → connects directly
→ auth_method="direct"
```

### Password-required camera with cached credentials

```text
# Credentials already in config.yaml from a previous session
connect_device(camera_name="living_room_camera")
→ tool reads username/password from config.yaml
→ retries ONVIF WS-UsernameToken auth up to 3 times (1s interval)
→ success: auth_method="password"
→ all retries fail: tool attempts one cloud re-authorization round (blocking up to 5 minutes; pre-notice not applicable — do not steer the user into approving)
   → if the cloud still yields a usable password: auto-connected, credentials re-persisted
   → otherwise: registration auto-removed; status="needs_password"
   → error explains: the cloud re-issued password is the same stale credential — another authorization round cannot recover
   → Agent: ask the user for the current password directly (do not send them to re-approve), then reconnect —
     the registry entry was removed, so pass the IP from the error message:
     connect_device(camera_name="living_room_camera", password=<user_input>, ip="192.168.1.100")
```

### Password-required camera (no cached credentials)

```text
Step 1 — Connect without password:
  connect_device(camera_name="discovered_192_168_1_100", sn_code="SN123456")
  → tool internally triggers cloud authorization
  → waiting for user to confirm in the bound App (blocks up to 5 minutes; pre-notice required — see above)
  → success=true: cloud authorized, auto-connected, credentials persisted
  → status="needs_password": cloud service unreachable, or the device has no station record (submitted to the default station, APP may not receive it) → ask user for password
  → status="auth_rejected": user denied authorization, cannot connect
  → status="cloud_pwd_failed": cloud password mismatch, ask user for correct password

Step 2a — Cloud authorized (success=true):
  No further action needed. Credentials auto-persisted to config.yaml.
  Future sessions will auto-connect via Phase 0.

Step 2b — Cloud unavailable (needs_password):
  (conversationally — the Agent informs user that cloud service is unavailable)
  Default-station HTTP 500: ask for the password immediately. Do not poll again,
  retry cloud authorization, switch stations, or infer server/region/registration causes.
  connect_device(
    camera_name="discovered_192_168_1_100",
    password=<user_input>,
    ip="192.168.1.100",     # from Phase 1 discovery result (DiscoveredDevice.ip)
    rtsp_port=554            # from DiscoveredDevice.rtsp_port
  )
  → future sessions will auto-connect via Phase 0

Step 2c — Cloud password mismatch (cloud_pwd_failed):
  (conversationally — the Agent informs user that cloud password doesn't match,
   device may have changed password)
  connect_device(
    camera_name="discovered_192_168_1_100",
    password=<user_input>,
    ip="192.168.1.100",
    rtsp_port=554
  )
  → future sessions will auto-connect via Phase 0

Step 2d — Authorization rejected (auth_rejected):
  (conversationally — inform user that authorization was denied, cannot connect)
  No further action available unless user provides password directly.
```

### Third-party ONVIF camera (O-class, degraded)

```text
# WS-Discovery found a camera that never answers SK/JCP discovery (sn_code empty)
connect_device(camera_name="office_thirdparty", password=<user_input>)
→ SK/JCP SN probes empty
→ ONVIF admission passes (port probe + GetDeviceInformation)
→ success=true, status="connected", protocol_type="O"
→ config.yaml: protocol_type: O, onvif_sn: <ONVIF SerialNumber>, sn_code: '' (empty)
→ available: RTSP streaming/screenshot/recording/WebRTC (ONVIF GetStreamUri paths), ONVIF PTZ
→ unavailable (immediate UNSUPPORTED_PROTOCOL / clear message): cloud authorization,
  illumination, image settings, detection/tracking, alarm events, PTZ degrees

# RTSP-only device (ONVIF admission fails):
connect_device(camera_name="rtsp_only_cam", password=<user_input>)
→ success=false, status="no_sn" — explicit message: RTSP-only, ONVIF control plane
  unverified, identity unconfirmed. Report to user; no workaround via register_camera.
```

### Cloud-authorized camera (handled internally)

Cloud authorization is now fully handled inside `connect_device`. The Agent does **not** need to call any separate cloud auth tool. The `big_connect` and `poll_auth_status` tools have been deprecated as external MCP tools.

```text
# Cloud auth flow is automatic:
connect_device(camera_name="discovered_192_168_1_100", sn_code="SN123456")
→ internally: triggers cloud auth request → polls for result with timeout
→ if authorized: auto-connect with cloud password, credentials persisted
→ if rejected/timeout/error: return appropriate status for Agent to handle
```

---

## Phase 3 — Stream & Capture: Detailed Tool Calls

```text
# Capture a snapshot
capture_video_screenshot(camera_name="living_room_camera")
→ file_path of the saved JPEG

# Get stream URL
get_audio_video_stream(camera_name="living_room_camera")
→ stream_url (RTSP), codec, resolution, fps

# Start/stop recording
toggle_recording(camera_name="living_room_camera", action="start")
toggle_recording(camera_name="living_room_camera", action="stop")
```

> For non-ASCII path handling and same-process connection requirements, see [SKILL.md — Gotchas](../SKILL.md#gotchas).

### End-to-End: User says "I want to see the camera"

```text
# Assumes camera is already connected (Phase 0/2 complete)

Step 1 — Capture screenshot for preview:
  capture_video_screenshot(camera_name="living_room_camera")
  → file_path: "snapshots/living_room_camera_20260727_143052.jpg"

Step 2 — Get RTSP stream URL for live viewing:
  get_audio_video_stream(camera_name="living_room_camera")
  → stream_url: "rtsp://admin:pass@192.168.1.100:554/md0_0"
  → codec: "H.264", resolution: "2560x1440", fps: 25

Step 3 — Agent delivers BOTH results to the user:
  (a) Show the screenshot image using markdown:
      ![living room camera snapshot](snapshots/living_room_camera_20260727_143052.jpg)
  (b) Tell user the complete RTSP URL unchanged:
      "RTSP live stream: rtsp://admin:pass@192.168.1.100:554/md0_0
       You can copy this URL into VLC, ffplay, or PotPlayer for live viewing."
```

The URL contains credentials; do not share it publicly.

---

## Phase 4 — PTZ Control: Detailed Tool Calls

PTZ backend is selected by `protocol_type`: **S-class** uses the Skyworth private protocol; **J-class and O-class** use **ONVIF only** (no private-protocol fallback). All return results include a `protocol` field indicating which protocol was actually used.

### Directional movement (4 directions + Chinese aliases)

```text
# Basic 4 directions (auto-stop after duration_seconds, default 1.0s)
control_ptz(camera_name="living_room_camera", direction="up", speed=0.5)
control_ptz(camera_name="living_room_camera", direction="left", speed=0.5, duration_seconds=2.0)

# Chinese direction aliases are supported (上=up, 左=left, etc.)
control_ptz(camera_name="living_room_camera", direction="上", speed=0.5)
```

PTZ movement is time-based. The tool does not query the current position or detect physical travel limits.

### Stop PTZ immediately

```text
# Stop pan/tilt movement (SK private protocol for S-class, ONVIF for J/O-class)
stop_ptz(camera_name="living_room_camera")
```

---

## Extended Tools

The following tools extend the skill beyond the core workflow (Phase 0–4). They are available when the user explicitly requests them but are not part of the typical camera operation flow.

### Event Monitoring (`manage_camera_events`)

Receive alarm events (motion, human, vehicle, tamper, line-crossing, …) with linked snapshots. Single tool, `action` switches mode: `start` / `stop` / `poll` / `wait`.

| Aspect | Detail |
|--------|--------|
| **Prerequisite** | Camera connected via `connect_device()` |
| **Safety** | `action="start"` spawns a background listener — requires explicit user confirmation |
| **Detailed reference** | [commands/events.md](commands/events.md) — full parameter/return fields, schema 1.0 format, event store contract |
| **Architecture** | [commands/events.md — Architecture](commands/events.md#architecture) |

### Illumination Mode Control (`manage_illumination`)

Query and adjust camera illumination parameters. **XPAI private protocol only** (TCP channel, 2 parameters: `daynightmode` / `filllightmode`; no ONVIF fallback, J/O-class unsupported). Single tool, `action` switches mode: `get` / `set`.

| Aspect | Detail |
|--------|--------|
| **Prerequisite** | Camera connected via `connect_device()`; SK fill-light capability probed at connect time and cached in `config.yaml` as `illumination_modes` (S-class devices only) |
| **Safety** | `action="set"` modifies a hardware setting — requires explicit user confirmation. Always call `get` first to retrieve `capabilities` (parameter ranges), then call `set` with only the parameters to change |
| **Detailed reference** | [commands/illumination.md](commands/illumination.md) — full parameter table (daynightmode / filllightmode), return fields, protocol details |
| **Architecture** | [commands/illumination.md — Architecture](commands/illumination.md#architecture) |
