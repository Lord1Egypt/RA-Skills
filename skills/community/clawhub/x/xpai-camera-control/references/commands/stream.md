# Stream & Capture

Audio/video streaming, snapshot capture, and recording — exposed as MCP tools by `scripts/mcp_server.py`

> **MCP-only:** All tools below are invoked exclusively through the MCP server (`scripts/mcp_server.py`). Never import this module directly or write standalone scripts to call these functions.

---

### `get_audio_video_stream(camera_name, sub_stream: bool = False, timeout_seconds: Optional[float] = None) -> StreamResult`

Fetch the real-time video stream URL.

| Aspect | Detail |
|--------|--------|
| **Safety** | Explicit Prompt + Code Validation |
| **Returns** | `StreamResult` (see field table below) |
| **Parameters** | `camera_name`: camera identifier. `sub_stream`: use sub-stream (lower quality) if `True`. `timeout_seconds`: max wait in seconds for the stream probe (default 20, max 120); raise it for known slow devices. |
| **Agent behavior** | Output the complete `stream_url` unchanged so the user can copy it into a media player (VLC, ffplay, PotPlayer). The URL contains credentials; do not share it publicly. |

**Execution model:** the stream probe runs **in-process via OpenCV (FFmpeg backend)** with hard per-stage timeouts (8 s open / 5 s read). RTSP media transport is **TCP on all supported OpenCV versions (≥ 4.8, empirically verified)**; the code additionally requests TCP explicitly (with UDP fallback) on legacy builds where the OpenCV API still allows selecting the transport. On open failure the main ↔ sub stream paths are tried in turn. There is **no code-level serial slot** — see the concurrency guidance under `capture_video_screenshot`. The MCP layer enforces a tool-level timeout (`timeout_seconds`).

**Timeout errors:** a tool-level timeout returns `{"success": false, "error_code": "timeout", ...}`. On timeout, the Agent may retry once with a larger `timeout_seconds`.

**StreamResult return fields:**

| Field | Type | Description |
|-------|------|-------------|
| `success` | bool | Whether the stream URL was retrieved |
| `stream_url` | string | RTSP URL with auto-injected credentials (e.g. `rtsp://admin:pass@192.168.1.100:554/md0_0`) |
| `codec` | string | Video codec: `"H.264"` / `"H.265"` / `"MJPEG"` |
| `resolution` | string | Resolution string (e.g. `"2560x1440"`) |
| `fps` | float | Frame rate |
| `bitrate` | int | Bitrate in kbps (0 if unavailable) |
| `error_message` | string | Failure reason (empty on success) |

---

### `capture_video_screenshot(camera_name, save_path: Optional[str] = None, timeout_seconds: Optional[float] = None) -> ScreenshotResult`

Capture a single frame from the current video stream and save as JPEG.

| Aspect | Detail |
|--------|--------|
| **Safety** | Explicit Prompt + Code Validation |
| **Returns** | `ScreenshotResult` (see field table below) |
| **Parameters** | `camera_name`: camera identifier. `save_path`: output directory path (optional; defaults to `snapshots/`). `timeout_seconds`: max wait in seconds for the frame grab (default 20, max 120); raise it for known slow devices. |
| **Agent behavior** | Display the screenshot image to the user using the `file_path` (e.g. `![screenshot](file_path)` in markdown). |

**Execution model:** RTSP screenshots run **in-process via OpenCV (FFmpeg backend)** over **TCP** (the default on all supported OpenCV versions ≥ 4.8, empirically verified; explicit TCP-first with UDP fallback applies only on legacy builds where the transport is selectable). Fallback ladder: stream path **main → sub**, and — beyond a plain open-only retry — a path is also retried when the session **opens but yields no decodable frame** (the classic "device accepted the session but the RTP pipeline stalled" shape, e.g. firmware resource contention during PTZ movement, or session-slot exhaustion after long idle). Each open attempt is bounded by 8 s open / 5 s read timeouts; on total failure the whole grab is retried once after 1 s. The MCP layer enforces a tool-level timeout (`timeout_seconds`).

**Concurrency guidance (Agent responsibility — there is no code-level serial slot):** these cameras have very few RTSP session slots and concurrent sessions can hang the device. Do **not** screenshot while the camera is recording (stop the recording first), and do **not** fan out simultaneous screenshots to multiple cameras — serialize such calls yourself.

**Timeout errors:** a tool-level timeout returns `{"success": false, "error_code": "timeout", ...}`. On timeout, the Agent may retry once with a larger `timeout_seconds`.

**ScreenshotResult return fields:**

| Field | Type | Description |
|-------|------|-------------|
| `success` | bool | Whether the screenshot was captured |
| `file_path` | string | Full path of the saved JPEG file |
| `width` | int | Image width in pixels |
| `height` | int | Image height in pixels |
| `error_message` | string | Failure reason (empty on success) |

**Note:** Uses `imencode` + `tofile` instead of `cv2.imwrite()` to support file paths containing non-ASCII characters (e.g. Chinese usernames on Windows).

---

### `toggle_recording(camera_name, action, save_path=None, duration=None) -> RecordingResult`

Start, stop, or query the status of local video recording.

| Aspect | Detail |
|--------|--------|
| **Safety** | Explicit Prompt + Code Validation |
| **Returns** | `RecordingResult` (see field table below) |
| **Parameters** | `camera_name`: camera identifier. `action`: `"start"`, `"stop"`, or `"status"`. `save_path`: recording directory (optional; defaults to `video/`). `duration`: recording duration in seconds (optional, auto-stops when set; only for `start`). |

**RecordingResult return fields:**

| Field | Type | Description |
|-------|------|-------------|
| `success` | bool | Whether the operation succeeded |
| `is_recording` | bool | Current recording state (`true` after start, `false` after stop/status query) |
| `file_path` | string | Recording file path (populated on stop) |
| `duration_seconds` | float | Recorded duration in seconds (populated on stop; elapsed time on `status`) |
| `auto_stop` | bool | Whether a fixed-duration auto-stop is set (`duration` was passed on `start`) |
| `error_message` | string | Failure reason (empty on success) |
