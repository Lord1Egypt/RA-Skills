---
name: skill-audit-framework
description: Structured security and quality audit framework for AI agent skills. Teaches you what to check before installing any skill.
homepage: https://github.com/ENAwareness/skill-auditor
metadata:
  openclaw:
    emoji: 🔍
    tags:
      - security
      - audit
      - skills
      - safety
      - review
      - trust
---

# Skill Auditor 🔍

A structured framework that teaches your agent how to audit ClawHub and MCP skills before you install them. Not a scanner — a systematic review methodology.

Unlike automated scanners that give false confidence, Skill Auditor walks through what matters: permissions, behavior, credentials, and persistence — so you understand exactly what a skill will do on your system.

## Why this exists

- 13.4% of ClawHub skills have critical security issues (Snyk ToxicSkills study)
- 341 malicious skills were found in a single campaign (ClawHavoc incident, Feb 2026)
- Automated scanners can miss context-dependent threats and provide false security
- Understanding what you're installing is better than trusting a green checkmark

## How to use

Ask your agent to audit any skill before installing:

```
Audit this skill before I install it: [skill-name or URL]
```

```
Review the security of @author/skill-name on ClawHub
```

```
I want to install [skill]. Is it safe?
```

## Audit Framework

The agent follows a 6-domain checklist. Each domain produces a PASS / WARN / FAIL verdict.

### 1. Identity & Provenance
- [ ] Author has a GitHub profile with other projects
- [ ] Skill has a public source repository (not ClawHub-only)
- [ ] Repository has commit history (not a single-commit dump)
- [ ] Author identity is consistent across platforms
- **FAIL if**: No source repo, no author history, single-commit repo

### 2. Permission & Scope Analysis
- [ ] `requires.env` only lists credentials the skill actually uses
- [ ] No credentials unrelated to the skill's purpose
- [ ] File access limited to workspace directory
- [ ] No requests for system-wide permissions
- **FAIL if**: Requests credentials beyond stated purpose, accesses files outside workspace

### 3. Behavior vs Description Match
- [ ] Every file in the skill serves the stated purpose
- [ ] No network calls to undeclared endpoints
- [ ] No data exfiltration patterns (sending user data to external URLs)
- [ ] Script behavior matches what SKILL.md describes
- **FAIL if**: Hidden functionality, undeclared network calls, description mismatch

### 4. Credential & Secret Handling
- [ ] API keys stored in env vars, not hardcoded
- [ ] No credentials logged or written to non-protected files
- [ ] OAuth tokens have minimal required scopes
- [ ] Cached tokens stored in workspace, not system-wide
- **FAIL if**: Hardcoded secrets, credentials in logs, excessive OAuth scopes

### 5. Persistence & Side Effects
- [ ] Files written only within workspace boundaries
- [ ] No system-level modifications (crontab, /etc/, systemd)
- [ ] No auto-start or background processes installed
- [ ] Uninstall is clean (no orphaned files or processes)
- **FAIL if**: System modifications, persistent background processes, dirty uninstall

### 6. Dependency & Supply Chain
- [ ] Dependencies are well-known packages (not obscure single-author libs)
- [ ] No `curl | bash` or `curl | python` install patterns
- [ ] No post-install scripts that download additional code
- [ ] Package versions are pinned (not `latest`)
- **FAIL if**: Unknown dependencies, pipe-to-shell installs, unpinned versions

## Output Format

The agent produces a structured report:

```
## Skill Audit Report: [skill-name]

Author: [name] | Source: [repo URL or "ClawHub only"]
Version: [X.Y.Z] | Files: [count] | Scripts: [count]

### Verdicts

| Domain                    | Verdict | Notes                |
|---------------------------|---------|----------------------|
| Identity & Provenance     | PASS    |                      |
| Permission & Scope        | WARN    | Requests broad perms |
| Behavior vs Description   | PASS    |                      |
| Credential Handling       | PASS    |                      |
| Persistence & Side Effects| FAIL    | Writes to /etc/      |
| Dependency & Supply Chain | PASS    |                      |

### Overall: ⚠️ WARN — Review flagged items before installing

### Flagged Items
1. [Domain]: [Specific issue and recommendation]

### What to Ask the Author
1. Why does the skill need [permission X]?
2. Can [flagged behavior] be made opt-in?
```

## Limitations

- This is a review framework, not a deterministic scanner
- The agent reads and reasons about skill files — it cannot execute or sandbox them
- Always read the source code yourself for high-privilege skills
- A PASS verdict means no issues were found, not that the skill is guaranteed safe

## Trust Hierarchy

When evaluating skill trust, consider this hierarchy:

1. **Highest trust**: Open-source on GitHub + active maintainer + ClawHub Benign scan + you read the code
2. **Moderate trust**: GitHub repo exists + ClawHub Benign scan + reasonable permissions
3. **Low trust**: ClawHub-only (no source repo) + Suspicious scan + broad permissions
4. **No trust**: No source, no author history, requests unrelated credentials
