---
name: sim-trading-mvp
description: Run a paper-trading / simulated investing workflow with explicit style selection, fixed risk rules, three decision windows per trading day, optional cron setup, persistent account and trade logs, and a post-market daily recap. Use when the user wants a simulated US stock trading account, asks the agent to act like an investor, maintain a model portfolio, make buy/sell/hold decisions, schedule trading decisions during market hours, or send a daily market/trading review. Especially use when the user cares about discipline, repeatability, and truthful reporting without fabricated data.
---

# Sim Trading MVP

Run a disciplined paper-trading loop for an OpenClaw user.

This skill is meant to be reusable across different OpenClaw setups. Do not assume one specific user's style, files, or schedule. Confirm the user's preferences before locking in the workflow.

Use a single structured market-data source for prices, benchmark tracking, and account valuation whenever possible. Current recommended source for this skill: **Finnhub**.

## Non-negotiable rule: truthfulness

Never fabricate market data, execution prices, benchmark performance, news, portfolio state, or trade history.

If data is missing, delayed, unavailable, or uncertain:

- say so clearly
- record the uncertainty explicitly
- prefer `HOLD` over pretending certainty
- never optimize for apparent profit by inventing facts

Trust matters more than simulated returns.

## Confirm these inputs before finalizing the workflow

Before turning the workflow into a persistent setup, confirm these four items with the user:

1. **Style**
2. **Initial rules**
3. **Three decision windows and cron behavior**
4. **Post-market report format**

Do not skip confirmation unless the user explicitly says to use the current/default version.

## 1. Style selection

The skill should support multiple styles.

Examples:

- conservative
- aggressive
- default growth
- custom

### Important

A `custom` style should be personalized for the current OpenClaw user based on their preferences, temperament, and working style. Do not assume one universal custom style across all users.

When building or updating a custom style:

- use the current user's stated preferences
- reflect their appetite for action vs stability
- capture what kind of process they want to watch every day
- write the resulting style into the local project/account files

## 2. Initial rules

Default starter rules for this MVP:

- Initial cash: `$10,000`
- Market: `US stocks + ETFs`
- Disallowed: `options`, `leverage`, `shorting`
- Max single-position weight: `30%`
- Minimum cash: `10%`
- Max high-volatility positions at once: `3`
- Benchmarks: `SPY` and `QQQ`

These are defaults, not sacred constants. If the user changes them, store the updated rules in the project files.

## 3. Three decision windows and automation

The default workflow uses three decision windows per trading day:

1. `pre_or_open`
2. `intraday`
3. `near_close`

In each window, output exactly one action:

- `BUY`
- `SELL`
- `HOLD`

`HOLD` is a valid action. Do not force activity.

If the user wants automation, set up cron jobs for:

- the three decision windows
- one post-market sync

If cron already exists, inspect before changing it. Avoid duplicate jobs.

## 4. Post-market report

The default post-market report should include:

- account equity
- daily return
- cumulative return
- benchmark comparison (`SPY` / `QQQ`)
- current positions
- today's three decision windows
- reasoning
- review / lessons / next watch items

The report can be concise, but it must remain honest and specific.

## Recommended project structure

Use a project directory so the simulated account survives across sessions.

Suggested files:

- `account.json` — account state, rules, style, positions, watchlist
- `trades.jsonl` — append-only decision / execution log
- `README.md` — brief project note

If the user already has a preferred project path, use that instead.

## Core workflow

Follow this order.

### Step 1: Load state

Read the account file and trade log before making any decision.

At minimum, know:

- current cash
- current positions
- current rules
- prior decisions from the same day
- current style

### Step 2: Identify the current decision window

Determine whether you are acting in:

- `pre_or_open`
- `intraday`
- `near_close`
- `postmarket_sync`

For the first three, make exactly one action decision.

### Step 3: Research before acting

Before every decision, gather enough real market context to justify the move.

Use **Finnhub as the primary single source** for:

- current price / quote lookups
- historical price context
- benchmark symbols such as `SPY` and `QQQ`
- account valuation inputs

Use open research/news sources as secondary inputs for:

- broad market tone
- relevant macro events
- company-specific catalysts
- earnings / guidance
- narrative context around held names and watchlist names

Prefer a small number of useful sources over noisy overcollection.

## Data source and secrets

Store API keys outside the skill itself, for example in a local project `.env` or another secret-bearing runtime configuration.

Never hardcode, publish, commit, or echo a user's market-data API key into `SKILL.md`, reference files, public repos, or ClawHub releases.

For this skill, Finnhub may be required for robust price and benchmark handling, but the key must stay in local runtime configuration only.

## Authenticity guardrails

When researching and reporting:

- do not state a price unless you actually retrieved or calculated it from a real source
- do not imply a trade happened unless it was actually recorded
- do not backfill trades after the fact to make the log look better
- do not invent benchmark performance
- do not turn missing information into confident narrative

If the needed data is unavailable, say something like:

- `Market data was unavailable for this window, so I recorded HOLD rather than fabricate a view.`

## Risk enforcement

Always enforce the stored account rules.

If a proposed action breaks the rules, reject it and record `HOLD` with the reason.

Examples:

- position would exceed max concentration
- cash floor would be broken
- security type is not allowed
- too many high-volatility names would be held simultaneously

## Action format

For every `BUY` or `SELL`, record three things:

1. why act now
2. what would invalidate the thesis
3. what the exit / damage-control plan is

For `HOLD`, explain why patience is better than forced activity.

## Logging format

Append one JSON object per line to `trades.jsonl`.

Suggested shape:

```json
{"date":"2026-03-12","window":"intraday","action":"HOLD","ticker":null,"qty":0,"price":null,"reason":"No clean setup.","thesisInvalidation":null,"exitPlan":null,"dataStatus":"incomplete"}
```

For executed buys/sells, include:

- ticker
- quantity
- execution price assumption
- reason
- thesis invalidation
- exit plan
- data quality note if needed

## Post-market sync behavior

At the end of the trading day, send a concise Chinese recap containing:

- account performance
- benchmark comparison
- positions
- today's three decisions
- reasoning
- review
- what to watch next

If any figures are incomplete or estimated, label them clearly.

## Tone

- Sound like an investor with a process.
- Do not sound like a hype bot.
- Discipline beats excitement.
- Truth beats pretty results.
- A boring honest recap is better than a flashy fake one.

## References

Read `references/project-template.md` when setting up a new account from scratch.
Read `references/report-template.md` when formatting the daily sync.
Read `references/log-schema.md` when updating or validating the trading log format.
Read `references/cron-setup.md` when the user wants automated decision windows and post-market sync.
Read `references/style-profiles.md` when selecting or generating a style profile, especially `custom`.

## Scripts

Use `scripts/update_account.py <account.json>` as a minimal account-update helper.

It currently:

- recalculates account equity from `cash` plus position market value when `currentPrice` is available
- updates `totalReturnPct`
- refreshes `updatedAt`

Treat it as a safe starter framework. Extend it when the project grows, but do not silently turn missing price data into fake marks.
