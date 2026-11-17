---
name: skill-trust-auditor
description: Audit a named ClawHub skill or skill URL before installation by combining OpenClaw verification with bounded static analysis. Use when the user explicitly asks whether a skill is safe or requests a pre-install review; report evidence and uncertainty instead of treating a score as proof.
metadata:
  openclaw:
    version: "1.1.5"
    emoji: "🛡️"
    homepage: https://clawhub.ai/jonathanjing/skill-trust-auditor
    requires:
      bins: [python3]
    envVars:
      - name: ANTHROPIC_API_KEY
        required: false
        description: Optional LLM judge credential for ambiguous findings.
---

# Skill Trust Auditor

Audit any ClawHub skill for security risks before installation.

## 🛠️ Installation

### 1. Ask OpenClaw (Recommended)
Tell OpenClaw: *"Install @jonathanjing/skill-trust-auditor."*

### 2. Manual Installation (CLI)
If you prefer the terminal, run:
```bash
openclaw skills install @jonathanjing/skill-trust-auditor
```

## Setup (first run only)

```bash
bash "{baseDir}/scripts/setup.sh"
```

## Audit a Skill

First request the registry trust envelope:

```bash
openclaw skills verify @owner/skill --json
```

Then run bounded local analysis when the user asks for a deeper audit:

```bash
bash "{baseDir}/scripts/audit.sh" [skill-name-or-url]
# Example:
bash "{baseDir}/scripts/audit.sh" steipete/clawhub
bash "{baseDir}/scripts/audit.sh" https://clawhub.ai/someuser/someskill
```

Output:
```json
{
  "skill": "someuser/someskill",
  "trust_score": 72,
  "verdict": "INSTALL WITH CAUTION",
  "risks": [
    {"level": "HIGH", "pattern": "curl to external domain", "location": "scripts/sync.sh:14"},
    {"level": "MEDIUM", "pattern": "reads MEMORY.md", "location": "SKILL.md:23"}
  ],
  "safe_patterns": ["no env var access", "no self-modification"],
  "author_verified": false,
  "recommendation": "Review scripts/sync.sh:14 before installing. The external curl call could exfiltrate data."
}
```

Post to user with clear summary:
```
🛡️ Trust Audit: someuser/someskill
Score: 72/100 — ⚠️ INSTALL WITH CAUTION

🔴 HIGH: curl to unknown domain in scripts/sync.sh:14
🟡 MEDIUM: reads your MEMORY.md

Recommendation: Inspect line 14 of sync.sh before proceeding.
Inspect the exact version's Files tab or installed folder before proceeding.
```

## Trust Score Guide

| Score | Verdict | Action |
|-------|---------|--------|
| 90-100 | ✅ SAFE | Install freely |
| 70-89 | ⚠️ CAUTION | Review flagged items first |
| 50-69 | 🟠 RISKY | Only if you understand the risks |
| 0-49 | 🔴 DO NOT INSTALL | High probability of malicious intent |

## Risk Pattern Reference

**HIGH RISK** (-30 each):
- `process.env` access in scripts
- `curl`/`wget` to non-standard domains
- Reading `~/.config` or `~/.openclaw` directly
- `exec()` with user-controlled input
- Instructions to modify `SOUL.md`/`AGENTS.md`/`openclaw.json`

**MEDIUM RISK** (-10 each):
- Any outbound API calls (even to known services)
- File writes outside workspace
- Reading `MEMORY.md` or diary files

**LOW RISK** (-3 each):
- `web_fetch` to standard domains
- Read-only file access in workspace

Do not auto-install from an audit score. Present findings, the registry decision, and the exact install reference; let the user authorize installation separately.

## ClawHavoc Pattern Reference

See `{baseDir}/references/clawhavoc-patterns.md` for known malicious patterns. Treat it as a heuristic reference, not a complete malware signature set.
