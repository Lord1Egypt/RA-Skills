---
name: security-hardener
description: One-command OpenClaw security audit, scoring, and auto-remediation. Addresses CVE-2026-33579 and common misconfigurations. Scans for exposed API keys, weak file permissions, unauthenticated endpoints, unsafe plugin configs, insecure transport settings, and missing auth. Generates a 0-100 security score with severity-ranked findings and auto-fixes what it can. Use when asked to "harden my OpenClaw", "security audit", "am I secure", "fix my security", "security score", "check for exposed keys", "audit my agent", "CVE check", "lock down my instance", or when setting up a new OpenClaw installation and want to verify security posture before going live.
---

# Security Hardener

One-command security audit + auto-fix for OpenClaw. Generates a score, finds vulnerabilities, fixes what it can.

## Quick Start

```bash
# Full audit — scan everything, show score + findings
python3 scripts/security-hardener.py audit

# Auto-fix all fixable issues (creates backup first)
python3 scripts/security-hardener.py fix

# Scan for exposed API keys only
python3 scripts/security-hardener.py keys

# Check auth configuration
python3 scripts/security-hardener.py auth

# Generate markdown report
python3 scripts/security-hardener.py report
```

## Commands

### `audit` — Full Security Audit
Runs all checks, produces a 0-100 security score:
- **Auth check** — Is authentication enabled? What type?
- **Transport check** — HTTPS/TLS configured? Certificates valid?
- **Key exposure scan** — API keys/tokens in config, memory, git history
- **Permission check** — File permissions on sensitive files (config, memory, soul)
- **Plugin audit** — Untrusted plugins, unsigned skills, risky permissions
- **Network check** — Bound interfaces, exposed ports, firewall status
- **CVE check** — Known OpenClaw CVEs against installed version

Options: `--json` for machine-readable output, `--verbose` for detailed findings.

### `fix` — Auto-Remediate
Creates a timestamped backup, then fixes:
- Sets restrictive file permissions (600 for config, 700 for workspace)
- Removes API keys from memory/SKILL.md files (moves to .env)
- Enables auth if disabled
- Restricts bind address from 0.0.0.0 to 127.0.0.1
- Disables unsigned plugins

Options: `--dry-run` to preview fixes without applying, `--backup-dir <path>`.

### `keys` — API Key Scanner
Searches config files, memory files, SKILL.md files, .env files, shell history, and git history for exposed secrets. Pattern library covers 40+ key formats (AWS, OpenAI, Anthropic, Stripe, etc.).

### `auth` — Auth Configuration Check
Verifies authentication is properly configured:
- Gateway auth enabled and strong
- Session tokens rotated
- CORS policy appropriate
- Rate limiting configured

### `report` — Markdown Report
Generates a security posture report suitable for compliance or auditing. Includes score, all findings, recommendations, and fix commands.

## Scoring

| Range | Rating | Meaning |
|-------|--------|---------|
| 90-100 | 🟢 Excellent | Production-ready |
| 70-89 | 🟡 Good | Minor issues, fix recommended |
| 50-69 | 🟠 Fair | Significant gaps, fix required |
| 0-49 | 🔴 Critical | Unsafe for any exposure |

Each finding has a severity (critical/high/medium/low) and a weight that affects the score.

## CVE Coverage

Checks against known OpenClaw CVEs including:
- CVE-2026-33579 — Unauthenticated remote access (63% of instances affected)
- Transport layer vulnerabilities
- Plugin sandbox escapes

See `references/cve-database.md` for full list and mitigation details.
