# xai-prepaid-monitor

OpenClaw skill for monitoring xAI prepaid credit balance with a reusable Python script and simple alert workflow patterns.

## What it does

This skill provides:

- a small Python script that queries the xAI Management API and returns normalized JSON balance data
- reusable cron prompt examples for:
  - alert-only monitoring
  - alert + follow-up task creation

It is useful when you want to warn on low Grok/xAI prepaid balance without hard-coding delivery or task-system logic into the script itself.

## Files

- `SKILL.md` — skill metadata and usage instructions
- `scripts/check_xai_balance.py` — balance-check script
- `references/cron-examples.md` — example cron prompt patterns

## Required environment

Set these environment variables before using the script:

- `XAI_TEAM_ID`
- `XAI_MANAGEMENT_KEY`

Optional threshold overrides:

- `XAI_BALANCE_WARN_BELOW_CENTS` (default `300`)
- `XAI_BALANCE_CRITICAL_BELOW_CENTS` (default `200`)

## Run the script directly

```bash
/usr/bin/python3 scripts/check_xai_balance.py
```

Example output:

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

- `ok=false` — check failed
- `status=ok` — no action needed
- `status=warn` — remaining balance is below warning threshold
- `status=critical` — remaining balance is below critical threshold

## Packaging

To package the skill:

```bash
python3 <openclaw-install>/skills/xai-prepaid-monitor/scripts/package_skill.py . ./dist
```

## Notes

- Keep delivery routing outside the script so the skill stays reusable across setups.
- Prefer environment variables for thresholds instead of editing the script.
- If the xAI billing API changes, update the script and cron examples together.
