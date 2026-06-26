---
name: janitor
description: Automated transcript trimming, LLM memory extraction, and session hygiene for OpenClaw gateways. Keeps transcripts from bloating, extracts structured memories before archiving, and prunes stale sessions.
metadata: {"openclaw": {"requires": {"bins": ["python3", "jq"]}}}
---

# Session Janitor

Automated transcript and session hygiene for OpenClaw gateways.

## What It Does

- **Sidecar offloader** — extracts large tool outputs (≥5KB) to `.toolcache/` files, replacing inline content with lightweight stubs. Runs before trim on every turn.
- **Trims oversized transcripts** — keeps recent exchanges + synthetic compaction summary, archives the rest
- **LLM memory extraction** — uses the gateway's chat completions API to extract structured memories (facts, decisions, lessons) from trimmed content before discarding
- **Prunes stale sessions** — removes old subagent/cron session entries from sessions.json
- **Archives orphan transcripts** — files with no active session after a grace period
- **Cleans old archives** — removes pre-trim, reset, and checkpoint files after retention period
- **Cleans orphaned checkpoints** — removes `*.checkpoint.*.jsonl` files left behind by auto-compaction once the parent session no longer has an active transcript

## Setup

```bash
bash skills/session-janitor/scripts/setup.sh
```

Setup auto-discovers all gateway installations (`~/.openclaw/`, `~/.openclaw-*/`), generates `config.json`, installs a cron job, and installs the watcher service (systemd on Linux, launchd on macOS).

### macOS Prerequisites

Install `fswatch` for the per-turn watcher:

```bash
brew install fswatch
```

The cron-based janitor works without it (trimming every 15 min instead of within ~3s of each turn).

For architecture details, trimming mechanics, and token math, see `ARCHITECTURE.md`.

## Configuration

Edit `config.json` after setup to tune thresholds:

| Key | Default | Description |
|-----|---------|-------------|
| `trimMaxKB` | 250 | Trim transcripts larger than this. Trim always fires when exceeded — there is no minimum pair count. |
| `keepPairs` | 10 | Number of recent user/assistant pairs to keep after trim. If fewer pairs exist than this, all are kept (no skip). |
| `keepFullPairs` | 2 | Most recent N assistant turns that keep full toolResult bodies (older turns are collapsed to summary lines) |
| `minArchivePairs` | 5 | Informational only — no longer blocks trim. Sessions exceeding `trimMaxKB` are always trimmed. |
| `trimFullThresholdPct` | 50 | Two-stage aggressive reduction when trimmed output still exceeds this % of `trimMaxKB`: (1) strip all assistant turns (tool args + thinking removed); (2) if still over threshold, drop all toolResult entries entirely. Set to 100 to disable. |
| `archiveRetentionDays` | 7 | Delete old archives after this many days (applies to `.reset.*`, `.deleted.*`, `.pre-trim.*`, `.bak-*`, `.purged.*`, `.emergency-*`) |
| `keepPreTrimFiles` | 3 | Max `.pre-trim.*` files to keep per session (oldest deleted immediately, regardless of retention period) |
| `orphanGraceMinutes` | 30 | Wait before archiving orphan transcripts |
| `staleSubagentHours` | 24 | Prune subagent session entries older than this |
| `staleCronSessionHours` | 24 | Prune cron session entries older than this |
| `llmExtraction.enabled` | true | Use LLM to extract memories from trimmed content |
| `llmExtraction.model` | `openclaw` | Model identifier to use for extraction calls |
| `llmExtraction.maxInputChars` | 20000 | Max characters of archived content sent to LLM |
| `llmExtraction.timeoutSecs` | 60 | LLM API call timeout in seconds |
| `llmExtraction.maxMemories` | 15 | Max memories to accept from a single LLM extraction |
| `llmExtraction.minArchived` | 3 | Minimum archived messages required before running LLM extraction |
| `llmExtraction.maxPerRun` | 1 | Max LLM extractions per cron cycle (cost control) |
| `memCli.enabled` | false | Store extracted memories via `mem` CLI (requires mem) |
| `cronSchedule` | `*/15 * * * *` | How often to run |
| `sidecar.enabled` | true | Offload large toolResult entries to `.toolcache/` files |
| `sidecar.minEntryBytes` | 5120 | Minimum toolResult content size (bytes) to trigger offload |
| `extractOnTrim.enabled` | false | Fire async LLM memory extraction after each watcher-triggered trim |
| `extractOnTrim.minArchivedPairs` | 3 | Minimum archived message pairs required before running extraction |
| `extractOnTrim.scene` | `auto` | Memory scene tag to use (`auto` lets the LLM infer from context) |
| `extractOnTrim.salience` | 0.5 | Default salience for extracted memories (0.1–1.0) |
| `watchdog.enabled` | false | Run hung-session detector after each janitor pass |
| `watchdog.staleMinutes` | 5 | Session `updatedAt` age threshold to consider stuck |
| `watchdog.alertSlack` | true | Send Slack DM when a stuck session is detected |
| `watchdog.slackTarget` | — | Slack user ID or channel to notify |
| `watchdog.autoRestart` | false | Auto-trigger safe-restart script on detection (use with caution) |
| `watchdog.restartScriptSlack` | `~/bin/safe-slack-restart.sh` | Safe restart script path for Slack gateway |
| `watchdog.restartScriptDiscord` | `~/bin/safe-gateway-restart.sh` | Safe restart script path for Discord gateway |

## Gateway Discovery

Setup scans for `~/.openclaw/openclaw.json` and `~/.openclaw-*/openclaw.json`. Each discovered gateway gets its own entry in `config.json` with:
- Port (from `gateway.port` in config)
- Auth token (from `gateway.auth.token`)
- Sessions directory path

Works with single-gateway installs, multi-gateway (Discord + Slack), or any custom layout.

## LLM Extraction Guardrails

- **Lockfile** — only one extraction at a time across all gateways
- **Max per run** — configurable cap per cron cycle (default: 1)
- **20K char input cap** — truncates middle of very long conversations
- **60s hard timeout** — SIGALRM kills hung API calls
- **Dedup** — state file tracks processed trims, never re-runs
- **No context inflation** — memories go to `mem` DB only, never to files that get auto-loaded into session context

## Manual Run

```bash
bash skills/session-janitor/scripts/janitor.sh
```

## Logs

```bash
tail -f /tmp/session-janitor.log
```

## Watcher Service

The watcher fires trim within ~3 seconds of each turn completing (vs. waiting for the next cron cycle). `setup.sh` installs it automatically as a system service.

*Linux (systemd):*
```bash
systemctl --user status session-janitor-watcher
systemctl --user restart session-janitor-watcher
tail -f /tmp/session-janitor-watcher.log
```

*macOS (launchd):*
```bash
launchctl list | grep session-janitor
launchctl unload ~/Library/LaunchAgents/ai.openclaw.session-janitor-watcher.plist
launchctl load  ~/Library/LaunchAgents/ai.openclaw.session-janitor-watcher.plist
tail -f /tmp/session-janitor-watcher.log
```

- *Linux* uses `inotifywait` (from `inotify-tools`) and watches via inotify kernel events.
- *macOS* uses `fswatch` (via Homebrew) and watches via FSEvents.

## Watchdog

The watchdog runs after every janitor pass and checks `updatedAt` on all active sessions. If any session is stale longer than `watchdog.staleMinutes`, it fires a Slack alert. Optional `autoRestart` will trigger the appropriate safe-restart script.

Alert cooldown is 10 minutes per session to prevent spam. State is tracked in the janitor state file.

```bash
# Run standalone
bash skills/session-janitor/scripts/watchdog.sh 5 ~/.openclaw/session-janitor-state.json
```

## Sub-Agent Reporting Conventions

Workers spawned via Foreman should use prefixed `sessions_send` messages to prevent the parent agent from spawning new sub-agents in response to status updates:

```
# Intermediate status (fire-and-forget — parent relays but does NOT spawn)
sessions_send(sessionKey="{PARENT}", message="STATUS: 🤖 [label]: doing X (60%)", timeoutSeconds=0)

# Errors/failures (normal delivery — parent may intervene)
sessions_send(sessionKey="{PARENT}", message="ERROR: 🤖 [label]: what failed — details")

# Completion (no prefix, normal delivery)
sessions_send(sessionKey="{PARENT}", message="🤖 [label]: ✅ done — summary")
```

- `STATUS:` → relay-only; `timeoutSeconds=0` prevents reply-back loops
- `ERROR:` → parent receives and considers recovery action
- No prefix → completion; parent handles and relays to channel

## Files

```
skills/session-janitor/
├── SKILL.md                              # This file
├── ARCHITECTURE.md                       # Deep dive: trimming mechanics, token math, examples
├── config.json                           # Generated by setup (gitignored)
├── config.example.json                   # Reference config
├── session-janitor-watcher.service       # Linux: systemd user service template
├── session-janitor-watcher.plist         # macOS: launchd LaunchAgent template
└── scripts/
    ├── setup.sh           # Discovery + config gen + cron + service install (Linux + macOS)
    ├── janitor.sh         # Main cron entry point
    ├── trim.py            # Transcript trimming (thinking, toolCall args, toolResult collapse)
    ├── sidecar.py         # Large toolResult offloader (→ .toolcache/ files)
    ├── watcher.sh         # Per-turn trigger (sidecar + trim; inotifywait/fswatch)
    ├── extract-llm.py     # LLM memory extraction
    ├── prune-sessions.py  # Stale session pruning
    ├── watchdog.sh        # Hung-session detector + Slack alert
    ├── test-sidecar.py    # Sidecar test suite (8 scenarios, 22 assertions)
    └── test-sidecar.sh    # Shell wrapper for sidecar tests
```
