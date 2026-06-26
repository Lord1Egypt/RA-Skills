---
name: skill-onboarder
description: Auto-wires new skills into core system. On skill install detected, reads SKILL.md/AGENT.md/SOUL.md/hooks and injects into soul/memory/agent files.
version: 1.1.0
trigger: "installed|new skill|onboard|wire skill|onboarding|skill wired"
homepage: https://github.com/clawhub/skill-onboarder
metadata: {"openclaw": {"skillKey": "skill-onboard", "emoji": "🔧", "always": true, "requires": {"bins": []}, "triggers": [{"kind": "event", "event": "skill:post-install", "future": true}]}}
---

# Skill Onboarder

## Purpose

Auto-wire new skills. On trigger, reads skill files → wires to core system.

## Trigger

Matches: "installed", "new skill", "onboard", "wire skill", "onboarding"

Future: Auto-fires on `skill:post-install` event (not yet implemented)

## Files Written

| File | Adds |
|------|------|
| `soul/master.md` | Skill sections |
| `agent/skills-active.md` | Triggers + rules |
| `workspace/_index.md` | Registration |

## Process

1. Detect trigger → extract skill name
2. Read: SKILL.md, AGENT.md, SOUL.md, hooks/
3. Extract: triggers, rules (hard/soft), sections
4. Inject to core files
5. Confirm

## Idempotent

Safe to re-run. Checks before write. Updates version if changed.