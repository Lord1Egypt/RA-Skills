# Skill Security Audit - Reference

## Overview

This skill scans OpenClaw skills for security vulnerabilities before installation. It performs static analysis on skill files and provides a risk assessment.

## Security Check Categories

### 🔴 CRITICAL - Block Installation

These issues will cause automatic rejection of skill installation:

| Check | Pattern | Description |
|-------|---------|-------------|
| exec/eval with user input | `exec(request.args...)` | Dynamic code execution with unsanitized input |
| Hardcoded credentials | `password = "..."` | Credentials will be exposed to all users |
| Environment exfiltration | `os.environ[key]` → `requests.post()` | Sends secrets to external servers |
| Shell injection | `subprocess(user_input)` | Command injection vulnerabilities |
| File exfiltration | `open(os.environ[...])` | Reads files based on env vars |

### 🟠 HIGH - Require Confirmation

These issues will prompt a warning but allow manual override:

| Check | Pattern | Description |
|-------|---------|-------------|
| Network without timeout | `curl ...` (no -m) | May hang indefinitely |
| os.system usage | `os.system(cmd)` | Shell command execution |
| Raw socket connections | `socket.connect()` | Unknown network destinations |
| Sensitive paths | `/etc/passwd`, `/proc/` | System file access |

### 🟡 MEDIUM - Caution

These issues are noted but don't block installation:

| Check | Pattern | Description |
|-------|---------|-------------|
| eval usage | `eval(...)` | Dynamic code execution risk |
| Dynamic imports | `__import__`, `importlib` | Module injection risk |
| Pickle deserialization | `pickle.load()` | Arbitrary code execution |
| Unsafe YAML | `yaml.load(..., Loader=...)` | Configuration injection |

### 🔵 LOW / ⚪ INFO - Informational

These are best practice violations:

- Subprocess output not captured
- Very long timeout values
- Printing sensitive data
- Broad exception catching

## Using the Scanner

### Command Line

```bash
python3 skill_audit.py /path/to/skill
python3 skill_audit.py /path/to/skill.skill
```

### Exit Codes

- `0` - Allow installation (no major issues)
- `1` - Warning (high risk issues, user confirmation needed)
- `2` - Block installation (critical issues found)

## Example Output

```
🔒 SKILL SECURITY SCAN REPORT
============================================================

📊 SUMMARY:
   🔴 CRITICAL   0
   🟠 HIGH       2
   🟡 MEDIUM     1
   🔵 LOW        0
   ⚪ INFO       3

📋 RECOMMENDATION:
   ⚠️  WARN - High risk issues detected, review before installing

📝 DETAILED ISSUES:

🟠 HIGH:
   • scripts/install.sh:15
     curl/wget without timeout
     → Network requests without timeout - may hang indefinitely
   • scripts/install.sh:23
     os.system usage
     → Shell command execution - verify commands are safe
```

## Integration

This scanner is used by OpenClaw when:
1. Installing skills from ClawHub
2. Loading skills from local files
3. Before executing untrusted skill code

## False Positives

Some checks may flag legitimate code. Common false positives:

- `curl` in install scripts (verify the URL is trusted)
- `os.system` in build scripts (verify no user input)
- `eval` in data processing (verify input source)

Review each flagged item carefully before deciding to install.
