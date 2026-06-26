---
name: self-optimization
description: "Injects a self-optimization reminder during agent bootstrap"
metadata: {"openclaw":{"emoji":"🧠","events":["agent:bootstrap"]}}
---

# Self-Optimization Hook

Injects a lightweight bootstrap reminder so the agent remembers to convert work into reusable improvements.

## What It Does

- Fires on `agent:bootstrap`
- Adds a virtual reminder file before workspace prompt files load
- Skips sub-agent sessions to avoid noisy duplication
- Nudges the agent to capture, link, promote, and extract useful patterns

## Enable

```bash
openclaw hooks enable self-optimization
```
