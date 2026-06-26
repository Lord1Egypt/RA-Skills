# Domotics Hook Setup Guide

Configure optional hooks for domotics self-improvement reminders.

## Overview

Hooks help maintain logging discipline:
- `UserPromptSubmit`: injects reminder to evaluate `LRN` / `DOM` / `FEAT`
- `PostToolUse (Bash)`: scans tool output for high-signal domotics failure patterns

All hooks are reminder-only and must not execute direct physical actions.

## Claude Code Setup

Create `.claude/settings.json`:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "./skills/self-improving-domotics/scripts/activator.sh"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "./skills/self-improving-domotics/scripts/error-detector.sh"
          }
        ]
      }
    ]
  }
}
```

## Codex Setup

Use equivalent settings file and same script paths.

## Verification

```bash
chmod +x ./skills/self-improving-domotics/scripts/*.sh
bash -n ./skills/self-improving-domotics/scripts/activator.sh
bash -n ./skills/self-improving-domotics/scripts/error-detector.sh
bash -n ./skills/self-improving-domotics/scripts/extract-skill.sh
```

Start a new session and confirm reminder tags appear.

## Troubleshooting

1. Check script permissions.
2. Validate relative paths from project root.
3. Restart the session after hook config changes.
4. If overhead is too high, keep only `UserPromptSubmit`.

## Safety Notes

- Hook output should stay concise.
- Avoid logging secrets, lock codes, or personal occupancy schedules.
- Keep automation commands out of hook scripts; reminders only.
