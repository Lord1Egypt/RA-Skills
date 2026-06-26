# Hook Setup Guide (Science)

Configure automatic self-improvement triggers for scientific research and ML workflows.

## Overview

Hooks enable proactive learning capture by injecting reminders at key moments:
- **UserPromptSubmit**: Reminder after each prompt to evaluate experiment learnings
- **PostToolUse (Bash)**: ML/data error detection when commands fail

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
            "command": "./skills/self-improving-science/scripts/activator.sh"
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
            "command": "./skills/self-improving-science/scripts/error-detector.sh"
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
            "command": "~/.claude/skills/self-improving-science/scripts/activator.sh"
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
            "command": "./skills/self-improving-science/scripts/activator.sh"
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
            "command": "./skills/self-improving-science/scripts/activator.sh"
          }
        ]
      }
    ]
  }
}
```

## GitHub Copilot Setup

Copilot doesn't support hooks directly. Add guidance to `.github/copilot-instructions.md`:

```markdown
## Self-Improvement (Science)

After completing tasks that involved:
- Debugging data quality issues or leakage
- Fixing statistical test misapplication
- Resolving model training failures
- Discovering reproducibility problems
- Revising hypotheses based on results

Consider logging the learning to `.learnings/` using the self-improving-science format.

For high-value learnings, promote to experiment checklists, model cards, or methodology standards.
```

## Verification

### Test Activator Hook

1. Enable the hook configuration
2. Start a new Claude Code session
3. Send any prompt
4. Verify you see `<science-improvement-reminder>` in the context

### Test Error Detector Hook

1. Enable PostToolUse hook for Bash
2. Run a command that produces ML errors: `python -c "import torch; torch.tensor([1.0]) / torch.tensor([0.0])"`
3. Verify you see `<science-error-detected>` reminder

### Dry Run Extract Script

```bash
./skills/self-improving-science/scripts/extract-skill.sh test-skill --dry-run
```

## Troubleshooting

### Hook Not Triggering

1. **Check script permissions**: `chmod +x scripts/*.sh`
2. **Verify path**: Use absolute paths or paths relative to project root
3. **Check settings location**: Project vs user-level settings
4. **Restart session**: Hooks are loaded at session start

### Permission Denied

```bash
chmod +x ./skills/self-improving-science/scripts/activator.sh
chmod +x ./skills/self-improving-science/scripts/error-detector.sh
chmod +x ./skills/self-improving-science/scripts/extract-skill.sh
```

### Script Not Found

If using relative paths, ensure you're in the correct directory or use absolute paths:

```json
{
  "command": "/absolute/path/to/skills/self-improving-science/scripts/activator.sh"
}
```

### Too Much Overhead

If the activator feels intrusive:

1. **Use minimal setup**: Only UserPromptSubmit, skip PostToolUse
2. **Add matcher filter**: Only trigger for experiment-related prompts:

```json
{
  "matcher": "train|model|experiment|data|analysis|test",
  "hooks": [...]
}
```

## Hook Output Budget

The activator is designed to be lightweight:
- **Target**: ~60-120 tokens per activation
- **Content**: Structured reminder with science-specific triggers
- **Format**: XML tags for easy parsing

## Security Considerations

- Hook scripts run with the same permissions as Claude Code
- Scripts only output text; they don't modify files or run commands
- Error detector reads `CLAUDE_TOOL_OUTPUT` environment variable
- Treat `CLAUDE_TOOL_OUTPUT` as potentially sensitive; do not log or forward it verbatim
- All scripts are opt-in (you must configure them explicitly)
- Recommended default: enable `UserPromptSubmit` only

## Disabling Hooks

To temporarily disable without removing configuration:

1. **Comment out in settings**:
```json
{
  "hooks": {
    // "UserPromptSubmit": [...]
  }
}
```

2. **Or delete the settings file**: Hooks won't run without configuration
