---
name: web-search
description: "Search the public web through the AISA web search endpoint and return structured titles, links, and snippets. Use when: the user asks to look something up online, gather recent sources, or browse general web results."
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
# Web Search

## When to Use

- Search the public web through the AISA web search endpoint and return structured titles, links, and snippets. Use when: the user asks to look something up online, gather recent sources, or browse general web results.

## When NOT to Use

- Do not use this skill for browser-cookie extraction, passwords, Keychain access, or other local sensitive credential access.
- Prefer a different skill when the user request is outside this skill's domain.

## Capabilities

- Return fast structured web results for general online lookup tasks.

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

- Search the web for the latest open-source browser automation tools.

## Notes

- This is the lightest-weight general search option in the bundle.
