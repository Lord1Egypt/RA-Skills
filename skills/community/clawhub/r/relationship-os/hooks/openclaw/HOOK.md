---
name: relationship-os
description: "Injects relationship context during agent bootstrap for the Relationship OS skill"
metadata: {"openclaw":{"emoji":"💜","events":["agent:bootstrap"]}}
---

# Relationship OS Hook

Injects a relationship context summary (~150 tokens) at the start of each agent session, so the agent knows the current relationship state.

## Injected Content

- Current relationship stage and interaction count
- Pending open threads awaiting follow-up
- Active shared goals
- Agent stance reminders
- Recent milestones

## Events

- `agent:bootstrap` — Adds the relationship context virtual file before workspace file injection

## Configuration

No additional configuration needed. Automatically enabled once the skill is installed.
