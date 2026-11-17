---
name: skillgate
description: Trust infrastructure for AI agent skills: static security scanning, machine-checkable Trust Score, dependency checks, report generation (terminal/JSON/SARIF/JUnit/Markdown/HTML), optional skill benchmarking, and registry watch. Bundles a companion medical-compliance skill library (ISO 13485 QMS, IEC 62304 SDLC, IEC 62366 usability, IEC 60601 electrical safety, IEC 81001 cybersecurity, ISO 10993 biocompatibility, IFU/labeling, PMS, CER, change control, dataset/algorithm checks) — these are documented companion skills, not hidden functionality. Use when the user asks to audit, review, or check an AI agent skill's safety, quality, or trustworthiness.
version: 1.0.0
license: MIT
author: zhaoxinghua09-cell
metadata:
  openclaw:
    requires:
      bins:
        - python
    homepage: https://github.com/zhaoxinghua09-cell/skillgate
    emoji: "🛡️"
tags:
- security
- trust
- audit
- scanner
- agent
- skills
---

# SkillGate — Skill Trust Scanner

## When to Use

- The user wants to **audit or review an AI agent skill** for security issues, quality, or trustworthiness.
- The user asks *"is this skill safe?"*, *"can I trust this skill?"*, *"check this skill for problems"*.
- You are about to **install or run a third-party skill** and want to make sure it's not malicious.
- You want to **compare two skills** and see which one has a better Trust Score.

## Package Contents & Operating Boundaries

- **Static scanner only, zero code-execution paths**: SkillGate analyzes skill source code with AST + regex rules; the package contains **no subprocess/`os.system`/`Popen` execution points** (rule-library pattern strings aside, which are data, not calls). It does not execute the code it scans, and no `--lenient`/downgrade mode exists that could weaken findings.
- **Benchmarking is dry-run only**: `skillbench.py run` previews/export test definitions and **never executes** code; `skillwatch.py` is a read-only monitor (in-process scan calls; no file is written unless an explicit `--history FILE` is given, and that location is guarded against symlink/junction redirection). Real test execution happens only in the repository's own `tests/` pytest suite (developer environment).
- **MCP server is in-process**: `skillgate-mcp.py` imports and calls SkillGate's scan functions directly — no subprocess, no network egress, no credential reads.
- **Companion skill library**: the `skills/` folder bundles 17 documented companion skills — 12 medical-device compliance checks (ISO 13485 QMS, IEC 62304 SDLC, IEC 62366 usability, IEC 60601 electrical safety, IEC 81001 cybersecurity, ISO 10993 biocompatibility, IFU/labeling, PMS, CER, change control, AI dataset quality, AI algorithm validation), 2 quality checks (`code-complexity-check`, `doc-format-check`), and 3 workflow companions (`medical-device-chain`, `medical-file-watcher`, `medical-recommender`). All are listed in `skills/SKILLS-INDEX.md` and are first-class features of this package.
- **Detection rule library contains dangerous-pattern strings by design**: SkillGate must recognize threat patterns (dynamic code execution, credential access, prompt injection, privilege escalation) to flag them. Those strings live in the rule library and are *patterns to detect*, not code SkillGate executes. Findings tagged from the rule library are annotated accordingly.
- **Suppression markers cannot be abused**: `# skillgate: ignore` markers are honored **only when SkillGate scans its own directory** (rule library self-scan). Markers inside scanned third-party skills have **no effect** and are reported as a `suppression-abuse` finding, so a malicious skill can never hide findings or manipulate its Trust Score. Every suppressed finding is counted and disclosed in all report formats, never silently dropped.
- **Target config cannot exclude payload**: `.skillgate.yml/.yaml` `paths.exclude` rules are honored **only during self-scan**. A scanned third-party skill's bundled config is ignored entirely, so it cannot silently exclude its own dangerous files from review.
- **Zero network egress**: the scanner makes **no network requests** — dependency CVE checking is offline by default (only a local note is emitted), so an untrusted scanned folder cannot trigger outbound traffic.
- **Confined writes**: `--output`/`--badge` (and bench `--output`) can only write **inside the scanned folder**; attempts to write anywhere else are rejected. The scanner never modifies files outside the selected folder.
- **MCP server**: `skillgate-mcp.py` exposes scan/report/badge endpoints and runs only `python` subprocesses with timeouts; no network egress, no credential reads.

## Usage

```bash
# Scan a skill folder and get a Trust Score
python scripts/skillgate.py scan ./path/to/skill/

# Scan with more output
python scripts/skillgate.py scan ./path/to/skill/ --verbose

# Output JSON (for programmatic use)
python scripts/skillgate.py scan ./path/to/skill/ --format json

# Output HTML report (beautiful, shareable)
python scripts/skillgate.py scan ./path/to/skill/ --format html
```

Exit code `0` = all good (Trust Score >= 80), `1` = issues found (Trust Score < 80), `2` = usage error.

## What It Checks

| Category | What it looks for |
|----------|-------------------|
| 🔒 **Secrets** | API keys, tokens, passwords hardcoded in the code |
| ☠️ **Dangerous code** | `eval()`, `exec()`, `os.system()`, `subprocess` with shell=True |
| 📦 **Dependencies** | Outdated or vulnerable dependencies |
| 📝 **SKILL.md quality** | Missing description, missing version, missing license |
| 🌐 **Network calls** | Unnecessary or suspicious network requests |
| 📂 **File system access** | Reading/writing files outside the skill folder |

## Trust Score

Start at 100 points, subtract based on findings:
- CRITICAL issue: -15 points
- HIGH issue: -8 points
- MEDIUM issue: -3 points
- LOW issue: -1 point

| Score | Grade | Meaning |
|-------|-------|---------|
| 90+ | A+ | Excellent — very safe |
| 80+ | A | Good — minor issues |
| 70+ | B | Fair — some concerns |
| 60+ | C | Poor — needs review |
| < 60 | D | Unsafe — do not use |

## Known Limits (be explicit with users)

- This is a **static scanner** — it looks at the code, it doesn't run it.
- It catches **known bad patterns**, not zero-day vulnerabilities.
- A clean scan means "no obvious red flags", not "100% safe".
- It only scans the code in the folder, not what the skill does when it runs.

## Output Discipline

- Always show the Trust Score and Grade prominently.
- List CRITICAL and HIGH findings first, don't bury them.
- Give a clear recommendation: *"safe to use"* / *"use with caution"* / *"do not use"*.
- Don't hide or downplay serious issues.
