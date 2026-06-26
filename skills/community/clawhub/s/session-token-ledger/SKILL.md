---
name: session-token-ledger
description: Analyze local OpenClaw session token usage from a generated SQLite ledger and markdown summaries. Use when the user asks for a token audit, token体检报告, context-bloat diagnosis, session efficiency review, largest sessions, daily token trends, input/output ratio analysis, cache-read heavy sessions, or wants SQL/SQLite-based inspection of local OpenClaw session usage.
---

# Session Token Ledger

Analyze local OpenClaw session-token usage from a generated ledger stored under this skill.

## What lives here

- `scripts/rebuild_sqlite.py` — rebuild the local ledger from OpenClaw session transcripts
- `scripts/report.py` — generate markdown reports for all sessions or one session
- `references/overview.md` — schema, views, and design notes
- `references/queries.sql` — canned SQLite queries for common audits
- `references/hook-setup.md` — optional OpenClaw hook setup for automatic rebuilds
- `references/ANOMALIES.md` — populated after rebuild with suspicious or bad transcript lines
- `assets/session_tokens.db` — populated after rebuild; SQLite ledger
- `assets/index.json` — populated after rebuild; machine-readable session index
- `assets/TOTAL_TOKENS.txt` — populated after rebuild; quick aggregate summary
- `assets/YYYY-MM-DD_N.md` — populated after rebuild; one markdown file per completed session

## Default workflow

1. Rebuild the ledger with `python3 scripts/rebuild_sqlite.py` if data looks stale.
2. Start with `assets/index.json` for session list and top-level totals.
3. If the user wants trends or rankings, inspect `assets/session_tokens.db`.
4. If the user wants a narrative for one session, read the matching `assets/YYYY-MM-DD_N.md` file.
5. If the user wants root-cause analysis, inspect these views first:
   - `largest_sessions`
   - `usage_efficiency`
   - `bloated_sessions`
   - `top_context_hogs`
   - `daily_efficiency`
6. If something looks wrong, read `references/ANOMALIES.md`.

## Read these references only when needed

- Read `references/overview.md` when you need schema or view meaning.
- Read `references/queries.sql` when you need canned SQL.
- Read `references/hook-setup.md` when you want automatic rebuilds after `/new`, `/reset`, `/stop`, or gateway startup.

## Quick path

Generate reports:

```bash
python3 scripts/report.py
python3 scripts/report.py --session SESSION_ID
python3 scripts/report.py --save
python3 scripts/report.py --session SESSION_ID --save
```

Use read-only SQLite queries when available:

```bash
sqlite3 -readonly assets/session_tokens.db "SELECT * FROM overall_summary;"
sqlite3 -readonly assets/session_tokens.db "SELECT * FROM largest_sessions LIMIT 10;"
sqlite3 -readonly assets/session_tokens.db "SELECT * FROM bloated_sessions LIMIT 10;"
sqlite3 -readonly assets/session_tokens.db "SELECT * FROM top_context_hogs LIMIT 10;"
sqlite3 -readonly assets/session_tokens.db "SELECT * FROM daily_efficiency ORDER BY date DESC;"
```

For one session:

```bash
sqlite3 -readonly assets/session_tokens.db "SELECT * FROM usage_efficiency WHERE session_id='SESSION_ID';"
```

If `sqlite3` CLI is unavailable, use the bundled Python scripts instead.

## Reporting rules

- Lead with the plain-English conclusion.
- Separate total tokens, input tokens, output tokens, and cache read.
- Call out whether waste came from long context, too many topic switches, long outputs, or repeated tool/doc loading.
- For subscription-style billing, emphasize token totals and efficiency, not fake precision on dollar cost.
- When giving recommendations, prefer a short ranked list over a long essay.

## Boundaries

- Treat this ledger as local analysis data, not ground truth for provider billing.
- Do not modify the database unless the user explicitly asks to rebuild or update the ledger.
- Rebuilds skip the currently active live `.jsonl` session when a matching `.lock` file exists, so the ledger defaults to completed sessions only.
- Prefer querying the DB over manually re-deriving totals from raw session logs unless the ledger appears stale or broken.
