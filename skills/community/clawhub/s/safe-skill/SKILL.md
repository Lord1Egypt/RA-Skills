---
name: safe-skill
version: 1.2.0
description: >
  Programmatic security scanner for AI agent skills. Performs AST analysis, regex pattern matching,
  Shannon entropy detection, URL/IP extraction, and permission scope inference — with Markdown
  context awareness to reduce false positives. Use before installing any skill from ClawHub, GitHub,
  or untrusted sources. Trigger: "scan this skill", "vet this skill", "is this skill safe",
  "check skill security", "审查这个skill", "扫描skill安全性", "这个skill安全吗".
---

# Safe-Skill

Programmatic security scanner for AI agent skills. Unlike prompt-only vetting checklists,
this skill includes an automated scanner (`scripts/scan.py`) that performs real static analysis.
Zero external dependencies. Runs anywhere Python 3.8+ is available.

## Quick Start

```bash
# Scan a local skill directory
python3 {baseDir}/scripts/scan.py /path/to/skill-directory

# Scan a single file
python3 {baseDir}/scripts/scan.py /path/to/SKILL.md

# JSON output for machine consumption
python3 {baseDir}/scripts/scan.py /path/to/skill --json

# Save report to file
python3 {baseDir}/scripts/scan.py /path/to/skill -o report.txt

# Verbose mode (show clean files too)
python3 {baseDir}/scripts/scan.py /path/to/skill -v

# With explicit whitelist config
python3 {baseDir}/scripts/scan.py /path/to/skill -w /path/to/.vetterrc
```

### Remote Fetch + Scan

```bash
# GitHub URL
python3 {baseDir}/scripts/fetch_and_scan.py https://github.com/openclaw/skills/tree/main/skills/someone/cool-skill

# ClawHub slug
python3 {baseDir}/scripts/fetch_and_scan.py clawhub:author/skill-name

# GitHub shorthand
python3 {baseDir}/scripts/fetch_and_scan.py github:openclaw/skills/skills/author/skill-name
```

## What It Scans

The scanner runs **five analysis passes** on every file in a skill:

### Pass 1: Pattern Matching (65+ rules)
Regex-based detection across 10 categories: RCE, data exfiltration, credential access,
obfuscation, privilege escalation, agent identity theft, persistence/backdoor, suspicious
network, filesystem abuse, and runtime package installation.

### Pass 2: Python AST Analysis
For `.py` files, parses the Abstract Syntax Tree to detect patterns regex cannot —
e.g. `eval(dynamic_var)` vs `eval("literal")`, only flagging the dangerous one.

### Pass 3: Shannon Entropy Detection
Catches encoded payloads (base64, hex, encrypted blobs) that evade keyword-based detection.

### Pass 4: URL / IP Extraction
Extracts all URLs and hardcoded IPs, classifying each by risk level.

### Pass 5: Permission Scope Inference
Automatically extracts what the skill accesses: files, network, commands, env vars, packages.

## Markdown Context Awareness

Security documentation describes the very patterns it warns against. Safe-Skill parses
Markdown structure and **automatically downgrades findings** under documentation headings
(containing words like "red flag", "warning", "reject", "danger", etc.) — dramatically
reducing false positives for security-related skills.

## Whitelist Configuration (.vetterrc)

Place a `.vetterrc` in the skill directory to suppress known-good patterns. See `.vetterrc.example`.

## Risk Scoring

Quantitative scoring (0-100+):

| Score | Level | Verdict |
|-------|-------|---------|
| 0 | CLEAN | Safe to install |
| 1-15 | LOW | Safe to install |
| 16-40 | MEDIUM | Install with caution |
| 41-80 | HIGH | Human review required |
| 81+ | EXTREME | Do not install |

Exit codes: `0` = CLEAN/LOW, `1` = MEDIUM, `2` = HIGH/EXTREME.

## Workflow for the Agent

When asked to vet a skill:

1. **Run the scanner**: `python3 {baseDir}/scripts/scan.py <target_path>`
   - For remote skills, use: `python3 {baseDir}/scripts/fetch_and_scan.py <url_or_slug>`
2. **Review the report**: Focus on critical/high severity items NOT marked `[DOC]`.
3. **Cross-reference**: For MEDIUM+ findings, read the flagged lines and assess context.
4. **Recommend**: Provide a final recommendation based on scan results + contextual review.

## Limitations

- **Static analysis only** — no sandboxing or dynamic execution tracing
- **No network reputation lookup** — URL risk is heuristic
- **Regex limits** — creative obfuscation can evade; AST helps for Python only
- **False positives** — legitimate skills using subprocess, network calls will trigger findings

Zero external dependencies. Runs anywhere Python 3.8+ is available.
