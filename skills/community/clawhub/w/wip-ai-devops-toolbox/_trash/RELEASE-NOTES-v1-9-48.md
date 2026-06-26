# Release Notes: wip-ai-devops-toolbox v1.9.48

**Document wip-repos claude command in SKILL.md and TECHNICAL.md.**

## What changed

- SKILL.md: added `wip-repos claude` commands to the wip-repos section
- TECHNICAL.md: full documentation of how the ecosystem generator works, template locations, delimiter convention

## Why

v1.9.47 shipped the `wip-repos claude` command without updating technical docs. Now documented.

## Issues closed

- #212 (docs portion)

## How to verify

```bash
grep "wip-repos claude" SKILL.md TECHNICAL.md
```
