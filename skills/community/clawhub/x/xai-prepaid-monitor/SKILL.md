---
name: xai-prepaid-monitor
description: Monitor xAI prepaid credit balance with a reusable Python script and alert workflow. Use when setting up or troubleshooting low-credit checks for xAI/Grok usage, building cron jobs that warn on prepaid balance thresholds, or creating follow-up automations such as Discord alerts or task creation when xAI credits run low.
---

Use this skill to add a reusable xAI prepaid balance check to an OpenClaw setup.

## What this skill provides

- `scripts/check_xai_balance.py`, a small script that queries the xAI Management API and returns normalized JSON
- a reference file with cron prompt patterns for:
  - alert-only monitoring
  - alert + follow-up task creation

## Environment required

Set these env vars in OpenClaw config or the runtime environment before using the script:

- `XAI_TEAM_ID`
- `XAI_MANAGEMENT_KEY`

Optional thresholds:

- `XAI_BALANCE_WARN_BELOW_CENTS` (default `300`)
- `XAI_BALANCE_CRITICAL_BELOW_CENTS` (default `200`)

## Run the script

Use:

```bash
/usr/bin/python3 /path/to/skills/xai-prepaid-monitor/scripts/check_xai_balance.py
```

The script prints JSON like:

```json
{
  "ok": true,
  "status": "warn",
  "total_cents": 700,
  "used_cents": 450,
  "remaining_cents": 250,
  "total": "$7.00",
  "used": "$4.50",
  "remaining": "$2.50",
  "warn_below": "$3.00",
  "critical_below": "$2.00",
  "billing_cycle": "..."
}
```

## Output contract

Interpret the result this way:

- `ok=false`: the check failed, surface the error briefly
- `status=ok`: no action needed
- `status=warn`: remaining balance is below warning threshold
- `status=critical`: remaining balance is below critical threshold

## Recommended workflow

1. Run the script with `exec`
2. Parse the JSON output
3. If `ok=false`, send a short failure alert
4. If `status=ok`, stay quiet or log success
5. If `status=warn` or `critical`, send a concise alert
6. Optionally create a follow-up task in the user’s task system

## Cron setup

For prompt patterns, read:

- `references/cron-examples.md`

## Guardrails

- Keep delivery logic separate from the script. The script should only fetch and normalize balance data.
- Do not hard-code Discord channel IDs, Todoist paths, or user-specific routing into the script.
- Prefer environment variables for thresholds so the same script works across setups.
- If the xAI API contract changes, update the script and the examples together.
