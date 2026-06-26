---
name: workflow-guardian-on-violation
description: Fires immediately on any rule violation. Writes violation entry, enforces gate or advisory, updates memory and soul.
---

# On-Violation Hook

## Trigger
Any hard or soft rule broken during workflow execution.

---

## Step 1 — Classify

```
Hard violation (hard-do / hard-dont / gate failed)?
  → STOP current step
  → Surface immediately: [GATE BLOCKED] workflow: <id> | rule: <id> | detail: <what>
  → Wait for owner resolution

Soft violation (soft-do / soft-dont / advisory)?
  → Log and continue
  → Surface as warning: [ADVISORY] workflow: <id> | rule: <id> | detail: <what>
```

---

## Step 2 — Write Violation Entry

Write minimum viable to `violations/raw/<slug>/entry.md` IMMEDIATELY:

```markdown
# <YYYY-MM-DD-workflow-id-rule-id>

## Meta
- Workflow:   <workflow-id>
- Rule:       <rule-id>
- Rule type:  hard-do | hard-dont | soft-do | soft-dont | gate | checkpoint
- Severity:   hard | soft
- Status:     raw
- Captured:   YYYY-MM-DD HH:MM IST

## What Happened
[One sentence — exactly what rule was broken]

## Context
[What step was executing when it happened]

## Impact
[What is blocked or degraded as a result]

## Post-Fix Required
[yes — what needs to be corrected | no — advisory only]
```

---

## Step 3 — Update Run Log

```
YYYY-MM-DD HH:MM | VIOLATION: <rule-id> | severity: hard/soft | slug: <slug>
```

---

## Step 4 — Update Memory + Soul

- Append to `memory/index.json` violations array
- Append to soul `[RECENT VIOLATIONS]`
- If pattern detected (same rule 3+ times) → upsert soul `[VIOLATION PATTERNS]`
- Update `STATS.md`
