---
name: skill-onboarder-on-install
description: On trigger: read skill files → extract → inject → confirm.
---

# On-Install

## Read

| File | Extract |
|------|---------|
| SKILL.md | name, version, triggers |
| AGENT.md | rules (hard/soft) |
| SOUL.md | sections |
| hooks/*.md | hook names |

## Classify Rules

- Contains MUST/SHALL/ALWAYS/CANNOT → HARD
- Contains SHOULD/PREFER → SOFT
- Default → SOFT

## Inject

Writes to: soul/master.md, agent/skills-active.md, workspace/_index.md