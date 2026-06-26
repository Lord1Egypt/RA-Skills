---
name: stock-analysis
description: "Analyze stocks and cryptocurrencies with live AISA-backed scoring, signals, confidence, and risk flags. Use when: the user asks to analyze a ticker, compare investments, or review market positioning."
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
# Stock Analysis

## When to Use

- Analyze stocks and cryptocurrencies with live AISA-backed scoring, signals, confidence, and risk flags. Use when: the user asks to analyze a ticker, compare investments, or review market positioning.

## When NOT to Use

- Do not use this skill for browser-cookie extraction, passwords, Keychain access, or other local sensitive credential access.
- Prefer a different skill when the user request is outside this skill's domain.

## Capabilities

- Score stocks and crypto assets with live data-backed analysis.
- Return BUY HOLD SELL style signals, confidence, and key risks.

## Quick Start

```bash
export AISA_API_KEY="your-key"
```

## Primary Runtime

Use the bundled Python client as the canonical ClawHub runtime path:

```bash
python3 scripts/analyze_stock.py
```

## Example Queries

- Analyze AAPL versus MSFT and summarize the stronger setup.

## Notes

- Informational only and not financial advice.
