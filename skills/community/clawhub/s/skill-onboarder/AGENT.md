---
name: skill-onboarder-agent
description: Rules: On trigger, reads skill files → wires to core.
---

# Rules

## 1. Detect Trigger

Trigger on: "installed", "new skill", "onboard", "wire", "onboarding"

Extract skill name → begin onboarding.

## 2. Read Files

1. `<skill>/SKILL.md` — name, version, triggers
2. `<skill>/AGENT.md` — rules (hard/soft)
3. `<skill>/SOUL.md` — sections
4. `<skill>/hooks/*.md` — hooks

Missing → warn, continue.

## 3. Show Summary

```
EXTRACTION: <skill>
Sections: N
Rules: N hard, N soft
Hooks: N
```

Wait confirm → inject.

## 4. Write (Idempotent)

Check existing → skip if same version → update if diff → add if new.

## 5. Create Paths

From SKILL.md structure → mkdir -p missing paths.

## 6. Confirm

```
✓ <skill> wired
Sections: N | Rules: N hard/N soft
```