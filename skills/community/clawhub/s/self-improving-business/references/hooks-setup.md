# Business Hook Setup Guide

Configure automatic business self-improvement reminders for coding agents.

## Overview

Hooks can remind the agent to capture high-signal business administration findings:
- `UserPromptSubmit`: broad reminder after each prompt
- `PostToolUse` (Bash): pattern reminder from command output

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
            "command": "./skills/self-improving-business/scripts/activator.sh"
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
            "command": "./skills/self-improving-business/scripts/error-detector.sh"
          }
        ]
      }
    ]
  }
}
```

## Codex CLI Setup

Create `.codex/settings.json` with the same pattern.

## Verification

1. Start a new session.
2. Send a prompt and confirm activator output appears.
3. Run `echo "missed SLA and overdue approval"` and confirm detector reminder appears.

## Troubleshooting

- Ensure scripts are executable: `chmod +x scripts/*.sh`
- Confirm path is correct relative to project root
- Restart session after hook configuration updates

## Safety Boundary

Hooks are reminder-only and do not execute approvals, spending, commitments, payroll, or legal actions.
