# Quorum — Claude Code Skill

Multi-critic quality validation for code, configs, and documentation.

## Install

```bash
git clone https://github.com/SharedIntellect/quorum
cp -r quorum/ports/claude-code ~/.claude/skills/quorum
```

## Usage

### Full validation (all critics)
"Run Quorum validation on this file"
"Validate api_handler.py with Quorum"

### Single critic
"Run the security critic on auth.py"
"Check this config for completeness"

### Cross-artifact consistency
"Check if implementation.py matches spec.md"

## What It Checks
- **Correctness** — Logic errors, contradictions, false claims
- **Completeness** — Missing sections, edge cases, broken promises
- **Security** — OWASP ASVS 5.0, CWE Top 25, framework-grounded
- **Code Hygiene** — ISO 25010/5055, structural quality beyond linting
- **Cross-Consistency** — Spec/impl, docs/code, schema contracts

## Verdict Scale
- **PASS** — No issues found
- **PASS_WITH_NOTES** — Minor issues only (MEDIUM/LOW)
- **REVISE** — HIGH severity issues requiring rework
- **REJECT** — CRITICAL issues found

## Requirements
- Claude Code CLI
- Python 3.10+ (for pre-screen script)
- No additional dependencies
