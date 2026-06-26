---
name: skill-security
description: Security checks for installing skills, packages, or plugins. Use BEFORE any `npm install`, `openclaw plugins install`, `clawhub install`, or similar install commands. Also use when reviewing a newly installed skill before first use. Triggered by any install, add, or package addition request.
---

# Skill Security

Run these checks before installing ANY skill, package, or plugin. Always warn the user before proceeding.

## Pre-Install Checklist

### 1. Source Verification
- Is it from clawhub.com (vetted) or a random npm package?
- Who's the author? Do they have other packages / reputation?
- Is there a GitHub repo? Check for recent commits, open issues, maintainer activity.

### 2. Popularity Check
- `npm info <package>` — check weekly downloads, last publish date, version history
- Low downloads (< 100/week) + recent publish = higher risk

### 3. Dependency Audit
- `npm info <package> dependencies` — how many deps does it pull in?
- More dependencies = larger attack surface
- Flag packages with 50+ transitive dependencies

### 4. Lifecycle Scripts (HIGH RISK)
- Check for `preinstall`, `install`, `postinstall` scripts — these run arbitrary code
- `npm info <package> scripts` or inspect `package.json`
- pnpm blocks these by default; npm does NOT
- If lifecycle scripts exist, flag it explicitly to the user

### 5. Scan After Install
- `npm audit` after install to catch known vulnerabilities

### 6. Check for Dynamic Content
- Search the skill code for URLs that are fetched at runtime
- Skills that download and execute content from external endpoints can change behavior after install

## Red Flags — Stop and Ask

- 🚩 Package published very recently with no history
- 🚩 Maintainer has no other packages or reputation
- 🚩 Package name similar to a popular one (typosquatting: e.g., `reqeust` vs `request`)
- 🚩 Requests permissions beyond what it claims to do
- 🚩 No GitHub repo, or repo is empty/suspicious
- 🚩 Postinstall scripts that download from unknown URLs
- 🚩 **Dynamic content fetching** — skill calls external URLs at runtime (2.9% of ClawHub skills do this; payload can change after install)
- 🚩 **Base64 in install instructions** — ClickFix social engineering pattern (fake errors → paste base64 command → malware)
- 🚩 **New uploader, bulk uploads** — single user uploading many skills rapidly (ClawHavoc: 354 skills from one account)
- 🚩 **Skill references credential paths** — `~/.openclaw/credentials/`, `~/.clawdbot/.env`, `.env` files

## Core File Protection

Skills are NEVER allowed to modify these files without explicit user approval:

- `SOUL.md` — agent identity
- `AGENTS.md` — agent rules
- `IDENTITY.md` — agent metadata
- `USER.md` — user's personal info
- `MEMORY.md` or `memory/*.md` — agent memories
- `TOOLS.md` — infrastructure notes

## Data Exfiltration Checks

After installing a skill, before running it:

1. **Read SKILL.md** — understand what the skill does
2. **Check file paths** — does it reference paths outside its own directory and workspace?
3. **Check exec commands** — does it `curl` to unknown domains?
4. **Check write/edit calls** — are target paths outside `workspace/`?
5. **Check for credential access** — `.env`, `~/.ssh/`, `~/.gnupg/`, API keys
6. **Check for dynamic content** — does it fetch and execute content from external URLs at runtime? (Snyk: 2.9% of ClawHub skills do this)

## ClawHub-Specific Checks

When installing from ClawHub:

- **Check uploader history** — is this a new account? Do they have other skills? Bulk uploads from unknown accounts = red flag (ClawHavoc: 354 skills from one malicious account)
- **Check skill stars/reviews** — community feedback is a signal, not proof
- **Check VirusTotal** — OpenClaw has a VirusTotal partnership; check if the skill has been scanned
- **Verify semantic versioning** — legitimate skills typically have version history and changelogs
- **Search for security reports** — search web for "[skill-name] malicious" before installing

## Known Attack Campaigns (as of March 2026)

Reference for identifying patterns:

- **ClawHavoc** — 300+ coordinated skills, ClickFix social engineering, downloads Atomic Stealer (AMOS)
- **AuthTool** — dormant payload, activates on specific natural language prompts, establishes reverse shell
- **Hidden Backdoor** — fake "Apple Software Update" during install, encrypted tunnel to attacker
- **Credential Exfiltration** — targets `~/.clawdbot/.env` and `~/.openclaw/credentials/` for API keys

## Red Flags — Skill Behavior

- 🚩 Skill reads `.env` or credential files
- 🚩 Skill makes network requests to unfamiliar domains
- 🚩 Skill writes to paths outside workspace
- 🚩 Skill modifies core files (SOUL, AGENTS, MEMORY, USER, IDENTITY, TOOLS)
- 🚩 Skill sends data to external URLs not part of stated purpose

## What To Tell The User

Before installing, give a brief summary:

> "⚠️ Installing [package]: [downloads/week], [last updated], [dep count] deps, [lifecycle scripts?]. Looks [clean/sketchy] — proceed?"

If red flags found:

> "🚩 Flags on [package]: [list issues]. Want me to proceed anyway?"
