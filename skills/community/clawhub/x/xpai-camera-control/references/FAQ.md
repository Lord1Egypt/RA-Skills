# FAQ & Troubleshooting Index

> English reference for **Agent self-healing** and English-speaking users · Chinese version (manual self-service): [FAQ.zh-CN.md](FAQ.zh-CN.md) · **Keep both files in sync when editing either one.**

**Self-healing posture:** this system is Agent-readable by design — on failure, the Agent diagnoses and recovers **by itself**, guided by the [SKILL.md Decision Table](../SKILL.md#decision-table--error--status--action) first and this FAQ second. Manual troubleshooting (below, and the Chinese version) is a fallback for users who explicitly want to fix things themselves.

## FAQ

### Install & Startup

**Q: `"<MCP_PYTHON>" -m pip install -r requirements.txt` is slow or fails.**
A: Use a 64-bit Python 3.10+ interpreter — `<MCP_PYTHON>` is the absolute path of the interpreter that launches the MCP server; always install via `-m pip` on that exact interpreter (a bare `pip` may belong to a different Python environment). If PyPI is slow in your region, install through a local mirror (`"<MCP_PYTHON>" -m pip install -r requirements.txt -i <mirror-url>`) — all dependencies, including the native library camera-proto, are regular PyPI packages, and mirrors apply to them equally.

**Q: A camera tool call reports "camera-proto package is not installed".**
A: The dependency is not installed in the interpreter that launches the MCP server. Run `"<MCP_PYTHON>" -m pip install -r requirements.txt` on that same interpreter (the tool error prints this command with the actual paths), then retry the tool — no server restart is needed (the loader retries on the next call, so the install takes effect in the same process). Installation happens at setup time; MCP startup itself downloads nothing.

**Q: A camera tool call reports "Failed to load camera protocol library", "Camera protocol library ABI version mismatch", or "Camera protocol library not found".**
A: Load failures are usually a system/interpreter architecture or native-dependency problem; an ABI mismatch means the camera-proto version does not pair with the facade; a missing library file means an incomplete package. First run `"<MCP_PYTHON>" -m pip install -r requirements.txt` on the interpreter that launches the MCP server to verify the pinned dependency, then retry the tool; if load failure persists, check for a 64-bit interpreter matching the system architecture.

**Q: The camera tools are not in my tool list at all.**
A: The MCP server is not registered. Follow the three-step [Installation](../SKILL.md#installation) in SKILL.md — never fall back to importing `scripts.toolkit` directly or writing wrapper scripts.

**Q: Server exits immediately; all tools unavailable (exit code 70).**
A: Exit 70 = clean shutdown after the stdio session ended (the host closed it); restarting is enough. A lock conflict no longer exits the server — the instance lock is taken lazily on first camera use, so a busy lock port surfaces as an `instance_lock_conflict` tool error on the call itself (next entry). If the exit is unexpected, read the startup stderr for the actual reason. Details: [SKILL.md Gotchas](../SKILL.md#gotchas).

**Q: Camera tools stopped working after another session started using the camera.**
A: By design: only one session holds the camera (single-instance server), and a newer session automatically takes over — the older session's connection is dropped. Retry the camera action in the session you want to use and it takes the camera back the same way — not a malfunction. If a call instead returns `instance_lock_conflict`, a non-skill program occupies the lock port: `error_message` names the PID; close it, then retry.

### Discovery & Connection

**Q: `search_devices()` finds nothing.**
A: Check camera and host share the same LAN and the camera is online. Discovery auto-selects SK private / JCP / WS-Discovery — no protocol choice needed. USB webcams are not auto-discovered (manual `config.yaml` entry; no PTZ/device management).

**Q: A camera worked yesterday but fails today.**
A: Its IP likely changed (DHCP lease renewal) and config.yaml holds a stale IP. Call `search_devices()` once to refresh the registry, then retry. Never retry repeatedly against the cached IP.

**Q: The tool keeps asking for a password (`needs_password`).**
A: Cached credentials expired and cloud re-auth also failed, the cloud service is unreachable, or the device has no SN for cloud auth. Ask the user for the device password, then `connect_device(camera_name, password=user_input)`. The password is printed on the camera's body label.

**Q: The cloud authorization prompt never gets confirmed.**
A: `connect_device` blocks waiting for confirmation in the vendor's mobile APP. Ask the user to confirm it there; the call then completes by itself.

**Q: Third-party ONVIF camera (O-class) — what works?**
A: Password connection only (no cloud auth, no SK/JCP SN). RTSP streaming and PTZ via ONVIF work; SK-private-only capabilities (events, illumination, image settings, tracking) return `UNSUPPORTED_PROTOCOL` — a device-class limitation, not a failure.

**Q: Connection refused with `no_sn`.**
A: Either an S/J-class device lost its SN (retry after `search_devices()`), or an RTSP-only device failed ONVIF admission — final, do not retry or bypass. Manually registering it or hand-editing config.yaml is forbidden.

### Stream · Screenshot · Recording

**Q: WebRTC preview is black or stutters.**
A: The browser likely lacks H265 WebRTC (e.g. Edge). Retry with `start_webrtc_stream(video_codec="h264")` — it switches the device encoder (briefly interrupting its RTSP sessions) and restarts the preview.

**Q: go2rtc is not detected.**
A: go2rtc is not bundled. Download the platform binary from the go2rtc GitHub Releases (author AlexxIT; zip archive on Windows), place it in the skill root or on `PATH`, then retry `start_webrtc_stream()`. Details: [SKILL.md Phase 3](../SKILL.md#phase-3--stream--capture).

**Q: Where are screenshots/recordings saved?**
A: `snapshots/` and `video/` (events in `events/`). If you pass a custom `save_path`, use ASCII-only paths — Chinese characters in Windows paths make `cv2.imwrite()` fail silently.

**Q: Recording never stops.**
A: Always start with `toggle_recording(action="start", duration=<seconds>)`; the server auto-stops when time is up. Agent-side "sleep then stop" buries the stop call and holds the camera's RTSP session indefinitely.

**Q: `error_code="timeout"` on stream/screenshot.**
A: Retry once with a larger `timeout_seconds` (max 120); if it still fails, check the device is online.

**Q: Screenshot/recording fails to write (file not created or empty).**
A: Possible causes: disk full, invalid `save_path` (nonexistent or no write permission; non-ASCII paths on Windows make `cv2.imwrite()` fail silently), or a recording too short to produce data. Check free space on the disk containing the actual save directory, path, and permissions, then retry. For recording errors, inspect the ffmpeg `.log` file beside the video.

### PTZ · Events · Data

**Q: PTZ `degrees` mode unsupported.**
A: The J/O-class ONVIF backend supports velocity + duration only. Use `duration_seconds`.

**Q: No events / no illumination / no image settings / no tracking.**
A: These are S-class-only capabilities. J/O-class returns `UNSUPPORTED_PROTOCOL` with a reason — inform the user of the device-class limitation; not a malfunction or timeout.

**Q: The event listener receives nothing.**
A: Events require an S-class camera and `manage_camera_events(action="start")` with explicit user confirmation; auto-resume only re-arms listeners enabled before. Poll/wait semantics: [commands/events.md](commands/events.md).

**Q: `DEVICE_UNREACHABLE` on illumination/image/tracking.**
A: Transient private-protocol port flapping — bounded auto-retry: same parameters after 2-3 s, up to 3 attempts, no user confirmation needed. Do not reconnect or rediscover mid-retry.

**Q: Does my data leave the LAN? Are passwords stored in plaintext?**
A: Usage-phase traffic is LAN-only; the connection phase talks to the vendor cloud only to verify connection status. Files are written only to `config.yaml`, `snapshots/`, `video/`, `events/`. Credentials (`password`/`sn_code`/`sn`/`pkdk`) are stored obfuscated (XOR + base64 with an `enc1:` prefix) and restored in memory only at the point of use; values passed back through the tool API are decoded exactly once.

## Best Practices

1. Session start: `get_registered_cameras()` → `connect_device()` per camera; after a long idle period, `search_devices()` first (stale DHCP IPs).
2. Fixed-duration recording only via `duration=<seconds>` — never sleep-then-stop.
3. Custom save paths: ASCII only.
4. Pure-numeric passwords/SNs must be JSON strings (`"847226"`), never bare numbers.
5. Never hand-build RTSP URLs — use the `stream_url` returned by `get_audio_video_stream()`.
6. Never hardcode ONVIF port 80 — use `onvif_port` from `search_devices()` / config.yaml.
7. Get explicit user confirmation before PTZ, streaming, screenshots, event-monitor start, and illumination/image/tracking changes.
8. Camera is single-instance: a newer session auto-takes-over the camera (the older connection is dropped) — retry your camera action in the session you want to use.
9. O-class identity uses `onvif_sn` for matching only — never feed it to cloud auth or SK HTTP as `sn_code`.
10. Building an external consumer on the event store → [EVENT_INTEGRATION.md](EVENT_INTEGRATION.md).

## Troubleshooting Index

Symptom-first map to the authoritative source (this FAQ paraphrases; the sources win on conflict):

| Symptom | Quick fix | Authoritative source |
|---------|-----------|----------------------|
| Server exits immediately; tools unavailable (exit 70) | Clean shutdown (stdio session ended) — restart; lock conflicts are tool errors now, see FAQ above | [SKILL.md Gotchas](../SKILL.md#gotchas) · README Troubleshooting |
| Tool reports "camera-proto package is not installed" / library load failure / ABI mismatch | Run `"<MCP_PYTHON>" -m pip install -r requirements.txt` with the MCP-launching interpreter, then retry the same tool (no restart needed) | [SKILL.md Decision Table](../SKILL.md#decision-table--error--status--action) · [Installation](../SKILL.md#installation) |
| `not_connected` / `needs_password` / `no_sn` / auth-failure group | Reconnect / ask for password / final-refusal handling | [SKILL.md Decision Table](../SKILL.md#decision-table--error--status--action) · [WORKFLOW.md Phase 2](WORKFLOW.md) |
| `UNSUPPORTED_PROTOCOL` on events/illumination/image/tracking | Device-class limitation, inform user | [SKILL.md Capability Matrix](../SKILL.md#extended-capabilities--protocol-matrix) · `commands/*.md` |
| Stream / screenshot / recording errors (`timeout`, `recording in progress`, write failure) | Retry rules per Decision Table | [SKILL.md Decision Table](../SKILL.md#decision-table--error--status--action) · [commands/stream.md](commands/stream.md) |
| PTZ `degrees` mode unsupported on J/O cameras | Use `duration_seconds` | [SKILL.md Phase 4](../SKILL.md#phase-4--ptz-control) · [commands/ptz.md](commands/ptz.md) |
| `DEVICE_UNREACHABLE` (illumination/image/tracking) | Bounded auto-retry ×3 | [SKILL.md Decision Table](../SKILL.md#decision-table--error--status--action) · `## Error codes` in `commands/*.md` |
| Event store external consumption | Contract & schema | [EVENT_INTEGRATION.md](EVENT_INTEGRATION.md) · [commands/events.md](commands/events.md) |
| config.yaml schema / manual pre-configuration | Full schema | [CONFIG.md](CONFIG.md) |
