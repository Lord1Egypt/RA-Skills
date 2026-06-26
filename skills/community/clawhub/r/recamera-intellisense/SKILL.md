---
name: recamera-intellisense
description: Register and control reCamera Pro devices from an agent — onboard cameras, pick AI detection models by name, configure rule-based triggers (AI / timer / GPIO / TTY / HTTP / always-on), poll detection events with snapshots, capture JPG/RAW/MP4 on demand, browse recorded clips, manage storage, and drive GPIO pins. Uses a bundled stdlib-only Python SDK invoked via a single JSON argument per command. Trigger this skill whenever the user mentions reCamera, camera onboarding, object/person detection, event polling, snapshot or video capture, recording rules, on-device GPIO, or asks to wire a physical camera into an agent workflow — even when they don't name the product explicitly.
metadata: {
  "openclaw": {
    "emoji": "📷",
    "requires": {
      "bins": ["python3"],
      "config_paths": ["~/.recamera/devices.json"]
    }
  }
}
user-invocable: true
---

# reCamera Intellisense

Drive one or more [reCamera Pro (Pending Release)](https://wiki.seeedstudio.com/recamera/) devices: device registration, AI detection configuration, rule-based recording, event polling, on-demand capture, storage/records management, and GPIO control. The skill bundles a Python SDK (`scripts/recamera_intellisense/`) that is the **single source of truth** for every command's parameters; the same package backs the MCP server, so CLI and MCP schemas are identical.

## Requirements

- `python3` ≥ 3.9 (stdlib only — no `pip install` needed)
- Reachable reCamera HTTP/HTTPS API (default TCP `80`/`443`) **or** a local `rcisd` daemon serving HTTP over the Unix socket `/dev/shm/rcisd.sock`
- Per-device auth token in the form `sk_<chars>` (Web Console → Device Info → Connection Settings → HTTP/HTTPS)
- Credential store at `~/.recamera/devices.json` (auto-created, chmod `600`). Shared with the MCP server if installed.

## Security

- **Tokens are long-lived bearer credentials** — do not commit `~/.recamera/devices.json` (auto-created `chmod 600`), and avoid logging the `token` field.
- **Same-origin redirect enforcement** — the HTTP client refuses to follow any 3xx redirect whose `(scheme, host, port)` differs from the registered device, so the bearer token is never forwarded to an unexpected origin (SSRF-safe).
- **Secure-by-default TLS** — HTTPS devices validate the certificate chain unless you explicitly register with `"allow_unsecured": true` (intended for self-signed LAN certs; do not use on the public Internet).
- **HTTP is the default transport.** On untrusted networks, provision HTTPS on the device and register with `"protocol":"https"` plus a trusted cert.
- **Path hygiene** — `fetch_file` / `delete_file` reject non-absolute paths, `..` traversal segments, and NUL bytes client-side; the daemon additionally enforces an allowlist.
- **Scope of trust**: this skill reads and writes files on the camera (captures, events), controls GPIO, and can format storage. Only point it at hardware you own.
- **Source review encouraged** — the full SDK is under `scripts/recamera_intellisense/`; every command is a short, stdlib-only Python function.

## Invocation

The bundled SDK runs without installation. From `{baseDir}` (the skill root):

```bash
# One-shot
PYTHONPATH="{baseDir}/scripts" python3 -m recamera_intellisense <command> '<json>'

# Convenience alias for a session
export PYTHONPATH="{baseDir}/scripts"
alias rci='python3 -m recamera_intellisense'
rci list_devices
```

Calling convention (uniform across every command):

- **Input**: exactly one CLI positional argument — a JSON object whose keys match the function's keyword parameters. Omit the argument for commands with no required fields (e.g. `list_devices`).
- **Success**: pretty-printed JSON on stdout (mutating commands may print nothing); exit code `0`.
- **Failure**: actionable message on stderr; non-zero exit code. Surface the stderr back to the user and propose one concrete fix.
- **Discovery**: `python3 -m recamera_intellisense` with no args prints every command with its required/optional keys.

Python use (in-process, preferred for loops):

```python
import sys, time
sys.path.insert(0, "{baseDir}/scripts")
from recamera_intellisense import (
    list_devices, set_detection_rules, get_detection_events,
    capture_image, fetch_file,
)
```

## Command catalogue

All commands accept `device_name` (string) unless noted. `device_name` resolves against `~/.recamera/devices.json`; run `list_devices` to see what is registered. Selector commands (`get_device`, `remove_device`, everything that takes `device_name`) also accept the alias `name`, so a record emitted by `list_devices` can be forwarded verbatim.

### Device registry
| Command | Required | Optional |
|---|---|---|
| `detect_local_device` | — | `socket_path` (default `/dev/shm/rcisd.sock`) |
| `add_device` | `name`, `host`, `token` | `protocol` (`http`/`https`), `allow_unsecured`, `port` |
| `update_device` | `device_name` | any of `host`, `token`, `protocol`, `allow_unsecured`, `port` |
| `remove_device` / `get_device` | `device_name` | — |
| `list_devices` | — | — |

`add_device` / `update_device` probe `/api/v1/recamera-generate-204` before persisting; a bad token or host fails fast.

### Detection (high-level facade, AI-only)
| Command | Required | Optional |
|---|---|---|
| `get_detection_models_info` | `device_name` | — |
| `get_detection_model` | `device_name` | — |
| `set_detection_model` | `device_name` | **one of** `model_id` or `model_name`, `fps` (default 30) |
| `get_detection_schedule` / `set_detection_schedule` | `device_name` | `schedule` (null / empty list / omit the key disables → always active) |
| `get_detection_rules` | `device_name` | — |
| `set_detection_rules` | `device_name`, `rules` | `ensure_writer` (default `true`), `ensure_storage` (default `true`) |
| `get_detection_events` | `device_name` | `start_unix_ms`, `end_unix_ms` (inclusive) |
| `clear_detection_events` | `device_name` | — |

`set_detection_rules` installs an `inference_set` record trigger and, by default, enables the rule pipeline with a JPG writer and a ready storage slot — override only if the caller already configured them. `get_detection_rules` returns `[]` whenever the current trigger is **not** `inference_set`.

### Rule system (low-level, all trigger kinds)
`get_rule_system_info`, `get_record_config`, `set_record_config`, `get_schedule_rule`, `set_schedule_rule`, `get_record_trigger`, `set_record_trigger`, `activate_http_trigger`. Use these to combine detection with non-AI triggers (see below) or to tune the writer.

### Capture (independent of rule pipeline)
| Command | Required | Optional |
|---|---|---|
| `get_capture_status` | `device_name` | — |
| `start_capture` | `device_name` | `output` (absolute **on-device** directory; omit to use the selected storage slot), `format` (`JPG`/`RAW`/`MP4`), `video_length_seconds` |
| `stop_capture` | `device_name` | — |
| `capture_image` | `device_name` | `output`, `timeout` |

`capture_image` is the one-shot helper: it starts a `JPG`, polls until terminal, fetches the file, and returns `{event, path, size, content_base64}` (where `event` is the terminal capture event with `status == "COMPLETED"`). For `MP4`, drive the pipeline manually: `start_capture` → poll `get_capture_status` until `last_capture.status` is terminal (`COMPLETED` / `FAILED` / `INTERRUPTED` / `CANCELED`) → `fetch_file` using the event's `output_directory` + `file_name`. `stop_capture` is only meaningful for in-flight video.

### Storage
`get_storage_status`, `set_storage_slot`, `configure_storage_quota`, `storage_task_submit`, `storage_task_status`, `storage_task_cancel`. Actions: `FORMAT`, `FREE_UP`, `EJECT`, `REMOVE_FILES_OR_DIRECTORIES` (the last requires `files`, paths relative to the slot's data directory). Default is async; `"sync": true` is accepted only for fast actions (`EJECT`, `REMOVE_FILES_OR_DIRECTORIES`) — `FORMAT`/`FREE_UP` must run async and be polled with `storage_task_status`.

### Records (relay-backed browsing, recommended for recordings)
- `list_records {device_name, path?, dev_path?, limit?, offset?}` — `path` is relative to the record data directory (empty = root). Returns a paginated object `{entries, offset, limit, total, has_more}`; directories sort first, then by name. `limit` defaults to `100`, max `500`. Slot auto-resolved if `dev_path` omitted.
- `fetch_record {device_name, path, dev_path?, max_inline_bytes?}` — images/≤5 MiB inline as base64; videos or larger payloads return `{url, size, note}`.

### Files (daemon, arbitrary absolute paths)
- `fetch_file {device_name, path, max_inline_bytes?}` — for detection-event snapshots (`snapshot_path` is absolute) and arbitrary allowed paths. Returns `{path, content_type, size, content_base64}` inline, or `{path, content_type, size, note}` when oversized. (Python callers may also pass `raw=True` to get raw `bytes`; the CLI does not accept `raw`.)
- `delete_file {device_name, path}`.

### GPIO
`list_gpios`, `get_gpio_info {pin_id}`. `set_gpio_value {pin_id, value}` drives `0` or `1` and auto-reconfigures the pin as push-pull output. `get_gpio_value {pin_id, debounce_ms?}` returns `0` or `1` and auto-reconfigures the pin as floating input. Debounce defaults to 100 ms; when `debounce_ms > 0` and the pin's edge mode was `none`, the SDK also switches it to both-edge detection (the device rejects debounce with `edge=none`). Both calls have this side effect on pin direction — don't use them as read-only probes.

## Key schemas

### Detection rule
```json
{
  "name": "front-door-person",
  "debounce_times": 3,
  "confidence_range_filter": [0.25, 1.0],
  "label_filter": ["person"],
  "region_filter": [[[0.1,0.1],[0.9,0.1],[0.9,0.9],[0.1,0.9]]]
}
```

- `label_filter` contains **label names as they appear in `get_detection_models_info`.labels** — never indexes. Leave empty to match any label.
- `region_filter` is a list of polygons of normalized `[x, y]` in `[0,1]`; omit or leave null for the full frame.
- `confidence_range_filter` is `[min, max]` with both in `[0.0, 1.0]` and `min ≤ max`; defaults to `[0.25, 1.0]`. `debounce_times` defaults to `3` (consecutive matching frames).

### Schedule range
`{"start": "Mon 08:00:00", "end": "Mon 18:00:00"}` — three-letter day (`Mon`/`Tue`/`Wed`/`Thu`/`Fri`/`Sat`/`Sun`); `Day 24:00:00` is valid. Pass a list; `null` or `[]` disables and means "always active".

### Record trigger (tagged union, `kind` field)
```json
{"kind":"inference_set", "rules":[ /* DetectionRule[] */ ]}
{"kind":"timer", "interval_seconds": 60}
{"kind":"gpio", "num":1, "state":"PULL_UP", "signal":"FALLING", "debounce_ms":50}
{"kind":"tty",  "name":"tty0", "command":"SHOOT"}
{"kind":"http"}
{"kind":"always_on"}
```
For `gpio` provide one of `name` or `num`; `state` ∈ {`DISABLED`,`FLOATING`,`PULL_UP`,`PULL_DOWN`}; `signal` ∈ {`HIGH`,`LOW`,`RISING`,`FALLING`}.

### Detection event
```json
{"timestamp":"2026-04-20T12:34:56Z","timestamp_unix_ms":1745152496000,"rule_name":"front-door-person","snapshot_path":"/mnt/.../abcd.jpg"}
```
`snapshot_path` (when present) is an absolute on-device path — feed it to `fetch_file`, not `fetch_record`.

## Agent rules

1. Always supply a complete JSON object; never prompt interactively.
2. Identify the target by `device_name` (preferred). `list_devices` is cheap — call it if unsure.
3. Token format must match `sk_[A-Za-z0-9_\-]+`; validation is enforced by `add_device`.
4. `label_filter` takes **label names** from `get_detection_models_info`. Do not translate names into numeric indexes — the MCP/SDK expects strings.
5. For AI-only use, prefer `set_detection_rules` (it ensures writer + storage). For hybrid triggers (GPIO, timer, TTY, HTTP, always-on), use `set_record_trigger` directly — only one record trigger is active at a time.
6. Poll `get_detection_events` with a checkpointed `start_unix_ms` (1–10 s cadence). Events accumulate on-device; `clear_detection_events` to reset.
7. Prefer event metadata first; fetch imagery only when the user needs it. Images/≤5 MiB inline; videos/larger return a URL + `note`.
8. When a storage slot is required (rules, timer, always-on), the facade's `ensure_storage=true` default will select the internal slot if none is enabled; for removable media the user must provision a slot beforehand.

## Workflows

### 1 — Onboard a device
1. (Optional) `detect_local_device` to confirm a local daemon.
2. `add_device '{"name":"cam1","host":"192.168.1.100","token":"sk_xxxx"}'`.
3. `list_devices` to confirm.

### 2 — Person/object detection by name
1. `get_detection_models_info` → inspect `labels` to choose a target label.
2. `set_detection_model '{"device_name":"cam1","model_name":"yolo11n"}'`.
3. `set_detection_rules '{"device_name":"cam1","rules":[{"name":"front-door-person","label_filter":["person"],"debounce_times":3}]}'`.
4. (Optional) `set_detection_schedule` for office hours.
5. `clear_detection_events` to start fresh.

### 3 — Monitor events (long-running)
```python
ckpt = int(time.time() * 1000)
while True:
    events = get_detection_events(device_name="cam1", start_unix_ms=ckpt)
    for e in events:
        ckpt = max(ckpt, e["timestamp_unix_ms"] + 1)
        if e.get("snapshot_path"):
            img = fetch_file(device_name="cam1", path=e["snapshot_path"])
            # img["content_base64"] or dispatch on img["url"] when oversized
    time.sleep(2)
```

### 4 — On-demand snapshot / video
- **JPG**: `capture_image '{"device_name":"cam1"}'` → returns base64 inline.
- **MP4**: `start_capture '{"device_name":"cam1","format":"MP4","video_length_seconds":10}'`, then poll `get_capture_status` until `last_capture.status` is terminal, then `fetch_file` with the absolute path assembled from the event's `output_directory` + `file_name`.

### 5 — Browse and retrieve recordings
- `list_records '{"device_name":"cam1"}'` → `{entries, offset, limit, total, has_more}`; iterate top-level date folders from `entries`.
- `list_records '{"device_name":"cam1","path":"2026-04-20","limit":200,"offset":0}'` — drill in, paginate if `has_more` is true.
- `fetch_record '{"device_name":"cam1","path":"2026-04-20/clip-001.mp4"}'` → returns `{url, note}` for video.

### 6 — Hybrid trigger (GPIO pulse → 5 s MP4)
```json
{"device_name":"cam1","trigger":{"kind":"gpio","num":1,"state":"PULL_UP","signal":"FALLING","debounce_ms":50}}
```
Pair with `set_record_config '{"device_name":"cam1","rule_enabled":true,"writer_format":"MP4","writer_interval_ms":0}'` and ensure a storage slot is selected (`set_storage_slot`).

### 7 — GPIO control
- Read: `get_gpio_value '{"device_name":"cam1","pin_id":2,"debounce_ms":50}'` → prints `0` or `1`.
- Write: `set_gpio_value '{"device_name":"cam1","pin_id":1,"value":1}'` → prints `1`.

## CLI quickstart

```bash
export PYTHONPATH="{baseDir}/scripts"
alias rci='python3 -m recamera_intellisense'

rci # list all commands
rci add_device '{"name":"cam1","host":"192.168.1.100","token":"sk_xxxx"}'
rci list_devices
rci get_detection_models_info '{"device_name":"cam1"}'
rci set_detection_model '{"device_name":"cam1","model_name":"yolo11n"}'
rci set_detection_rules '{"device_name":"cam1","rules":[{"name":"person","label_filter":["person"]}]}'
rci get_detection_events '{"device_name":"cam1","start_unix_ms":1745150000000}'
rci capture_image '{"device_name":"cam1"}'
rci list_records '{"device_name":"cam1"}'
rci fetch_record '{"device_name":"cam1","path":"2026-04-20/evt-001.jpg"}'
rci get_storage_status '{"device_name":"cam1"}'
rci set_gpio_value '{"device_name":"cam1","pin_id":1,"value":1}'
```

## Execution checklist (copy for multi-step tasks)

```text
reCamera Task Progress
- [ ] Resolve device (list_devices, then device_name)
- [ ] Validate JSON (required keys per command)
- [ ] Ensure prerequisites (storage slot, schedule, model) when configuring rules
- [ ] Run command; parse stdout or handle stderr
- [ ] For polling, checkpoint start_unix_ms and rate-limit
- [ ] On error, surface stderr + one concrete fix
```

## Troubleshooting

| Symptom | Likely cause / fix |
|---|---|
| `HTTP 401/403` | Token missing/invalid — re-copy from Web Console; confirm `sk_` prefix. |
| `Connection refused` / `timed out` | Wrong `host`/`port`/`protocol`; verify LAN reachability and device power. |
| HTTPS certificate error | Add `"allow_unsecured": true` for self-signed LAN certs (not for the public Internet). |
| `get_detection_rules` returns `[]` | Current trigger is not `inference_set` — call `set_detection_rules` (or inspect `get_record_trigger`). |
| Rules set but no events | No storage slot configured (`get_storage_status`); schedule window inactive; `region_filter`/`confidence_range_filter` too tight; `debounce_times` too high. |
| `fetch_record` returns only `{url, note}` | File is a video or exceeds `max_inline_bytes` (default 5 MiB). Fetch the URL directly or raise the budget. |
| `storage_task_submit` rejects `sync=true` | `FORMAT`/`FREE_UP` must run async — resubmit with `"sync": false` and poll `storage_task_status`. |
| `Schedule rejected` | Use `Day HH:MM:SS` with three-letter day; `Day 24:00:00` valid. |
| `set_detection_model` fails: "not installed" | Run `get_detection_models_info` and use one of the returned names/ids. |
| `detect_local_device` returns null | No `rcisd` daemon is listening on the Unix socket (default `/dev/shm/rcisd.sock`) within 3 s. Start the daemon or pass a different `socket_path`. |
| `start_capture` rejects `output` with code 30022 | `output` must be an on-device directory under a mounted storage slot (check `get_storage_status.mount_path`). Local paths like `/tmp/...` are **not** valid — omit `output` to use the default slot, then `fetch_file` the result. |
| `ImportError: recamera_intellisense` | Set `PYTHONPATH="{baseDir}/scripts"` or `cd {baseDir}/scripts` before `python3 -m recamera_intellisense`. |

## Reference pointers

- **Command schemas at runtime**: `python3 -m recamera_intellisense` (prints every command with required/optional keys).
- **Per-module sources**: `scripts/recamera_intellisense/{device,detection,model,rule,storage,records,capture,files,gpio,relay}.py` — short, stdlib-only, each file's `COMMAND_SCHEMAS` dict is authoritative.
- **Credential store**: `~/.recamera/devices.json` (schema matches the Rust `DeviceEntry` in the MCP server; the two surfaces interoperate).
