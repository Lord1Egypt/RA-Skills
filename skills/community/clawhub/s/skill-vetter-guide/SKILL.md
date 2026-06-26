---
name: skill-vetter-guide
description: "Guide for vetting third-party OpenClaw skills before installation using the Skill Vetter security protocol. Use when installing any third-party skill, auditing existing skills, enforcing vet-before-install SOP, performing periodic security audits of installed skills, or setting up Skill Vetter on a new OpenClaw instance. Triggers on: install a skill, vet this skill, audit skills, skill security, review skill safety, set up skill vetter, skills security audit."
---

# Skill Vetter Guide

Security-first protocol for vetting third-party OpenClaw skills before installation.

**Core rule: Never install a skill without vetting it first.**

## Install Skill Vetter

Install to the user-global skills directory so all agents can use it:

```
~/.agents/skills/skill-vetter/
```

Source: `useai-pro/openclaw-skills-security@skill-vetter` on ClawHub, or the equivalent GitHub repo.

After installation, verify:
1. Confirm `~/.agents/skills/skill-vetter/SKILL.md` exists and is complete
2. Check the skill appears in the agent's available skills list

## Vetting SOP

When asked to install any third-party skill, follow this flow:

```
Discover skill → Fetch source → Review ALL files → Risk grade → Decide → Install & document
```

### 1. Check Source Metadata

- Origin (ClawHub / GitHub / personal share)
- Author, last update, stars/downloads, community feedback
- Clear purpose statement

### 2. Full Code Review (Mandatory)

Review **every file** in the skill, not just SKILL.md. Check for these red flags:

| Red Flag | Why It Matters |
|----------|---------------|
| `curl`/`wget` to unknown URLs | Data exfiltration |
| Sending data to external servers | Privacy leak |
| Requesting tokens/API keys/credentials | Credential theft |
| Reading `~/.ssh`, `~/.aws`, `~/.config` | Sensitive directory access |
| Reading `MEMORY.md`, `USER.md`, `SOUL.md`, `IDENTITY.md`, `TOOLS.md`, `openclaw.config.json` | OpenClaw private file access |
| `base64` decode of opaque content | Obfuscation |
| `eval()`/`exec()` with external input | Code injection |
| Modifying files outside workspace | System tampering |
| Installing undeclared dependencies | Supply chain risk |
| IP address connections (not domains) | Evasion of DNS-based controls |
| Minified/obfuscated code blocks | Hidden behavior |
| `sudo`/elevated permissions | Privilege escalation |
| Accessing browser cookies/sessions | Session hijacking |

### 3. Assess Permissions Scope

Determine what the skill reads, writes, executes, and whether it needs network access. Verify permissions are minimal and match stated functionality.

### 4. Assign Risk Level

| Level | Meaning | Action |
|-------|---------|--------|
| 🟢 LOW | Local text/formatting/weather | Install after review |
| 🟡 MEDIUM | File ops, browser, third-party APIs | Install with caution |
| 🔴 HIGH | Credentials, system config, auto-send | **Human approval required** |
| ⛔ EXTREME | Root, security policy changes, broad sensitive reads | **Do not install** |

### 5. Output Vetting Report

Use the standard report format. See [references/report-template.md](references/report-template.md).

### 6. Document Installation

After installing, record: date, skill name, source, risk level, review summary, install path.
Write to `memory/YYYY-MM-DD.md` or a dedicated `security-audits/` directory.

## Periodic Audit

Audit all installed third-party skills under `~/.agents/skills/` periodically:
- Quick scan every 4 hours (automated via cron)
- Full re-review weekly or monthly (human-assisted)

For each skill, check for new suspicious files, changed code, or newly introduced red flags.
Output status per skill: ✅ Normal / ⚠️ Needs attention / ❌ Problematic.

Write results to timestamped files: `security-audits/skills-audit-YYYY-MM-DD_HHMM.md`.
See [references/audit-template.md](references/audit-template.md) for the audit file format.

## AGENTS.md Enforcement

Add this rule to `AGENTS.md` to make vetting mandatory for all agents:

```markdown
## Skill Security Rule

All third-party skills must be vetted with Skill Vetter before installation. No exceptions.

- Review ALL files, not just SKILL.md
- Check for: outbound network calls, sensitive file access, obfuscated code, eval/exec, credential requests, elevated permissions
- Output a standardized vetting report
- HIGH / EXTREME risk requires human approval
- Skills that fail vetting must not be installed
```

## Prompt Templates

Ready-to-use prompts for common operations. See [references/prompt-templates.md](references/prompt-templates.md).

## Multi-Instance Environments

When managing multiple OpenClaw instances:
- Vet skills independently per machine
- Record installed versions per host
- Do not assume "safe on A = safe on B"
- Leave audit trails when syncing or upgrading skills across hosts
