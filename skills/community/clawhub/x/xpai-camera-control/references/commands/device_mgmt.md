# Device Management

Device discovery, connection, and management — exposed as MCP tools by `scripts/mcp_server.py`

> **MCP-only:** All tools below are invoked exclusively through the MCP server (`scripts/mcp_server.py`). Never import this module directly or write standalone scripts to call these functions.

---

## Safety Constraints

| Constraint | Meaning |
|------------|---------|
| **Explicit Prompt** | Inform the user what operation will be performed and wait for confirmation before executing. |
| **Code Validation** | Validate parameter legality, device state, and connection availability before executing. |

---

### `get_registered_cameras() -> List[CameraConfig]`

Read all camera entries from `config.yaml` and return their configurations.

| Aspect | Detail |
|--------|--------|
| **Safety** | None |
| **Returns** | List of `CameraConfig` objects (see field table below) |
| **Parameters** | None |
| **When to call** | At session start (Phase 0) — always call before any discovery |

**CameraConfig return fields:**

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Camera unique identifier |
| `connection_type` | string | `"onvif"` (only supported value) |
| `ip` | string | Camera IP address |
| `port` | int | ONVIF service port (0 = not yet verified) |
| `username` | string | Login username (default: `"admin"`) |
| `password` | string | Login password (decoded from config.yaml at the point of use; never display to user) |
| `rtsp_port` | int | RTSP port (default: 554) |
| `rtsp_path` | string | Main stream RTSP path |
| `rtsp_sub_path` | string | Sub stream RTSP path |
| `device_class` | string | `"password_required"` or `"direct_connect"` |
| `sn_code` | string | Device serial number |
| `pkdk` | string | Device identity token |
| `illumination_modes` | list[string] | Supported illumination parameter names (`daynightmode` / `filllightmode`) cached from the SK private-protocol fill-light capability probe (S-class devices only); empty = unsupported or not yet probed. Written by `connect_device()` after a successful connection. |
| `protocol_type` | string | Protocol class for registered cameras: `"S"` (Skyworth private), `"J"` (JCP — media + PTZ over ONVIF), or `"O"` (third-party ONVIF-only, degraded). Written by `connect_device()` via the authoritative SK-first unicast probe; `"O"` is asserted only when SK/JCP probes are empty and the ONVIF admission probe passes (`"W"` and empty both mean no class asserted yet, legacy entries are treated as SK). |
| `onvif_sn` | string | ONVIF `GetDeviceInformation` SerialNumber (O-class identity/matching only). **Never** used as `sn_code` and never fed to cloud auth or SK HTTP. Empty for S/J entries. |

---

### `register_camera(name, ip="", port=0, username="admin", password="", rtsp_port=554, rtsp_path="/md0_0", device_class="direct_connect", rtsp_sub_path="/md0_1", **kwargs) -> RegisterResult`

Write a camera entry to `config.yaml`, persisting credentials for future auto-connect.

| Aspect | Detail |
|--------|--------|
| **Safety** | None (internal config write; does not expose credentials to user) |
| **Returns** | `RegisterResult` (see field table below) |
| **Parameters** | `name`: unique camera name. `ip`: camera IP. `port`: ONVIF port — **only pass a verified port; omit when unknown (0 = unknown)**, `connect_device` probes the real port and writes it back automatically. `username`/`password`: credentials (saved obfuscated to config.yaml, never displayed; `password` accepts plaintext or an `enc1:` value and is decoded once). `rtsp_port`/`rtsp_path`: stream parameters. `device_class`: `"password_required"` or `"direct_connect"`. Additional kwargs: `sn_code`, `pkdk`, `rtsp_sub_path`, `connection_type`, `illumination_modes`, `protocol_type`, `onvif_sn` (internal — written by `connect_device`; do not set manually to bypass connection gates). |
| **When to call** | After first successful `connect_device()` |

**RegisterResult return fields:**

| Field | Type | Description |
|-------|------|-------------|
| `success` | bool | Whether the registration succeeded |
| `camera_name` | string | Name of the registered camera |
| `error_message` | string | Failure reason (empty on success) |

---

### `search_devices(timeout: float = 15.0) -> SearchResult`

Search for available cameras on the local network. The tool automatically selects the best discovery protocol and returns unified results. **Search also reconciles `config.yaml`**: every discovered device that is reachable (RTSP probe result not `"unreachable"`) is written into the registry through the same three-tier match as `register_camera` (name → IP → SN) — basic info only (name, IP, SN, device class, ports), never a password (existing credentials are preserved by the empty-value inheritance). Registered cameras that are **not** discovered in this run **and** whose IP no longer responds are removed. If any discovery provider fails, registration still runs but removal is skipped — a partial sweep cannot prove a device is gone.

| Aspect | Detail |
|--------|--------|
| **Safety** | None (writes `config.yaml`: registers discovered devices, removes unreachable stale entries) |
| **Returns** | `SearchResult` (see field tables below) |
| **Parameters** | `timeout`: discovery timeout in seconds (default 15.0). The tool internally tries all available protocols (XPAI private, JCP, ONVIF WS-Discovery) and merges results. |
| **Implementation** | Internally dispatches to the corresponding discovery protocol; results are normalized into `DiscoveredDevice` objects |

**SearchResult return fields:**

| Field | Type | Description |
|-------|------|-------------|
| `success` | bool | Whether the search succeeded |
| `devices` | list | List of `DiscoveredDevice` objects (see table below) |
| `error_message` | string | Failure reason (empty on success) |

**DiscoveredDevice fields** (each item in `devices`):

| Field | Type | Description |
|-------|------|-------------|
| `ip` | string | Device IP address |
| `onvif_port` | int | ONVIF service port (0 = unknown; probed by `connect_device`) |
| `rtsp_port` | int | RTSP port (default: 554) |
| `device_class` | string | `"password_required"` or `"direct_connect"` (classified via RTSP probe) |
| `sn_code` | string | Device serial number |
| `model` | string | Device model |
| `manufacturer` | string | Manufacturer name |
| `supported_media` | list[string] | Supported media settings |
| `discovery_method` | string | How the device was found: `"sky_discovery"` / `"jcp_discovery"` / `"ws_discovery"` |
| `rtsp_access` | string | Reachability probe result for the main stream: `"open"` (no auth) / `"auth_required"` / `"unreachable"`. Devices reported `"unreachable"` are not written to `config.yaml`. |
| `protocol_type` | string | Protocol class: `"S"` (device answered SK private discovery — conclusive) or empty (found via JCP/WS-Discovery; no class asserted, since both protocols are shared with S-class firmware). `connect_device` resolves and persists the final class (`"S"`/`"J"`/`"O"`) via the authoritative SK-first unicast probe; `"O"` (third-party ONVIF-only) is asserted at connect time when SK/JCP probes are empty and ONVIF admission passes. |
| `sky_subtype` | string | XPAI device subtype (1=bullet/2=dome/3=halfdome/5=PTZ/6=bullet+dome); empty for non-XPAI |
| `sky_name` | string | Device display name (XPAI only) |
| `sky_dtype` | string | Device type code (XPAI only) |
| `sky_hw_version` | string | Hardware version (XPAI only) |
| `sky_sw_version` | string | Software version (XPAI only) |
| `sky_did` | string | Device ID (XPAI only) |
| `sky_channels` | int | Channel count (0=non-XPAI, 1=mono, 2=binocular) |
| `sky_channel_list` | list | Channel details with RTSP codec modes (XPAI only) |
| `sky_web_port` | int | Web UI port (XPAI only) |
| `sky_udp_port` | int | UDP command port (XPAI only) |
| `sky_net_type` | string | Network type: `"eth"` / `"wifi"` (XPAI only) |
| `sky_ip_mode` | string | IP mode: 0=DHCP, 1=adaptive, 2=manual (XPAI only) |
| `sky_mask` | string | Subnet mask (XPAI only) |
| `sky_gateway` | string | Gateway address (XPAI only) |
| `sky_mac` | string | MAC address (XPAI only) |
| `supported_illumination_modes` | list[string] | Supported illumination modes probed during discovery (empty when not probed or unsupported; populated by `connect_device()` post-connect) |

---

### `connect_device(camera_name, password=None, ip=None, port=None, rtsp_port=None, rtsp_path="/md0_0", username="admin", sn_code="", device_class="", protocol_type="") -> ConnectResult`

Establish connection to a camera. Uses cached credentials (retry 3x) → user-provided password → RTSP probe, in that order.

| Aspect | Detail |
|--------|--------|
| **Safety** | None (credentials are local-only) |
| **Returns** | `ConnectResult` (see field table and scenario examples below) |
| **When to call** | Phase 0 (cached cameras), Phase 2 (new cameras) |

**ConnectResult return fields:**

| Field | Type | Description |
|-------|------|-------------|
| `success` | bool | Whether the connection succeeded |
| `auth_method` | string | Authentication method used: `"password"` (manual or cached), `"cloud_password"` (cloud-issued), or `"direct"` (empty if not connected) |
| `status` | string | `"connected"` / `"needs_password"` / `"no_sn"` / `"cloud_pwd_failed"` / `"auth_rejected"` / `"failed"` |
| `error_message` | string | Failure reason or status detail (empty on success) |
| `needs_password` | bool | `true` = Agent must prompt user for password and re-call with `password` arg |
| `onvif_port` | int | Verified ONVIF port (0 = not verified; auto-probed by `connect_device`) |
| `protocol_type` | string | Resolved protocol class of the device (`"S"`/`"J"`/`"O"`, empty when unresolved) — relay O-class degradation to the user |

**ONVIF port verification:** before the ONVIF probe, candidate ports are probed with unauthenticated `GetSystemDateAndTime`. Only ports returning a SOAP Envelope are accepted. Verified ports are written back to config.yaml automatically.

**Illumination capability probing:** after a successful connection on the password-auth and direct-connect paths (S-class devices only), `connect_device()` automatically probes the SK private-protocol fill-light capability via `probe_illumination_capability()`. The result is persisted to `config.yaml` as `illumination_modes`; probe failures are silently ignored (the field stays empty) so they never delay the connection flow. If `illumination_modes` is already cached in config.yaml from a previous session, re-probing is skipped.

**J-class (JCP) connection:** JCP cameras connect over **ONVIF + RTSP**. The SN gate falls back to JCP discovery when the SK SN probe returns nothing, so J-class devices are no longer rejected with `status="no_sn"`. On success the tool persists `protocol_type="J"`, the verified ONVIF port, and the ONVIF-authoritative main/sub RTSP paths (from `GetStreamUri`). The SK-only illumination probe is skipped for J-class.

**O-class (third-party ONVIF-only) connection:** a WS-Discovery device whose SK **and** JCP SN probes return nothing is admitted to the connected state only when the **ONVIF admission probe** passes — ONVIF port probe plus a `GetDeviceInformation()` reachability check (not a credential check). On success the tool persists `protocol_type="O"` and the ONVIF SerialNumber as `onvif_sn` (`sn_code` stays empty — it is the SK-ecosystem key and must never receive an ONVIF serial). O-class never enters cloud authorization (no SN), skips the SK illumination probe, and uses ONVIF-authoritative stream paths + ONVIF PTZ like J-class. If ONVIF admission fails (RTSP-only device), the connection is rejected with `status="no_sn"` and an explicit message; cached-O reconnects stay O without requiring a fresh ONVIF verification, and a later successful SK/JCP probe upgrades a cached O back to S/J.

**Connection flow (ONVIF → RTSP):**

1. Check `config.yaml` for cached credentials → if found, retry connection up to 3 times (1s interval) using ONVIF/RTSP verification. For password devices, the password must pass **RTSP authentication** to be considered valid. All retries fail → attempt **cloud re-authorization** (if SN available) to fetch a fresh password; cloud also fails → auto-remove registration from config.yaml → return `status="needs_password"`
2. If password provided by user → single attempt with ONVIF/RTSP verification (no retry, no cache cleanup). RTSP auth failure → `status="failed"`
3. If no password and `device_class == "password_required"` → internally initiate cloud authorization (POST request + polling). Cloud returns password → verify via ONVIF + RTSP → success: persist credentials and return `auth_method="cloud_password"`; failure: return `status="cloud_pwd_failed"`
4. If not `password_required` → probe RTSP stream:
   - `200 OK` (direct-connect) → probe SN via XPAI private protocol → register to config.yaml with SN → `auth_method="direct"`
   - `200 OK` but SN probes empty → ONVIF admission probe: pass → register as `protocol_type="O"` with `onvif_sn` → `auth_method="direct"`; fail → `status="no_sn"` rejection (RTSP-only device)
   - `401 Unauthorized` → SN probes empty and no S/J assertion → `status="needs_password"` (O-class has no cloud channel); otherwise internally initiate cloud authorization (same as step 3)
5. Cloud authorization outcomes: authorized → auto-connect with cloud password and return `auth_method="cloud_password"`; rejected → `status="auth_rejected"`; timeout/error → `status="needs_password"`. A device with no cloud station record is submitted to the default station (same host as the station-lookup interface); transport, TLS, HTTP and signature failures are reported directly — no fallback

**Password verification standard:** A password is valid only when RTSP DESCRIBE returns 200. ONVIF `GetDeviceInformation` is a control-plane reachability check and may succeed with any password; RTSP 401 or an unreachable RTSP port rejects the password.

#### Return JSON examples by scenario

**Cached credentials — auto-connect (Phase 0):**
```json
{
  "success": true,
  "auth_method": "password",
  "status": "connected",
  "error_message": "",
  "needs_password": false,
  "onvif_port": 8000
}
```

**Cached credentials failed (cloud re-auth attempted, registration auto-removed):**
```json
{
  "success": false,
  "auth_method": "",
  "status": "needs_password",
  "error_message": "Cached credentials cleared (invalid: RTSP authentication failed (password may be invalid for RTSP)). Cloud re-auth re-issued the same stale credential; approving again cannot pass device verification. Enter the current correct password for device living_room_camera (192.168.1.100) manually.",
  "needs_password": true,
  "onvif_port": 0
}
```
→ Agent: prompt user for password → `connect_device(camera_name, password=user_input, ip=...)`.

**Direct-connect — no password needed:**
```json
{
  "success": true,
  "auth_method": "direct",
  "status": "connected",
  "error_message": "",
  "needs_password": false,
  "onvif_port": 0
}
```

**Password required (no cached credentials):**
```json
{
  "success": false,
  "auth_method": "",
  "status": "needs_password",
  "error_message": "Device living_room_camera (192.168.1.100) requires a password. Please provide the camera's admin password (default username is usually admin).",
  "needs_password": true,
  "onvif_port": 0
}
```
→ Agent: prompt user for password, then re-call `connect_device(camera_name, password=user_input, ip=..., rtsp_port=...)`.

**Connection failed (user-provided password wrong):**
```json
{
  "success": false,
  "auth_method": "",
  "status": "failed",
  "error_message": "Password authentication failed: RTSP authentication failed (password may be invalid for RTSP); verify the password and retry",
  "needs_password": true,
  "onvif_port": 8000
}
```

**RTSP port unreachable (password not verified):**
```json
{
  "success": false,
  "auth_method": "",
  "status": "failed",
  "error_message": "Password authentication failed: RTSP port unreachable; password not verified over RTSP; verify the password and retry",
  "needs_password": true,
  "onvif_port": 8000
}
```

**Cloud password verification failed (credential isolation or password mismatch):**
```json
{
  "success": false,
  "auth_method": "",
  "status": "cloud_pwd_failed",
  "error_message": "The password delivered by the cloud failed verification on device living_room_camera (192.168.1.100) (RTSP authentication failed (password may be invalid for RTSP)). The device may have had its LAN password changed or has credential isolation. Please enter the correct LAN password.",
  "needs_password": true,
  "onvif_port": 0
}
```
→ Agent: prompt user for password → `connect_device(camera_name, password=user_input)`.

---

### `disconnect_device(camera_name) -> DisconnectResult`

Disconnect a camera and release all resources (ONVIF connection, session state).

| Aspect | Detail |
|--------|--------|
| **Safety** | None |
| **Returns** | `DisconnectResult` (see field table below) |
| **When to call** | When the user is done with a camera or before re-connecting with new credentials |

**DisconnectResult return fields:**

| Field | Type | Description |
|-------|------|-------------|
| `success` | bool | Whether the disconnect succeeded |
| `session_released` | bool | Whether the cloud session was released |
| `error_message` | string | Failure reason (empty on success) |

---
