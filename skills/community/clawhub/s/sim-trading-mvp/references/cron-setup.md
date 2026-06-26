# Cron setup

Use this guide when the user wants the simulated trading workflow automated.

## Default decision windows

Use four jobs on US trading days (`America/New_York`):

1. `pre_or_open`
   - around `09:25`
2. `intraday`
   - around `12:30`
3. `near_close`
   - around `15:45`
4. `postmarket_sync`
   - around `16:10`

## Behavior

### Decision windows

For the first three jobs:

- load account state
- inspect prior same-day decisions
- load price context from the single primary market-data source (recommended: Finnhub)
- research real market context
- output one action only: `BUY`, `SELL`, or `HOLD`
- update account/log files
- do not send the user an intermediate summary unless explicitly requested

### Post-market sync

For the last job:

- read the updated account and trade log
- compute the best available truthful summary
- send the user the daily recap in Chinese

## Example OpenClaw cron commands

```bash
openclaw cron add --name "sim-trading-preopen" --cron "25 9 * * 1-5" --tz "America/New_York" --session isolated --light-context --no-deliver --message "Sim trading decision window: pre_or_open. Read the account and trade log, research real finance context, then record exactly one action: BUY, SELL, or HOLD. Do not fabricate data."

openclaw cron add --name "sim-trading-intraday" --cron "30 12 * * 1-5" --tz "America/New_York" --session isolated --light-context --no-deliver --message "Sim trading decision window: intraday. Read the account and trade log, research real finance context, then record exactly one action: BUY, SELL, or HOLD. Do not fabricate data."

openclaw cron add --name "sim-trading-nearclose" --cron "45 15 * * 1-5" --tz "America/New_York" --session isolated --light-context --no-deliver --message "Sim trading decision window: near_close. Read the account and trade log, research real finance context, then record exactly one action: BUY, SELL, or HOLD. Do not fabricate data."

openclaw cron add --name "sim-trading-postmarket-sync" --cron "10 16 * * 1-5" --tz "America/New_York" --session isolated --light-context --announce --message "Post-market sync for simulated trading. Read the account and trade log, then send the user a truthful Chinese recap with performance, positions, today's three decisions, reasoning, and review."
```

## Safety checks

Before creating cron jobs:

- confirm the user wants automation
- inspect existing jobs to avoid duplicates
- keep job names predictable
- make sure the project file paths are correct

If jobs already exist, patch or replace them intentionally rather than piling up duplicates.
