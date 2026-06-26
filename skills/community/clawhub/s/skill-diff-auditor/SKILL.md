---
name: skill-diff-auditor
version: 1.1.0
description: Audits what changed between your installed skill and a pending update — flags new tool requests and risk changes before you approve. Free taster. Full audit in the ClawHub Ops Pack.
author: ordo-tech
tags: [security, auditing, skills, updates, diff, clawhub, safety]
requires:
  env: []
  tools: [read, web_fetch]
---

## What this skill does

Before updating an installed skill, this skill compares the installed version with the new one and flags what changed.

**Included (free version):**
- ✅ New tools requested (e.g. `exec`, `write` added in the update)
- ✅ Overall risk direction (increased / decreased / unchanged)
- ✅ Plain-English verdict: Safe to update / Update with caution / Do not update

**Not included (full version — Ops Pack):**
- Full instruction diff (plain-English summary of logic changes)
- New external endpoints and domains introduced
- Detailed risk rationale per change
- Batch audit across all pending updates

Get the full diff audit → **[ClawHub Ops Pack](https://theagentgordo.gumroad.com/l/clawhub-ops-pack)**

---

## When to use it

- Before running `clawhub update <skill-name>`
- When a skill update notification arrives and you want to know what's changing
- In production environments where skill changes need review before deployment

---

## Usage

> "Audit the update for skill-weather before I apply it"
> "Check what changed in skill-gh-issues v2.0.0"

The agent:
1. Reads the installed SKILL.md
2. Fetches the new version from ClawHub
3. Compares tool lists and risk posture
4. Returns a verdict

---

## Report format

```
## Skill Diff Audit (Free): <skill-name>
Installed: x.y.z → Available: a.b.c

### Verdict
[Safe to update | Update with caution | Do not update]
Reason: <one line>

### New tools requested
<list, or "None">

### Risk profile
[Increased | Decreased | Unchanged]

---
*Full diff audit (instruction changes + new endpoints): https://theagentgordo.gumroad.com/l/clawhub-ops-pack*
```

---

## Requirements

- `read` — to access installed SKILL.md
- `web_fetch` — to retrieve the new version from ClawHub
- No API keys required

## Support

https://clawhub.com/@ordo-tech | Full Ops Pack: https://theagentgordo.gumroad.com/l/clawhub-ops-pack
