# Hook Setup Guide

Configure automatic finance self-improvement triggers for AI coding agents.

## Overview

Hooks enable proactive finance-pattern capture by injecting reminders at key moments:
- **UserPromptSubmit**: Reminder after each prompt to evaluate finance learnings
- **PostToolUse (Bash)**: Detection when reconciliation, variance, or control-related output appears

## Claude Code Setup

### Option 1: Project-Level Configuration

Create `.claude/settings.json` in your project root:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "./skills/self-improving-finance/scripts/activator.sh"
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
            "command": "./skills/self-improving-finance/scripts/error-detector.sh"
          }
        ]
      }
    ]
  }
}
```

### Option 2: User-Level Configuration

Add to `~/.claude/settings.json` for global activation:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/skills/self-improving-finance/scripts/activator.sh"
          }
        ]
      }
    ]
  }
}
```

### Minimal Setup (Activator Only)

For lower overhead, use only the UserPromptSubmit hook:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "./skills/self-improving-finance/scripts/activator.sh"
          }
        ]
      }
    ]
  }
}
```

## Codex CLI Setup

Codex uses the same hook system. Create `.codex/settings.json`:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "./skills/self-improving-finance/scripts/activator.sh"
          }
        ]
      }
    ]
  }
}
```

## GitHub Copilot Setup

Copilot doesn't support hooks. Add guidance to `.github/copilot-instructions.md`:

```markdown
## Finance Self-Improvement

After identifying finance issues, consider logging to `.learnings/`:
- Reconciliation breaks, control failures, variance analysis → FINANCE_ISSUES.md
- Control weaknesses, regulatory gaps, valuation errors → LEARNINGS.md
- Tool/capability requests → FEATURE_REQUESTS.md

Always anonymize data. Never log real account numbers, bank details, or client names.
Promote recurring patterns to close checklists or control matrices.
```

## Verification

### Test Activator Hook

1. Enable the hook configuration
2. Start a new Claude Code session
3. Send any prompt
4. Verify you see `<finance-self-improvement-reminder>` in the context

### Test Error Detector Hook

1. Enable PostToolUse hook for Bash
2. Run a command that produces reconciliation-related output
3. Verify you see `<finance-issue-detected>` reminder

### Dry Run Extract Script

```bash
./skills/self-improving-finance/scripts/extract-skill.sh test-skill --dry-run
```

## Troubleshooting

### Hook Not Triggering

1. **Check script permissions**: `chmod +x scripts/*.sh`
2. **Verify path**: Use absolute paths or paths relative to project root
3. **Check settings location**: Project vs user-level settings
4. **Restart session**: Hooks are loaded at session start

### Permission Denied

```bash
chmod +x ./skills/self-improving-finance/scripts/activator.sh
chmod +x ./skills/self-improving-finance/scripts/error-detector.sh
chmod +x ./skills/self-improving-finance/scripts/extract-skill.sh
```

### Script Not Found

If using relative paths, ensure you're in the correct directory or use absolute paths:

```json
{
  "command": "/absolute/path/to/skills/self-improving-finance/scripts/activator.sh"
}
```

### Too Much Overhead

If the activator feels intrusive:

1. **Use minimal setup**: Only UserPromptSubmit, skip PostToolUse
2. **Add matcher filter**: Only trigger for finance-related prompts:

```json
{
  "matcher": "reconcil|variance|close|audit|SOX|budget|forecast",
  "hooks": [...]
}
```

## Hook Output Budget

The activator is designed to be lightweight:
- **Target**: ~50-100 tokens per activation
- **Content**: Structured finance-specific reminder, not verbose instructions
- **Format**: XML tags for easy parsing

## Security Considerations

- Hook scripts run with the same permissions as the agent
- Scripts only output text; they don't modify files or run commands
- Error detector reads `CLAUDE_TOOL_OUTPUT` environment variable
- Treat `CLAUDE_TOOL_OUTPUT` as potentially sensitive — it may contain financial data; do not log verbatim
- All scripts are opt-in
- Recommended default: enable `UserPromptSubmit` only; add `PostToolUse` when you want reconciliation/variance/control detection

## Disabling Hooks

To temporarily disable without removing configuration:

1. Comment out in settings
2. Or delete the settings file — hooks won't run without configuration
