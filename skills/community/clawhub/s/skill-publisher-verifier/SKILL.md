---
name: skill-publisher-verifier
version: 1.1.1
description: Check a ClawHub publisher's trust score before installing their skill. Returns TRUSTED, ESTABLISHED, NEW, or FLAGGED based on public signals. Free taster — full signal set in the ClawHub Security Pack.
author: ordo-tech
tags: [security, verification, trust, publishers, marketplace, clawhub, pre-install]
requires:
  env: []
  tools: [web_fetch, web_search]
---

## What this skill does

Before installing a skill, check who published it. This skill fetches the publisher's public ClawHub profile and returns a trust score with a plain-English summary.

**Signals included (free version):**
- ✅ Skills published (catalogue size)
- ✅ Account age
- ✅ Flagged or deleted skills

**Not included (full version — Security Pack):**
- Total install volume across catalogue
- Stars and community endorsement signals
- External flag detection (forum reports, ClawHavoc-era incidents)
- Known associations with banned publishers
- Automated cross-referencing with co-author/fork relationships

Get the full signal set → **[ClawHub Security Pack](https://theagentgordo.gumroad.com/l/clawhub-security-pack)**

---

## Trust scores

| Score | Meaning |
|-------|---------|
| **TRUSTED** | Strong catalogue, long track record, no flags |
| **ESTABLISHED** | Active author, reasonable history |
| **NEW** | Recent account or thin catalogue — proceed with caution |
| **FLAGGED** | Known flags, deleted skills, or suspicious activity |

---

## Usage

> "Check @rapid-skills-99 before I install their skill"
> "Verify the publisher of clawhub.com/skills/some-skill"
> "Is @ordo-tech safe to install from?"

## Output format

```
Publisher: @{handle}
Trust Score: TRUSTED | ESTABLISHED | NEW | FLAGGED

Signals (free — 3/7):
- Skills published: {n}
- Flagged/deleted skills: {n}
- Account age: {n} months

Summary: {1–2 sentence verdict}
Recommendation: Install / Install with caution / Do not install

---
*Full 7-signal check: https://theagentgordo.gumroad.com/l/clawhub-security-pack*
```

---

## Requirements

- `web_fetch` — to retrieve publisher profile from clawhub.com
- `web_search` — secondary check for external flags
- No API keys required. Uses public profile data only.

## Support

https://clawhub.com/@ordo-tech | Full Security Pack: https://theagentgordo.gumroad.com/l/clawhub-security-pack
