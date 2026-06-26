---
name: self-improving-engineering
description: "Injects engineering self-improvement reminder during agent bootstrap"
metadata: {"openclaw":{"emoji":"🏗️","events":["agent:bootstrap"]}}
---

# Self-Improving Engineering Hook

Injects a reminder to evaluate engineering learnings during agent bootstrap.

## What It Does

- Fires on `agent:bootstrap` (before workspace files are injected)
- Adds a reminder block to check `.learnings/` for engineering-relevant entries
- Prompts the agent to log architecture decisions, build failures, test gaps, and performance regressions

## Configuration

No configuration needed. Enable with:

```bash
openclaw hooks enable self-improving-engineering
```
