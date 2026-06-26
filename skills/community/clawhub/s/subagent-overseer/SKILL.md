---
name: subagent-overseer
version: 1.1.0
description: "You spawned 4 sub-agents. One died 20 minutes ago. You're still waiting. Overseer watches them so you don't have to — zero tokens, pure OS-level process checks. No polling loops, no wasted heartbeats."
metadata:
  openclaw:
    emoji: "👁️"
    notes:
      security: "No network calls. Reads process status and filesystem diffs only. Pure bash daemon."
---

# Sub-Agent Overseer

Lightweight pull-based daemon that monitors sub-agent health. Writes a status file every N seconds. The heartbeat handler reads it — no push, no noise.

## Architecture

```
overseer.sh (bash, runs in background)
    ├── /proc/<pid>  → gateway alive? CPU? threads?
    ├── openclaw sessions list  → sub-agent count + ages
    ├── find -newer marker  → filesystem activity
    └── writes /tmp/overseer/status.json  (atomic mv)

heartbeat (agent, every 3min)
    └── reads /tmp/overseer/status.json → summarize or HEARTBEAT_OK
```

**Key principle:** The overseer does all data collection. The heartbeat handler does zero tool calls if the status file is fresh and healthy.

## Quick Start

### 1. Start the overseer when spawning sub-agents

```bash
setsid scripts/overseer.sh \
  --workdir /path/to/repo \
  --interval 180 \
  --max-stale 4 \
  --voice \
  &>/dev/null &
```

### 2. Heartbeat reads the status file

```bash
cat /tmp/overseer/status.json
```

### 3. Interpret the status

| Field | Meaning |
|---|---|
| `subagents.count` | Active sub-agent sessions |
| `subagents.details[].stale` | Consecutive cycles with no filesystem changes |
| `subagents.details[].status` | `active` / `idle` / `warning` / `stuck` |
| `gateway.health.alive` | Is `openclaw-gateway` running? |
| `filesystem.changes_since_last` | Files modified since last check |

### 4. Staleness thresholds (at 180s interval)

| stale count | Time | Status | Action |
|---|---|---|---|
| 0-1 | 0-3 min | `active`/`idle` | Normal |
| 2-3 | 6-9 min | `warning` | Voice alert (if --voice) |
| ≥4 | ≥12 min | `stuck` | Agent should investigate/kill |

## Heartbeat Handler Protocol

When HEARTBEAT.md fires:

1. **Read `/tmp/overseer/status.json`** — if missing or stale (>10 min), restart overseer
2. **If `subagents.count == 0` for 2+ cycles** → overseer auto-exits → reply `HEARTBEAT_OK`
3. **If all agents `active`** → brief one-line status → `HEARTBEAT_OK`
4. **If any `stuck`** → report which labels are stuck → consider killing via `subagents kill`
5. **Never cache a previous heartbeat response.** Always read the status file fresh.

## Flags

| Flag | Default | Description |
|---|---|---|
| `--interval` | 180 | Seconds between checks |
| `--workdir` | cwd | Directory to watch for file changes |
| `--labels` | (all) | Comma-separated labels to filter |
| `--max-stale` | 4 | Cycles before marking `stuck` |
| `--voice` | off | Local TTS alerts via `jarvis` command |

## How It Works (No AI Tokens)

1. **Gateway health:** Reads `/proc/<pid>/status` for CPU, memory, threads, FD count. Pure kernel data.
2. **Sub-agent list:** Single `openclaw sessions list` call per cycle. Parses grep output.
3. **Filesystem diff:** `find -newer marker` — detects any file writes in the workdir.
4. **Status file:** JSON written atomically (write to temp, `mv` into place). Any reader sees a complete file.
5. **Self-exit:** If no sub-agents for 2 consecutive cycles, the overseer stops itself.
6. **Dedup:** `flock` ensures only one overseer instance runs at a time.

## Cost

- Overseer: **$0.00** (bash + /proc + one CLI call per cycle)
- Voice alerts: **$0.00** (local sherpa-onnx via `jarvis`)
- Heartbeat reads status file: **$0.00** (one `cat` command)
- Only cost is the heartbeat model itself (qwen3 local = free)

## Pairs Well With

- [agent-superpowers](https://clawhub.com/globalcaos/agent-superpowers) — the three-agent review pipeline that Overseer was built to monitor
- [smart-model-router](https://clawhub.com/globalcaos/smart-model-router) — auto-select models for each sub-agent role

👉 **https://github.com/globalcaos/tinkerclaw**

_Clone it. Fork it. Break it. Make it yours._
