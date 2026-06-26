---
description: "Run shark.ps1 loop enforcer with a task (OS-level 25s timeout per turn)"
argument-hint: "TASK_DESCRIPTION [--max-loops N] [--timeout S]"
allowed-tools: ["Bash(powershell.exe -ExecutionPolicy Bypass -File:*)"]
---

# Shark Loop (External Enforcer)

Run the shark loop enforcer script which wraps `claude --print` with a hard OS-level timeout per turn.

## Instructions

Parse the arguments:
- The main text is the TASK_DESCRIPTION
- `--max-loops N` sets SHARK_MAX_LOOPS (default: 50)
- `--timeout S` sets SHARK_LOOP_TIMEOUT in seconds (default: 25)

Run the shark loop:

```
$env:SHARK_MAX_LOOPS = "<N>"
$env:SHARK_LOOP_TIMEOUT = "<S>"
powershell.exe -ExecutionPolicy Bypass -File "$SKILL_DIR/shark.ps1" "<TASK_DESCRIPTION>"
```

Report the result when complete.
