# Hook Setup Guide

Configure automatic negotiation self-improvement reminders for AI agents.

## Overview

Hooks provide two optional automations:
- `UserPromptSubmit`: inject negotiation reminder
- `PostToolUse (Bash)`: detect negotiation risk signals in command output

Both are reminder-only.

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
            "command": "./skills/self-improving-negotiation/scripts/activator.sh"
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
            "command": "./skills/self-improving-negotiation/scripts/error-detector.sh"
          }
        ]
      }
    ]
  }
}
```

## Codex Setup

Use the same hook pattern in `.codex/settings.json`.

## Verification

```bash
bash ./skills/self-improving-negotiation/scripts/activator.sh
CLAUDE_TOOL_OUTPUT="deadlock and unresolved redline" bash ./skills/self-improving-negotiation/scripts/error-detector.sh
```

## Troubleshooting

1. Ensure script permissions:
   ```bash
   chmod +x ./skills/self-improving-negotiation/scripts/*.sh
   ```
2. Validate shell syntax:
   ```bash
   bash -n ./skills/self-improving-negotiation/scripts/activator.sh
   bash -n ./skills/self-improving-negotiation/scripts/error-detector.sh
   bash -n ./skills/self-improving-negotiation/scripts/extract-skill.sh
   ```
3. Use absolute paths if relative resolution fails.

## Safety

Hook scripts do not execute agreement actions.
They only emit reminders to log and review negotiation patterns.
