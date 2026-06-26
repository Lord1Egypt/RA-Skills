---
name: skill-auto-router
description: Automatically discover and route relevant installed skills for the current task, plus run a daily skill audit. Use when you want pre-task skill matching across installed skills, heartbeat-based daily relevance checks, or help wiring "auto-skill selection" into AGENTS/HEARTBEAT workflows.
---

# Skill Auto Router

Run a lightweight preflight before non-trivial work so the agent loads the right skills instead of guessing.

## Quick Start

### 1) Pre-task routing (before work starts)

```bash
python scripts/skill_router.py --task "<user task text>"
```

This returns ranked skill candidates with match reasons.

### 2) Daily audit (once per day)

```bash
python scripts/skill_router.py --daily
```

This reports:
- discovered skill count
- duplicate/overlapping trigger language
- weak or vague descriptions that reduce trigger quality

## Recommended Integration

To make this behavior automatic, wire it into your workspace steering:

1. In `AGENTS.md` pre-task checklist: run pre-task routing for non-trivial tasks.
2. In `HEARTBEAT.md`: run `--daily` once per day and log result.

Use `references/setup-checklist.md` for copy/paste snippets.

## Operating Rules

- Prefer top 1-3 matching skills only (avoid loading everything).
- If no good match is found, continue without skill load.
- If multiple matches tie, choose the most specific skill description.
- Never claim a skill was loaded unless it actually was.

## scripts/

- `scripts/skill_router.py` — deterministic local matcher + daily audit

## references/

- `references/setup-checklist.md` — integration snippets for AGENTS/HEARTBEAT
