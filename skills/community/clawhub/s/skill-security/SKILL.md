---
name: skill-security
description: >
  Security audit tool for OpenClaw skills. Scans for credential harvesting, code injection,
  network exfiltration, obfuscation. ALWAYS run before installing any new skill from external
  sources. Triggers on: new skill installation, skill audit, security scan, skill review,
  before loading external skill.
---

# Skill Security Scanner

Security audit tool for OpenClaw skills. **Run before installing any new skill.**

## Quick Audit

```bash
# Audit a skill directory
~/workspace/skills/skill-security/audit.sh /path/to/skill

# Audit all installed skills
~/workspace/skills/skill-security/audit-all.sh
```

## What It Checks

| Check | Risk Level | Pattern |
|-------|------------|---------|
| **Network Exfiltration** | 🚨 HIGH | `requests.`, `urllib`, `http.client`, `socket.`, `fetch(`, `axios` |
| **Credential Harvesting** | 🚨 HIGH | `.ssh/`, `.aws/`, `pass `, `keyring`, `credential`, `secret`, `token` file reads |
| **Code Injection** | 🚨 CRITICAL | `exec(`, `eval(`, `compile(`, `Function(`, `__import__` |
| **Obfuscation** | ⚠️ MEDIUM | `base64.decode`, `atob`, encoded payloads |
| **Env Dumping** | ⚠️ MEDIUM | `os.environ`, `process.env`, `getenv` bulk access |
| **Subprocess Abuse** | ⚠️ MEDIUM | `subprocess.run`, `os.system`, `child_process` with credentials |

## Severity Levels

- **CRITICAL** (🚨): Block installation, report to owner
- **HIGH** (🔴): Requires manual review before use
- **MEDIUM** (🟡): Note but allow if from trusted source
- **LOW** (🟢): Informational only

## Safe Skill Checklist

Before using any skill:

1. ✅ Is it from a trusted source? (official OpenClaw, known publisher)
2. ✅ Is the code readable (not obfuscated)?
3. ✅ Does it document why it needs network/credential access?
4. ✅ Does it scope file access to its own directory?
5. ✅ Has it been audited by the community?

## Integration with AGENTS.md

Add this to your workflow:

```markdown
## Skill Installation Protocol

Before loading any new skill:
1. Run `~/workspace/skills/skill-security/audit.sh <skill-path>`
2. If CRITICAL/HIGH findings → STOP, alert the user
3. If MEDIUM findings → Review manually, proceed if justified
4. If CLEAN → Safe to use
```

## Automatic Protection

The scanner creates a blocklist at `./blocklist.txt`.
Skills with CRITICAL findings are automatically added.

## Manual Override

If a skill is flagged but you've verified it's safe:

```bash
echo "skill-name:verified:YYYY-MM-DD:reason" >> allowlist.txt
```

---

## Premium Skills

Like this? Check out our premium skills at **[skillpacks.dev](https://skillpacks.dev)**:

- 🛡️ **Security Suite** — Full PII scanning, secrets detection, prompt injection defense — [$9.90](https://polycatai.gumroad.com/l/bsrugo)
- 🧠 **Structured Memory** — Three-tier memory replacing flat MEMORY.md — [$9.90](https://polycatai.gumroad.com/l/goawrg)
- 📋 **Planning & Execution** — Systematic task plans with batch execution — [$9.90](https://polycatai.gumroad.com/l/uydfto)
- 💎 **[Bundle — all 3 for $24.90](https://polycatai.gumroad.com/l/atsrl)**
