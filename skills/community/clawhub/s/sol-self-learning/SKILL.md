---
name: openclaw-self-learning-skill
description: Persistent memory and self-improvement for AI agents — writes and refines its own memory files over time.
version: 1.0.0
author: TheSolAI
permissions: ["file.read", "file.write"]
---

# Self-Learning Skill

Gives any AI agent persistent memory and self-improvement. The agent writes and refines its own memory files — capturing failures, extracting patterns, generating fixes, and validating them before committing.

## Triggers

Use when:
- Starting a new session with the agent
- After a task fails or produces unexpected output
- When the agent makes the same mistake twice
- Regular review of memory files for stale or incorrect entries
- Improving the agent's performance based on past experience

## How It Works

The self-learning loop:

1. **Capture** — After each session or failure, log: what was attempted, what went wrong, system state
2. **Analyse** — Identify the root cause pattern, not just the symptom
3. **Generate** — Create a fix or prevention rule based on the pattern
4. **Validate** — Test the fix before committing it to memory
5. **Commit** — Update the agent's memory files only when validation succeeds

## Files Created

- `~/.openclaw/workspace/memory/failures/` — Log of failed tasks with full context
- `~/.openclaw/workspace/memory/lessons/` — Generated fixes and prevention rules
- `~/.openclaw/workspace/MEMORY.md` — Consolidated memory (auto-updated on commit)

## What Gets Captured

- **Task failures** — What the agent tried, why it failed, what it would do differently
- **User corrections** — Explicit feedback that changes how the agent approaches tasks
- **Error patterns** — Repeated mistakes suggesting a systematic fix is needed
- **Preference shifts** — Changes in user requirements that should update future behaviour

## Why File-Based

No external dependencies — just the filesystem. Zero latency, full transparency, human-readable. The agent doesn't just store facts — it stores *actionable lessons*.

## Installation

```bash
openclaw skills install https://github.com/TheSolAI/openclaw-self-learning-skill
```
