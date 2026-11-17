---
name: tt_live
description: TikTok LIVE monitor. Check whether a TikTok user is live right now, resolve their current m3u8 stream URL, or spawn a background daemon that polls them over a timer window and emits go_live / go_offline / rename_detected events for the sub-agent to announce.
version: 0.1.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
    os:
      - linux
      - darwin
    emoji: "🎥"
---

# tt-live — TikTok LIVE Monitor

Inspect a TikTok user's live status, resolve their stream URL, or watch
them over time. Operate on `uniqueId` (the `@handle`) at the input
boundary; track `secUid` as the stable primary key inside the workspace.

This skill is a pure data provider. It does not push notifications. All
chat announcements are the sub-agent's job through the normal OpenClaw
announce mechanism in the requester's channel.

---

## When to invoke

Invoke this skill when the requester asks any of:

- "Is @&lt;user&gt; live right now?" — one-shot status check
- "Give me the stream URL for @&lt;user&gt;" — m3u8 URL resolution
- "Watch @&lt;user&gt; and tell me when they go live or offline over the
  next N hours" — daemon-mode watch
- "Did @&lt;user&gt; rename recently?" — identity history lookup via the
  workspace identity store or daemon events

Do NOT invoke this skill for:

- Anything outside TikTok LIVE (regular TikTok videos, comments, DMs,
  user analytics)
- Downloading or recording the stream — this skill only resolves the URL
- Pushing notifications to external services (Slack, Discord,
  webhooks). The sub-agent owns announcements; the skill does not.

---

## Workspace

All state lives under `$TT_LIVE_WORKSPACE`, default
`~/.openclaw/workspace/tiktok-monitor/`. Created automatically on first
invocation.

```
workspace/
├── tiktok-names/
│   ├── identities/<sec_uid>.json     canonical identity records
│   └── pointers/<unique_id>.json     @handle → sec_uid pointers
├── state/tt-live/
│   ├── <sec_uid>.state.json          per-user live state + URL cache
│   └── <sec_uid>.events              append-only daemon event log
└── logs/
    └── daemon-<user>-<UTC-ts>.log    daemon stderr+stdout
```

---

## Entry points

All entry points are invoked through `tt-live.sh` (the bash wrapper)
which dispatches to `tt_live.py`. The wrapper handles backgrounding for
the daemon case.

### `tt-live.sh check <username>`

One-shot status check. Updates identity + state stores. Prints a JSON
record with `sec_uid`, `unique_id`, `nickname`, `user_id`, `live`,
`room_id`, `title`, `start_time`, `rename_detected`, `checked_at`.

Exit codes: `0` = live, `1` = offline, `2` = error.

### `tt-live.sh url <username> [--verbose|-v]`

Resolve the current m3u8 stream URL. Cache-first (3-day retention);
falls back to direct webcast API → yt-dlp → streamlink. Prints the URL
on stdout.

Exit codes: `0` = ok, `1` = offline, `2` = all extraction strategies
failed.

With `-v`, prints `# source: cache|api|yt-dlp|streamlink` to stderr.

### `tt-live.sh daemon <username> [--hours N] [--poll-min M]`

Spawn a background daemon. Defaults: `--hours 12`, `--poll-min 5`. The
`--poll-min` value has a hard floor of 5; lower values are silently
clamped.

The wrapper prints `pid=...`, `username=...`, `workspace=...`,
`log=...`, `events_dir=...` and returns immediately. The daemon writes
structured events to `<events_dir>/<sec_uid>.events`.

Exit codes: `0` = spawned and alive after 1s, `2` = spawn failed
(check the printed log path).

---

## Standalone tools (workspace-free)

These two scripts are independent of `tt_live.py`. They do not read or
write the workspace. Use them for ad-hoc probes.

### `get_room_id.py <username>`

SIGI_STATE scrape from `/@<user>/live`. Prints identity + room fields
as JSON. Exit `0`/`1`/`2` (live/offline/error).

### `check_alive.py <room_id>`

Webcast API liveness check on an already-known room_id. Prints
`{room_id, alive, checked_at}`. Exit `0`/`1`/`2` (alive/not/error).

These are read-only counterparts to `tt_live.py check` for cases where
workspace side-effects are not wanted.

---

## Canonical workflow for long-running watch

When the requester asks "watch @&lt;user&gt; for N hours and tell me when
they go live / offline":

**Step 1.** Resolve identity. The JSON output contains `sec_uid`, which
is needed for the events file path.

```bash
JSON="$(tt-live.sh check <user>)"
SEC_UID="$(echo "$JSON" | python3 -c 'import json,sys; print(json.load(sys.stdin)["sec_uid"])')"
```

**Step 2.** Spawn the daemon. Capture the workspace + events_dir from
the printed key=value lines.

```bash
DAEMON_OUT="$(tt-live.sh daemon <user> --hours N --poll-min 5)"
EVENTS_DIR="$(echo "$DAEMON_OUT" | awk -F= '/^events_dir=/{print $2}')"
EVENTS_FILE="$EVENTS_DIR/$SEC_UID.events"
```

**Step 3.** Tail the events file. For each new line, parse `evt=` and
announce to the requester's chat channel:

| Event | Sub-agent action |
|---|---|
| `daemon_start` | Acknowledge the watch has begun (optional) |
| `go_live` | Announce live + share the `stream_url` value |
| `go_offline` | Announce the stream ended |
| `rename_detected` | Announce the @handle change (`old_unique_id` → `unique_id`) |
| `poll_err` | Log internally; do not announce unless multiple in a row |
| `poll_ok` | Do not announce — these are normal heartbeats |
| `daemon_end` | Announce watch window ended (include `reason` + `transitions`) |

**Step 4.** When `daemon_end` arrives, the watch is complete. Stop
tailing.

The skill itself never announces. The sub-agent is responsible for
turning events into human-readable chat messages.

---

## Event format

One line per event. Field order is fixed:

```
ts=<iso> evt=<type> sec_uid=<...> unique_id=<...> [k=v ...] [stream_url=...]
```

Rules:

- `ts=` is always first
- `evt=` is always second
- `sec_uid=`, `unique_id=` follow if present
- `stream_url=` is **always the last key** when present, because its
  value contains `&` and `=` which would break key=value parsers
- All seven event types: `daemon_start`, `daemon_end`, `poll_ok`,
  `poll_err`, `go_live`, `go_offline`, `rename_detected`

See `tt_live.md` §10 for the per-event field reference.

---

## Hard constraints

These are baked into the code and not configurable at runtime:

- **360p stream cap.** URL extraction is fixed at 360p height. Sub-agent
  use cases assume predictable bandwidth.
- **5-minute poll floor.** `--poll-min` values below 5 are clamped.
  TikTok rate-limits aggressive polling and there is no benefit to
  finer resolution for go_live / go_offline transitions.
- **No outbound notifications.** No webhooks, no Slack-from-Python, no
  Discord posts. The sub-agent's announce mechanism is the only output
  channel.
- **Stream URL validity is tied to the live session.** When the user
  goes offline and live again, the previous URL is gone — even if it's
  within the 3-day retention window. The cached URL is still useful as
  a forensic record but not as a playable stream.
- **`sec_uid` is the primary key.** Track users by `sec_uid`, not by
  `unique_id`. Users can rename their @handle; `sec_uid` does not change.

---

## Out of scope

- Recording / saving the stream content
- Multi-user batch monitoring (one user per daemon)
- Notifications to external services
- TikTok video downloads, comments, follower lists, anything not LIVE
- Stop / pause / resume controls — to stop a daemon, the sub-agent kills
  the printed `pid=` and the daemon writes a `daemon_end
  reason=interrupted` event on the way out
