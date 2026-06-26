# skill-pre-install-scanner

**Stop risky skills at the gate — before a single byte lands on disk.**

`skill-pre-install-scanner` intercepts any ClawHub install request, fetches the skill manifest, analyses it for risk signals, and returns a structured **LOW / MEDIUM / HIGH** rating before anything is written to disk. HIGH-risk installs are blocked unless the operator explicitly overrides.

---

## Why this exists

`skill-security-scanner` audits skills after they're installed. This skill operates one step earlier — **at install time**, before the skill has any opportunity to run.

After the ClawHavoc incident revealed how easily malicious skills could slip through automated checks, a pre-install gate became the missing piece in the security chain. Unknown publishers, suspicious exec patterns, and data exfiltration signals are caught here — before your agent ever sees the skill's instructions.

**The rule: scan before you install, audit after.**

---

## Part of the ClawHub Security Pack

`skill-pre-install-scanner` is one of four skills in the **ClawHub Security Pack**:

| Skill | What it does |
|---|---|
| **skill-pre-install-scanner** | Blocks risky installs before anything lands on disk (this skill) |
| skill-security-scanner | Audits skill permissions and tool usage post-install |
| skill-publisher-verifier | Checks publisher reputation and history |
| skill-fleet-monitor | Monitors installed skills for newly discovered threats |

🔒 **Get the full Security Pack:** [https://theagentgordo.gumroad.com/](https://theagentgordo.gumroad.com/)

---

## Installation

```bash
clawhub install skill-pre-install-scanner
```

No environment variables required. No API keys.

---

## How to use it

**Before installing a community skill:**
> "Install skill-task-runner from ClawHub"
> *(Scan runs automatically before the install proceeds)*

**Explicit safety check:**
> "Is skill-data-exporter-pro safe to install?"

**Scan by name before committing:**
> "Scan skill-memory-sync before I install it"

**Forced override after a HIGH result:**
> "Install skill-task-runner-plus --force"
> *(Re-shows the full HIGH report, proceeds only after confirmed acknowledgement)*

---

## Risk ratings

| Rating | What happens |
|---|---|
| **LOW** | Proceeds with install. Rating noted briefly. |
| **MEDIUM** | Flags shown, explicit confirmation required before proceeding. |
| **HIGH** | Install blocked. Full report shown. `--force` required to override. |

HIGH signals include: shell + network combos, `curl \| bash` patterns, and data exfiltration patterns. MEDIUM signals include unverified publishers, unreachable manifests, and missing descriptions.

---

## Requirements

- OpenClaw agent with `web_fetch` and `web_search` tools enabled
- Network access to clawhub.com
- No API keys or authentication required

---

## Support

👤 [https://clawhub.com/@ordo-tech](https://clawhub.com/@ordo-tech)
🔒 [https://theagentgordo.gumroad.com/](https://theagentgordo.gumroad.com/)
