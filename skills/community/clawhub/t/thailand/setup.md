# Setup - Thailand Guide

Read this when `~/thailand/` is missing or empty.
Keep first-use setup short and practical.

## First Activation Priorities

1. Answer the immediate Thailand question first.
2. Confirm whether this skill should auto-activate for Thailand travel or relocation topics.
3. Capture only the minimum context needed to improve recommendations.

## Initial Questions (Natural, Not a Form)

- Is this a short trip, scouting trip, or relocation move?
- Which region is most likely: Bangkok, Chiang Mai, Phuket, islands, or undecided?
- What timeline matters: this month, next season, or long-term planning?
- Is the user optimizing for low cost, comfort, family needs, or work opportunities?
- Any constraints: visa class, mobility limits, health needs, schooling, or remote work requirements?

## Local Memory Initialization

If approved by the user context, initialize local memory:

```bash
mkdir -p ~/thailand
touch ~/thailand/memory.md
chmod 700 ~/thailand
chmod 600 ~/thailand/memory.md
```

If `~/thailand/memory.md` is empty, initialize it from `memory-template.md`.

## Returning Users

- Read `~/thailand/memory.md` silently.
- Reuse known priorities and constraints.
- Ask only what changed since last conversation.
- Update memory with new region, date, budget, and risk changes.

## Guardrails

- Do not claim visa certainty without telling the user what official source to re-check.
- Do not provide fixed budgets without a range and season context.
- Do not recommend risky mobility patterns without safety caveats.
