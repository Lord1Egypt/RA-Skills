---
name: skill-sandbox
description: >
  Sandboxed ClawHub skill installation with automated security scanning.
  Use when: (1) Installing any new skill from ClawHub, (2) Auditing an already-installed skill,
  (3) Promoting a quarantined skill after review. Installs skills to a staging area, runs a
  multi-layer static security scan (file inventory, code patterns, dangerous instructions,
  dependency analysis, publisher verification), then auto-promotes clean skills or quarantines
  flagged ones for manual review. Prevents supply chain attacks from untrusted skill publishers.
---

# Skill Sandbox

Sandboxed installation pipeline for ClawHub skills. Install → Stage → Scan → Promote or Quarantine.

## Quick Start

```bash
# Install a skill (stages, scans, auto-promotes if clean)
bash {baseDir}/scripts/skill-sandbox.sh <skill-name>

# Install a specific version
bash {baseDir}/scripts/skill-sandbox.sh <skill-name> --version 1.2.0

# Force install (bypass VirusTotal flags from clawhub)
bash {baseDir}/scripts/skill-sandbox.sh <skill-name> --force

# Re-scan a staged skill
bash {baseDir}/scripts/skill-sandbox.sh <skill-name> --scan-only

# Promote a quarantined skill after manual review
bash {baseDir}/scripts/skill-sandbox.sh <skill-name> --promote

# List all quarantined skills
bash {baseDir}/scripts/skill-sandbox.sh --list-staged
```

## How It Works

1. **Stage** — Skill is installed to `skills/_staging/<name>` (never directly to live)
2. **Scan** — 5-layer automated security scan runs:
   - File inventory (hidden files, symlinks, binaries)
   - Code pattern analysis (eval, exec, network calls, secret access, obfuscation)
   - SKILL.md instruction review (dangerous agent directives)
   - Dependency check (package.json install scripts, known-risky deps)
   - Publisher verification (metadata, origin registry)
3. **Verdict:**
   - ✅ **PASS** (0 findings) → auto-promoted to `skills/`
   - ⚠️ **WARN** (warnings only) → quarantined, manual review recommended
   - ❌ **FAIL** (critical findings) → quarantined, deep audit required

## Scan Details

### Critical Findings (auto-quarantine)
- `eval()`, `new Function()` — dynamic code execution
- Symlinks — path traversal risk
- `postinstall` / `preinstall` scripts in package.json — npm supply chain vector
- Dangerous SKILL.md instructions (disable security, exfiltrate, reverse shells, chmod 777)

### Warning Findings (review recommended)
- Network calls (`fetch`, `curl`, `axios`, `http`)
- Shell execution (`child_process`, `exec`, `spawn`, `subprocess`)
- Environment/secret access (`process.env`, `API_KEY`, `TOKEN`)
- Base64 encoding patterns (potential obfuscation)
- File system writes
- Hidden files (excluding `.clawhub/`)
- Non-text binary files

## Integration with Agent Workflows

For teams using security auditor agents (like Sentinel), the recommended flow:

1. Run `skill-sandbox.sh` for the fast automated scan
2. If WARN or FAIL → spawn your security agent for a deep LLM-powered audit of the staged files
3. After agent clears it → `skill-sandbox.sh <name> --promote`

## Directory Structure

```
skills/
├── _staging/          ← quarantine area (gitignored)
│   └── <skill>/       ← flagged skills live here until promoted
├── skill-sandbox/     ← this skill
│   ├── SKILL.md
│   └── scripts/
│       └── skill-sandbox.sh
└── <other-skills>/    ← promoted (live) skills
```

## Notes

- The `_staging/` directory should be added to `.gitignore`
- Clean skills auto-promote — no manual step needed for safe installs
- The script returns exit codes: 0 (pass/warn), 2 (fail) for CI integration
- All scan patterns are static regex — no network calls, no external dependencies
