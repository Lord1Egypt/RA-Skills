# YNAB API Skill for Claude Code

Manage your [YNAB](https://www.ynab.com/) budget directly from Claude Code. Add transactions, track goals, monitor spending, create transfers, and generate reports.

## Installation

```bash
clawhub install ynab-api
```

## Configuration

Get your API token from https://app.ynab.com/settings/developer and create `~/.config/ynab/config.json`:

```json
{
  "api_key": "YOUR_YNAB_TOKEN",
  "budget_id": "YOUR_BUDGET_ID"
}
```

Or set `YNAB_API_KEY` and `YNAB_BUDGET_ID` environment variables.

## What it does

Once installed, Claude Code can:

- **Add transactions** -- "add a 10 euro expense at Coffee Shop"
- **Check budget** -- "how much did I spend this month?" / "check my budget"
- **Track goals** -- "how are my budget goals doing?"
- **Upcoming bills** -- "what bills are coming up?"
- **Compare months** -- "compare this month vs last month"
- **Create transfers** -- properly linked between YNAB accounts

## Included Scripts

- `daily-budget-check.sh` -- Morning budget overview
- `goals-progress.sh` -- Visual goal progress bars
- `scheduled-upcoming.sh` -- Upcoming scheduled transactions
- `month-comparison.sh` -- Month-over-month spending analysis
- `transfer.sh` -- Properly linked account transfers
- `ynab-helper.sh` -- General helper (search, categories, etc.)

All scripts output to stdout and can be scheduled with any cron/scheduler.

## License

MIT
