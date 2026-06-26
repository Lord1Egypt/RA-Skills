---
name: verified-capability-evolver
description: "Injects a verified capability evolution reminder during agent bootstrap"
metadata: {"openclaw":{"emoji":"🧠","events":["agent:bootstrap"]}}
---

# Verified Capability Evolver Hook

Injects a reminder to capture learnings and require verification before promotion.

## What It Does

- Fires on `agent:bootstrap` (before workspace files are injected)
- Adds a reminder block to check `.learnings/` for relevant entries
- Prompts the agent to log corrections, errors, and discoveries
- Reminds the agent that permanent behavior changes require verification before promotion

## Configuration

No configuration needed. Enable with:

```bash
openclaw hooks enable verified-capability-evolver
```
