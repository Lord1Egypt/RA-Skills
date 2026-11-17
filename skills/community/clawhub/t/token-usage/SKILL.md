---
name: token-usage
description: "Track, aggregate, and report OpenClaw token usage and costs across sessions."
homepage: https://github.com/space-cadet/openclaw-token-usage
license: MIT
---

# Token Usage Tracker

Parse OpenClaw and Codex session JSONL files to extract token usage, aggregate by date/model/session, and generate cost reports across providers.

## When to Use

- User asks "how many tokens did I use today/this week"
- User wants to know session costs or model breakdown
- Budget monitoring and anomaly detection
- Before/after optimization comparisons

## Workflow

1. **Locate sessions** — Find `.jsonl` files in OpenClaw agent sessions and nested Codex rollout sessions
2. **Parse usage** — Extract OpenClaw message usage or Codex `event_msg`/`token_count` per-turn usage
3. **Aggregate** — Group by date, model, session ID
4. **Report** — Output summaries, trends, cost estimates

## Commands

### Report by process type and name (friendly labels)
```bash
python3 ${OPENCLAW_HOME}/.openclaw/skills/token-usage/scripts/parse.py --by-process --today
python3 ${OPENCLAW_HOME}/.openclaw/skills/token-usage/scripts/parse.py --by-process --last-hour
python3 ${OPENCLAW_HOME}/.openclaw/skills/token-usage/scripts/parse.py --by-process --since 2026-09-22T13:00:00 --until 2026-09-22T14:00:00 --costs
```

Resolves each session's friendly name from `session_nodes` (display_name / label),
falls back to a derived session_key label like `telegram:direct:849773381` or
`cron:daily-job-hunt`. Groups by process, then model, sorted by token volume.

### Arbitrary time windows
```bash
python3 ${OPENCLAW_HOME}/.openclaw/skills/token-usage/scripts/parse.py --today --since 2026-09-22T10:00:00
python3 ${OPENCLAW_HOME}/.openclaw/skills/token-usage/scripts/parse.py --last-hour --json
```

`--last-hour` covers the last 60 minutes; `--since`/`--until` take ISO times
(matching the UTC 'Z' timestamps stored in the transcript DB).

### Parse and aggregate current sessions (OpenClaw + Codex)
```bash
python3 ${OPENCLAW_HOME}/.openclaw/skills/token-usage/scripts/parse.py --today
```

### Weekly report with cost estimates
```bash
python3 ${OPENCLAW_HOME}/.openclaw/skills/token-usage/scripts/parse.py --week --costs
```

### Report by cron job (daily breakdown per job)
```bash
python3 ${OPENCLAW_HOME}/.openclaw/skills/token-usage/scripts/parse.py --week --by-cron
```

### Weekly cron report with costs (JSON output)
```bash
python3 ${OPENCLAW_HOME}/.openclaw/skills/token-usage/scripts/parse.py --week --by-cron --costs --json
```

### All-time summary by model
```bash
python3 ${OPENCLAW_HOME}/.openclaw/skills/token-usage/scripts/parse.py --all --by-model
```

### Export to JSON for external dashboards
```bash
python3 ${OPENCLAW_HOME}/.openclaw/skills/token-usage/scripts/parse.py --week --json > /tmp/token-report.json
```

## Data Format

Sessions are stored as JSONL with lines like:
```json
{"type":"message","message":{"role":"assistant",...},"usage":{"input":1000,"output":500,"totalTokens":1500},...}
```

## Cost Estimation

Uses model pricing from `scripts/pricing.json` (user-editable). The bundled table includes Kimi, OpenAI/GPT, Anthropic/Claude, and OpenRouter models. Unknown models are reported without a cost estimate rather than silently priced as Kimi.

Default examples (USD per 1M tokens):
- Kimi k2.7: $0.50/1M input, $2.00/1M output
- Claude Sonnet 4: $3.00/1M input, $15.00/1M output
- GPT-4o: $2.50/1M input, $10.00/1M output

Costs are approximate. Cache read/write pricing applied when available.

## Important: What "Total" Means

The script reports **uncached input + output tokens** as the usage metric. These are summed per turn, so prompt context repeated on later turns is counted again as processing volume; this is not unique text supplied by the user.

For Codex rollout events, `input_tokens` includes cached prompt tokens; the parser subtracts `cached_input_tokens` before reporting `input`, and reports cached reads separately. OpenClaw usage records already report input and cache separately. The `totalTokens` field can include cached context; do not add it to the reported input. Cost estimates apply separate input and cache rates where available.

## Output Locations

- Daily summaries: `${OPENCLAW_HOME}/.openclaw/skills/token-usage/logs/YYYY-MM-DD.md`
- Weekly reports: `${OPENCLAW_HOME}/.openclaw/skills/token-usage/logs/week-YYYY-Www.md`
- Raw JSON exports: user-specified or `/tmp/token-usage-*.json`

## Limitations

- OpenClaw records are parsed from `message.usage`; Codex rollouts are parsed from `payload.info.last_token_usage` in `token_count` events
- `uncached input + output` is per-turn processing volume, not unique/new user text; cache reads are separate
- Historical sessions before JSONL format are not supported
- Costs are estimates; actual billing may differ
