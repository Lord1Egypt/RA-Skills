# Session Token Ledger

This is the final local token-ledger system for this workspace, designed so it can later be packaged as a reusable skill.

## Files
- `session_tokens.db` — SQLite database
- `TOTAL_TOKENS.txt` — human-readable aggregate summary
- `index.json` — machine-friendly session index
- `ANOMALIES.md` — bad lines / missing usage / suspicious sessions
- `queries.sql` — ready-to-run SQL templates
- `YYYY-MM-DD_N.md` — per-session readable files

## SQLite objects
### Tables
- `sessions`
- `daily_summary`

### Views
- `overall_summary`
- `model_summary`
- `provider_summary`
- `channel_summary`
- `largest_sessions`
- `cost_estimate`
- `usage_efficiency`
- `bloated_sessions`
- `channel_efficiency`
- `daily_efficiency`
- `top_context_hogs`

## What the waste-analysis views do
- `usage_efficiency` → input/output ratio per session
- `bloated_sessions` → likely oversized sessions worth inspecting first
- `channel_efficiency` → which channel burns the most tokens and has the worst ratios
- `daily_efficiency` → which day was fattest and least efficient
- `top_context_hogs` → sessions dominated by input/context, not output

## Future-skill-friendly billing fields
The schema intentionally keeps billing semantics portable:
- `billing_mode` → `subscription | api | hybrid | unknown`
- `cost_applicable` → `0 | 1`
- `estimated_cost_usd` → only meaningful when `cost_applicable = 1`
- `pricing_note` → human explanation of the pricing assumption

## Current local mode
- `billing_mode = subscription`
- Cost is retained structurally, but not directly billable per session.
- For subscription users, the more useful analytics are token totals, largest sessions, and waste-analysis views.

## Automation
This skill can be paired with an optional OpenClaw hook for automatic rebuilds.

Common trigger events:
- `command:new`
- `command:reset`
- `command:stop`
- `gateway:startup`

See `references/hook-setup.md` for a portable setup pattern.

## Important boundary
The active ongoing live `.jsonl` session is skipped by default when a matching `.lock` file exists. It is usually finalized into the ledger on the next `/new`, `/reset`, `/stop`, or gateway restart.
