---
name: session-observer
description: Observe OpenClaw session usage, token consumption, context pressure, and model/runtime state. Use when the user asks about token usage, context size, model in use, cache behavior, session health, or wants a lightweight status summary with practical next actions.
---

# Session Observer

## Overview

Inspect OpenClaw session state with minimal disruption. Prefer `session_status` first, then summarize token usage, context pressure, cache ratio, model/runtime details, and any obvious follow-up actions.

## Workflow

### 1. Start with session status

Use `session_status` first when the user asks about:
- token usage
- model in use
- context usage
- cache hit rate
- premium/chat budget remaining
- session health

If the user refers to another session, target that session explicitly.

### 2. Extract the practical signals

Report the fields most useful to the user:
- current model
- input/output token counts
- context used and total context window
- cache hit ratio
- budget or usage percentage when available
- runtime mode and whether reasoning is enabled

Do not dump raw status cards unless the user asks.

### 3. Interpret, do not just repeat

Classify the situation:
- **healthy**: low or moderate context pressure, no obvious issues
- **watch**: context is growing, cache low, or usage notably climbing
- **high pressure**: context is large enough that compaction, a new thread, or cleanup may help

### 4. Recommend the smallest next step

Examples:
- continue as-is
- start a fresh thread for a new topic
- reduce unnecessary logs or verbose outputs
- use a sub-agent for a large parallel task
- check a specific session if the user suspects cost spikes

## Output format

Use:
- **Current state**
- **What it means**
- **Recommended next step**

Keep it short unless the user asks for detail.

## Safety rules

- Do not invent cost numbers not shown by the tool.
- If a field is unavailable, say unavailable.
- Prefer `session_status` over guesswork.
