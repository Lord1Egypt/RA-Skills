# skill-fleet-monitor

> **Ongoing security re-auditing for all your installed OpenClaw skills.**

Most agents install a skill once and never look at it again. But skills change. Publishers get compromised. New attack patterns emerge. `skill-fleet-monitor` watches your whole skill fleet continuously and tells you when something needs your attention.

---

## What it checks

On each run, it audits every installed skill for:

- **Version drift** — is the installed version behind what's currently published?
- **Publisher standing** — has the publisher been flagged, suspended, or banned since install?
- **Security advisories** — does any published ClawHub advisory cover this skill or version? (If the advisory feed is unavailable, this check is skipped and noted in the report rather than failing the run.)
- **Known bad patterns** — exfiltration hooks, prompt injection, hidden obfuscation, core file tampering
- **Excessive permissions** — declared tools or env vars that are obviously disproportionate to the skill's description and stated purpose

Every run produces a fleet health report with three status levels: ✅ Clean, ⚠️ Review Recommended, 🚨 Action Required.

---

## Part of the ClawHub Security Pack

| Skill | What it does |
|---|---|
| skill-security-scanner | Scans individual skills at install time |
| skill-publisher-verifier | Verifies publisher reputation |
| skill-diff-auditor | Diffs skill versions before updates |
| **skill-fleet-monitor** | Ongoing fleet-wide re-audit (this skill) |

Use them together for defense in depth across the full skill lifecycle.

🔒 **Get the full Security Pack:** [theagentgordo.gumroad.com](https://theagentgordo.gumroad.com/)

---

## Installation

```bash
clawhub install skill-fleet-monitor
```

No API keys required. No env vars. Works on publicly accessible ClawHub data only.

---

## How to use it

**On demand:**
> "Run a fleet audit on all my installed skills."

**Via heartbeat (recommended):** Add to `HEARTBEAT.md`:
```
- Run skill-fleet-monitor and surface any ⚠️ or 🚨 items.
```

Reports are written to `memory/fleet-monitor-YYYY-MM-DD.md` for audit trail purposes. Critical findings are surfaced immediately without waiting for the next scheduled check.

---

## Requirements

- OpenClaw agent with `read`, `web_fetch`, and `web_search` tools enabled
- No API keys or authentication required

---

## Support

- ClawHub: [clawhub.com/@ordo-tech](https://clawhub.com/@ordo-tech)
- Full Security Pack: [theagentgordo.gumroad.com](https://theagentgordo.gumroad.com/)
