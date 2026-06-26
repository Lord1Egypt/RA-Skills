---
name: sessions-dashboard
description: Live dashboard viewer for OpenClaw sessions (CLI + web) that shows color-coded states, token/cost totals, and shareable HTML panels. Requires local OpenClaw CLI access (`openclaw sessions` and optional `openclaw logs`). Created by Nate Teshome (stellarsitesai.com).
---

# Sessions Dashboard ("Live Dashboard Viewer")

Creator: **Nate Teshome** — <https://stellarsitesai.com>

## What this skill delivers
- **Color-coded CLI monitor** (`scripts/agents_cli_monitor.py`): RUN/IDLE/STALE/EXIT states, runtime, last update, token + USD estimates, model/kind, plus a live KPI banner (state counts, Σ tokens/cost, longest run, avg lag).
- **Shareable HTML dashboard** (`scripts/agents_canvas_snapshot.py`): dark-mode cards + table, status pills, runtime/lag columns, and auto-refresh browser view for leadership/client reviews.
- **Looping web generator** (`--loop <seconds>`): continuously rewrites the HTML so you don’t need separate `watch` commands. Pair with the built-in `<meta refresh>` (default 5 s) for a true live panel.

Use this when you need a polished, always-on view of every OpenClaw session—perfect for ops rooms, agency war rooms, or lightweight audits.

## Requirements & security
- **OpenClaw CLI** (`openclaw` >= 2025.x) must be installed and authenticated so `openclaw sessions --json` works.
- **Optional log tail**: the CLI monitor subscribes to `openclaw logs --json --follow` for instant RUN/IDLE bumps. Those logs can contain prompts, tool arguments, secrets, or PII. Nothing is printed or stored, but if you don’t want to expose log contents, pass `--no-subscribe` (poll-only) or run on a machine without log access.
  - Set `AGENT_MONITOR_NO_SUBSCRIBE=1` to default to poll-only everywhere; pass `--subscribe` to override per run.
- **Gateway scope**: run the dashboard only on hosts that are already allowed to query your OpenClaw gateway; everything stays local/in-memory.

## Directory
```
skills/sessions-dashboard/
├── SKILL.md
├── scripts/
│   ├── agents_cli_monitor.py        # Live terminal UI (color + KPI banner)
│   └── agents_canvas_snapshot.py    # HTML generator (+ --loop for continuous refresh)
└── assets/
    └── agents_canvas.html           # Default output target for the web panel
```

## CLI monitor quick start
```bash
cd ~/.openclaw/workspace/skills/sessions-dashboard
./scripts/agents_cli_monitor.py --interval 2 --cost-per-1k 0.015
```
Key flags:
- `--interval SECONDS` (default 3, min 0.5)
- `--active-minutes MINS` (default 720) to widen the lookback
- `--agent <id>` / `--all-agents` to filter
- `--retention SECONDS` (default 120) to control how long EXITED rows linger
- `--cost-per-1k USD` or env `AGENT_MONITOR_COST_PER_1K`
- `--once` for a single snapshot, `--no-subscribe` to disable the log tailer

### What the CLI shows
- **State** (RUN green, IDLE amber, STALE magenta, EXIT gray)
- **Runtime + start time** for quick “how long has this been around?” checks
- **Last update lag** (`00:12 ago`) to spot stuck sessions
- **Tokens & projected cost** per session
- **Model / kind** (channel) for context
- **KPI banner** (top line) summarizing RUN/IDLE/STALE/EXIT counts, Σ tokens/cost, the longest-running session, and mean lag — ideal for screenshots or lightweight reporting.

## Web dashboard (Canvas / browser)
Generate the HTML and keep it running in one command:
```bash
cd ~/.openclaw/workspace/skills/sessions-dashboard
./scripts/agents_canvas_snapshot.py \
  --loop 5 \
  --refresh 5 \
  --cost-per-1k 0.015 \
  --output assets/agents_canvas.html
```
What the script does:
- Hits `openclaw sessions --json` on each loop.
- Rebuilds `assets/agents_canvas.html` with cards (state counts, Σ tokens/cost, longest run, avg lag) plus the detailed table.
- Inserts a `<meta refresh>` so the browser (or Canvas tab) reloads itself every `--refresh` seconds.
- When `--loop` > 0, the script stays alive forever and rewrites the file at that cadence (Ctrl+C to stop). No extra `watch` command needed.

### Presenting the dashboard
- **Open locally:** `open assets/agents_canvas.html`
- **Canvas:** `openclaw canvas present --path skills/sessions-dashboard/assets/agents_canvas.html`
- **Remote share:** host the HTML anywhere static files are allowed; it has no external dependencies.

## Troubleshooting
- **`command not found`:** `chmod +x scripts/*.py` and run from the skill directory (or use absolute paths).
- **Gateway errors:** verify `openclaw gateway status`; the scripts just print the stderr and retry.
- **No color in CLI:** set `NO_COLOR=1` to disable, otherwise the monitor auto-detects TTY support.
- **Browser not updating:** make sure `--loop` is running so the HTML file actually changes; `--refresh` only reloads the page.
- **Cost column blank:** pass `--cost-per-1k` or export `AGENT_MONITOR_COST_PER_1K` to enable projections.

## Release notes (current version)
- Added colorized states + KPI banner to the CLI monitor.
- Added looping mode and a polished dark-mode layout for the HTML dashboard.
- Default assets are optimized for screenshots / executive readouts.

That’s it—launch the CLI, fire up the live HTML panel, and give your team a real-time Sessions Dashboard without cobbling together spreadsheets.
