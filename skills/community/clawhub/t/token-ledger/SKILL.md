---
name: token-ledger
description: Audit-grade token and cost ledger for OpenClaw. Use when you need to (1) record every model call’s usage (input/output/cache read/cache write/cost) into SQLite, (2) install/manage the ledger watcher LaunchAgent, (3) query ledger.db for daily usage/cost, fixed overhead, or historical billing reconciliation, or (4) generate low-token financial reports from SQL.
---

# Token Ledger (SQLite)

## What this skill provides

- A **SQLite ledger** at `~/.openclaw/ledger.db` with per-call usage rows.
- A **watcher daemon** that tails OpenClaw session JSONL files and writes usage into SQLite (near-real-time).
- Deterministic, low-token **SQL-first** finance reports (no JSONL rescans).

This skill is designed to be **public/reusable**: prefer stable paths, versioned pricing (`price_versions` table), and minimal assumptions.

## Canonical usage definitions (do not mix these)

- `input_tokens`: uncached input tokens for the call (can be tiny)
- `cache_write_tokens`: tokens written to cache (can be huge)
- `cache_read_tokens`: tokens read from cache (can be huge)
- `output_tokens`: generated tokens
- **total_context_tokens (effective prompt size)** = `input_tokens + cache_write_tokens + cache_read_tokens`

## Files & paths

- SQLite DB: `~/.openclaw/ledger.db`
- Checkpoint: `~/.openclaw/ledger-checkpoint.json`
- Sessions JSONL source: `~/.openclaw/agents/main/sessions/*.jsonl`

Skill scripts:
- `scripts/ledger_watcher.py` — watcher daemon (supports `--once`)
- `scripts/ledger_schema.sql` — DDL
- `scripts/com.openclaw.token-ledger-watcher.plist` — LaunchAgent template

## Standard operations (use exec)

### 1) One-shot backfill (safe)

```bash
python3 ~/.openclaw/workspace/skills/token-ledger/scripts/ledger_watcher.py --once
```

### 2) Install / start daemon (macOS LaunchAgent)

This renders the plist with your local `$HOME` (no hard-coded username paths):

```bash
python3 ~/.openclaw/workspace/skills/token-ledger/scripts/render_plist.py \
  > ~/Library/LaunchAgents/com.openclaw.token-ledger-watcher.plist
launchctl load ~/Library/LaunchAgents/com.openclaw.token-ledger-watcher.plist
launchctl list | rg token-ledger-watcher
```

### 3) Stop daemon

```bash
launchctl unload ~/Library/LaunchAgents/com.openclaw.token-ledger-watcher.plist
```

### 4) Quick sanity query

```bash
sqlite3 ~/.openclaw/ledger.db \
  "select provider, model, count(*) calls, round(sum(cost_total),4) cost from calls where ts >= date('now') group by 1,2 order by cost desc limit 20;"
```

## How to build low-token Finance reports

Preferred flow:
1) Run SQL queries directly against `ledger.db`.
2) Format results with a deterministic template (no long reasoning).
3) Only if numbers look anomalous: drill into `calls` for the specific session/model.

For daily reports, use:
- per-model totals
- cached vs uncached mix
- top sessions by cost
- cost_source breakdown (`provider|calculated|local|unknown`)

## Notes / caveats

- Provider billing can still exceed ledger totals due to retries/timeouts/streaming interruptions. Ledger is **auditable**, not magical.
- Keep pricing versioned. Do not retroactively reprice historical calls unless explicitly requested.


## Preset queries (safe)

```bash
python3 ~/.openclaw/workspace/skills/token-ledger/scripts/ledger_query.py today
python3 ~/.openclaw/workspace/skills/token-ledger/scripts/ledger_query.py history --days 30
python3 ~/.openclaw/workspace/skills/token-ledger/scripts/ledger_query.py top-sessions --days 7 --limit 20
```

## Deterministic daily report (no LLM)

```bash
python3 ~/.openclaw/workspace/skills/token-ledger/scripts/ledger_report_daily.py
```
