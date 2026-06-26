---
name: skill-pre-install-scanner
version: 1.1.0
description: Pre-install safety check for ClawHub skills — scans for the 3 highest-risk signals before anything lands on disk. Free taster. Full 10-signal scanner in the ClawHub Security Pack.
author: ordo-tech
tags: [security, pre-install, scanner, clawhub, safety, permissions]
requires:
  env: []
  tools: [web_fetch, web_search]
---

# Pre-Install Scanner (Free)

Intercept a `clawhub install` request and run a quick safety check — before anything is written to disk.

**Signals included (free version — 3 of 10):**

| Signal | Tier | What it catches |
|--------|------|----------------|
| `shell+network combo` | HIGH | `exec` + outbound network in same skill — classic exfil pattern |
| `hardcoded-external-url` | HIGH | Raw external URLs embedded in instructions |
| `unverified-publisher` | MEDIUM | Publisher has no verified badge on clawhub.com |

**Not included (full version — Security Pack):**
- Data exfiltration pattern detection
- Suspicious exec chain analysis (`curl | bash`, `base64 -d | bash`)
- Source unreachable handling
- Missing/vague description flag
- Excessive permissions check
- New publisher signal
- No changelog signal

Get all 10 signals → **[ClawHub Security Pack](https://theagentgordo.gumroad.com/)**

---

## When to run

- `"Install [skill-name] from ClawHub"` — runs automatically before install
- `"Is [skill-name] safe to install?"` — on-demand scan
- `"clawhub install [skill-name]"` — intercepts and scans first

## Output format

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 Pre-Install Scan (Free — 3/10 signals): <skill-name>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Publisher : <name> [verified / unverified]
Version   : <version>
Risk      : LOW | MEDIUM | HIGH

Flags:
  ⚠️  <signal>  — <one-line explanation>

Summary: <1–2 sentences>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

*Full 10-signal scan: https://theagentgordo.gumroad.com/*
```

## Actions by rating

| Rating | Action |
|--------|--------|
| LOW | Proceed with install |
| MEDIUM | Warn user, ask for confirmation |
| HIGH | Block install. Requires `--force` to override |

## Requirements

- `web_fetch` — to retrieve the SKILL.md from ClawHub
- `web_search` — to check publisher standing
- No API keys required

## Support

https://clawhub.com/@ordo-tech | Full pack: https://theagentgordo.gumroad.com/
