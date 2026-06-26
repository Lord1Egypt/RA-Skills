---
name: security-sentinel-ultimate
description: Scans a skill directory for security issues and best practices
tools:
  - name: scan_skill
    description: Analyzes a skill directory for security vulnerabilities, misconfigurations, and compliance with best practices.
    arguments:
      - name: path
        description: The file path to the skill directory to scan.
        type: string
        required: true
    execution:
      command: python3 {{SKILL_DIR}}/scanner.py "{{path}}"
      output_format: markdown
---

# Security Sentinel

Scans a skill directory for security issues, misconfigurations, and best practices.

## What It Detects

| Category | Examples | Severity |
|----------|---------|----------|
| Dangerous calls (critical) | `os.system`, `eval`, `exec` | 🔴 Critical |
| Dangerous calls (warning) | `subprocess.run`, `os.popen` | 🟡 Warning |
| Hardcoded secrets | API keys, tokens, passwords, credentials in string literals | 🔴 Critical |
| Network calls | `requests.get`, `urllib.request.urlopen`, `http.client` | 🟡 Warning |
| Obfuscation | `getattr` indirection, `__import__`/`importlib` dynamic loading, `chr()`-encoded strings | 🔴 Critical |
| Hidden files | Files and directories starting with `.` (e.g. `.env`, `.hidden_script.py`) | 🟡 Warning |

## Severity Model

The scanner uses a three-tier severity system:

| Status | Meaning |
|--------|---------|
| 🔴 **CRITICAL** | Immediate security risk — hardcoded secrets, `eval`/`exec`, `os.system`, obfuscation detected. Requires urgent review. |
| 🟡 **WARNING** | Potential risk — `subprocess` usage, network calls, hidden files. Review recommended. |
| 🟢 **OK** | No findings. File is clean. |

Each file gets an individual severity rating. The **overall status** is the highest severity across all files — if even one file is red, the entire scan is marked CRITICAL.

## Obfuscation Defenses (Defensive Depth)

The scanner catches three common bypass techniques:

1. **`getattr` indirection** — `getattr(os, 'system')('whoami')` is flagged because the second argument resolves to a known dangerous attribute name.
2. **Dynamic imports** — `__import__('subprocess')` and `importlib.import_module('subprocess')` are both detected and flagged as dangerous module loads.
3. **String construction** — Secrets built via concatenation (`key = "sk-" + "abcd..."`) or `chr()` sequences are resolved at scan time and matched against secret patterns.

## Usage

The `scan_skill` tool accepts a `path` argument pointing to a skill directory. It runs `scanner.py` against all `.py` files in that directory tree and returns a Markdown report with tables of findings grouped by file and category.
