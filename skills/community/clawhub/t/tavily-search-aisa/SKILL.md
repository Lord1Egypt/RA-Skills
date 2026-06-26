---
name: tavily-search
description: "Run Tavily web search through AISA with filters for depth, topic, and time range. Use when: the user needs flexible web search with stronger filtering than a plain keyword search."
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
# Tavily Search

## When to Use

- Run Tavily web search through AISA with filters for depth, topic, and time range. Use when: the user needs flexible web search with stronger filtering than a plain keyword search.

## When NOT to Use

- Do not use this skill for browser-cookie extraction, passwords, Keychain access, or other local sensitive credential access.
- Prefer a different skill when the user request is outside this skill's domain.

## Capabilities

- Offer filtered web search with Tavily-specific controls.

## Quick Start

```bash
export AISA_API_KEY="your-key"
```

## Primary Runtime

Use the bundled Python client as the canonical ClawHub runtime path:

```bash
python3 scripts/search_client.py
```

## Example Queries

- Search AI funding news from the last month with Tavily filters.

## Notes

- Useful when recency and filtering matter.
