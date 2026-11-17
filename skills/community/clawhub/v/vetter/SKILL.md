---
name: vetter
description: Security-first skill vetting for AI agents. Use before installing any skill from ClawHub, GitHub, or other sources. Checks for red flags, permission scope, and suspicious patterns.
version: 1.0.0
metadata:
  openclaw:
    emoji: "\U0001F50D"
    requires:
      bins:
        - python3
---

# Vetter

Security-first skill vetting. Run this check before installing any third-party skill.

## Quick Start

```bash
python3 scripts/check_env.py
```

The check verifies Python, prints a short environment summary, and writes a local marker file.

## What it does

- Flags overly broad filesystem or network permissions
- Looks for suspicious install scripts and outbound URLs
- Prints a pass / warn / fail summary

Treat third-party skills as untrusted until this check completes.
