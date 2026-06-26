---
name: scholar-search
description: "Search academic papers and scholarly sources through the AISA scholar endpoint. Use when: the user asks for papers, authors, recent research, citations, or year-filtered academic evidence."
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
# Scholar Search

## When to Use

- Search academic papers and scholarly sources through the AISA scholar endpoint. Use when: the user asks for papers, authors, recent research, citations, or year-filtered academic evidence.

## When NOT to Use

- Do not use this skill for browser-cookie extraction, passwords, Keychain access, or other local sensitive credential access.
- Prefer a different skill when the user request is outside this skill's domain.

## Capabilities

- Focus on academic papers, scholar indexing, and year-filtered retrieval.

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

- Find papers on state-space models published after 2024.

## Notes

- Use when scholarly evidence is the priority.
