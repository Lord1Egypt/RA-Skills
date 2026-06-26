# session-distiller

An OpenClaw skill that batch-processes completed and live session transcripts, Granola meeting notes, and Captain's Log entries into structured daily memory files. Ensures zero session knowledge is lost — even from short conversations that end before the real-time memory flush threshold.

---

## What It Does

session-distiller has two components:

### 1. Session Distiller (`distill.py`)

Processes multiple sources into daily memory files (`memory/YYYY-MM-DD.md`):

- **Batch mode** — closed OpenClaw session transcripts (`.reset`, `.deleted`, `.bak` files)
- **Live mode** — live distill-in-place with offset tracking for approved group chat sessions
- **Granola mode** (`--granola`) — distills Granola meeting notes from `memory/granola/` into daily memory files
- **Captain's Log mode** (`--captains-log`) — ingests AM/PM Captain's Log files into daily memory files

### 2. Context Gate (`context-gate.py`)

External cron-based context usage monitor. Polls the OpenClaw gateway for live session context percentages. Sends a Telegram advisory alert at the warning threshold, and triggers auto-distillation + a hard alert at the gate threshold. Enforces the context flush policy externally — George can't miss it even if deep in a task.

---

## Daily LTM Pipeline

The distiller builds a complete daily memory file from multiple sources, in chronological order:

```
memory/YYYY-MM-DD.md
  ├── Captain's Log AM  (--captains-log)
  ├── Granola meetings  (--granola, distilled via LLM)
  ├── Captain's Log PM  (--captains-log)
  └── Session distillations  (batch/live mode)
```

---

## How It Works

### Memory Pipeline

```
STM (context window)
  ↓ memory flush (real-time, if token threshold reached)
  ↓ session distillation (batch, catches sessions that ended before flush)
  ↓
LTM (memory/YYYY-MM-DD.md — indexed by memory_search)
```

### Batch Distillation Flow

```
~/.openclaw/agents/main/sessions/
  *.jsonl.reset.*     ─┐
  *.jsonl.deleted.*    ─┤──▶ Parse ──▶ Filter ──▶ Distill ──▶ Append ──▶ Trash
  *.jsonl.bak.*        ─┘                                       │
                                                                 ▼
                                                    memory/YYYY-MM-DD.md
```

1. **Scan** — Find session files with `.reset`, `.deleted`, or `.bak` suffixes older than 24 hours (configurable)
2. **Parse** — Read JSONL (`{"type":"message","message":{"role":"...","content":...}}` format)
3. **Filter** — Strip heartbeat polls, empty email checks, `NO_REPLY` turns, cron noise, and system boilerplate. Skip files with fewer than 3 meaningful messages.
4. **Distill** — Feed filtered transcript + existing daily log (for dedup context) to Claude via LiteLLM proxy at `localhost:4000`
5. **Append** — Add a `## Session Distillation — {uuid}` section to the matching day's memory file
6. **Trash** — Move processed session to macOS Trash via `trash` CLI (never `rm`)

### Live Distill-in-Place (Phase 2)

Group chat sessions (e.g., Telegram groups) stay open indefinitely — they never close, so batch mode never touches them. The `--live` mode uses offset tracking (`offsets.json`) to read only new lines since the last run, distill them, and update the offset. The session file is read-only (never renamed or trashed).

### Context Gate Flow (Phase 3)

```
Every 5 minutes (07:00–22:00):
  ┌─ Poll openclaw gateway call status --json
  │
  ├─ < CONTEXT_WARN_PCT → silent
  ├─ ≥ CONTEXT_WARN_PCT → Telegram advisory alert (once per session)
  └─ ≥ CONTEXT_HARD_PCT → auto-distill → Telegram hard gate alert (once per session)
```

Per-session state is persisted in `gate-state.json` to prevent repeat alerts. Stale entries (sessions that no longer exist) are cleaned up automatically.

---

## Requirements

- macOS (reads from `~/.openclaw/agents/main/sessions/`)
- Python 3.8+
- LiteLLM proxy at `http://localhost:4000` with a Claude-compatible model configured
- [`trash`](https://github.com/ali-rantakari/trash) CLI (`brew install trash`)
- OpenClaw gateway running (for context-gate.py)
- Telegram bot token + chat ID (for context-gate.py alerts)

---

## Installation

```bash
# Clone into the OpenClaw workspace skills directory
cd ~/.openclaw/workspace/skills
git clone <repo-url> session-distiller

# Verify
python3 session-distiller/scripts/distill.py --version
python3 session-distiller/scripts/context-gate.py --version
```

No pip dependencies — uses only Python stdlib plus `curl` and `trash` CLI tools.

---

## Configuration

### Live Session Allowlist

Edit `LIVE_ALLOWLIST_KEYS` in `scripts/distill.py`. Keys are session keys from `sessions.json` (stable across UUID rotations):

```python
LIVE_ALLOWLIST_KEYS = {
    "agent:main:telegram:group:-5166698025": "My Group Chat",
    "agent:main:telegram:direct:123456789": "Direct Session",
}
```

### LiteLLM Endpoint

Distillation calls go to `http://localhost:4000/v1/chat/completions` using model `claude-opus-4-6`. Change these in the `distill_transcript()` function in `distill.py` to match your deployment.

### Context Gate Thresholds

Set via environment variables:

```bash
export CONTEXT_WARN_PCT=40   # Advisory warning (default: 40%)
export CONTEXT_HARD_PCT=60   # Hard gate + auto-distill (default: 60%)
export BOT_TOKEN="<your-telegram-bot-token>"
export CHAT_ID="<your-telegram-chat-id>"
```

---

## Usage

### distill.py

```bash
# Dry-run: preview what would be processed (no writes, no trash)
python3 scripts/distill.py --dry-run

# Process all eligible closed sessions, trash source files after
python3 scripts/distill.py

# Process all eligible closed sessions, keep source files
python3 scripts/distill.py --no-trash

# Process a specific session file
python3 scripts/distill.py --file ~/.openclaw/agents/main/sessions/<uuid>.jsonl.reset.<ts>

# Change minimum age threshold (default: 24 hours)
python3 scripts/distill.py --min-age-hours 48

# Live mode: distill all approved group chat sessions
python3 scripts/distill.py --live
python3 scripts/distill.py --live --dry-run

# Live mode: distill a specific session on demand
python3 scripts/distill.py --live-session <session-uuid>
python3 scripts/distill.py --live-session <session-uuid> --dry-run

# Granola mode: distill meeting notes into daily memory files
python3 scripts/distill.py --granola
python3 scripts/distill.py --granola --dry-run
python3 scripts/distill.py --granola --limit 20        # cap batch size
python3 scripts/distill.py --granola --trash           # trash instead of move to ingested/

# Captain's Log mode: ingest AM/PM logs into daily memory files
python3 scripts/distill.py --captains-log
python3 scripts/distill.py --captains-log --dry-run
python3 scripts/distill.py --captains-log --no-move    # keep source files in place
python3 scripts/distill.py --captains-log --trash      # trash instead of move to ingested/

# Show version
python3 scripts/distill.py --version
```

### context-gate.py

```bash
# Live run (requires BOT_TOKEN and CHAT_ID env vars for alerts)
python3 scripts/context-gate.py

# Dry run: log what would happen without sending alerts
python3 scripts/context-gate.py --dry-run

# Show version
python3 scripts/context-gate.py --version

# Custom thresholds
CONTEXT_WARN_PCT=70 CONTEXT_HARD_PCT=85 python3 scripts/context-gate.py
```

---

## Scheduling

### Batch Distiller (03:00 Daily)

Add to OpenClaw cron configuration to run daily at 03:00:

```
# Session distiller — batch mode, nightly at 0300
python3 /path/to/skills/session-distiller/scripts/distill.py --min-age-hours 48
```

> **Note on 0300 timeouts:** See [Known Issues](#known-issues).

### Context Gate (Every 5 Minutes, 07:00–22:00)

Add to shell crontab:

```
*/5 7-22 * * *  BOT_TOKEN="..." CHAT_ID="..." python3 /path/to/skills/session-distiller/scripts/context-gate.py
```

Or use a wrapper script that exports the environment variables.

---

## Distillation Prompt

The LLM distillation prompt is in `prompts/distill.txt`. It instructs the model to extract:

- Decisions and rationale
- Action items (completed and pending)
- Errors, incidents, and resolutions
- Key technical facts (config values, commands, architecture)
- People mentioned and their roles
- Project/ticket references
- Lessons learned
- User preferences for future behavior

Sessions with nothing worth remembering get a `NO_DISTILL` response — they are not appended to memory and not trashed (preserved for future re-processing with improved prompts).

---

## Deduplication

- Session UUID (first 8 chars) is checked against the target daily file before processing
- If the UUID already appears, the session is skipped
- The distillation prompt receives the full existing daily log to avoid duplicating already-captured information
- Multiple session files sharing the same UUID (e.g., `.bak` and `.reset` variants) — first one processed wins, rest are skipped

---

## Known Issues

### Batch Distiller Cron Timeouts (Critical)

The 03:00 cron has a 600-second timeout. With ~44+ sessions each requiring an LLM call, the batch run consistently times out. **5 consecutive timeout errors observed.**

**Mitigations:**

1. Use `--min-age-hours 48` to reduce batch size to only sessions older than 48 hours (skips recently created files that are still accumulating)
2. Split into multiple targeted runs (e.g., two 30-minute windows instead of one batch)
3. Run on-demand during low-traffic hours instead of scheduled cron

### context-gate.py: Hardcoded Path for openclaw Binary

The script calls `/opt/homebrew/bin/openclaw`. On non-Homebrew or non-macOS installations, this path may need adjustment. Set via the `get_session_status()` function in `scripts/context-gate.py`.

### Edited/Deleted Messages in Group Chats

If a message is edited or deleted in a group chat after it has been distilled, the distilled version persists in memory. This is by design (memory is append-only) but may cause minor inaccuracies in edge cases.

### Session File Rotation

If OpenClaw rotates a live group chat session file, the stored offset becomes invalid. Mitigation: the script detects when the offset exceeds the file's current line count and resets to 0 with a warning. First run after rotation will reprocess the full file history.

---

## Roadmap

The canonical roadmap, future ideas, and long-term known issues are tracked in [`references/ROADMAP.md`](references/ROADMAP.md). GitHub issues in this repo are used for actionable bugs and features; the ROADMAP is the source of truth for strategic direction and upstream dependency status.

---

## Contributing

1. Do not modify functional logic in `distill.py` or `context-gate.py` without running a full dry-run test against a real sessions directory
2. Always use `--dry-run` first when testing against production session files
3. `trash` over `rm` — always
4. Test `--version` after any edits to verify `__version__` is consistent
5. Keep `LIVE_ALLOWLIST_KEYS` minimal — only explicitly approved sessions


