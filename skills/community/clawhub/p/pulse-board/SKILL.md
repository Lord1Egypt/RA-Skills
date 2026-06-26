---
name: pulse-board
description: "Universal operational digest for agent skill stacks. Every scheduled skill logs its outcome with log-append.sh. Twice daily, digest-agent.sh reads the log, composes a human-readable summary via your configured OpenClaw agent, delivers it to Telegram/Discord/log, and clears. Falls back to mechanical format if the agent call fails. install.sh handles everything interactively in one run. plug.sh wires any skill's cron job in one command."
---

# Pulse Board 📋

**Operational heartbeat for your agent stack. Every cron job, one digest.**

---

## How it works

```
skill cron runs
  → log-append.sh appends one line to pending.log
  → digest-agent.sh (twice daily)
      reads pending.log
      writes full raw log to last-digest.md
      calls openclaw agent to compose human-readable summary
        (falls back to mechanical format if agent call fails)
      delivers to Telegram / Discord / log
      clears pending.log
      prunes old detail logs
```

---

## What this skill touches

### Filesystem
| Path | Action |
|------|--------|
| `~/.pulse-board/` | Created by `install.sh` — config, logs, registry, locks |
| `~/.pulse-board/config/pulse.yaml` | Written once by `install.sh`, never overwritten on re-run |
| `~/.pulse-board/logs/pending.log` | Appended by skill cron wrappers, cleared after each digest |
| `~/.pulse-board/logs/last-digest.md` | Raw `pending.log` snapshot — written by `digest-agent.sh`, never overwritten |
| `~/.pulse-board/logs/last-delivered.md` | The composed/LLM message actually sent to the channel — written by `deliver.sh` |
| `~/.pulse-board/registry/<skill>.conf` | Written by `plug.sh`, removed by `unplug.sh` |

### Crontab
| Script | Action |
|--------|--------|
| `install.sh` | Adds two digest cron entries (`pulse-board-morning`, `pulse-board-evening`) |
| `plug.sh` | Adds one wrapped cron entry per skill (`# pulse-board:<skill>`) |
| `unplug.sh` | Removes the matching cron entry for a skill |

All crontab writes are done via `python3 subprocess`. Existing entries are never modified.

### Secrets env file
`install.sh` will ask for explicit confirmation before appending anything.
It may add `LLM_API_KEY=ollama` and `OPENCLAW_WORKSPACE=<path>` if missing.

### Network
- **Telegram:** `POST https://api.telegram.org/bot<token>/sendMessage`
- **Discord:** `POST <your webhook URL>`
- **OpenClaw agent:** `openclaw agent --agent <id> --message <prompt> --json` (local gateway call)
  ⚠️ The raw log is included in the prompt. If your agent uses a remote/cloud LLM, log content will be transmitted off-host. Use a local-only agent if log privacy is required.
- **Log only:** no network calls

### Credentials
- Bot token / webhook URL read from `pulse.yaml` or env vars
- Secrets env sourced at runtime by `digest-agent.sh`, `deliver.sh`, and cron wrappers
- Credentials never written to logs or included in digest output

---

## Install

```bash
chmod +x ~/.openclaw/skills/pulse-board/*.sh
bash ~/.openclaw/skills/pulse-board/install.sh
```

---

## Plug in a skill

```bash
bash ~/.openclaw/skills/pulse-board/plug.sh \
  --skill my-skill \
  --cron "*/15 * * * *" \
  --cmd "bash ~/.openclaw/skills/my-skill/run.sh"
```

Optional flags: `--label`, `--ok`, `--error`, `--log`

Or run `plug.sh` with no arguments for interactive discovery mode.

---

## Remove a skill

```bash
bash ~/.openclaw/skills/pulse-board/unplug.sh --skill my-skill
```

---

## Test

```bash
bash ~/.openclaw/skills/pulse-board/log-append.sh \
  --skill test --status OK --message "Hello Pulse Board"

bash ~/.openclaw/skills/pulse-board/digest-agent.sh
```

---

## Log files

| File | Contains |
|------|----------|
| `~/.pulse-board/logs/last-digest.md` | Full raw log from `pending.log` — preserved every run |
| `~/.pulse-board/logs/last-delivered.md` | The composed message that was sent to the channel |

The raw log is written first, before the agent call and before delivery.
`deliver.sh` writes only to `last-delivered.md` and never touches `last-digest.md`.

To review the raw log on demand, ask your agent:
*"show me last night's full digest log"* — it will read `last-digest.md`.

> ⚠️ **Privacy note:** when LLM composition is enabled, the raw log is passed
> to your OpenClaw agent as prompt context. If that agent uses a remote/cloud
> LLM, log content will leave this host. Use a local-only agent (Ollama) if
> log privacy is required.

---

## Files

| File | Purpose |
|------|---------|
| `install.sh` | One-time interactive setup |
| `plug.sh` | Register a skill + wire cron |
| `unplug.sh` | Remove a skill + cron entry |
| `log-append.sh` | Called by skill cron wrappers |
| `digest-agent.sh` | Runs on schedule, composes + delivers digest |
| `deliver.sh` | Internal delivery handler (Telegram/Discord/log) |

---

## Updating

```bash
cd ~/.openclaw/skills/pulse-board && git pull && chmod +x *.sh
```

---

## Requirements

- bash 4+, curl, python3 — standard on any modern Linux/macOS
- `openclaw` CLI in PATH (for LLM digest; falls back to mechanical if absent)
- No sudo. No root. No system path writes outside `~/.pulse-board/`
