---
name: skill-vetter-v2
description: "Injects a reminder to vet packaged skills before trusting or installing them"
metadata: {"openclaw":{"emoji":"🛡️","events":["agent:bootstrap"]}}
---

# Skill Vetter v2 Hook

Injects a reminder to review the full skill package and keep verdict decisions local.

## What It Does

- Fires on `agent:bootstrap`
- Adds a reminder to inspect the whole package, not just `SKILL.md`
- Prompts the agent to classify install-time risk, runtime risk, and trust dependency
- Reminds the agent that optional verification applies only to the final report
