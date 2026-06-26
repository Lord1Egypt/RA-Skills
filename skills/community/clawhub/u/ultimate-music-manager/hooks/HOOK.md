---
name: sonic-phoenix-safety-guard
description: "Intercepts destructive Sonic Phoenix scripts and injects a confirmation warning"
metadata: {"openclaw":{"emoji":"🛡️","events":["PreToolUse"]}}
---

# Safety Guard Hook

Prevents accidental execution of destructive utility scripts in the Sonic Phoenix pipeline.

## What It Does

- Fires on `PreToolUse` for Bash commands
- Checks if the command references a destructive script (`05D`, `05F`, `total_scrub`, `absolute_zero_sort`)
- If matched, injects a warning reminding the agent to confirm with the user before proceeding
- Silent (zero output) for all non-destructive commands — no overhead

## Destructive Scripts Guarded

| Script | What It Deletes |
| ------ | --------------- |
| `05D_force_delete_residue.py` | Entire `Unidentified/` directory |
| `05F_final_scrub.py` | Garbage files outside `Sorted/` |
| `total_scrub.py` | Everything under `MUSIC_ROOT` except protected directories |
| `absolute_zero_sort.py` | `Unidentified/` tree after sorting matched files out |

## Configuration

### Claude Code

Add to `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "./ultimate-music-manager/hooks/safety-guard.sh"
      }]
    }]
  }
}
```

### OpenClaw

```bash
openclaw hooks enable sonic-phoenix-safety-guard
```
