---
name: shark-loop
description: "Run shark.ps1/shark.sh loop enforcer with OS-level timeout per turn"
---

# Shark Loop (External Enforcer)

Run the shark loop enforcer script which wraps `claude --print` with a hard OS-level timeout per turn.

## Instructions

Parse the arguments:
- The main text is the TASK_DESCRIPTION
- `--max-loops N` sets SHARK_MAX_LOOPS (default: 50)
- `--timeout S` sets SHARK_LOOP_TIMEOUT in seconds (default: 25)

On Windows, run:
```
$env:SHARK_MAX_LOOPS = "<N>"
$env:SHARK_LOOP_TIMEOUT = "<S>"
powershell.exe -ExecutionPolicy Bypass -File "$SKILL_DIR/../shark.ps1" "<TASK_DESCRIPTION>"
```

On Linux/Mac, run:
```
SHARK_MAX_LOOPS=<N> SHARK_LOOP_TIMEOUT=<S> bash "$SKILL_DIR/../shark.sh" "<TASK_DESCRIPTION>"
```

Report the result when complete.
