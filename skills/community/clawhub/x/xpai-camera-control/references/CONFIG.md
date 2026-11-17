# Configuration Reference

Full schema for `config.yaml` — the configuration file for the Camera Control skill.

## File Location

Place `config.yaml` at the skill root (`xpai-camera-control/config.yaml`) to define camera configurations. Cameras discovered at runtime via the XPAI private protocol, JCP, or WS-Discovery do not need to be pre-configured. USB webcams are **not supported** by this skill — LAN IP cameras (ONVIF/RTSP) only.

**Automatic sync:** `search_devices()` writes every discovered and reachable camera into this file (basic info only — name, IP, SN, device class, ports; never a password) and removes entries that are no longer discoverable **and** unreachable. `connect_device()` persists credentials and the verified ONVIF port after a successful connection. Manual edits are possible but not required.

**Sensitive field storage:** `password`, `sn_code`, `sn`, and `pkdk` are stored obfuscated as `enc1:` + base64(XOR) — never plaintext on disk. Values are decoded exactly once at the point of use; an `enc1:` value passed back through a tool argument is decoded, not re-encoded. Tool arguments accept plaintext or an `enc1:` value. Legacy entries without the prefix remain readable and are rewritten with it on the next registration/sync. Do not hand-edit these fields; an unreadable value is treated as missing and the toolkit re-asks for credentials (`needs_password`). All other fields are stored as plaintext and can be edited normally.

---

## Full Schema

```yaml
# ── Camera definitions ──
cameras:
  - name: string              # Required. Unique camera identifier
    connection_type: string   # "onvif" (only supported value)

    # ONVIF-specific (dual-format fields for cross-scheme compatibility)
    ip: string                # Camera IP address
    port: int                 # ONVIF service port (0 = unknown/unverified; auto-probed & written back by connect_device)
    onvif_port: int           # Alias for port (password auth scheme compatibility)
    username: string          # Login username (default: "admin")
    password: string          # Login password (stored as "enc1:..." XOR+base64, never plaintext)
    rtsp_port: int            # RTSP port (default: 554)
    rtsp_path: string         # Main stream path (default: "/md0_0")
    rtsp_path_main: string    # Alias for rtsp_path (password auth scheme compatibility)
    rtsp_sub_path: string     # Sub stream path (default: "/md0_1")
    rtsp_path_sub: string     # Alias for rtsp_sub_path (password auth scheme compatibility)

    # Device identity (populated by discovery or manual entry)
    sn_code: string           # Device serial number (stored as "enc1:..." obfuscated, never plaintext)
    sn: string                # Alias for sn_code (stored as "enc1:..." obfuscated; password auth scheme compatibility)
    onvif_sn: string          # ONVIF GetDeviceInformation SerialNumber (O-class identity/matching only — NEVER used as sn_code / for cloud auth; stored plaintext)
    pkdk: string              # Device identity token (populated during registration; stored as "enc1:..." obfuscated, never plaintext)

    # Device classification
    device_class: string      # "password_required" | "direct_connect" (auto-detected via RTSP probe)

    # Illumination capability (probed at connect time via the SK private protocol, cached)
    illumination_modes: list   # Supported illumination modes; empty = unsupported or not yet probed

    # Protocol classification (resolved and persisted by connect_device via the authoritative SK-first unicast probe)
    protocol_type: string      # "S" (Skyworth private) | "J" (JCP, ONVIF PTZ + RTSP media) | "O" (third-party ONVIF-only, degraded) | "" (not yet resolved; legacy values incl. "W" are treated as SK)

```

---

## Camera Config Details

### `name` (required)

Unique string identifier for the camera.

- Static cameras: use descriptive names like `living_room`, `front_door`
- Auto-discovered cameras: registered as `<model|SN|"camera">_<last IP octet>` (e.g. `CSDE2_107` for a camera at `192.168.1.107`). The name is derived from the discovery result — when a camera's IP changes, the next `search_devices()` re-registers it under a name derived from the new IP.

### `connection_type` (required)

| Value | Protocol | Use case |
|-------|----------|----------|
| `onvif` | ONVIF + RTSP | LAN IP cameras (the only supported connection type) |

### ONVIF Parameters

| Field | Default | Notes |
|-------|---------|-------|
| `ip` | `""` | Required for ONVIF cameras. |
| `port` | `0` (unknown) | ONVIF service port. **Only verified ports are persisted** — `connect_device` probes candidates and writes back the real port automatically. `0` means not yet verified. |
| `onvif_port` | — | Alias for `port`. Written for compatibility with password auth scheme. |
| `username` | `"admin"` | ONVIF login username. |
| `password` | `""` | ONVIF login password. Auto-cached to config.yaml as an "enc1:"-prefixed obfuscated value after successful connection. The tool argument accepts plaintext. |
| `rtsp_port` | `554` | RTSP streaming port. |
| `rtsp_path` | `"/md0_0"` | Main stream RTSP path. Aliases: `rtsp_path_main`. XPAI cameras use vendor-specific paths; the toolkit auto-tries fallback paths when the configured path fails. |
| `rtsp_sub_path` | `"/md0_1"` | Sub stream RTSP path. Aliases: `rtsp_path_sub`. Same fallback behavior as main stream. |

### Device Identity Parameters

| Field | Default | Notes |
|-------|---------|-------|
| `sn_code` | `""` | Device serial number from SK/JCP discovery — the key of the SK private-protocol ecosystem (cloud authorization, SK HTTP illumination/image). Never populate it with an ONVIF serial. Stored as an "enc1:"-prefixed obfuscated value. |
| `sn` | `""` | Alias for `sn_code`. Written for compatibility with password auth scheme. Stored as an "enc1:"-prefixed obfuscated value. |
| `onvif_sn` | `""` | ONVIF `GetDeviceInformation` SerialNumber, persisted only for O-class entries. Identity/matching only (e.g. re-aligning a registry entry after a DHCP IP change) — **never** used as `sn_code`, never sent to cloud auth or SK HTTP. |
| `pkdk` | `""` | Device identity token. Populated automatically during registration. Stored as an "enc1:"-prefixed obfuscated value. |
| `device_class` | auto | Auto-detected by RTSP probe: 401 response → `"password_required"` (needs username/password); 200 response → `"direct_connect"` (no password, connects immediately). |
| `illumination_modes` | `[]` | Probed by `connect_device()` after a successful connection via the SK private-protocol fill-light capability query (`probe_illumination_capability`, S-class devices only). Contains the supported illumination parameter names/modes or an empty list when the device does not support illumination control or the probe did not succeed. Written to config.yaml after the probe; subsequent sessions read the cache and skip re-probing. |
| `protocol_type` | `""` | Protocol class resolved and persisted by `connect_device` via the authoritative SK-first unicast probe: `"S"` (Skyworth private — full feature set), `"J"` (JCP — media over RTSP + PTZ over ONVIF; illumination/image/tracking/events and PTZ degrees are unsupported), or `"O"` (third-party ONVIF-only — same degradation as J plus **no cloud authorization**; asserted only when SK/JCP probes are empty and the ONVIF admission probe passes). `search_devices` only asserts `"S"` when the device answered SK private discovery (conclusive); devices found via JCP/WS-Discovery carry no asserted class, since both protocols are shared with S-class firmware. Empty = not yet resolved (legacy values incl. `"W"` are treated as SK). |

### RTSP URL Construction

The system builds RTSP URLs internally by auto-injecting credentials:

```
rtsp://{username}:{password}@{ip}:{rtsp_port}{rtsp_path}
```

When ONVIF is available, the URL is fetched dynamically via `GetStreamUri` which may return a different path. Bare RTSP URLs from ONVIF are auto-injected with auth credentials (existing credentials in the URL are replaced). URL encoding is applied to username and password.


## Example Configs

### Single ONVIF camera (password-required)

```yaml
cameras:
  - name: office_cam
    connection_type: onvif
    ip: 192.168.1.100
    port: 2000          # verified ONVIF port (written back by connect_device)
    onvif_port: 2000
    username: admin
    password: "<enc1:obfuscated>"   # stored obfuscated — never plaintext
    rtsp_port: 554
    rtsp_path: /stream1
    rtsp_path_main: /stream1
    rtsp_sub_path: /stream2
    rtsp_path_sub: /stream2
    sn_code: "<enc1:obfuscated>"
    sn: "<enc1:obfuscated>"
    device_class: password_required
    illumination_modes: ["daynightmode", "filllightmode"]
```

### Direct-connect camera (no password)

```yaml
cameras:
  - name: front_cam
    connection_type: onvif
    ip: 192.168.1.50
    port: 2000
    username: admin
    password: ""
    rtsp_port: 554
    rtsp_path: /stream1
    device_class: direct_connect
```

### JCP (J-class) camera

```yaml
cameras:
  - name: garage_jcp
    connection_type: onvif
    ip: 192.168.1.112
    port: 2000              # verified ONVIF port (JCP devices commonly use 2000)
    onvif_port: 2000
    username: admin
    password: "<enc1:obfuscated>"
    rtsp_port: 554
    rtsp_path: /md0_0       # ONVIF-authoritative main stream path (from GetStreamUri)
    rtsp_sub_path: /md0_1   # ONVIF-authoritative sub stream path
    sn_code: "<enc1:obfuscated>"
    device_class: password_required
    protocol_type: J        # media over RTSP, PTZ over ONVIF; SK-only features unsupported
```

### Mixed: ONVIF (password) + direct-connect

```yaml
cameras:
  - name: main_ipc
    connection_type: onvif
    ip: 192.168.1.100
    port: 2000
    onvif_port: 2000
    username: admin
    password: "<enc1:obfuscated>"
    rtsp_port: 554
    rtsp_path: /stream1
    rtsp_path_main: /stream1
    sn_code: "<enc1:obfuscated>"
    sn: "<enc1:obfuscated>"
    device_class: password_required

  - name: garden_cam
    connection_type: onvif
    ip: 192.168.1.200
    port: 2000
    username: admin
    password: ""
    rtsp_port: 554
    rtsp_path: /stream1
    device_class: direct_connect
```

### Third-party ONVIF camera (O-class, degraded)

```yaml
cameras:
  - name: office_thirdparty
    connection_type: onvif
    ip: 192.168.1.120
    port: 80                # verified ONVIF port (written back by connect_device)
    onvif_port: 80
    username: admin
    password: "<enc1:obfuscated>"
    rtsp_port: 554
    rtsp_path: /Streaming/Channels/101    # ONVIF GetStreamUri-authoritative path
    rtsp_sub_path: /Streaming/Channels/102
    device_class: password_required
    protocol_type: O        # asserted by connect_device: SK/JCP silent, ONVIF admission passed
    onvif_sn: "0123456789ABCDEF"   # ONVIF SerialNumber — identity only, never sn_code
    # sn_code / sn intentionally absent: O-class has no SK/JCP SN; cloud auth unavailable
```

