---
name: stock-hot
description: "Scan trending stocks and crypto movers with live AISA market signals. Use when: the user asks what is hot, what is moving, market momentum, top gainers, or news-driven movers right now."
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
# Hot Scanner

## When to Use

- Scan trending stocks and crypto movers with live AISA market signals. Use when: the user asks what is hot, what is moving, market momentum, top gainers, or news-driven movers right now.

## When NOT to Use

- Do not use this skill for browser-cookie extraction, passwords, Keychain access, or other local sensitive credential access.
- Prefer a different skill when the user request is outside this skill's domain.

## Capabilities

- Surface top movers, momentum names, and quick market summaries.

## Quick Start

```bash
export AISA_API_KEY="your-key"
```

## Primary Runtime

Use the bundled Python client as the canonical ClawHub runtime path:

```bash
python3 scripts/hot_scanner.py
```

## Example Queries

- Show the hottest stocks and crypto movers right now.

## Notes

- Informational only and not financial advice.
