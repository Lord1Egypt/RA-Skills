---
name: self-improvement
description: Self-learning system — checks pending learnings, writes session context, and tracks patterns at gateway startup
metadata:
  openclaw:
    emoji: "🧠"
    events: ["gateway:startup"]
---

# Self-Improvement Gateway Hook

Runs at gateway startup. Writes actionable context to `memory/.hook-context.txt` for the agent to read at session start.

## What It Does

- Checks `.learning-trail.json` for pending high-priority items
- Checks for overdue verifications
- Detects patterns ready for promotion (≥2 occurrences)
- Checks if recent session summaries exist
- Writes findings to `memory/.hook-context.txt`

## Agent Usage

At session start, the agent should:
```bash
cat memory/.hook-context.txt
```

This file is regenerated at each gateway startup and contains the current state of the learning system.

## Installation

The hook is auto-installed by OpenClaw when the skill is enabled.
