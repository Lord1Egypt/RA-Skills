---
name: learning-capture
description: Capture user corrections, failed tool runs, recurring gotchas, and useful lessons as short structured notes. Use when a mistake or workflow learning should be remembered for future work. Keep entries redacted, human-reviewable, and project-scoped. Do not change agent rules or configuration without explicit user approval.
---

# Learning Capture

Use this skill to turn mistakes and corrections into small reusable notes.

The goal is simple: if the same issue appears again, the agent can check the note before repeating the mistake.

## Core Rules

- Write short notes, not raw transcripts.
- Redact credentials, auth tokens, private messages, customer data, and full command output.
- Prefer project-scoped `.learnings/` files.
- Do not edit `AGENTS.md`, `SOUL.md`, `CLAUDE.md`, hooks, or config unless the user explicitly approves.
- Treat every promotion to long-term instructions as a proposal first.

## When To Use

| Situation | Action |
|---|---|
| User corrects the agent | Add a correction note |
| Tool/command fails unexpectedly | Add an error note with redacted summary |
| A project gotcha is discovered | Add a learning note |
| Same issue repeats | Link the related notes and propose a durable rule |
| User requests a missing capability | Add a feature-request note |

## Setup

Create these files in the project root if they do not exist:

```text
.learnings/LEARNINGS.md
.learnings/ERRORS.md
.learnings/FEATURE_REQUESTS.md
```

Use normal file-writing tools. Never overwrite existing notes.

## Learning Note Format

```markdown
## LRN-YYYYMMDD-001 — short-title

**Logged:** ISO timestamp
**Priority:** low | medium | high
**Status:** pending | resolved | proposed
**Area:** frontend | backend | infra | tests | docs | workflow

### Summary
One sentence.

### What happened
Short redacted context.

### Better next time
Concrete behavior to apply in future.

### Tags
- tag-one
- tag-two
```

## Error Note Format

```markdown
## ERR-YYYYMMDD-001 — short-title

**Logged:** ISO timestamp
**Priority:** low | medium | high
**Status:** pending | resolved

### Summary
What failed, in one sentence.

### Redacted Evidence
Minimal safe excerpt. No credentials, tokens, private data, or full logs.

### Likely Cause
If known.

### Fix / Next Step
Concrete action.
```

## Feature Request Format

```markdown
## FEAT-YYYYMMDD-001 — short-title

**Logged:** ISO timestamp
**Status:** proposed

### Requested Capability
What the user wanted.

### Why It Matters
What problem it solves.

### Possible Implementation
Short option list, if useful.
```

## Promotion Rule

If a note is broadly useful:

1. Propose the distilled rule to the user.
2. Wait for approval.
3. Only then update durable project or agent instructions.
4. Mark the original note as `proposed` or `resolved` with a link to the approved location.

## Output

When done, respond briefly:

```text
Logged: .learnings/LEARNINGS.md#LRN-YYYYMMDD-001
```

If no durable learning exists, do nothing.
