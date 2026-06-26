---
name: stock-portfolio
description: "Create and manage stock crypto portfolios with live AISA pricing and P&L tracking. Use when: the user wants to add holdings, inspect portfolio performance, rename portfolios, or review current profit and loss."
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
# Portfolio Management

## When to Use

- Create and manage stock crypto portfolios with live AISA pricing and P&L tracking. Use when: the user wants to add holdings, inspect portfolio performance, rename portfolios, or review current profit and loss.

## When NOT to Use

- Do not use this skill for browser-cookie extraction, passwords, Keychain access, or other local sensitive credential access.
- Prefer a different skill when the user request is outside this skill's domain.

## Capabilities

- Create, update, list, rename, and delete portfolios from the command line.
- Track live P&L with repo-local state instead of default home-directory persistence.

## Quick Start

```bash
export AISA_API_KEY="your-key"
```

## Primary Runtime

Use the bundled Python client as the canonical ClawHub runtime path:

```bash
python3 scripts/portfolio.py
```

## Example Queries

- Create a portfolio for AI stocks and show the current P&L.

## Notes

- Default state is stored in `./.clawdbot/skills/stock-analysis/portfolios.json` unless `CLAWDBOT_STATE_DIR` is set.
