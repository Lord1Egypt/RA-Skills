---
name: self-improving-conversation
description: "Injects conversation self-improvement reminder during agent bootstrap"
metadata: {"openclaw":{"emoji":"💬","events":["agent:bootstrap"]}}
---

# Conversation Self-Improvement Hook

Injects a reminder to evaluate dialogue learnings during agent bootstrap.

## What It Does

- Fires on `agent:bootstrap` (before workspace files are injected)
- Adds a reminder block to check `.learnings/` for conversation-related entries
- Prompts the agent to log tone mismatches, context losses, hallucinations, and escalation failures

## Configuration

No configuration needed. Enable with:

```bash
openclaw hooks enable self-improving-conversation
```
