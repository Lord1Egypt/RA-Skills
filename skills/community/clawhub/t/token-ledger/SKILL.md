---
name: token-ledger
description: Audit-grade token and cost ledger for OpenClaw. Use when you need to (1) record every model call's usage (input/output/cache read/cache write/cost) into SQLite, (2) install/manage the ledger watcher LaunchAgent, (3) query ledger.db for daily usage/cost, fixed overhead, or historical billing reconciliation, or (4) generate low-token financial reports from SQL.
metadata:
  openclaw:
    version: "0.1.2"
    emoji: "🧾"
    homepage: https://clawhub.ai/jonathanjing/token-ledger
    requires:
      bins: [python3]
    envVars:
      - name: LOCAL_API_HUB_URL
        required: false
        description: Optional loopback API used to synchronize local Spark usage.
      - name: TOKEN_LEDGER_POLL_INTERVAL
        required: false
        description: Optional watcher interval in seconds.
---

# Token Ledger (SQLite)

Install with:

```bash
openclaw skills install @jonathanjing/token-ledger
```

## What this skill provides

- A **SQLite ledger** at `~/.openclaw/ledger.db` with per-call usage rows
- A **watcher daemon** that tails OpenClaw session JSONL files and writes usage into SQLite (near-real-time)
- **Spark token sync** - pulls DGX Spark local inference logs via API Hub
- Deterministic, low-token **SQL-first** finance reports (no JSONL rescans)

## Canonical usage definitions

- `input_tokens`: uncached input tokens for the call
- `cache_write_tokens`: tokens written to cache
- `cache_read_tokens`: tokens read from cache
- `output_tokens`: generated tokens
- **total_context_tokens** = `input_tokens + cache_write_tokens + cache_read_tokens`

## Files & paths

| File | Path |
|------|------|
| SQLite DB | `~/.openclaw/ledger.db` |
| Checkpoint | `~/.openclaw/ledger-checkpoint.json` |
| Spark Checkpoint | `~/.openclaw/ledger-spark-checkpoint.json` |
| Sessions JSONL | `~/.openclaw/agents/main/sessions/*.jsonl` |
| Cron Runs | `~/.openclaw/cron/runs/**/*.jsonl` |
| Spark Token Log (NFS) | `~/spark-nfs/.spark/token-ledger.jsonl` |

## Standard operations

### One-shot backfill (safe)

```bash
python3 "{baseDir}/scripts/ledger_watcher.py" --once
```

### Backfill source_kind for existing records

```bash
python3 "{baseDir}/scripts/ledger_watcher.py" --backfill
```

### Sync Spark tokens only

```bash
python3 "{baseDir}/scripts/ledger_watcher.py" --sync-spark
```

### Install / start daemon (macOS LaunchAgent)

```bash
python3 "{baseDir}/scripts/render_plist.py" \
  > ~/Library/LaunchAgents/com.openclaw.token-ledger-watcher.plist
launchctl load ~/Library/LaunchAgents/com.openclaw.token-ledger-watcher.plist
launchctl list | rg token-ledger-watcher
```

### Stop daemon

```bash
launchctl unload ~/Library/LaunchAgents/com.openclaw.token-ledger-watcher.plist
```

### Quick sanity query

```bash
sqlite3 ~/.openclaw/ledger.db \
  "SELECT provider, model, COUNT(*) calls, ROUND(SUM(cost_total),4) cost FROM calls WHERE ts >= date('now') GROUP BY 1,2 ORDER BY cost DESC LIMIT 20;"
```

## How to build low-token Finance reports

Preferred flow:
1. Run SQL queries directly against `ledger.db`
2. Format results with a deterministic template (no long reasoning)
3. Only if numbers look anomalous: drill into `calls` for the specific session/model

For daily reports, use:
- per-model totals
- cached vs uncached mix
- top sessions by cost
- source_kind breakdown (interactive | cron | spark)

## Notes / caveats

- Provider billing can still exceed ledger totals due to retries/timeouts/streaming interruptions. Ledger is **auditable**, not magical.
- Keep pricing versioned. Do not retroactively reprice historical calls unless explicitly requested.
- **Deleted threads**: Watcher handles `.jsonl.deleted*` files
- **Spark local tokens**: Spark local calls are logged via `spark-token-ledger.jsonl`. API Hub provides `/spark/token-log` endpoint for the watcher to pull (unidirectional sync).
- **Model normalization**: Cloud models (Claude/GPT/Gemini) are normalized from `provider/model` format. Local Spark models are normalized to `qwen-spark-35b` or `qwen-spark-27b`.

## Architecture

Use the bundled scripts as the source of truth; do not assume a separate workspace-specific reference file exists.

### Data Flow

```
OpenClaw Sessions          Cron Jobs               DGX Spark
      ↓                        ↓                        ↓
*.jsonl               cron/runs/*.jsonl      spark-token-ledger.jsonl
      ↓                        ↓                        ↓
      └────────────────────┬──────────────────────────┘
                           ↓
                ledger_watcher.py
                           ↓
                    ledger.db (SQLite)
                           ↓
               SQL Queries / Reports
```

### Key Tables

- `calls` - Per-call usage records
- `turns` - Aggregated turn-level metrics (60s window)
- `price_versions` - Historical pricing for audit

### Source Kind Detection

| Source | Detection |
|--------|-----------|
| Interactive | Default, or from sessions.json |
| Cron | Path contains `cron/runs` OR session_key contains `:cron:` |
| Subagent | Session key contains `:subagent:` or `:run:` |
| Spark | Records from Spark token log sync |

## Preset queries

```bash
# Today
today() {
  sqlite3 ~/.openclaw/ledger.db "SELECT provider, model, COUNT(*) calls, SUM(input_tokens) input, SUM(output_tokens) output, ROUND(SUM(cost_total),4) cost FROM calls WHERE ts >= date('now') GROUP BY 1,2 ORDER BY cost DESC;"
}

# By source kind
today_by_source() {
  sqlite3 ~/.openclaw/ledger.db "SELECT source_kind, COUNT(*) calls, ROUND(SUM(cost_total),4) cost FROM calls WHERE ts >= date('now') GROUP BY 1;"
}

# Spark usage (local models)
spark_usage() {
  sqlite3 ~/.openclaw/ledger.db "SELECT model, COUNT(*) calls, SUM(input_tokens + output_tokens) tokens FROM calls WHERE provider = 'local-dgx-spark' GROUP BY model;"
}
```

## Pricing integrity

Use the versioned `price_versions` table. The watcher persists every bundled
rate, its effective timestamp, and the provider pricing-page URL when the
database opens. Provider pricing changes over time; do not copy a current price
table into reports without recording its effective date and source.
