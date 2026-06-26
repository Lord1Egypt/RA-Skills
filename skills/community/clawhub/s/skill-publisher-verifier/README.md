# skill-publisher-verifier

**Know who you're installing from — before you install.**

`skill-publisher-verifier` checks a ClawHub publisher's reputation before you run their skill. It surfaces the signals that matter — catalogue history, install volume, flagged or deleted skills, community standing, and account age — and returns a clear trust score you can act on.

One command. Four possible verdicts: **TRUSTED / ESTABLISHED / NEW / FLAGGED**.

---

## Why this matters

After ClawHavoc, a cluster of suspicious skills were quietly deleted or hidden from ClawHub. Some of the publishers behind them created new accounts. This skill helps you spot those patterns before they become your problem.

**The rule is simple: verify the publisher, then install the skill.**

---

## Part of the ClawHub Security Pack

`skill-publisher-verifier` is one of four skills in the **ClawHub Security Pack**:

| Skill | What it does |
|---|---|
| **skill-publisher-verifier** | Checks publisher reputation before install (this skill) |
| skill-security-scanner | Audits skill permissions and tool usage |
| skill-diff-auditor | Reviews changes between skill versions |
| skill-fleet-monitor | Monitors installed skills for new threats |

🔒 **Get the full Security Pack:** [https://theagentgordo.gumroad.com/](https://theagentgordo.gumroad.com/)

---

## Installation

```bash
clawhub install skill-publisher-verifier
```

No environment variables required. No API keys. Works on public ClawHub profile data only.

---

## How to use it

**By publisher handle:**
> "Verify the publisher @rapid-skills-99 before I install anything from them."

**By skill URL:**
> "Check the publisher of https://clawhub.com/skills/auto-deployer-pro"

**By skill name:**
> "Who publishes `memory-exporter` and should I trust them?"

---

## Trust score guide

| Score | What it means |
|---|---|
| **TRUSTED** | Established author, high installs, no flags, long track record |
| **ESTABLISHED** | Active author, reasonable history, no significant concerns |
| **NEW** | Recently created or minimal catalogue — proceed with care |
| **FLAGGED** | Known flags, deleted skills, or suspicious associations — do not install |

---

## Requirements

- OpenClaw agent with `web_fetch` and `web_search` tools enabled
- Network access to clawhub.com
- No API keys or authentication required

---

## Support

👤 [https://clawhub.com/@ordo-tech](https://clawhub.com/@ordo-tech)
🔒 [https://theagentgordo.gumroad.com/](https://theagentgordo.gumroad.com/)
