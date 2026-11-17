# XPAI Camera Control — MCP Server Tools API Reference

> **Version**: v1.5.6 | **Transport**: stdio (JSON-RPC) | **Service name**: `xpai-camera-control`

All tool functions are exposed via MCP (Model Context Protocol). The caller sends JSON-RPC requests, and return values are uniformly serialized as JSON objects. On failure, `{"success": false, "error": "<error message>"}` is returned.

---

## Table of Contents

1. [Device Management](#1-device-management)
2. [Stream](#2-stream)
3. [PTZ Control](#3-ptz-control)
4. [Event Listening](#4-event-listening)
5. [WebRTC Live Preview](#5-webrtc-live-preview)
6. [Illumination Control](#6-illumination-control)
7. [Image Settings](#7-image-settings)
8. [Detection & Tracking](#8-detection--tracking)

---

## 1. Device Management

### `get_registered_cameras`

Load the configuration of all registered cameras (including credentials) from `config.yaml`. Does not scan the network; only reads locally saved records. **Call this first at the start of a session**.

**Parameters**: none

**Returns**: `CameraConfig[]`

| Field                  | Type     | Description                                       |
|------------------------|----------|--------------------------------------------------|
| `name`                 | string   | Camera name                                      |
| `connection_type`      | string   | `"onvif"`                                  |
| `ip`                   | string   | IP address                                       |
| `port`                 | int      | ONVIF port (0 = unknown)                         |
| `username`             | string   | Login username                                   |
| `password`             | string   | Login password                                   |
| `rtsp_port`            | int      | RTSP port                                        |
| `rtsp_path`            | string   | Main stream path                                |
| `rtsp_sub_path`        | string   | Sub stream path                                 |
| `device_class`         | string   | `"password_required"` / `"direct_connect"` |
| `sn_code`              | string   | Serial number                                   |
| `pkdk`                 | string   | Device public key identifier                    |
| `illumination_modes`   | string[] | List of supported illumination modes            |

---

### `register_camera`

Persist camera credentials to `config.yaml`. Renaming is supported: when a new name is passed but the IP or SN matches an existing entry, the old name is replaced automatically. Usually called internally by `connect_device` / `search_devices`.

**Parameters**:

| Parameter         | Type   | Required | Default              | Description                                       |
|-------------------|--------|:--:|----------------------|--------------------------------------------------|
| `name`            | string | ✅  | —                    | Unique camera name                               |
| `ip`              | string |    | `""`                 | IP address                                       |
| `port`            | int    |    | `0`                  | ONVIF port (pass only verified real ports)       |
| `username`        | string |    | `"admin"`             | Login username                                   |
| `password`        | string |    | `""`                 | Login password                                   |
| `rtsp_port`       | int    |    | `554`                | RTSP port                                        |
| `rtsp_path`       | string |    | `"/md0_0"`           | Main stream path                                 |
| `device_class`    | string |    | `"direct_connect"`   | `"password_required"` / `"direct_connect"` |
| `connection_type` | string |    | `"onvif"`            | `"onvif"` (only supported value)                        |
| `sn_code`         | string |    | `""`                 | Serial number                                    |
| `pkdk`            | string |    | `""`                 | Device public key identifier                     |
| `rtsp_sub_path`   | string |    | `"/md0_1"`           | Sub stream path                                  |

**Returns**: `RegisterResult`

| Field            | Type   | Description                        |
|------------------|--------|------------------------------------|
| `success`        | bool   | Whether registration succeeded     |
| `camera_name`    | string | Registered camera name             |
| `error_message`  | string | Failure reason (empty on success)  |

---

### `search_devices`

Scan the LAN to discover available cameras (WS-Discovery + Skyworth private protocol + JCP, three protocols, deduplicated by IP in the order Skyworth → JCP → WS-Discovery, first-come-first-served). **When multiple devices are found, present every one of them to the user individually — never omit any.**

**Searching also reconciles `config.yaml`**: devices that are discovered and reachable (RTSP probe not `unreachable`) are written into the registry via three-level matching on `name → IP → SN` (basic info only: name/IP/SN/device class/ports, never a password; existing passwords are preserved via empty-value inheritance). Registered entries not found this round and whose IP is unreachable are removed. If any discovery link fails, only registration happens — no removals (a half round of scanning is insufficient to prove a device has left the network). When a camera has not been used for a long time (its IP may have changed via DHCP) or a connection fails, call this tool first to refresh the registry before connecting.

**Parameters**:

| Parameter | Type   | Required | Default | Description                                                                                                                                   |
|-----------|--------|:--:|---------|------------------------------------------------------------------------------------------------------------------------------------------------|
| `timeout` | number |    | `15.0`  | Overall time limit (seconds). Returns early once discovery goes quiet: short re-probe rounds, ending after 2 consecutive rounds with no new devices — usually well before the limit |

**Returns**: `SearchResult` (with additional `device_count` and `_display_instruction` fields)

| Field                  | Type               | Description                            |
|------------------------|--------------------|----------------------------------------|
| `success`              | bool               | Whether the search succeeded           |
| `devices`              | DiscoveredDevice[] | List of discovered devices             |
| `device_count`         | int                | Number of devices (additional field)   |
| `_display_instruction` | string             | Display instruction (additional field) |
| `error_message`        | string             | Failure reason                         |

**DiscoveredDevice fields**:

| Field               | Type   | Description                                         |
|--------------------|--------|-----------------------------------------------------|
| `ip`               | string | IP address                                          |
| `onvif_port`       | int    | ONVIF port (0 = unknown)                            |
| `rtsp_port`        | int    | RTSP port                                           |
| `device_class`     | string | `"password_required"` / `"direct_connect"`     |
| `sn_code`          | string | Device serial number                                |
| `model`            | string | Device model                                        |
| `manufacturer`     | string | Manufacturer                                        |
| `sky_subtype`      | string | Device subtype: `1` bullet / `2` PTZ dome / `3` hemispheric / `5` pan-tilt / `6` bullet-PTZ combo |
| `sky_name`         | string | Device name                                         |
| `sky_channels`     | int    | Channel count (0 = non-Skyworth, 1 = single-lens, 2 = dual-lens) |
| `sky_hw_version`   | string | Hardware version                                    |
| `sky_sw_version`   | string | Software version                                    |
| `sky_mac`          | string | MAC address                                         |
| `discovery_method` | string | Discovery method: `"ws_discovery"` / `"sky_discovery"` / `"jcp_discovery"` |
| `rtsp_access`      | string | Main stream reachability probe result: `"open"` (reachable without auth) / `"auth_required"` (authentication required) / `"unreachable"` (unreachable, not written to the registry) |
| `protocol_type`    | string | Protocol class: `"S"` (answered SK private discovery, conclusive) / `""` (found via JCP/WS, protocol shared so not asserted; the connect-phase authoritative probe determines the final `S`/`J`/`O`) |

---

### `connect_device`

Connect to a camera. Automatically loads cached credentials (validated over RTSP; ONVIF is used for control-plane reachability); when the cache is invalid, cloud re-authorization is attempted first, and only if that fails is the user asked for input. If the camera has not been used for a long time or a previous connection/stream attempt failed, call `search_devices` first to refresh the registry (the device IP may have changed) before connecting.

**Parameters**:

| Parameter       | Type   | Required | Default | Description                          |
|-----------------|--------|:--:|---------|---------------------------------------|
| `camera_name`   | string | ✅  | —       | Camera name                          |
| `password`      | string |    | —       | User password (optional)             |
| `ip`            | string |    | —       | Device IP                            |
| `port`          | int    |    | —       | ONVIF port (auto-probed if omitted)  |
| `rtsp_port`     | int    |    | —       | RTSP port                            |
| `rtsp_path`     | string |    | —       | RTSP path                            |
| `username`      | string |    | —       | Login username                       |
| `sn_code`       | string |    | —       | Device SN                            |
| `device_class`  | string |    | —       | Device class (optional, passed through from discovery results) |
| `protocol_type` | string |    | —       | Protocol class `"S"`/`"J"`/`"O"` (may be left empty; when empty, the connect phase determines and persists it via the authoritative SK unicast probe; J-class uses ONVIF+RTSP and skips the Skyworth private probe; O = third-party ONVIF degraded access) |

**Returns**: `ConnectResult`

| Field             | Type   | Description                                                                                              |
|------------------|--------|----------------------------------------------------------------------------------------------------------|
| `success`        | bool   | Whether the connection succeeded                                                                        |
| `status`         | string | `"connected"` / `"needs_password"` / `"no_sn"` / `"failed"` / `"auth_rejected"` / `"cloud_pwd_failed"` |
| `auth_method`    | string | Auth method: `"password"` (manual or cached) / `"cloud_password"` (cloud-issued) / `"direct"`             |
| `needs_password` | bool   | Whether the user needs to provide a password                                                            |
| `onvif_port`     | int    | Verified ONVIF port (0 = unverified)                                                                    |
| `protocol_type`  | string | Device protocol class `"S"`/`"J"`/`"O"` (empty if unresolved); for O-class, explain the degraded capability set to the user |
| `error_message`  | string | Failure reason                                                                                          |

**status handling**:
- `connected` → connected, ready to operate
- `needs_password` → ask the user for the password, then call again
- `no_sn` → refuses to enter the connected state: the SN of an S/J-asserted device is missing (retry after refreshing with `search_devices`), or the ONVIF admission probe failed for a WS-Discovery device (only RTSP reachable) → report to the user; **never** bypass it via manual `register_camera` / hand-editing config.yaml
- `auth_rejected` → the cloud refused authorization
- `cloud_pwd_failed` → cloud password verification failed; ask the user to enter the correct password

---

### `disconnect_device`

Disconnect a camera and release all resources.

**Parameters**:

| Parameter     | Type   | Required | Description |
|--------------|--------|:--:|-------------|
| `camera_name` | string | ✅  | Camera name |

**Returns**: `DisconnectResult`

| Field               | Type   | Description                     |
|--------------------|--------|---------------------------------|
| `success`          | bool   | Whether disconnection succeeded |
| `session_released` | bool   | Whether the cloud session was released |
| `error_message`    | string | Failure reason                  |

---

## 2. Stream

### `get_audio_video_stream`

Get the camera's live RTSP video stream URL and metadata. Returns the stream URL only; does not capture frames.

**Parameters**:

| Parameter     | Type   | Required | Default  | Description                    |
|--------------|--------|:--:|----------|---------------------------------|
| `camera_name` | string | ✅  | —        | Camera name                     |
| `sub_stream`  | bool   |    | `false`  | Use the sub stream (lower quality) |
| `timeout_seconds` | number |    | `20`     | Max wait in seconds for the stream probe (capped at 120); enforced by the MCP layer — raise it for known slow devices on retry |

**Returns**: `StreamResult`

| Field            | Type   | Description                              |
|-----------------|--------|------------------------------------------|
| `success`       | bool   | Whether the operation succeeded          |
| `stream_url`    | string | RTSP stream URL (with credentials)       |
| `codec`         | string | Codec (e.g. `"H.264"`, `"H.265"`)       |
| `resolution`    | string | Resolution (e.g. `"1920x1080"`)          |
| `fps`           | float  | Frame rate                               |
| `bitrate`       | int    | Bitrate                                  |
| `error_message` | string | Failure reason                           |

---

### `capture_video_screenshot`

Capture a single frame from the video stream and save it as a JPEG image (single-frame snapshot). Defaults to the `snapshots/` directory.

**Parameters**:

| Parameter     | Type   | Required | Default      | Description                          |
|--------------|--------|:--:|--------------|---------------------------------------|
| `camera_name` | string | ✅  | —            | Camera name                          |
| `save_path`   | string |    | `snapshots/` | Save directory or full file path     |
| `timeout_seconds` | number |    | `20`     | Max wait in seconds for the frame grab (capped at 120); enforced by the MCP layer — raise it for known slow devices on retry |

**Returns**: `ScreenshotResult`

| Field            | Type   | Description              |
|-----------------|--------|--------------------------|
| `success`       | bool   | Whether the operation succeeded |
| `file_path`     | string | Screenshot file path     |
| `width`         | int    | Image width (pixels)     |
| `height`        | int    | Image height (pixels)    |
| `error_message` | string | Failure reason           |

---

### `toggle_recording`

Start, stop, or query local MP4 recording. Defaults to the `video/` directory.

**Parameters**:

| Parameter     | Type   | Required | Default  | Description                                                    |
|--------------|--------|:--:|----------|-----------------------------------------------------------------|
| `camera_name` | string | ✅  | —        | Camera name                                                     |
| `action`      | string | ✅  | —        | `"start"` / `"stop"` / `"status"`                             |
| `save_path`   | string |    | `video/` | Recording save directory                                        |
| `duration`    | number |    | —        | Recording duration (seconds); valid for `start` only; auto-stops when set |

**Returns**: `RecordingResult`

| Field               | Type   | Description                        |
|--------------------|--------|------------------------------------|
| `success`          | bool   | Whether the operation succeeded    |
| `is_recording`     | bool   | Whether currently recording        |
| `file_path`        | string | Recording file path                |
| `duration_seconds` | float  | Recording duration (seconds)       |
| `auto_stop`        | bool   | Whether auto-stop is set           |
| `error_message`    | string | Failure/exception reason           |

**Notes**:
- When recording multiple devices simultaneously, call them one by one (2-3 seconds apart) to avoid concurrent startup failures
- Long recordings (>10 minutes) may be interrupted by network fluctuations; inspect periodically with `status`
- On recording errors, check the `.log` file with the same name as the video for the ffmpeg exit reason

---

## 3. PTZ Control

### `control_ptz`

Control PTZ pan/tilt in four directions. Movement stops after the requested duration without querying the PTZ position.

> **Dispatched by protocol**: SK-class (`protocol_type="S"`) uses the Skyworth private protocol; JCP-class (`protocol_type="J"`) and third-party ONVIF-class (`protocol_type="O"`) use ONVIF (`ContinuousMove`/`Stop`, normalized velocity vectors). **J/O-class does not support the `degrees` angle mode** (returns an explicit unsupported notice; use `duration_seconds` instead).

**Parameters**:

| Parameter          | Type   | Required | Default | Description                                         |
|--------------------|--------|:--:|---------|------------------------------------------------------|
| `camera_name`      | string | ✅  | —       | Camera name                                          |
| `direction`        | string | ✅  | —       | Direction, see the list below                        |
| `speed`            | number |    | `0.5`   | Speed 0.0–1.0 (speed adjustment not supported by current SK direction commands) |
| `duration_seconds` | number |    | —       | Rotation duration (seconds); mutually exclusive with `degrees`; defaults to `1.0` when neither is given |
| `degrees`          | number |    | —       | Rotation angle (converted at 1 second = 34 degrees); mutually exclusive with `duration_seconds` (not supported by J/O-class) |

**direction values**: `up` / `down` / `left` / `right`

**Returns**: `PTZMoveResult`

| Field                        | Type   | Description                                                    |
|------------------------------|--------|----------------------------------------------------------------|
| `success`                    | bool   | Whether the operation succeeded                                |
| `protocol`                   | string | Protocol used (`"sky_private"` or `"onvif"`)                   |
| `requested_duration_seconds` | float  | Requested move duration                                        |
| `actual_duration_seconds`    | float  | Duration used for the movement command                         |
| `degrees`                    | float  | Requested angle in degrees mode                                |
| `method`                     | string | Execution method: `"sk_time"` / `"sk_degrees"` / `"onvif_time"` |
| `error_message`              | string | Failure reason                                                 |

---

### `stop_ptz`

Immediately stop ongoing pan/tilt movement.

**Parameters**:

| Parameter     | Type   | Required | Description |
|--------------|--------|:--:|-------------|
| `camera_name` | string | ✅  | Camera name |

**Returns**: `PTZMoveResult`

| Field            | Type   | Description              |
|-----------------|--------|--------------------------|
| `success`       | bool   | Whether the stop succeeded |
| `protocol`      | string | `"sky_private"` or `"onvif"` |
| `error_message` | string | Failure reason           |

---

## 4. Event Listening

### `manage_camera_events`

Unified management entry for camera alarm events; switches between four operating modes via `action`.

> **Not supported by J-class**: Event listening is a Skyworth private protocol capability; for JCP-class cameras (`protocol_type="J"`), all actions immediately return an explicit unsupported notice (not a timeout).

**Parameters**:

| Parameter           | Type   | Required | Default | Description                                                  |
|--------------------|--------|:--:|---------|---------------------------------------------------------------|
| `action`           | string | ✅  | —       | `"start"` / `"stop"` / `"poll"` / `"wait"`                  |
| `camera_name`      | string |    | —       | Camera name (required for `start`/`stop`; omitted means all cameras for `poll`/`wait`) |
| `debounce_seconds` | number |    | `5.0`   | Deduplication window (seconds, `start` only)                  |
| `limit`            | int    |    | `100`   | Max events returned per call (`poll` only)                    |
| `timeout_seconds`  | number |    | `60`    | Blocking timeout (seconds, capped at 60, `wait` only)         |

**Returns**:

- **`start` / `stop`** → `EventMonitorResult`:

| Field              | Type     | Description                             |
|-------------------|----------|-----------------------------------------|
| `success`         | bool     | Whether the operation succeeded         |
| `camera_name`     | string   | Camera name                             |
| `running`         | bool     | Whether monitoring is running           |
| `active_channels` | string[] | Activated protocol channels (e.g. `["private"]`) |
| `error_message`   | string   | Failure reason                          |

- **`poll` / `wait`** → `PendingEventsResult`:

| Field            | Type            | Description                           |
|-----------------|-----------------|---------------------------------------|
| `success`       | bool            | Whether the operation succeeded       |
| `events`        | CameraEvent[]   | Events consumed this time             |
| `remaining`     | int             | Number of unconsumed events in storage |
| `monitors`      | object          | Running state of each monitor         |
| `error_message` | string          | Failure reason                        |

**CameraEvent fields**:

| Field             | Type     | Description                                                                                              |
|------------------|----------|----------------------------------------------------------------------------------------------------------|
| `schema_version` | string   | `"1.0"`                                                                                                  |
| `event_id`       | string   | Unique event ID                                                                                          |
| `event_type`     | string   | Normalized event type: `motion`/`human`/`vehicle`/`tamper`/`region_intrusion`/`line_crossing`/`high_temp`/`low_temp` |
| `camera_id`      | string   | Camera registration name                                                                                 |
| `camera_name`    | string   | Display name                                                                                             |
| `timestamp`      | string   | ISO 8601 timestamp                                                                                       |
| `severity`       | string   | `"info"` / `"warning"` / `"critical"`                                                                    |
| `title`          | string   | Human-readable title                                                                                     |
| `message`        | string   | Human-readable body                                                                                      |
| `label`          | string?  | Target class (e.g. `"person"`, `"car"`); `null` when extraction is unavailable                           |
| `confidence`     | float?   | Confidence; `null` when the protocol does not provide it                                                 |
| `snapshot_path`  | string   | Linked snapshot path (may be empty within the rate-limit window)                                         |
| `tags`           | string[] | Tags (e.g. `["guardian"]`)                                                                               |

---

## 5. WebRTC Live Preview

### `start_webrtc_stream`

Start a WebRTC live preview: converts the RTSP stream into a WebRTC stream playable directly in a browser and returns an HTTP access URL.

**Parameters**:

| Parameter     | Type   | Required | Default  | Description                    |
|--------------|--------|:--:|----------|---------------------------------|
| `camera_name` | string | ✅  | —        | Camera name                     |
| `sub_stream`  | bool   |    | `false`  | Use the sub stream (lower quality) |
| `video_codec` | string |    | —        | Optional: switch the device video encoder to `"h264"`/`"h265"` before starting the preview. Device-wide (main + sub stream); omit to leave the device codec unchanged |
| `port`        | int    |    | `1984`   | Web UI port                     |

**Returns**: `WebRTCResult`

| Field            | Type   | Description                                        |
|-----------------|--------|----------------------------------------------------|
| `success`       | bool   | Whether the operation succeeded                    |
| `web_url`       | string | Browser access URL (e.g. `"http://localhost:1984"`) |
| `rtsp_url`      | string | Source RTSP URL                                    |
| `video_codec`   | string | Codec requested in this call (`"H264"`/`"H265"`); empty when `video_codec` was not passed |
| `error_message` | string | Failure reason                                     |

**Codec switching (`video_codec`)**: the tool switches the device encoder first (SK private protocol, read-modify-write — only `encode` changes, all other stream parameters are preserved), verifies by read-back, then restarts the preview. A failed switch returns `success=false` and leaves any running preview untouched. Primary use: Edge has no H265 WebRTC support, so its preview falls back to the fragile MSE path and may stutter/black out — switching to `"h264"` gives Edge a stable RTC path. The change is device-wide: NVR/recording/event-monitoring sessions on the same device are briefly interrupted (monitoring auto-reconnects).

---

### `stop_webrtc_stream`

Stop the WebRTC live preview and shut down the stream conversion process.

**Parameters**: none

**Returns**: `bool` (`true` means stopped)

---

## 6. Illumination Control

### `manage_illumination`

Query or set the camera's illumination and night-vision modes. Only two adjustments are supported: `daynightmode` (day/night mode) and `filllightmode` (fill-light mode). Controls physical illumination hardware; different from `manage_image_settings`.

> **Not supported by J-class**: Illumination/night vision is a Skyworth private protocol capability; JCP-class cameras (`protocol_type="J"`) immediately return `error_code="UNSUPPORTED_PROTOCOL"` (not a timeout).

**Parameters**:

| Parameter         | Type         | Required | Default | Description                |
|------------------|-------------|:--:|---------|-----------------------------|
| `action`          | string      | ✅  | —       | `"get"` / `"set"`          |
| `camera_name`     | string      | ✅  | —       | Camera name                 |
| `daynightmode`    | int/string  |    | —       | Day/night mode (`set` only) |
| `filllightmode`   | int/string  |    | —       | Fill-light mode (`set` only) |

**daynightmode values**:

| Value | Aliases            | Description |
|:-:|----------------------|-------------|
| 0 | `day`                | Day mode    |
| 1 | `night`              | Night mode  |
| 2 | `auto`               | Auto mode   |
| 3 | `timer`              | Timer mode  |
| 4 | `smart`              | Smart mode  |

**filllightmode values**:

| Value | Aliases               | Description       |
|:-:|-----------------------|-------------------|
| 0 | `color`               | Full-color mode   |
| 1 | `ir`                  | Infrared mode     |
| 2 | `smart`               | Smart night vision |

**Returns**:

- **`get`** → `FilllightQueryResult`:

| Field            | Type   | Description                                                                      |
|-----------------|--------|----------------------------------------------------------------------------------|
| `ok`            | bool   | Whether the operation succeeded                                                  |
| `camera`        | string | Camera name                                                                      |
| `channel`       | string | Protocol channel actually in effect (`"sk"`)                                       |
| `capabilities`  | array  | Capability list (with `name`/`label`/`min`/`max`/`current`/`current_text`/`options`) |
| `current`       | object | Current values (e.g. `{"daynightmode": 2, "filllightmode": 0}`)                    |
| `error_code`    | string | Error code                                                                       |
| `message`       | string | Description message                                                              |

- **`set`** → `FilllightSetResult`:

| Field          | Type   | Description                              |
|---------------|--------|------------------------------------------|
| `ok`          | bool   | Whether the operation succeeded          |
| `camera`      | string | Camera name                              |
| `channel`     | string | `"sk"`                                   |
| `updated`     | object | Fields applied this time (read-back confirmed) |
| `current`     | object | Current values read back after setting   |
| `verified`    | bool   | Whether read-back verification passed    |
| `error_code`  | string | Error code                               |
| `message`     | string | Description message                      |

---

## 7. Image Settings

### `manage_image_settings`

Query or set the camera's image parameters. Pure SK private protocol single channel, no ONVIF fallback. Adjusts image rendering parameters; different from `manage_illumination` (which controls the physical fill light).

> **Not supported by J-class**: Image parameter adjustment is a Skyworth private protocol capability; JCP-class cameras (`protocol_type="J"`) immediately return `error_code="UNSUPPORTED_PROTOCOL"` (not a timeout).

**Parameters**:

| Parameter     | Type   | Required | Default | Description                |
|--------------|--------|:--:|---------|-----------------------------|
| `action`      | string | ✅  | —       | `"get"` / `"set"`          |
| `camera_name` | string | ✅  | —       | Camera name                 |
| `brightness`  | int    |    | —       | Brightness (`set` only)     |
| `contrast`    | int    |    | —       | Contrast (`set` only)       |
| `saturation`  | int    |    | —       | Saturation (`set` only)     |
| `sharpness`   | int    |    | —       | Sharpness (`set` only)      |
| `flip`        | int    |    | —       | Image flip (`set` only), see the table below |

**flip values**:

| Value | Description        |
|:-:|--------------------|
| 0 | Normal             |
| 1 | Diagonal flip      |
| 2 | Horizontal flip    |
| 3 | Vertical flip      |

**Returns**:

- **`get`** → `ImageQueryResult`:

| Field            | Type   | Description                                                                      |
|-----------------|--------|----------------------------------------------------------------------------------|
| `ok`            | bool   | Whether the operation succeeded                                                  |
| `camera`        | string | Camera name                                                                      |
| `channel`       | string | `"sk"`                                                                           |
| `capabilities`  | array  | Capability list (with `name`/`label`/`min`/`max`/`current`/`current_text`/`options`) |
| `current`       | object | Current values (e.g. `{"brightness": 128, "contrast": 50, ...}`)                  |
| `error_code`    | string | Error code                                                                       |
| `message`       | string | Description message                                                              |

- **`set`** → `ImageSetResult`:

| Field          | Type   | Description                              |
|---------------|--------|------------------------------------------|
| `ok`          | bool   | Whether the operation succeeded          |
| `camera`      | string | Camera name                              |
| `channel`     | string | `"sk"`                                   |
| `updated`     | object | Fields applied this time (read-back confirmed) |
| `current`     | object | Full current values read back after setting |
| `error_code`  | string | Error code                               |
| `message`     | string | Description message                      |

---

## 8. Detection & Tracking

> **Not supported by J-class**: Smart detection/tracking is a Skyworth private protocol capability; JCP-class cameras (`protocol_type="J"`) immediately return `error_code="UNSUPPORTED_PROTOCOL"` when calling `query_tracking_capabilities` / `set_tracking` (not a timeout).

### `query_tracking_capabilities`

Query the camera's smart detection and tracking capabilities, returning available parameters and current settings for each detection type. Read-only query.

**Parameters**:

| Parameter     | Type   | Required | Default  | Description                     |
|--------------|--------|:--:|----------|----------------------------------|
| `camera_name` | string | ✅  | —        | Camera name                      |
| `detect_type` | string |    | `"all"`  | Detection type, see the list below |

**detect_type values**: `human` / `vehicle` / `area` / `motion` / `line` / `all`

**Returns**: `TrackingQueryResult`

| Field                    | Type   | Description                                              |
|-------------------------|--------|----------------------------------------------------------|
| `ok`                    | bool   | Whether the operation succeeded                          |
| `camera`                | string | Camera name                                              |
| `channel`               | string | `"sk"`                                                   |
| `human_capabilities`    | array  | Human detection capabilities (with `name`/`label`/`current`/`current_text`) |
| `human_current`         | object | Current human detection values                           |
| `vehicle_capabilities`  | array  | Vehicle detection capabilities                           |
| `vehicle_current`       | object | Current vehicle detection values                         |
| `area_capabilities`     | array  | Area detection capabilities                              |
| `area_current`          | object | Current area detection values                            |
| `motion_capabilities`   | array  | Motion detection capabilities                            |
| `motion_current`        | object | Current motion detection values                          |
| `line_capabilities`     | array  | Line-crossing detection capabilities                     |
| `line_current`          | object | Current line-crossing detection values                   |
| `error_code`            | string | Error code                                               |
| `message`               | string | Query result summary                                    |

**Settable fields** (common to all detection types): `enable` (on/off switch) / `tracking` (tracking) / `level` (sensitivity level 0-3)

---

### `set_tracking`

Turn the camera's smart detection and tracking features on or off. Modifies hardware settings; requires user confirmation. Pass only the parameters to change; omitted parameters remain unchanged.

**Parameters**:

| Parameter          | Type   | Required | Default | Description                                                        |
|-------------------|--------|:--:|---------|---------------------------------------------------------------------|
| `camera_name`      | string | ✅  | —       | Camera name                                                         |
| `detect_type`      | string | ✅  | —       | `"human"` / `"vehicle"` / `"area"` / `"motion"` / `"line"`       |
| `enable`           | bool   |    | —       | Whether to enable this detection feature                           |
| `tracking`         | bool   |    | —       | Whether to enable tracking (valid for `human`/`vehicle`/`motion` only) |
| `sensitivity_level` | int    |    | —       | Sensitivity level: `0` off / `1` low / `2` medium / `3` high        |

**Returns**: `TrackingSetResult`

| Field          | Type   | Description                              |
|---------------|--------|------------------------------------------|
| `ok`          | bool   | Whether the operation succeeded          |
| `camera`      | string | Camera name                              |
| `channel`     | string | `"sk"`                                   |
| `detect_type` | string | Detection type operated on               |
| `updated`     | object | Fields applied this time (read-back confirmed) |
| `current`     | object | Current values read back after setting   |
| `message`     | string | Description message                      |
| `error_code`  | string | Error code                               |
