---
name: smart-search
description: "Combine web and academic search into one smart AISA search mode. Use when: the user needs a balanced research pass that mixes public web coverage with academic depth."
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
# Smart Search

## When to Use

- Combine web and academic search into one smart AISA search mode. Use when: the user needs a balanced research pass that mixes public web coverage with academic depth.

## When NOT to Use

- Do not use this skill for browser-cookie extraction, passwords, Keychain access, or other local sensitive credential access.
- Prefer a different skill when the user request is outside this skill's domain.

## Capabilities

- Blend public web coverage with academic retrieval in one query flow.

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

- Research benchmark progress for open-weight reasoning models.

## Notes

- Good default when the query spans both news and papers.
