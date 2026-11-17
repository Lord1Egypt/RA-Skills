# termux-compat-runner

> Advisory skill for safe shell command execution on Termux/Android. Detects platform, checks tool availability, classifies risk, and provides a dry-run validator. Does NOT execute commands.

## Overview

See SKILL.md for full reference.

## When to Use

**Use when:**
- Running shell commands on Termux/Android and need compatibility validation
- Checking if a tool is available before executing
- Classifying command risk (read-only vs destructive)
- Need a dry-run safety check before manual execution

**Don't use when:**
- Operating on non-Termux environments without compatibility concerns
- Executing destructive operations without user confirmation
- Running unverified scripts without inspection

## Usage

```bash
# Dry-run validate a read-only command
bash scripts/run_safe.sh "ss -tulpen" --timeout 60

# Dry-run validate a mutating command (flagged, not executed)
bash scripts/run_safe.sh "pkg update" --timeout 60

# Destructive command (DENIED)
bash scripts/run_safe.sh "rm -rf /tmp/old"
```

The validator NEVER executes commands. It only classifies them as READ-ONLY, MUTATING, or DENIED.

---

*Maintained by pmuhammadagus-byte.*
