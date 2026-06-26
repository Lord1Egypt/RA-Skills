---
name: skill-fleet-monitor
version: 1.1.3
description: Scans all installed skills for version drift and delisted publishers. Free taster — full 6-check fleet health report in the ClawHub Ops Pack.
author: ordo-tech
tags: [security, audit, fleet, skills, monitoring, permissions, heartbeat]
requires:
  env: []
  tools: [read, web_fetch, web_search]
---

## What this skill does

Audits all installed skills and surfaces anything that needs attention.

**Checks included (free version):**
- ✅ Version drift — which installed skills have updates available
- ✅ Delisted skills — any installed skill removed from ClawHub (returns 404)

**Not included (full version — Ops Pack):**
- Publisher standing checks (suspended/banned authors)
- Security advisory cross-reference
- Permission relevance audit (tools vs. stated purpose)
- Known bad pattern detection (prompt injection, exfil patterns, identity spoofing)
- Automated report saved to workspace audit trail
- Heartbeat/cron integration with Telegram alerting

Get the full 6-check fleet scan → **[ClawHub Ops Pack](https://theagentgordo.gumroad.com/)**

---

## When to use it

- After installing new skills, to establish a baseline
- Monthly hygiene check
- After a security advisory or incident

---

## Usage

> "Run a fleet health check on my installed skills"
> "Which of my skills need updating?"
> "Are any of my installed skills delisted?"

---

## Output format

```
🛡️ Fleet Health Report (Free — 2/6 checks) — [Date]

Installed skills audited: N

✅ skill-name v1.0.0 — Up to date
⚠️ skill-name v0.9.0 — Update available (v1.1.0)
🚨 skill-name v1.0.0 — DELISTED (ClawHub returns 404)

---
*Full 6-check scan: https://theagentgordo.gumroad.com/*
```

---

## Requirements

- `read` — to inventory installed skill directories
- `web_fetch` — to check ClawHub for current versions
- `web_search` — to check publisher standing (full version)
- No API keys required

## Support

https://clawhub.com/@ordo-tech | Full Ops Pack: https://theagentgordo.gumroad.com/
