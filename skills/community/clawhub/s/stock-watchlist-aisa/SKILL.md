---
name: stock-watchlist
description: "Manage a stock crypto watchlist with target and stop alerts using live AISA price checks. Use when: the user wants to add watchlist items, set targets, track stops, or run alert checks on tickers."
author: aisa
version: "1.0.0"
license: Apache-2.0
user-invocable: true
primaryEnv: AISA_API_KEY
requires:
  env:
    - AISA_API_KEY
  bins:
    - python3
metadata:
  openclaw:
    primaryEnv: AISA_API_KEY
    requires:
      env:
        - AISA_API_KEY
      bins:
        - python3
---
# Watchlist Management

## When to Use

- Manage a stock crypto watchlist with target and stop alerts using live AISA price checks. Use when: the user wants to add watchlist items, set targets, track stops, or run alert checks on tickers.

## When NOT to Use

- Do not use this skill for browser-cookie extraction, passwords, Keychain access, or other local sensitive credential access.
- Prefer a different skill when the user request is outside this skill's domain.

## Capabilities

- Add, remove, list, and check watchlist entries from the command line.
- Store watchlist state in a repo-local directory by default for safer publishing.

## Quick Start

```bash
export AISA_API_KEY="your-key"
```

## Primary Runtime

Use the bundled Python client as the canonical ClawHub runtime path:

```bash
python3 scripts/watchlist.py
```

## Example Queries

- Add NVDA to the watchlist with a target and a stop price.

## Notes

- Default state is stored in `./.clawdbot/skills/stock-analysis/watchlist.json` unless `CLAWDBOT_STATE_DIR` is set.
