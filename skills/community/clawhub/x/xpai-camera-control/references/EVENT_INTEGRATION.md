# Event Store — External Consumer Contract

> **Audience:** Skill authors building upper-layer scenarios on top of this skill, external forwarders / agent-side module authors
> **Consumption method:** Pure disk reads (no MCP dependency, no IPC) — any language / framework can integrate
> **Skill package version:** 1.5.6 (schema 1.0)

This skill writes alarm events as structured records to a local text file for consumption by other skills or external modules. This is the **only public contract** for external collaboration — internal protocols, RTSP addresses, credentials, and connection state are never exposed.

---

## 1. Typical Upper-Layer Scenarios

| Scenario | Consumer | Description |
|----------|----------|-------------|
| Instant messaging forwarding | Forwarder skill / agent-side module | Push events + snapshots to WeChat, Slack, Telegram, DingTalk, etc. |
| Smart home automation | Home-automation skill | Trigger lights, buzzers, etc. on `region_intrusion` / `line_crossing` events |
| Multi-camera patrol | Patrol skill | Poll backlog per camera on a rotation, produce daily / weekly summaries |
| Desktop notifications | Agent-side module | System notifications triggered by the MCP process when no active session (skill-side roadmap) |

This skill is only responsible for **producing and persisting** events. The specific behavior of upper-layer scenarios is entirely up to the consumer.

## 2. Paths (relative to skill package root)

| Content | Relative path | Notes |
|---------|---------------|-------|
| Event store | `events/camera_events.txt` | One schema 1.0 JSON per line, UTF-8, append-only |
| Snapshots | `snapshots/` | The `snapshot_path` field in each event line provides the **absolute path** — read directly |
| Agent consumption cursor | `events/events_cursor.json` | Internal to this skill's MCP `poll`/`wait` consumption progress — **external consumers MUST NOT read or write** |
| Monitoring intent | `events/monitor_state.json` | Internal skill state (written on start / cleared on stop, used for auto-resume after process restart) — **external consumers MUST NOT read or write** |

Skill package root = the directory containing `SKILL.md`. If the skill is installed by an agent platform via "copy skill directory", the root is typically `~/.{platform}/skills/xpai-camera-control/` (exact path depends on the platform).

## 3. Write Semantics (conventions consumers must follow)

- **Encoding:** UTF-8, `ensure_ascii=False` (Chinese text is stored as-is and is directly readable)
- **Format:** One complete JSON object per line, terminated by `\n`; the skill appends via a single `write(line + \n)` call
- **Process only complete lines:** Consume only newline-terminated lines; skip empty lines; skip lines that fail JSON parsing
- **File may not exist:** When monitoring has never been started, the file does not exist — treat as "no events yet"
- **No rotation currently:** Do not assume the file will be truncated; however, tolerate future file cleanup by resetting offset to 0 or EOF when offset exceeds file size

## 4. Schema 1.0 Fields

```json
{
  "schema_version": "1.0",
  "event_id": "20260729_093000_frontdoor_motion",
  "event_type": "motion",
  "camera_id": "frontdoor",
  "camera_name": "Front Door",
  "timestamp": "2026-07-29T09:30:00+08:00",
  "severity": "warning",
  "title": "Motion detected at Front Door",
  "message": "Front Door camera detected motion at 09:30:00, snapshot captured.",
  "label": "person",
  "confidence": 0.92,
  "snapshot_path": "C:/.../snapshots/frontdoor_20260729_093000.jpg",
  "tags": ["guardian"]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `schema_version` | string | Fixed `"1.0"`; consumers should validate — on unknown version, fall back to forwarding only `title`/`message` |
| `event_id` | string | `{YYYYMMDD_HHMMSS}_{camera_id}_{event_type}` — **idempotent deduplication key** |
| `event_type` | string | `motion` / `human` / `vehicle` / `tamper` / `region_intrusion` / `line_crossing` / `high_temp` / `low_temp` (may be extended; treat unknown values as `info`) |
| `camera_id` | string | Camera registration name (key in `config.yaml`) |
| `camera_name` | string | Optional. Display name; defaults to `camera_id` when no separate display name is set |
| `timestamp` | string | ISO 8601 with local timezone, second precision |
| `severity` | string | Optional. `info` / `warning` (motion/human/vehicle) / `critical` (tamper/intrusion/line crossing/temperature) |
| `title` | string | Ready-to-use notification title |
| `message` | string | Ready-to-use notification body (includes time and snapshot status) |
| `label` | string \| null | Target class (person/car/truck…); `null` when extraction is unavailable |
| `confidence` | number \| null | Confidence score 0–1; `null` when the protocol does not provide it |
| `snapshot_path` | string | Absolute snapshot path; **may be empty string** (snapshots are sampled at a fixed 30 s interval — empty means no sample was due; a missing file means the asynchronous capture failed) — send text-only in either case |
| `tags` | string[] | Optional. Currently always `["guardian"]` |

## 5. Consumer Integration Guidelines

1. **Read-only tail consumption:** Poll (recommended 2–5 s) or watch the file for new content; maintain **your own** byte offset / line number (persist in the consumer's own directory — never touch any file under `events/`)
2. **Idempotency:** Deduplicate by `event_id` to avoid duplicate processing after offset resets or restarts
3. **Notification copy:** Forwarding consumers can use `title` + `message` directly, attaching the image from `snapshot_path` (empty = text-only) — this skill only raises alarms, it does not perform image analysis; deep analysis is the responsibility of upper-layer scenarios
4. **Noise reduction (optional):** Filter by `severity` (e.g. only `warning`/`critical`); apply consumer-side cooldown windows per `camera_id`+`event_type` (this skill already deduplicates at 5 s; consumers may add minute-level cooldown)
5. **Directory access permissions:** `events/` and `snapshots/` are strictly **read-only**; the cursor file `events/events_cursor.json` tracks this skill's MCP-side consumption progress — external consumers sharing this cursor would "eat" events intended for the skill's own `poll`/`wait`

## 6. Security Constraints (mandatory)

- **Off by default:** Any upper-layer scenario that sends events / snapshots outside the local network MUST require **explicit user authorization** and inform the user how to disable it; this skill only persists to local disk by default
- **Local copy is authoritative:** External consumption is an optional additional channel on top of local storage; any consumption failure must not affect the local event pipeline
- **Read-only, no analysis:** Forwarded content is limited to the schema 1.0 text and snapshots — credentials, RTSP addresses, connection state, and all other configuration are never exposed

## 7. Version Evolution

- Current contract version: `schema_version = "1.0"`
- Field extension policy: New fields use `Optional` semantics (consumers should tolerate missing new fields in older data); existing fields are never removed; if field semantics change, increment the `schema_version` major version and update this document accordingly
