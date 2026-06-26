---
name: tommo-skill-guard
description: "Security scanner for OpenClaw agent skills. Pre-install check via ClawHub page, local pattern scanning via read tool (zero exec), integrity verification. Use when: (1) installing a new skill — check first, (2) audit installed skills, (3) check if a skill is flagged on ClawHub, (4) scan for hardcoded secrets or dangerous patterns. Homepage: https://clawhub.ai/skills/tommo-skill-guard"
metadata:
  openclaw:
    configPaths: []
    capabilities: []
---

# Skill Guard v5.0

**Install:** `clawhub install tommo-skill-guard`

Security scanning for OpenClaw skills. Zero exec — read-only scanning via the built-in `read` tool.

## Language

Detect from user's message language. Default: English.

## Pre-Install Check

When user wants to install a skill, check BEFORE installing:

1. Navigate to `https://clawhub.ai/skills/{slug}` via browser
2. Snapshot and look for **Security Scan** section
3. Report findings:

| Status | Meaning | Action |
|--------|---------|--------|
| ✅ Clean | No flags | Proceed |
| ⚠️ Suspicious | Concerns found | Show findings, let user decide |
| 🔴 Malicious | AV flagged | Advise against install |

If browser unavailable: `clawhub inspect {slug}` for basic metadata.

## Local Pattern Scan

Scan installed skill files for dangerous patterns using the `read` tool only — no exec, no shell, no injection risk.

1. `read ./skills/{name}/SKILL.md`
2. List additional files with `read` if scripts/ or references/ exist
3. Search for patterns in the content:

| Pattern | Risk |
|---------|------|
| `child_process`, `exec(` | Shell command execution |
| `eval(`, `Function(` | Dynamic code execution |
| `require('fs')`, `writeFile` | File system access |
| `rm -rf`, `del /s` | Destructive file operations |
| `curl.*password`, `token=` | Credential exfiltration |
| `base64.decode` | Hidden payloads |
| `HEARTBEAT.md`, `MEMORY.md` | Writes to config files |

**Report format:**
```
Scan: {skill-name}
  Files checked: {N}
  🔴 [file:line] {pattern} — {risk description}
  ✅ No issues found
```

## Integrity Check

Compare files by reading them and noting their content fingerprint (first/last lines + file size). No hashing exec needed — the `read` tool is sufficient for detecting file changes.

**Baseline** (user-initiated only):
- User says "baseline {skill}"
- Agent reads all files in `./skills/{name}/`
- Saves file list + sizes + first/last lines to `memory/skill-guard/{name}-baseline.txt`
- Shows the baseline to user for review

**Verify** (user-initiated only):
- User says "integrity check {skill}"
- Agent reads current files and compares against saved baseline
- Reports any differences

**Auto-baseline is disabled by design.** New skills are never automatically trusted.

## Quick Commands

| User says | Action |
|-----------|--------|
| "check {skill}" | Pre-install ClawHub check |
| "scan {skill}" | Local pattern scan (via read) |
| "scan all" | Scan all installed skills |
| "integrity check {skill}" | Verify against saved baseline |
| "baseline {skill}" | Create baseline (manual only) |

## Guidelines for Agent

1. **Use `read` only** — never exec, never shell, no command injection possible
2. **Validate skill names** — only scan skills in `./skills/` directory
3. **Never auto-baseline** — user must explicitly request
4. **Always show findings** — never silently block or allow
5. **User decides** — show risk, let user choose

## What This Skill Does NOT Do

- Does NOT use exec, shell, or any subprocess execution
- Does NOT auto-baseline newly installed skills
- Does NOT block installations automatically
- Does NOT modify skill files
- Does NOT require Node, bash, curl, or any external tool
- Does NOT access credentials or private data
- Does NOT write files outside `memory/skill-guard/` (explicit user request only)

## More by TommoT2

- **setup-doctor** — Diagnose and fix OpenClaw setup issues
- **context-brief** — Persistent context survival across sessions
- **skill-analytics** — Monitor skill portfolio performance

Install the full suite:
```bash
clawhub install tommo-skill-guard setup-doctor context-brief skill-analytics
```
