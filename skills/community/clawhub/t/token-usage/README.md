# Token Usage Tracker

> **v2.5.2 fixes Codex input overcounting.** Codex `input_tokens` includes cached prompt tokens, so older reports could show cached tokens as ordinary input and then list them again under cache. The parser now reports uncached input and cache reads separately. This correction applies to Codex rollout records; OpenClaw session usage fields were already separate. Per-turn totals measure processing volume, not unique text typed, because repeated prompt context is counted again on later turns.

## Release Notes — v2.5.2

- Fixed Codex rollout accounting by subtracting `cached_input_tokens` from inclusive `input_tokens` before reporting uncached input.
- Kept cache reads separate in report totals and cache-aware cost calculations.
- Clarified that summed per-turn input is processing volume, not unique user-provided text.

Parse OpenClaw and Codex session files to extract token usage, aggregate by date/model/session type, and generate cost reports across providers. Works across OpenClaw storage eras — pre-9.x JSONL, 9.x SQLite, and transitional mixed storage.

## When to Use

- User asks "how many tokens did I use today/this week"
- Budget monitoring and anomaly detection
- Before/after optimization comparisons
- Cron job: daily token report to Telegram

## Version-Aware Storage Detection

The parser detects the installed OpenClaw version and storage backend automatically:

```
OpenClaw version : 2026.9.4
Storage backend  : mixed  (jsonl=5581, sqlite=1, zst_archives=22)
⚠️  Mixed storage: SQLite (9.x live) + loose JSONL files detected.
```

| OpenClaw Version | Storage | Behavior |
|------------------|---------|----------|
| pre-9.x (≤2026.6.x) | JSONL only | Reads `.jsonl` / `.jsonl.gz`; warns if SQLite DB found |
| 9.x (≥2026.9.x) | SQLite primary | Reads `transcript_events`; merges with any JSONL |
| transitional | mixed | Reads both; warns so you know to consolidate |
| unknown | auto-detect | Reads whatever is present; warns |

Version is detected by scanning all NVM node trees for `openclaw/package.json` and picking the newest — never shells out to `openclaw --version` (which can block on a live gateway lock).

## Architecture

```
scripts/
  parse.py     — Direct parser (primary; auto-detects version + storage)
  common.py    — Session discovery, parsing, model normalization, cost estimation
  ingest.py    — Incremental ingestion into SQLite (usage.db)
  report.py    — Report generation from SQLite
  pricing.json — Model pricing table (user-editable)
  registry.json — Model metadata: availability, provider, context windows
```

`parse.py` is the primary tool. `ingest.py` + `report.py` remain available for advanced SQL querying and long-term retention.

## Data Sources

| Source | Pattern | Classification |
|--------|---------|----------------|
| 9.x live transcripts | `openclaw-agent.sqlite → transcript_events` | `user` or `cron:<name>` |
| Interactive sessions | `*.jsonl`, `*.jsonl.gz` | `user` or `cron:<name>` |
| Zstd-compressed archives | `*.jsonl.deleted.*.zst` | `user` or `cron:<name>` |
| Codex app-server rollouts | `codex-home/sessions/**/*.jsonl` | `background:codex` |

## Key Behaviors

- **9.x SQLite backend** (T16): Live session transcripts moved into `openclaw-agent.sqlite`. The parser reads `transcript_events.event_json` via a snapshot-to-`/tmp` pattern (the live DB is in OpenClaw's protected state directory). macOS requires plain `sqlite3.connect()` — URI read-only mode (`file:...?mode=ro`) fails on temp files.
- **Timestamp normalization** (T16): SQLite stores UTC timestamps with `Z` suffix; `--since` / `--until` boundaries are local IST. `_normalise_ts()` strips `Z` so string comparison works across both formats.
- **Mtime pre-filter** (T16): `find_sessions(since=...)` only opens files modified within the time window. Critical with 5,600+ historical JSONL files — `--today` no longer scans everything.
- **Session type separation**: Codex rollout logs (background agent jobs using GPT-5.6-Luna etc.) are classified as `background:codex`, NOT merged into user-facing reports. Prevents false "you used 12M Luna tokens" reports when the user was actually on Kimi.
- **Zstd support**: Archived sessions are decompressed transparently via the `zstd` CLI.
- **Defensive parsing**: Records with `"info": null` are handled gracefully (Cloudy's fix — prevents `AttributeError` crash).
- **Incremental ingestion**: Only new/modified session files are processed. State tracked in `ingestion_log` table.

## Commands

```bash
# Direct parser (recommended — auto-detects version + storage)
python3 scripts/parse.py --today
python3 scripts/parse.py --yesterday
python3 scripts/parse.py --week
python3 scripts/parse.py --hours 24
python3 scripts/parse.py --days 7
python3 scripts/parse.py --since 2026-09-11 --until 2026-09-18
python3 scripts/parse.py --yesterday --costs --compact   # Telegram-friendly
python3 scripts/parse.py --session-detail              # Per-session breakdown
python3 scripts/parse.py --cache                       # Include cache columns

# Ingest new sessions into SQLite (optional, for advanced use)
python3 scripts/ingest.py

# Generate reports from SQLite
python3 scripts/report.py --today
python3 scripts/report.py --yesterday
python3 scripts/report.py --week
python3 scripts/report.py --month
```

## Pricing

Edit `scripts/pricing.json` to add/update model pricing. Format:
```json
{
  "kimi/k2.7": {"input": 0.50, "output": 2.00, "cache_read": 0.10, "cache_write": 0.50},
  "openai/gpt-5.6-luna": {"input": 0.20, "output": 1.20, "cache_read": null, "cache_write": null}
}
```

Costs are estimates in USD per 1M tokens. Unknown models report without cost. Run `update-pricing.py` to fetch current rates from OpenRouter + Moonshot direct.

## Known Issues / History

| Date | Issue | Fix |
|------|-------|-----|
| 2026-09-18 | Nightly report returned 0 tokens after 9.x upgrade | T16: version detection + SQLite backend + macOS connect fix + timestamp normalisation + mtime pre-filter |
| 2026-09-16 | Parser missed zstd-compressed sessions (`.jsonl.deleted.*.zst`) → false "no activity since Aug 16" | Added `*.jsonl.*.zst` glob + `_zstd_open()` in `common.py` |
| 2026-09-16 | Codex rollout usage merged into user reports → false "12M Luna tokens" | Added `background:codex` classification in `ingest.py` |
| 2026-09-16 | `"info": null` in Codex records caused `AttributeError` | Defensive `(payload.get("info") or {})` pattern (Cloudy's fix) |

## Dependencies

- `zstd` CLI (for `.zst` decompression)
- Python 3.10+ (stdlib only — no pip installs needed)
