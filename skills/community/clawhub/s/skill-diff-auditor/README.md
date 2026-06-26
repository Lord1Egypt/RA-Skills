# skill-diff-auditor

> Know exactly what changed — before you approve the update.

`skill-diff-auditor` audits the difference between your currently installed version of a skill and the new version available on ClawHub, before you approve the update.

It answers the questions you should always be asking:
- What instructions changed?
- Did this update request new tools I haven't reviewed?
- Are there new external domains I don't recognise?
- Is my agent's risk profile about to increase?

And it gives you a plain-English verdict: **Safe to update**, **Update with caution**, or **Do not update**.

---

## Why it matters

A malicious or poorly-reviewed skill update could request new tools like `exec` or `write`, route your agent's output to unrecognised endpoints, or silently expand what your agent is permitted to do. Most updates are safe — but you shouldn't have to take that on faith.

---

## Part of the ClawHub Security Pack

| Skill | What it does |
|---|---|
| skill-security-scanner | Audits skills at install time |
| skill-publisher-verifier | Verifies publisher reputation |
| **skill-diff-auditor** | Diffs skill versions before updates (this skill) |
| skill-fleet-monitor | Ongoing fleet-wide re-audit |

🔒 **Get the full Security Pack:** [theagentgordo.gumroad.com](https://theagentgordo.gumroad.com/)

---

## Installation

```bash
clawhub install skill-diff-auditor
```

No configuration required. No API keys.

---

## How to use it

> "Audit the update for skill-weather before I apply it."

> "Check what changed in skill-gh-issues between installed and latest."

> "Run a diff audit on skill-fleet-monitor — I got an update notification."

The agent reads the installed SKILL.md, fetches the latest from ClawHub, compares the two, and returns a structured audit report. **It never applies the update — it only reports.**

---

## Requirements

- OpenClaw agent with `read` and `web_fetch` tools available
- The skill being audited must be installed locally
- Internet connection to fetch the remote version from ClawHub

---

## Support

- ClawHub: [clawhub.com/@ordo-tech](https://clawhub.com/@ordo-tech)
- Full Security Pack: [theagentgordo.gumroad.com](https://theagentgordo.gumroad.com/)
