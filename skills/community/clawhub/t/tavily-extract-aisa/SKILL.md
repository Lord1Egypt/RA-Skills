---
name: tavily-extract
description: "Extract clean article content from URLs through the AISA Tavily extract endpoint. Use when: the user already has URLs and needs readable page content for summarization, comparison, or evidence review."
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
# Tavily Extract

## When to Use

- Extract clean article content from URLs through the AISA Tavily extract endpoint. Use when: the user already has URLs and needs readable page content for summarization, comparison, or evidence review.

## When NOT to Use

- Do not use this skill for browser-cookie extraction, passwords, Keychain access, or other local sensitive credential access.
- Prefer a different skill when the user request is outside this skill's domain.

## Capabilities

- Turn raw URLs into clean extractable text for downstream analysis.

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

- Extract these product announcement URLs and summarize the differences.

## Notes

- Best paired with search or follow-up synthesis.
