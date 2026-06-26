# Hook Setup Guide

Configure automatic verified-capability-evolver triggers for AI coding agents.

## Overview

Hooks enable proactive learning capture by injecting reminders at key moments:
- **UserPromptSubmit**: Reminder after each prompt to evaluate learnings
- **PostToolUse (Bash)**: Error detection when commands fail

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
            "command": "./skills/verified-capability-evolver/scripts/activator.sh"
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
            "command": "./skills/verified-capability-evolver/scripts/error-detector.sh"
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
            "command": "~/.claude/skills/verified-capability-evolver/scripts/activator.sh"
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
            "command": "./skills/verified-capability-evolver/scripts/activator.sh"
          }
        ]
      }
    ]
  }
}
```

## Codex CLI Setup

Codex uses the same hook system as Claude Code. Create `.codex/settings.json`:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "./skills/verified-capability-evolver/scripts/activator.sh"
          }
        ]
      }
    ]
  }
}
```

## GitHub Copilot Setup

Copilot doesn't support hooks directly. Instead, add guidance to `.github/copilot-instructions.md`:

```markdown
## Verified Capability Evolver

After completing tasks that involved:
- Debugging non-obvious issues
- Discovering workarounds
- Learning project-specific patterns
- Resolving unexpected errors

Consider logging the learning to `.learnings/` using the format from the verified-capability-evolver skill.

For high-value learnings that would benefit other sessions, consider skill extraction.
```


## Verification Gate

When a learning is likely to become permanent behavior, define a deterministic verification spec and promote only after verification returns PASS.

## Verification

### Test Activator Hook

1. Enable the hook configuration
2. Start a new Claude Code session
3. Send any prompt
4. Verify you see `<verified-capability-evolver-reminder>` in the context

### Test Error Detector Hook

1. Enable PostToolUse hook for Bash
2. Run a command that fails: `ls /nonexistent/path`
3. Verify you see `<error-detected>` reminder

### Dry Run Extract Script

```bash
./skills/verified-capability-evolver/scripts/extract-skill.sh test-skill --dry-run
```

Expected output shows the skill scaffold that would be created.

## Troubleshooting

### Hook Not Triggering

1. **Check script permissions**: `chmod +x scripts/*.sh`
2. **Verify path**: Use absolute paths or paths relative to project root
3. **Check settings location**: Project vs user-level settings
4. **Restart session**: Hooks are loaded at session start

### Permission Denied

```bash
chmod +x ./skills/verified-capability-evolver/scripts/activator.sh
chmod +x ./skills/verified-capability-evolver/scripts/error-detector.sh
chmod +x ./skills/verified-capability-evolver/scripts/extract-skill.sh
```

### Script Not Found

If using relative paths, ensure you're in the correct directory or use absolute paths:

```json
{
  "command": "/absolute/path/to/skills/verified-capability-evolver/scripts/activator.sh"
}
```

### Too Much Overhead

If the activator feels intrusive:

1. **Use minimal setup**: Only UserPromptSubmit, skip PostToolUse
2. **Add matcher filter**: Only trigger for certain prompts:

```json
{
  "matcher": "fix|debug|error|issue",
  "hooks": [...]
}
```

## Hook Output Budget

The activator is designed to be lightweight:
- **Target**: ~50-100 tokens per activation
- **Content**: Structured reminder, not verbose instructions
- **Format**: XML tags for easy parsing

If you need to reduce overhead further, you can edit `activator.sh` to output less text.

## Security Considerations

- Hook scripts run with the same permissions as Claude Code
- Scripts only output text; they don't modify files or run commands
- Error detector reads `CLAUDE_TOOL_OUTPUT` environment variable
- All scripts are opt-in (you must configure them explicitly)

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
