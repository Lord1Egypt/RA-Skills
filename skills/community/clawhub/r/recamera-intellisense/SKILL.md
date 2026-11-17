---
name: recamera-intellisense
description: Register and control reCamera Pro devices from an agent — onboard cameras, pick AI detection models by name, configure rule-based triggers (AI / timer / GPIO / TTY / HTTP / always-on / sound-event), poll detection events with snapshots, capture JPG/RAW/MP4 on demand, browse recorded clips, manage storage, and drive GPIO pins. Uses a bundled stdlib-only Python SDK invoked with flat key=value arguments (a single JSON object also works). Trigger this skill whenever the user mentions reCamera or a registered reCamera device — including requests in that context about camera onboarding, object/person or sound-event detection, event polling, snapshot or video capture, recording rules, on-device GPIO, or wiring a physical camera into an agent workflow.
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
allowed-tools: "Bash"
---

# reCamera Intellisense

Drive one or more [reCamera Pro](https://wiki.seeedstudio.com/recamera_pro_getting_started/) devices: registration, AI + sound-event detection, rule-based recording, event polling, on-demand capture, storage/records, and GPIO. The bundled Python SDK (`scripts/recamera_intellisense/`, stdlib-only) is the reference implementation; the MCP server is a schema-compatible Rust surface sharing the same credential store.

## Requirements

- `python3` ≥ 3.9 (stdlib only); reachable device HTTP/HTTPS API (TCP `80`/`443`)
- Per-device token (Web Console → Device Info → Connection Settings); may be empty for local devices. Store: `~/.recamera/devices.json` (auto-created, chmod `600`).

## Security

- **Capabilities**: network access to configured device IPs, credential persistence in `~/.recamera/devices.json`, filesystem writes (captures/downloads), GPIO control, and device administration (reboot, storage format, ISP changes). Host-level tool use is `Bash` only (invoking the bundled CLI).
- **Tokens are bearer credentials** — never commit or log them. Device-facing outputs (`list_devices` etc.) never include them.
- **Confirmation gates**: `storage_task_submit` (FORMAT/FREE_UP/EJECT/REMOVE), `delete_file`, and `reboot_device` refuse unless `confirm=true` — always ask the user first. `ensure_storage` prints a stderr note whenever it changes slot/rotation state.
- **Event clearing is deliberately ungated**: `clear_intellisense_events`/`clear_detection_events` purge only the daemon's transient event buffer, which refills itself continuously; the protected evidence (recordings, snapshots on disk) sits behind `delete_file` and storage-format gates. Confirm gates are reserved for irreversible operations with material harm, so agents do not learn to reflexively pass `confirm=true`.
- **Relay URLs**: `fetch_record` returns relay links for large recordings. They need no credentials, but the path embeds a random UUID (unguessable, capability-style) and the relay auto-expires (device default TTL 300s); still avoid sharing them publicly.
- **Same-origin redirects only** (SSRF-safe); **TLS verified by default** — local HTTPS devices use self-signed certs, so register `protocol=https allow_unsecured=true` (trusted LAN only, never the public Internet); a one-time stderr warning is printed whenever an unverified connection is used.
- `fetch_file`/`delete_file` reject relative paths, `..`, and NUL bytes; the daemon enforces an allowlist.
- This skill writes files, drives GPIO, and can format storage — point it only at hardware you own.

## Invocation

```bash
export PYTHONPATH="{baseDir}/scripts"
alias rci='python3 -m recamera_intellisense'

# (or use the standalone launcher from scripts/setup-skill.py — it writes
#  ~/.recamera/bin/rci and adds it to PATH by default. If `rci` is not found —
#  shell not restarted yet, or PATH setup skipped with --no-path — fall back to
#  the direct form above; the skill's bundled scripts always work)

rci <command> key=value ...            # flat (preferred)
rci <command> --key value              # flags; dashes normalize to underscores
rci <command> '{"key":"value"}'        # single JSON object (never mix forms)
rci <command> --help                   # usage + a working example, per command
```

- **Types** coerce from the function signature: ints (`quota_limit_bytes=-1`), floats, strict booleans (`true/false/yes/no/on/off/1/0`), `null`/`none` for optionals, JSON arrays/objects for structured params (`rules`, `schedule`, `trigger`, `files`) — inline or `@file.json` (`@-` = stdin; `@@` = literal `@`).
- **Success**: pretty JSON on stdout (`None` → `null`), exit 0. **Failure**: message **plus usage + example** on stderr, non-zero exit — surface it and propose one fix.
- **Discovery**: `rci` lists all 50 commands with required/optional keys; `rci list-commands` prints names only.

Python in-process (preferred for loops and low-latency voice agents — avoids process spawn + TLS setup per call): `sys.path.insert(0, "{baseDir}/scripts")`, then `from recamera_intellisense import …` — the package exports every CLI command.

## Device resolution

`device_name` is **optional** on every device command. Resolution order: explicit `device_name` → `$RECAMERA_DEVICE` → the sole registered device → zero-config local detect. The last path needs no registration at all: with `$RECAMERA_TOKEN` set (plus optional `$RECAMERA_HOST`, default `127.0.0.1`, and `$RECAMERA_PORT`) the first command probes the local API and persists it as the `local` device, so later calls skip detection — the way an agent running on the camera itself should operate.

## Command map

Full catalogue, per-command arguments, and key schemas: **[REFERENCE.md](REFERENCE.md)** — or `rci <command> --help` at runtime.

- **Device**: `detect_local_device host=…`, `add_device`, `update_device`, `get_device`, `remove_device`, `list_devices` (registration probes the device before persisting).
- **System**: `get_device_info` (firmware/sensor/serial), `get_resource_info` (CPU/NPU/mem/storage %), `get_battery_status`, `get_system_time`, `export_device_config output=./backup.tar` (snapshot config before changes), `reboot_device` (**disruptive** — drops all streams/sessions).
- **Image (ISP)**: `get_image_settings` (full config: video adjustment, night-to-day, 3 scene profiles), `set_image_settings section=… 'values={…}' [scene_id=…]` — sections: `video_adjustment`, `night_to_day`, `adjustment`, `exposure`, `backlight`, `white_balance`, `enhancement`; read-modify-write with validation (incl. BLC/HDR/HLC mutual exclusion). `scene_id` defaults to the active profile (`night_to_day.profile_current`) so writes apply visibly; the response re-reads the section as proof.
- **Detection**: `get_detection_models_info`, `get/set_detection_model` (by `model_id` or `model_name`), `get/set_detection_schedule`, `get/set_detection_rules`, `get_detection_events` (`start_unix_ms`/`end_unix_ms`), `clear_detection_events`. Facade: `set_detection_rules` installs the `inference_set` trigger and ensures writer + storage by default; `get_detection_rules` returns `[]` when the active trigger is not `inference_set`.
- **Acoustic**: `get_active_acoustic_model` → labels of the active sound model (null when the AcousticsLab app is stopped — start it in the App Center); `list_acoustic_models` → all trained heads across workspaces (active marked).
- **App Center**: `list_apps` (status/version/system flag; a stopped app produces no recording frames), `get_app_logs app_id=… tail=…`. Lifecycle: `start_app`/`stop_app`/`restart_app` (202 queued; system-app stop/restart needs `confirm=true`).
- **Writes that matter**: `set_notify_config` keeps stored secrets for omitted fields (never echo the `***` placeholder back) and restarts the result pipeline on apply; `set_acoustic_model` switches the live acoustic head; `set_video_encode` re-reads the device to verify the applied values.
- **Video**: `get_video_encode stream=main|sub` → codec/resolution/fps/GOP/RC/bitrate.
- **Result push**: `get_notify_config` → MQTT/HTTP/UART channels + shared payload templates (secrets redacted).
- **Rule system**: `get_rule_system_info`, `get_record_sources` (discover source ids + producible classes BEFORE compiling rules), `get/set_record_config`, `get/set_schedule_rule`, `get/set_record_trigger`, `activate_http_trigger`. Trigger kinds: `inference_set`, `timer`, `gpio`, `tty`, `http`, `always_on` — only one is active at a time. The legacy `sed` kind is **retired**: sound-event recording is an `inference_set` rule with `source_filter=["acousticslab"]`; firmware auto-migrates old `sed` configs at boot.
- **Capture**: `get_capture_status`, `start_capture` (`format=JPG|RAW|MP4`, `output` is an **on-device** directory — omit for the selected slot), `stop_capture`, `capture_image` (one-shot JPG → `{event, path, size, content_base64}`).
- **Storage**: `get_storage_status`, `set_storage_slot`, `configure_storage_quota`, `storage_task_submit/status/cancel` (actions `FORMAT`/`FREE_UP`/`EJECT`/`REMOVE_FILES_OR_DIRECTORIES`; `FORMAT`/`FREE_UP` must be async).
- **Records**: `list_records` (paginated `{entries, offset, limit, total, has_more}`), `fetch_record` (images/≤5 MiB inline base64; larger → `{url, note}`). Paths are relative to the record data dir.
- **Files**: `fetch_file` (absolute on-device paths, e.g. event `snapshot_path`), `delete_file`, `get_intellisense_events`, `clear_intellisense_events`.
- **GPIO**: `list_gpios`, `get_gpio_info pin_id=…`, `set_gpio_value` (→ push-pull output), `get_gpio_value` (→ floating input). Both value calls reconfigure pin direction — not read-only probes.

## Agent rules

1. Supply complete arguments in one call; never prompt interactively.
2. Identify targets by `device_name`; `list_devices` is cheap.
3. `label_filter` takes **label names** — vision from `get_detection_models_info`, sound from `get_record_sources` (or `get_active_acoustic_model`) — never numeric indexes.
4. Compile against reality: call `get_record_sources` first and only reference source ids + labels it reports; an unknown source or unproducible label is a loud error, not a silent never-firing rule. `set_detection_rules` scopes rules without `source_filter` to the `builtin` vision source (an empty filter matches EVERY source, including audio).
5. AI recording (vision or sound) → `set_detection_rules`; hybrid triggers (GPIO/timer/TTY/HTTP/always-on) → `set_record_trigger` directly.
5. Poll `get_detection_events` with a checkpointed `start_unix_ms` (1–10 s cadence); `clear_detection_events` to reset.
6. Prefer event metadata first; fetch imagery only when needed (inline ≤5 MiB, else URL + note).
7. Schedules: `[{"start":"Mon 08:00:00","end":"Mon 18:00:00"}]`; `schedule=null` disables (always active). Detection-rule and trigger schemas: see REFERENCE.md.
8. Storage slot required for rules/timer/always-on — the facade auto-selects internal storage; removable media must be provisioned first.

## Workflows

```bash
# 1 — Onboard
rci detect_local_device host=192.168.1.100
rci add_device name=cam1 host=192.168.1.100 token=sk_xxxx protocol=https allow_unsecured=true
rci list_devices

# 2 — Person detection by name
rci get_detection_models_info device_name=cam1            # pick a label
rci set_detection_model device_name=cam1 model_name=yolo11n
rci set_detection_rules device_name=cam1 'rules=[{"name":"person","label_filter":["person"]}]'
rci clear_detection_events device_name=cam1

# 3 — Snapshot / video
rci capture_image device_name=cam1                        # JPG inline base64
rci start_capture device_name=cam1 format=MP4 video_length_seconds=10
# poll get_capture_status until last_capture.status is terminal, then fetch_file
# with the event's output_directory + file_name

# 4 — Browse recordings
rci list_records device_name=cam1 path=2026-04-20 limit=200
rci fetch_record device_name=cam1 path=2026-04-20/clip-001.mp4

# 5 — Hybrid trigger (GPIO pulse → MP4)
rci set_record_config device_name=cam1 rule_enabled=true writer_format=MP4
rci set_record_trigger device_name=cam1 'trigger={"kind":"gpio","num":1,"state":"PULL_UP","signal":"FALLING","debounce_ms":50}'

# 6 — GPIO (pin direction side effects — see Command map)
rci get_gpio_value device_name=cam1 pin_id=2 debounce_ms=50
rci set_gpio_value device_name=cam1 pin_id=1 value=1

# 7 — Sound-event trigger
rci get_record_sources device_name=cam1                     # acousticslab running? pick a class
rci set_record_config device_name=cam1 rule_enabled=true writer_format=MP4
rci set_detection_rules device_name=cam1 'rules=[{"name":"alarm","source_filter":["acousticslab"],"label_filter":["Cat"],"debounce_times":3}]'
```

Event-polling loop (Python): checkpoint `ckpt = int(time.time()*1000)`, call `get_detection_events(device_name=…, start_unix_ms=ckpt)`, advance `ckpt` past each `timestamp_unix_ms`, `fetch_file` any `snapshot_path`, sleep 2 s.

## Scope and hand-off

This skill **orchestrates existing device capabilities** (compile intents into persistent record rules, capture, storage, GPIO) — it never adds new on-device behavior. When a request needs a new capability:

- **Custom app / model pipeline / result post-processing** → use the [recamera-pysdk](https://github.com/Seeed-Studio/recamera-pro-ext-api/tree/main/skill/recamera-pysdk) skill to assess, build, package, and debug a reCamera Pro App for the App Center.
- **Custom sound classes** → train/activate a head in the AcousticsLab console (`/extension/acousticslab`); this skill consumes its labels read-only.
- **Building NEW apps / model pipelines / result post-processing** → `recamera-pysdk`; heavy flows (app upload/install, model files, factory reset) stay in the device web UI.

If neither covers the request, say so plainly instead of inventing capabilities.

## Troubleshooting

| Symptom | Likely cause / fix |
|---|---|
| `HTTP 401/403` | Token missing/invalid — re-copy from Web Console. |
| `Connection refused` / `timed out` | Wrong host/port/protocol; check power and LAN. |
| HTTPS certificate error | Use `allow_unsecured=true` (self-signed LAN certs only). |
| `get_detection_rules` returns `[]` | Active trigger is not `inference_set` — see `get_record_trigger`. |
| Rules set but no events | No storage slot; inactive schedule window; filters too tight; debounce too high. |
| `{url, note}` instead of content | Video or >5 MiB — fetch the URL or raise `max_inline_bytes`. |
| `sync=true` rejected | `FORMAT`/`FREE_UP` are async-only; poll `storage_task_status`. |
| Model "not installed" | Pick `model_name`/`model_id` from `get_detection_models_info`. |
| Acoustic model is `null` / sound rule never fires | The AcousticsLab app is stopped or has no active head — start it in the App Center / AcousticsLab console; verify labels via `get_record_sources`; legacy `sed` triggers are retired (migrated at boot). |
| `start_capture` code 30022 | `output` must be under a mounted slot (`get_storage_status.mount_path`) — or omit it. |
| `ImportError: recamera_intellisense` | `PYTHONPATH` must point at `{baseDir}/scripts`; run `python3 -m recamera_intellisense`. |
| `code=500 … Backend connection failed` | Device-side daemon down — reboot the camera / check its logs, then retry. |

## Reference pointers

- **Full catalogue + key schemas**: [REFERENCE.md](REFERENCE.md) · **Runtime truth**: `rci <command> --help`
- **Sources**: `scripts/recamera_intellisense/*.py` — each command's signature is its schema.
- **Credential store**: `~/.recamera/devices.json` (shared with the MCP server).
