---
name: stock-rumors
description: "Scan M&A, insider, analyst, social, and regulatory rumor signals through AISA. Use when: the user asks about early market signals, rumors, insider activity, analyst changes, or takeover chatter."
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
# Rumor Scanner

## When to Use

- Scan M&A, insider, analyst, social, and regulatory rumor signals through AISA. Use when: the user asks about early market signals, rumors, insider activity, analyst changes, or takeover chatter.

## When NOT to Use

- Do not use this skill for browser-cookie extraction, passwords, Keychain access, or other local sensitive credential access.
- Prefer a different skill when the user request is outside this skill's domain.

## Capabilities

- Rank rumor-like signals by likely impact across several signal categories.

## Quick Start

```bash
export AISA_API_KEY="your-key"
```

## Primary Runtime

Use the bundled Python client as the canonical ClawHub runtime path:

```bash
python3 scripts/rumor_scanner.py
```

## Example Queries

- Scan for the strongest takeover or insider signals this week.

## Notes

- Rumors are unconfirmed and should be independently verified.
