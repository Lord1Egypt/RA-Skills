# reCamera Intellisense API Reference

The bundled SDK is the reference implementation for the skill: stdlib-only, signature-driven (each function's signature is its schema), and self-describing via `--help`.

## Invocation

From the skill directory:

```bash
PYTHONPATH="./scripts" python3 -m recamera_intellisense <command> key=value ...
```

Argument forms (never mixed in one call):

| Form | Example |
|---|---|
| `key=value` | `recamera get_device device_name=cam1` |
| `--key value` / `--key=value` | `recamera get_device --device-name cam1` |
| single JSON object | `recamera get_device '{"device_name":"cam1"}'` |

Values are coerced using the command function's type annotations:

- **integers/floats** — `pin_id=106`, `quota_limit_bytes=-1`, `timeout=30`
- **booleans** — strict: `true/false`, `yes/no`, `on/off`, `1/0`; anything else is an error (no silent `bool("false") == true` surprises)
- **`null` / `none`** — selects `None` for optional parameters (e.g. `schedule=null` disables the schedule)
- **JSON arrays/objects** — required for structured parameters (`rules`, `schedule`, `trigger`, `files`), inline (`'rules=[{"name":"person"}]'`) or from a file (`trigger=@trigger.json`; `@-` reads stdin)
- **`@path`** — in the key=value form, any value may be loaded from a file (e.g. `token=@token.txt`); prefix `@@` for a literal leading `@`. The single-JSON-object form does not perform `@` expansion

A successful command prints JSON to stdout: a Python `None` result prints `null`, an empty dictionary prints `{}`. Every usage error prints the command's `usage:` line and a copy-pasteable `example:` to stderr and exits non-zero. `recamera <command> --help` prints the same information on demand.

Run the command without arguments to print the complete runtime catalogue:

```bash
PYTHONPATH="./scripts" python3 -m recamera_intellisense
```

`device_name` is optional on device commands: resolution falls back to `$RECAMERA_DEVICE`, then the sole registered device, then zero-config local detection driven by `$RECAMERA_TOKEN` (see SKILL.md). The tables below list `device_name` as required for readability — it may be omitted whenever the fallback chain resolves. Registry commands (`add/update/remove/get_device`) still require an explicit name. Device records are stored in `~/.recamera/devices.json` with mode `0600`.

## Device registry

| Command | Required keys | Optional keys |
|---|---|---|
| `detect_local_device` | `host` | `port`, `token`, `timeout` |
| `add_device` | `name`, `host`, `token` | `protocol`, `allow_unsecured`, `port` |
| `update_device` | `device_name` | `host`, `token`, `protocol`, `allow_unsecured`, `port` |
| `remove_device` | `device_name` | — |
| `get_device` | `device_name` | — |
| `list_devices` | — | — |

`protocol` is `http` or `https`. Use `allow_unsecured: true` only for trusted LAN devices with self-signed HTTPS certificates. `token` may be empty only when the device does not require authentication.

## Detection models and events

| Command | Required keys | Optional keys |
|---|---|---|
| `get_detection_models_info` | `device_name` | — |
| `get_detection_model` | `device_name` | — |
| `set_detection_model` | `device_name` | one of `model_id` or `model_name`; `fps` |
| `get_detection_schedule` | `device_name` | — |
| `set_detection_schedule` | `device_name` | `schedule` |
| `get_detection_rules` | `device_name` | — |
| `set_detection_rules` | `device_name`, `rules` | `ensure_writer`, `ensure_storage` |
| `get_detection_events` | `device_name` | `start_unix_ms`, `end_unix_ms` |
| `clear_detection_events` | `device_name` | — |
| `get_active_acoustic_model` | `device_name` | — |
| `list_acoustic_models` | `device_name` | — |
| `set_acoustic_model` | `device_name` | `workspace_id`, `head_id`, `default` |

`set_acoustic_model` switches the live inference head (ids from `list_acoustic_models`; unknown ids fail loudly listing the available ones) or restores the factory head with `default=true`. Requires the AcousticsLab app running (`start_app`).

Detection labels are names returned by the selected model, not numeric indexes. A schedule is a list such as:

```json
[{"start":"Mon 08:00:00","end":"Mon 18:00:00"}]
```

Pass `null`, `[]`, or omit `schedule` to disable the schedule and make it always active. A detection rule can contain `name`, `debounce_times`, `confidence_range_filter`, `label_filter`, and `region_filter`.

## Rule system

| Command | Required keys | Optional keys |
|---|---|---|
| `get_rule_system_info` | `device_name` | — |
| `get_record_sources` | `device_name` | — |
| `get_record_config` | `device_name` | — |
| `set_record_config` | `device_name`, `rule_enabled`, `writer_format` | `writer_interval_ms` |
| `get_schedule_rule` | `device_name` | — |
| `set_schedule_rule` | `device_name` | `schedule` |
| `get_record_trigger` | `device_name` | — |
| `set_record_trigger` | `device_name`, `trigger` | — |
| `activate_http_trigger` | `device_name` | — |

Supported trigger kinds are `inference_set`, `timer`, `gpio`, `tty`, `http`, and `always_on`. Only one record trigger is active at a time. The legacy `sed` (sound-event) kind is **retired**: firmware auto-migrates old `sed` configs into `inference_set` rules at boot; for sound-triggered recording use `inference_set` with `source_filter=["acousticslab"]`.

`get_record_sources` lists the recording-rule sources (`builtin` vision, `acousticslab` sound, installed apps) with their running state and currently producible `classes`. Compile rules against it: unknown source ids and unproducible labels are rejected loudly by `set_detection_rules`.

Examples:

```json
{"kind":"timer","interval_seconds":60}
```

```json
{"kind":"gpio","num":106,"state":"PULL_UP","signal":"FALLING","debounce_ms":50}
```

## App Center

| Command | Required keys | Optional keys |
|---|---|---|
| `list_apps` | `device_name` | — |
| `get_app_logs` | `device_name`, `app_id` | `tail` |
| `start_app` / `restart_app` | `device_name`, `app_id` | `confirm` |
| `stop_app` | `device_name`, `app_id` | `confirm` |

`list_apps` returns installed apps plus firmware system apps (`builtin`, `acousticslab`) with `status`, `version`, and `system` flag. A stopped app produces no frames for recording rules (see `get_record_sources`). `get_app_logs` tails the app's log (clamped to [1, 2000], spans rotation).

Lifecycle: `start_app`/`stop_app`/`restart_app` queue the action (HTTP 202 — poll `list_apps` for the new status). Stopping or restarting a SYSTEM app interrupts a firmware-managed result source (recording rules fed by it go silent), so those calls require `confirm=true`. Building new apps: use the [recamera-pysdk](https://github.com/Seeed-Studio/recamera-pro-ext-api/tree/main/skill/recamera-pysdk) skill.

## Video encode

| Command | Required keys | Optional keys |
|---|---|---|
| `get_video_encode` | `device_name` | `stream` |
| `set_video_encode` | `device_name` | `stream`, `codec`, `resolution`, `frame_rate`, `gop`, `rc_mode`, `rc_quality`, `max_rate`, `enabled` |

`stream` is `main` (default) or `sub`. Returns `{stream, stream_type, enabled, codec, resolution, frame_rate, gop, rc_mode, rc_quality, max_rate}` (max_rate in kbps).

`set_video_encode` changes only the passed fields (`codec`: H.264/H.265; `resolution`: WxH within 384*384~3840*2160; `frame_rate`/`gop`: 1~120; `rc_mode`: CBR/VBR; `rc_quality`: highest/high/medium/low; `max_rate`: 3~65536 kbps; `enabled`), then re-reads the device and fails loudly if a value did not apply. Applying briefly re-inits the encoder.

## Result push (notify)

| Command | Required keys | Optional keys |
|---|---|---|
| `get_notify_config` | `device_name` | — |
| `set_notify_config` | `device_name` | `mode`, `mqtt`, `http`, `templates` |

Returns `{mode, mode_name, mqtt, http, uart, templates}` — the shared pipeline that fans results (built-in vision AND AcousticsLab classifications) out to MQTT / HTTP / UART. `mode`: 0=off, 1=MQTT, 2=HTTP, 3=UART. **`password`/`token` are redacted as `"***"`** — the device returns them in cleartext and they must not enter agent contexts. `templates` are the shared per-task payload templates; empty = built-in default.

`set_notify_config` takes `mode` (0-3), `mqtt` `{url, port, client_id, username, password, topic}`, `http` `{url, token}`, `templates` `{classification, detection, keypoint, segmentation, tracking}`. **Only the passed fields change** — omitted fields keep their stored values, so secrets survive a redacted read followed by a write (passing the literal `"***"` placeholder is rejected; pass `""` to clear a secret). NOTE: applying restarts the notify service and recameraipc — a brief pipeline gap.

## Capture

| Command | Required keys | Optional keys |
|---|---|---|
| `get_capture_status` | `device_name` | — |
| `start_capture` | `device_name` | `output`, `format`, `video_length_seconds` |
| `stop_capture` | `device_name` | — |
| `capture_image` | `device_name` | `output`, `timeout` |

`format` is `JPG`, `RAW`, or `MP4`. `output` is an absolute **on-device** directory under a mounted storage slot, not a local directory. Omit it to use the selected slot. `capture_image` waits for completion and returns the event, remote path, size, and inline base64 content.

## Storage

| Command | Required keys | Optional keys |
|---|---|---|
| `get_storage_status` | `device_name` | — |
| `set_storage_slot` | `device_name` | `by_dev_path`, `by_uuid` |
| `configure_storage_quota` | `device_name`, `dev_path`, `quota_limit_bytes` | `quota_rotate` |
| `storage_task_submit` | `device_name`, `action`, `dev_path`, `confirm` | `sync`, `files` |
| `storage_task_status` | `device_name`, `action`, `dev_path` | `task_uid` |
| `storage_task_cancel` | `device_name`, `action`, `dev_path` | `task_uid` |

Actions are `FORMAT`, `FREE_UP`, `EJECT`, and `REMOVE_FILES_OR_DIRECTORIES`. `FORMAT` and `FREE_UP` must be submitted asynchronously (`sync: false`) and polled with `storage_task_status`. Storage operations can destroy recordings; use them only with explicit authorization.

## Records and files

| Command | Required keys | Optional keys |
|---|---|---|
| `list_records` | `device_name` | `path`, `dev_path`, `limit`, `offset` |
| `fetch_record` | `device_name`, `path` | `dev_path`, `max_inline_bytes` |
| `fetch_file` | `device_name`, `path` | `max_inline_bytes` |
| `delete_file` | `device_name`, `path`, `confirm` | — |
| `get_intellisense_events` | `device_name` | `start_unix_ms`, `end_unix_ms` |
| `clear_intellisense_events` | `device_name` | — |

`list_records` paths are relative to the selected record data directory. `fetch_file` paths are absolute on-device paths and reject traversal segments and NUL bytes. Images and payloads within the inline limit are returned as base64; larger payloads return metadata and a relay `url`. Relay URLs need no credentials but embed a random UUID (unguessable, capability-style) and die with the relay TTL (device default 300s); still avoid sharing them publicly.

## GPIO

| Command | Required keys | Optional keys |
|---|---|---|
| `list_gpios` | `device_name` | — |
| `get_gpio_info` | `device_name`, `pin_id` | — |
| `set_gpio_value` | `device_name`, `pin_id`, `value` | — |
| `get_gpio_value` | `device_name`, `pin_id` | `debounce_ms` |

`set_gpio_value` accepts only `0` or `1` and configures the pin as push-pull output. `get_gpio_value` configures the pin as floating input and can enable edge detection when debouncing; both operations therefore have hardware side effects and should not be treated as passive inspection.

## Key schemas

### Detection rule (for `set_detection_rules` / `inference_set` triggers)

```json
{
  "name": "front-door-person",
  "debounce_times": 3,
  "confidence_range_filter": [0.25, 1.0],
  "label_filter": ["person"],
  "source_filter": ["builtin"],
  "region_filter": [[[0.1,0.1],[0.9,0.1],[0.9,0.9],[0.1,0.9]]]
}
```

- `label_filter` holds **label names** from `get_detection_models_info`.labels (vision) or `get_record_sources` / `get_active_acoustic_model`.labels (sound) — never indexes. Empty matches any label.
- `source_filter` holds source ids from `get_record_sources` (`"builtin"`, `"acousticslab"`, app ids). **Empty matches EVERY source** — including acoustic classifications — so `set_detection_rules` defaults omitted filters to `["builtin"]`. Pass an explicit `[]` (or use `set_record_trigger`) only for a genuine all-sources rule.
- `region_filter` is a list of polygons of normalized `[x, y]` in `[0,1]`; omit/null = full frame. Only sources with `supports_roi` honor it.
- `confidence_range_filter` is `[min, max]`, both in `[0.0, 1.0]`, `min <= max` (default `[0.25, 1.0]`). `debounce_times` defaults to `3` consecutive matching frames (AcousticsLab hops are ~960 ms apart, so N hops ≈ N seconds).

### Schedule range

`{"start": "Mon 08:00:00", "end": "Mon 18:00:00"}` — three-letter day; `Day 24:00:00` is valid. Pass a list; `null` or `[]` disables (always active).

### Record trigger (tagged union on `kind`)

```json
{"kind":"inference_set", "rules":[ /* DetectionRule[] */ ]}
{"kind":"inference_set", "rules":[{"name":"alarm","source_filter":["acousticslab"],"label_filter":["Cat"],"debounce_times":3}]}
{"kind":"timer", "interval_seconds": 60}
{"kind":"gpio", "num":1, "state":"PULL_UP", "signal":"FALLING", "debounce_ms":50}
{"kind":"tty",  "name":"tty0", "command":"SHOOT"}
{"kind":"http"}
{"kind":"always_on"}
```

`gpio`: one of `name`/`num`; `state` ∈ `DISABLED|FLOATING|PULL_UP|PULL_DOWN`; `signal` ∈ `HIGH|LOW|RISING|FALLING`. Sound-event recording (formerly `sed`): the second `inference_set` example above; firmware migrates legacy `dSED` sections to this shape at boot (window → debounce hops, ~960 ms each).

### Detection event

```json
{"timestamp":"2026-04-20T12:34:56Z","timestamp_unix_ms":1745152496000,"rule_name":"front-door-person","snapshot_path":"/mnt/.../abcd.jpg"}
```

`snapshot_path` (when present) is an absolute on-device path — feed it to `fetch_file`, not `fetch_record`.

## System

| Command | Required keys | Optional keys |
|---|---|---|
| `get_device_info` | `device_name` | — |
| `get_resource_info` | `device_name` | — |
| `get_battery_status` | `device_name` | — |
| `get_system_time` | `device_name` | — |
| `export_device_config` | `device_name`, `output` | — |
| `reboot_device` | `device_name`, `confirm` | — |

`get_device_info` → `{serial_number, firmware_version, sensor_model, base_plate_model}`. `get_battery_status` → `{attached, charging, display_steps, total_steps}` (`attached=false` on battery-less base plates). `export_device_config` downloads the full device config tarball to the LOCAL `output` path (read-only for the device; refuses to overwrite an existing file) — snapshot before making changes. `get_resource_info` → `{cpu_usage, npu_usage, memory: {total_gb, used_gb, usage_percent}, storage: {...}}`. `reboot_device` is disruptive: all streams, captures, and sessions drop. Destructive commands (`storage_task_submit`, `delete_file`, `reboot_device`) require `confirm=true` and otherwise refuse without touching the device.

## Image (ISP)

| Command | Required keys | Optional keys |
|---|---|---|
| `get_image_settings` | `device_name` | — |
| `set_image_settings` | `device_name`, `section`, `values` | `scene_id` |

`get_image_settings` returns the full config: `video_adjustment`, `night_to_day` (including `profile_current` — the profile the camera is currently using), and `profiles` (3 entries), each with `adjustment`, `exposure`, `backlight`, `white_balance`, `enhancement`.

`set_image_settings` merges a partial `values` object into one section (read-modify-write), PUTs it, and returns `{section, changed, state}` (+ `scene_id` for profile sections) with the section re-read after the write. For profile sections `scene_id` (0/1/2) defaults to the active profile (`profile_current`) so writes take visible effect immediately; pass it explicitly to pre-configure an inactive profile. It is rejected for the two global sections. Writes to an inactive profile are stored but have no visible effect until that profile goes live. Sections and fields:

| Section | Fields (friendly → device) |
|---|---|
| `video_adjustment` | `rotation` (0/90/180/270), `flip` (close/mirror/flip/centrosymmetric), `power_line_frequency` (PAL(50HZ)/NTSC(60HZ)) |
| `night_to_day` | `mode` (0=auto/1=scheduled/2=fixed), `filter_level` (0–2), `filter_time` (1–60 s), `dawn_time`/`dusk_time` (0–86400 s, dusk > dawn), `profile_select` (0–2) |
| `adjustment` | `brightness`, `contrast`, `hue`, `saturation`, `sharpness` (0–100) |
| `exposure` | `exposure_mode`, `gain_mode` (auto/manual), `exposure_time` (fraction string like `1/60`), `exposure_gain` (1–128) |
| `backlight` | `blc_region`/`hdr`/`hlc` (open/close — **mutually exclusive**, max one open), `blc_strength`, `dark_boost_level` (0–100), `hdr_level` (=1), `hlc_level` (1–100) |
| `white_balance` | `style` (auto/manual/daylight/streetlamp/outdoor), `color_temperature` (2800–7500 K) |
| `enhancement` | `noise_reduce_mode` (0/1), `spatial_denoise_level`, `temporal_denoise_level` (0–100) |

Example: `recamera set_image_settings device_name=cam1 section=adjustment 'values={"saturation":80}'`

## Python API

The same functions are available in-process:

```python
import sys
sys.path.insert(0, "./scripts")
from recamera_intellisense import capture_image, get_storage_status

image = capture_image(device_name="cam1")
```

The public SDK exports the 64 CLI commands listed above (each function's signature is its schema — the CLI derives required/optional arguments and types from it). `relay.py` also has internal helpers used by record browsing; relay lifecycle is managed automatically by `list_records` and `fetch_record`.
