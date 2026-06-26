---
name: vibe-billing-scan
description: Scan your OpenClaw API spend and find which run, session, or retry storm is costing you money. Use when your API bill looks too high, when you want to see per-session costs, or when you suspect a retry loop. Triggers: "why is my bill high", "scan my api spend", "check my costs", "vibe billing", "find expensive run", "retry loop cost", "api bill too high".
version: 1.0.0
metadata:
  openclaw:
    emoji: "🛡️"
    homepage: "https://api.jockeyvc.com"
    requires:
      bins: [node, npx]
---

# vibe-billing-scan

Find which OpenClaw run, session, or retry storm is costing you money. One command. No signup. Runs locally.

## When to Use

Activate this skill when the user:
- Says their API bill is higher than expected
- Wants to know which run or session cost the most
- Suspects a retry loop or rate-limit storm
- Asks about token usage, spending, or waste
- Uses phrases like: "why is my bill high", "find the bad run", "scan my spend", "check api costs", "retry loop", "bill shock"

## What This Does

Runs `npx vibe-billing scan` against the user's local OpenClaw logs and API proxy data. Returns:

1. **Which session/run cost the most** — ranked by spend
2. **Retry storm detection** — flags runs where 429 errors caused expensive retry chains
3. **Context accumulation analysis** — shows sessions where the context window grew unusually large
4. **Looped tool call detection** — identifies tool calls that repeated more than expected
5. **Total spend summary** — across all tracked requests

## Quick Reference

```
npx vibe-billing scan        # scan existing logs, no setup needed
npx vibe-billing setup       # install proxy for future runs (optional)
npx vibe-billing status      # show live runtime stats
```

## Step-by-Step Instructions

### Step 1 — Run the scan

Tell the user to run this in their terminal:

```bash
npx vibe-billing scan
```

### Step 2 — Interpret the output

- Requests: total API calls tracked
- Money Saved: estimated waste intercepted
- Tokens Saved: tokens deduplicated or cached
- Loops Blocked: retry storms stopped

### Step 3 — Identify the bad run

Almost always caused by one of:
1. Retry storm — agent hit 429, retried multiple times, each retry re-sent full context
2. Long session — 30+ turn conversation where every message re-sent all prior context
3. Looped tool call — agent called the same tool repeatedly on unexpected output

### Step 4 — Set up ongoing monitoring (optional)

```bash
npx vibe-billing setup
```

## Proof

- $7,691 saved across tracked requests
- 947 million tokens intercepted
- 161 loops blocked

## Landing Page

https://api.jockeyvc.com
