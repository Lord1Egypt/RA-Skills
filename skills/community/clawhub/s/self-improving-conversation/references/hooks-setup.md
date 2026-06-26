# Hook Setup Guide

Configure automatic conversation self-improvement triggers for AI agents.

## Overview

Hooks enable proactive dialogue learning capture by injecting reminders at key moments:
- **UserPromptSubmit**: Reminder after each prompt to evaluate conversation learnings
- **PostToolUse (Bash)**: Dialogue error detection when conversation-related commands fail

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
            "command": "./skills/self-improving-conversation/scripts/activator.sh"
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
            "command": "./skills/self-improving-conversation/scripts/error-detector.sh"
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
            "command": "~/.claude/skills/self-improving-conversation/scripts/activator.sh"
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
            "command": "./skills/self-improving-conversation/scripts/activator.sh"
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
            "command": "./skills/self-improving-conversation/scripts/activator.sh"
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
## Conversation Self-Improvement

After handling dialogue interactions that involved:
- Tone mismatches or formality gaps
- Misunderstood user intent
- Failed escalation to human agent
- Context loss in multi-turn conversations
- Hallucinated facts or policies

Consider logging the learning to `.learnings/` using the format from the self-improving-conversation skill.

For proven conversational patterns, consider skill extraction.
```

## Verification

### Test Activator Hook

1. Enable the hook configuration
2. Start a new Claude Code session
3. Send any prompt
4. Verify you see `<conversation-self-improvement-reminder>` in the context

### Test Error Detector Hook

1. Enable PostToolUse hook for Bash
2. Run a command that produces dialogue error patterns
3. Verify you see `<dialogue-error-detected>` reminder

### Dry Run Extract Script

```bash
./skills/self-improving-conversation/scripts/extract-skill.sh test-skill --dry-run
```

## Troubleshooting

### Hook Not Triggering

1. **Check script permissions**: `chmod +x scripts/*.sh`
2. **Verify path**: Use absolute paths or paths relative to project root
3. **Check settings location**: Project vs user-level settings
4. **Restart session**: Hooks are loaded at session start

### Permission Denied

```bash
chmod +x ./skills/self-improving-conversation/scripts/activator.sh
chmod +x ./skills/self-improving-conversation/scripts/error-detector.sh
chmod +x ./skills/self-improving-conversation/scripts/extract-skill.sh
```

### Too Much Overhead

If the activator feels intrusive:

1. **Use minimal setup**: Only UserPromptSubmit, skip PostToolUse
2. **Add matcher filter**: Only trigger for conversation-related prompts:

```json
{
  "matcher": "dialogue|conversation|chatbot|intent|escalat",
  "hooks": [...]
}
```

## Hook Output Budget

The activator is designed to be lightweight:
- **Target**: ~50-100 tokens per activation
- **Content**: Structured reminder, not verbose instructions
- **Format**: XML tags for easy parsing

## Security Considerations

- Hook scripts run with the same permissions as Claude Code
- Scripts only output text; they don't modify files or run commands
- Error detector reads `CLAUDE_TOOL_OUTPUT` environment variable
- Treat `CLAUDE_TOOL_OUTPUT` as potentially sensitive; do not log or forward it verbatim
- All scripts are opt-in (you must configure them explicitly)
- Never log user PII from conversations into hook output

## Disabling Hooks

To temporarily disable without removing configuration:

1. **Comment out in settings** or
2. **Delete the settings file** — hooks won't run without configuration
