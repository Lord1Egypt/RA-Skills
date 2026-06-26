---
name: session-distiller
description: >
  Batch-distill completed and live OpenClaw session transcripts into structured daily memory files.
  Two components: distill.py (batch + live session distillation, Granola meeting note distillation,
  Captain's Log ingestion) and context-gate.py (context usage monitor with auto-distill).
  Use when: (1) distilling closed session transcripts to memory, (2) running live distill-in-place
  for approved group chats, (3) monitoring context usage and auto-gating sessions approaching limits,
  (4) ingesting meeting notes into daily memory files (--meeting-notes / --granola),
  (5) ingesting daily log AM/PM files into daily memory files (--daily-log / --captains-log).
  NOT for: real-time memory flush (handled by OpenClaw compaction), vector store ingestion,
  or manual memory file editing.
version: 0.5.1
---

# session-distiller

Batch-process OpenClaw session transcripts into structured daily memory files (`memory/YYYY-MM-DD.md`). Ensures no session knowledge is lost — even from short conversations that end before the real-time memory flush threshold.

> **Platform:** macOS. Reads from `~/.openclaw/agents/main/sessions/`. Requires `trash` CLI.

## Components

| Script | Purpose |
|---|---|
| `scripts/distill.py` | Batch distill closed sessions + live distill-in-place for approved group chats |
| `scripts/context-gate.py` | Poll context usage, warn at threshold, auto-distill + alert at hard gate |

## Prerequisites

- Python 3.8+
- LiteLLM proxy running at `http://localhost:4000` (used for LLM distillation calls)
- `trash` CLI (`brew install trash`) — safe file removal to macOS Trash
- OpenClaw gateway running (for context-gate.py status polling)

## distill.py Usage

```bash
# Batch: dry-run preview of closed sessions
python3 scripts/distill.py --dry-run

# Batch: process all eligible closed sessions (default: 24h+ old)
python3 scripts/distill.py

# Batch: keep source files after distilling
python3 scripts/distill.py --no-trash

# Batch: process a specific session file
python3 scripts/distill.py --file <path-to-session.jsonl>

# Batch: change minimum age threshold
python3 scripts/distill.py --min-age-hours 48

# Live: distill all approved group chat sessions
python3 scripts/distill.py --live [--dry-run]

# Live: distill a specific session by UUID
python3 scripts/distill.py --live-session <session-id> [--dry-run]

# Meeting notes: distill into daily memory files (preferred)
python3 scripts/distill.py --meeting-notes [--dry-run] [--limit N] [--trash]

# Meeting notes: deprecated alias (emits deprecation warning)
python3 scripts/distill.py --granola [--dry-run] [--limit N] [--trash]

# Daily log: ingest AM/PM files into daily memory files (preferred)
python3 scripts/distill.py --daily-log [--dry-run] [--limit N]

# Daily log: deprecated alias (emits deprecation warning)
python3 scripts/distill.py --captains-log [--dry-run] [--limit N]

# Version
python3 scripts/distill.py --version
```

## context-gate.py Usage

```bash
# Live run — polls gateway, sends Telegram alerts
python3 scripts/context-gate.py

# Dry run — logs what would happen, no alerts sent
python3 scripts/context-gate.py --dry-run

# Version
python3 scripts/context-gate.py --version
```

### Environment Variables

| Variable | Default | Description |
|---|---|---|
| `CONTEXT_WARN_PCT` | `40` | Advisory warning threshold (%) |
| `CONTEXT_HARD_PCT` | `60` | Hard gate threshold — triggers auto-distill (%) |
| `BOT_TOKEN` | _(empty)_ | Telegram bot token (required for alerts) |
| `CHAT_ID` | _(empty)_ | Telegram chat ID for alerts (required for alerts) |

## Configuration

### Live Allowlist (`LIVE_ALLOWLIST_KEYS`)

In `scripts/distill.py`, the `LIVE_ALLOWLIST_KEYS` dict controls which sessions get live distill-in-place. Keys are session keys from `sessions.json` (stable across UUID rotations). Add entries as:

```python
LIVE_ALLOWLIST_KEYS = {
    "agent:main:telegram:group:-5166698025": "Claw & Order",
}
```

### Key Paths

| Path | Purpose |
|---|---|
| `~/.openclaw/agents/main/sessions/` | Source session JSONL files |
| `~/.openclaw/agents/main/sessions/sessions.json` | Session key → UUID index |
| `~/.openclaw/workspace/memory/` | Output daily memory files |
| `prompts/distill.txt` | LLM distillation prompt template |
| `offsets.json` | Live session offset tracker (runtime state, auto-created) |
| `gate-state.json` | Context gate per-session state (runtime state, auto-created) |

### LiteLLM Endpoint

Distillation calls go to `http://localhost:4000/v1/chat/completions` with model `claude-opus-4-6`. Change the model or endpoint in the `distill_transcript()` function if needed.

## Scheduling

### Batch Distill (distill.py)

Daily at 03:00 CST via OpenClaw cron. Runs as a sub-agent in an isolated session.

> **Known issue:** The 03:00 cron has a 600s timeout. With ~44 sessions × LLM calls, it times out (5 consecutive errors observed). Mitigations: run with `--min-age-hours 48` to reduce batch size, or split into multiple cron runs.

### Context Gate (context-gate.py)

Every 5 minutes, 07:00–22:00 via shell crontab:
```
*/5 7-22 * * *  /Users/<your-name>/.openclaw/scripts/cron-context-gate.sh
```

## References

- **[ROADMAP.md](references/ROADMAP.md)** — Future ideas, known issues, Phase 4 community release plans

---

## Changelog

### v0.5.1 — 2026-03-17

Hotfix: removed runtime state files from repo and added .gitignore.

- Added .gitignore covering offsets.json, gate-state.json, captains-log-ingested.json, granola-ingested.json
- Removed state files from git tracking (git rm --cached)

### v0.5.0 — 2026-03-17

Configurable paths + flag aliases + de-identification.

- Added configurable paths constants block (`MEETING_NOTES_DIR`, `DAILY_LOG_DIR`, `DAILY_LOG_PATTERN`, `MEMORY_DIR`) — override via env vars without editing the script
- Added `--meeting-notes` flag as the preferred replacement for `--granola`
- Added `--daily-log` flag as the preferred replacement for `--captains-log`
- `--granola` and `--captains-log` still work but now emit a deprecation warning to stderr
- Removed deployment-specific identifiers from docs (SKILL.md, ROADMAP.md); replace `<your-name>` / `<your-repo>` with your own values
- Bumped `__version__` to `0.5.0`

### v0.4.1 — 2026-03-15

Behavior change: `--captains-log` mode now moves source files to `memory/captains-log/ingested/` after successful ingestion (default cleanup, consistent with `--granola` mode).

- Added `--no-move` flag to preserve source files in place
- Added `--trash` flag to trash instead of move
- `memory/` is now clean after ingestion — no redundant duplicate files
- Backfill: existing pre-ingested source files moved to `ingested/` on first run

### v0.4.0 — 2026-03-14

New feature: Captain's Log AM/PM ingestion (`--captains-log` mode, closes #7).

- `--captains-log` flag scans `memory/` for `captains-log-YYYY-MM-DD-am.md` and `captains-log-YYYY-MM-DD-pm.md` files
- No LLM call — logs are already structured summaries, appended as-is
- AM ingested before PM for same date (chronological order guaranteed)
- Appends `## Captain's Log — AM (Morning Watch)` / `## Captain's Log — PM (Dog Watch)` sections
- `captains-log-ingested.json` sidecar for idempotent re-runs
- Source files preserved — not moved or trashed (reference artifacts)
- `--limit N` supported for backlog processing
- Completes the daily LTM pipeline: AM log → Granola meetings → PM log → session distillations

### v0.3.1 — 2026-03-14

New feature: Granola meeting note distillation (`--granola` mode, closes #4).

- `--granola` flag scans `memory/granola/` and distills un-ingested meeting notes into their corresponding `memory/YYYY-MM-DD.md` daily files
- Dedicated prompt file `prompts/distill-granola.txt` tuned for already-summarized meeting notes (extraction focus vs. summarization)
- `granola-ingested.json` sidecar tracks ingested UUIDs — idempotent on re-runs
- UUID dedup against target daily file (same logic as session distillation)
- Source files moved to `memory/granola/ingested/` on success (safe default)
- `--trash` flag to trash instead of move to ingested/
- `--limit N` to cap batch size (recommended for large backlogs)
- `_transcript.md` files skipped by default
- Appends `## Granola — {title} ({uuid8})` sections to daily files
- Creates daily file if none exists for that date
- First run processed 130 candidates: 76 distilled, 20 skipped, 6 NO_DISTILL

### v0.2.0 — 2026-03-12

BREAKING CHANGE (OpenClaw 2026.3.11): Gateway API no longer populates `totalTokens`, `remainingTokens`, or `percentUsed` for live sessions. context-gate.py was completely blind as a result.

Fix: JSONL fallback added to context-gate.py. When API fields are null, gate reads session file on disk, counts message chars, estimates tokens at chars÷4. Token source tagged in log output (`[api]`, `[api:inputTokens]`, or `[jsonl-estimate]`). Gate will auto-switch back to API source when upstream fixes the regression.

Also fixed: distill.py script path in Session Distiller cron was pointing to old `projects/session-distiller/distill.py` location — updated to `skills/session-distiller/scripts/distill.py`. This was causing 5 consecutive cron failures.

Other changes:
- Cron timeout increased 600s → 1800s
- ROADMAP.md updated with known issue entry for token count regression

**Upstream issue status (2026-03-14):** OpenClaw upstream addressed the token count issue at the display layer only (openclaw/openclaw #43987, #45268). The underlying API fields (`totalTokens`, `remainingTokens`, `percentUsed`) remain null as of 2026.3.13. The JSONL fallback introduced in v0.2.0 is the permanent workaround. See ROADMAP.md and <your-repo>/session-distiller #5 for details.

### v0.1.0 — 2026-03-11

Initial skill packaging of session-distiller project. Converted from `projects/session-distiller/` to structured OpenClaw skill. No functional logic changes. Added `--version` flags to both scripts. Removed hardcoded credentials from context-gate.py (now requires `BOT_TOKEN`/`CHAT_ID` env vars). Adjusted relative paths for new `scripts/` directory layout.
