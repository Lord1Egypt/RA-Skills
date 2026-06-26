---
name: security-review
description: Run a world-class security assessment before installing any external package, CLI, npm module, Python library, or third-party integration. Produces a GO/NO-GO/CONDITIONAL verdict with source code analysis, CVE search, and data flow review.
metadata:
  openclaw:
    emoji: "🔐"
    requires:
      tools:
        - sessions_spawn
        - web_search
        - web_fetch
---

# Security Review Skill

## Trigger
Run this skill BEFORE installing ANY external package, tool, CLI, npm module, Python library, browser extension, or third-party integration.

No exceptions. "Open source" is not a security clearance.

## What This Skill Does
Spawns a security review sub-agent that performs a world-class, current-intelligence security assessment and produces a GO / NO-GO / CONDITIONAL verdict.

## How to Use

### 1. Spawn the review agent
```
sessions_spawn with model: anthropic/claude-sonnet-4-6, task: [security review prompt below]
```

### 2. Standard Review Prompt Template
Fill in [PACKAGE NAME], [INSTALL COMMAND], [DESCRIPTION], [SOURCE URL]:

```
You are a world-class security analyst. Perform a comprehensive security review before installation.

PACKAGE: [PACKAGE NAME]
Source: [GitHub URL or npm/pypi link]
Install: [INSTALL COMMAND]
Description: [what it claims to do]

Cover ALL 7 sections:

1. LEGITIMACY & TRUST SIGNALS
   - Author/maintainer: GitHub profile, history, reputation
   - Stars, forks, contributors, last commit
   - Red flags: new account, copied code, suspicious activity

2. LATEST SECURITY INTELLIGENCE (USE web_search)
   Search: "[name] security vulnerability", "[name] malware", "[name] CVE",
   "[name] data exfiltration", "[author] security issues", HackerNews/Reddit discussions

3. SOURCE CODE ANALYSIS (USE web_fetch on raw GitHub files)
   - What does the entry point actually do?
   - Network calls — to where?
   - File system access beyond documented scope?
   - Obfuscated code?
   - npm/pip dependencies — any known-bad?

4. DATA FLOW ANALYSIS
   - What data does it access? (conversations, files, env vars, API keys)
   - Where does data go? Local only or external?
   - Telemetry/analytics present?
   - Exfiltration risk for workspace content?

5. PERMISSION SCOPE
   - System access required
   - Network access?
   - Touches env vars or config files?
   - Can it interfere with other processes?

6. DEPENDENCY RISK
   - Full dependency list
   - Any known-vulnerable deps?
   - Recent supply chain attacks on dependencies?

7. VERDICT
   GO / NO-GO / CONDITIONAL
   - Confidence: High/Medium/Low
   - Top 3 specific risks
   - If CONDITIONAL: exact conditions required before install

Write complete review to:
C:\Users\hhx-sandbox2\.openclaw\workspace\logs\security-review-[package-name]-[YYYY-MM-DD].md

Verify file exists and is complete before reporting done.
```

### 3. Read the output
After the sub-agent completes, read the file and surface the verdict to Marcus.

### 4. Marcus decides
Present the verdict clearly. Never install without explicit Marcus approval after a GREEN or CONDITIONAL review.

## Standing Rules

- **NO install without a completed security review** — not even "quick" ones
- **Web search is mandatory** — latest CVEs and community reports must be checked
- **Source code must be read** — not just the README
- **All reviews logged** to `logs/security-review-[package]-[date].md`
- **MEMORY.md updated** with verdict after each review

## Review Log Index
| Date | Package | Verdict | File |
|------|---------|---------|------|
| 2026-03-04 | claude-subconscious | Pending | logs/security-review-claude-subconscious-2026-03-04.md |
