---
name: termux-compat-runner
triggers:
  - "run shell commands on Termux Android with compatibility checks"
  - "validate command safety before executing on Termux"
  - "check Termux platform compatibility for shell commands"
description: "Advisory skill for safe shell command execution on Termux/Android. Detects platform, checks tool availability, classifies risk, and provides a dry-run validator. Does not execute commands — execution is left to the user."
metadata:
  openclaw:
    version: 2.0.0
author: pmuhammadagus-byte
license: MIT
---

# Termux Compat Runner

Advisory skill for safe shell command execution on Termux/Android. This skill is **advisory-only** — it guides safe command selection and provides a dry-run validator script. It does NOT execute commands.

**Language note:** This skill is language-agnostic. Use whichever language the user prefers.

## Tool & Permission Declaration

**Declared capability:** Read-only shell command validation (dry-run).
**Execution:** None — this skill never executes commands. All execution is left to the user.
**Allowed commands (read-only validation):** `ls`, `cat`, `head`, `tail`, `wc`, `echo`, `pwd`, `date`, `uname`, `whoami`, `id`, `ps`, `top`, `free`, `df`, `du`, `ss`, `netstat`, `ip`, `ifconfig`, `ping`, `getprop`, `dumpsys`, `git status`, `git log`, `git diff`, `git branch`, `git show`.
**Mutating commands (require explicit user confirmation):** `pkg install`, `pkg update`, `pkg upgrade`, `apt`, `dpkg`, `git fetch`, `git pull`.
**Denied commands:** `rm -rf`, `mkfs`, `dd`, `chmod -R`, `shutdown`, `reboot`, `systemctl`, fork bombs, writes to `/dev/`, and any command containing shell operators (`|`, `&&`, `||`, `;`, `$()`, backticks, `>`, `<`) unless explicitly approved by the user.

## When to Use

**Use when:**
- Running shell commands on Termux/Android and need compatibility validation
- Checking if a tool is available before executing
- Classifying command risk (read-only vs destructive)
- Need a dry-run safety check before manual execution

**Don't use when:**
- Operating on non-Termux environments without compatibility concerns
- Executing destructive operations without user confirmation
- Replacing backup/restore scripts
- Running unverified scripts without inspection

## Platform Detection

Before selecting a command strategy, detect the platform:

```bash
# Termux detection
echo "$PREFIX" | grep -q "com.termux" && echo "TERMUX" || echo "NOT_TERMUX"

# Architecture
uname -m  # usually aarch64 on Android

# API level (Termux only)
getprop ro.build.version.sdk 2>/dev/null
```

Detection must happen BEFORE choosing command strategy. Never assume platform.

## Tool Availability Check

Before executing any command, verify the tool exists:

```bash
command -v <tool>        # check if tool is available
pkg list-installed 2>/dev/null | grep <pkg>  # check installed package
```

If tool is not available:
1. Search for a fallback (see Command Compatibility below)
2. If no fallback exists → report ERROR and stop. Do not assume.

## Execution Runbook

```
1. DETECT    → platform + architecture
2. CHECK     → tool available? (command -v)
3. CLASSIFY  → read-only | mutating | destructive
4. VALIDATE  → run scripts/run_safe.sh for dry-run check
5. CONFIRM   → if mutating/destructive, ask user explicitly
6. EXECUTE   → user runs the command manually (skill does NOT execute)
7. VERIFY    → user checks exit code + side effects
8. REPORT    → output format below
```

Strict rules:
- Always use `timeout` when executing manually
- Maximum 2 retries on transient failure, then fallback
- Never continue if output is invalid
- Never ignore non-zero exit codes

## Risk Classification

| Category | Examples | Action |
|----------|----------|--------|
| Read-only | `ls`, `cat`, `uname`, `ps`, `ss` | Safe to run after validation |
| Mutating | `pkg install`, `git pull`, `apt` | Require explicit user confirmation |
| Destructive | `rm -rf`, `mkfs`, `dd`, `chmod -R` | Denied — require manual user execution with double confirmation |

## Timeout Policy

| Type | Timeout |
|------|---------|
| Fast (ls, cat, uname) | 15 seconds |
| Medium (pkg update, install) | 60 seconds |
| Heavy (build, large download) | 180 seconds |

If exceeded: report TIMEOUT, stop, use fallback or ask user.

## Command Compatibility

**AVOID on Termux/Android:**
- `systemctl` / systemd commands
- Paths `/usr/local/...`, `/etc/systemd`
- Desktop-only binaries without fallback
- glibc-only commands without verification

**USE Termux alternatives:**
- `pkg` for package management
- `termux-services` for service management
- `termux-setup-storage` for storage access
- Dynamic paths `$HOME` / `$PREFIX`, never hardcoded

## Verification

After any action, verify beyond exit code 0:
- Exit code = 0
- Output valid and matches intent
- Side effects confirmed (`ls -l`, check state)
- No hidden errors in stderr
- Within timeout

If verification fails: DIAGNOSE → RETRY (transient only, max 2x) → FALLBACK → REPORT ERROR.

## Error Recovery

| Error Type | Recovery | Example |
|------------|----------|---------|
| INPUT | Explain wrong format, show correct | `pkg instal` → `pkg install` |
| DEPENDENCY | Report missing package → suggest install | `python3` absent → `pkg install python` |
| TOOL | Report tool error → do not continue | `ss` absent → try `netstat` |
| NETWORK | Report failure → offline fallback | `pkg update` timeout → change mirror |
| TIMEOUT | Report duration → lighter command | build >180s → split task |
| PERMISSION | Report denied path → setup storage | `/storage` denied → `termux-setup-storage` |
| ENVIRONMENT | Report mismatch → Termux strategy | glibc binary failed |
| UNKNOWN | Capture exception → report clearly → STOP | Never assume |

## Dry-Run Validator

`scripts/run_safe.sh` validates a command against an allowlist. **It NEVER executes anything.**

```bash
# Check a read-only command
bash scripts/run_safe.sh "ss -tulpen" --timeout 60

# Check a mutating command (will be flagged as MUTATING, not ALLOWED)
bash scripts/run_safe.sh "pkg update" --timeout 60

# Destructive command (will be DENIED)
bash scripts/run_safe.sh "rm -rf /tmp/old"
```

The validator:
- Splits commands into READ-ONLY, MUTATING, and DENIED categories
- Rejects shell operators (`|`, `&&`, `||`, `;`, `$()`, backticks, `>`, `<`) unless user-approved
- Prints the command it WOULD run with timeout, but does NOT execute
- Always exits with a clear status: ALLOWED-READ, ALLOWED-MUTATING, or DENIED

## Output Format

```
COMMAND: <command validated>
PLATFORM: TERMUX / LINUX_DESKTOP / MACOS / UNKNOWN
CLASSIFICATION: READ-ONLY / MUTATING / DESTRUCTIVE
VALIDATION: ALLOWED-READ / ALLOWED-MUTATING / DENIED
TIMEOUT: <N>s
VERIFY: <how to verify after manual execution>
NEXT ACTION: <proceed / confirm-with-user / fallback / stop>
```

## Security Rules

- Never execute destructive commands without validation
- Never print secrets/credentials to output
- Never delete files without double confirmation
- Never execute scripts that have not been read and inspected
- Always classify risk before suggesting execution
- Shell operators require explicit user approval

## Quick Reference

| Situation | Action |
|-----------|--------|
| Need to run a command | Detect platform → check tool → classify → validate → confirm → user executes |
| Tool not available | Search fallback → or ERROR |
| Destructive command | DENIED — user must execute manually with confirmation |
| Shell operators present | Require explicit user approval |
| Timeout exceeded | Stop → fallback or user action |
| Unknown error | Report → stop, never assume |

## Remember

- This skill is advisory-only — it never executes commands
- Detect platform before choosing strategy
- Check tool availability before suggesting commands
- Classify risk: read-only, mutating, destructive
- Shell operators require explicit approval
- Never assume Linux desktop environment
- Verify results with evidence, not just exit codes
