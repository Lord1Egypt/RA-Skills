# Hook Setup Guide

Configure automatic supply chain self-improvement triggers for AI agents.

## Overview

Hooks enable proactive supply chain pattern capture by injecting reminders at key moments:
- **UserPromptSubmit**: Reminder after each prompt to evaluate supply chain learnings
- **PostToolUse (Bash)**: Error detection when supply chain commands reveal disruptions, stockouts, or delays

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
            "command": "./skills/self-improving-supply-chain/scripts/activator.sh"
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
            "command": "./skills/self-improving-supply-chain/scripts/error-detector.sh"
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
            "command": "~/.claude/skills/self-improving-supply-chain/scripts/activator.sh"
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
            "command": "./skills/self-improving-supply-chain/scripts/activator.sh"
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
            "command": "./skills/self-improving-supply-chain/scripts/activator.sh"
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
## Supply Chain Self-Improvement

After resolving supply chain issues, consider logging to `.learnings/`:
- Stockouts, delays, quality problems → SUPPLY_CHAIN_ISSUES.md
- Forecast misses, supplier risks, demand shifts → LEARNINGS.md
- Tool/capability requests → FEATURE_REQUESTS.md

Promote recurring patterns to supplier scorecards, safety stock policies, or routing playbooks.
```

## Verification

### Test Activator Hook

1. Enable the hook configuration
2. Start a new Claude Code session
3. Send any prompt
4. Verify you see `<supply-chain-self-improvement-reminder>` in the context

### Test Error Detector Hook

1. Enable PostToolUse hook for Bash
2. Run a command that produces supply chain output with keywords like "stockout" or "backorder"
3. Verify you see `<supply-chain-disruption-detected>` reminder

### Dry Run Extract Script

```bash
./skills/self-improving-supply-chain/scripts/extract-skill.sh safety-stock-optimization --dry-run
```

## Troubleshooting

### Hook Not Triggering

1. **Check script permissions**: `chmod +x scripts/*.sh`
2. **Verify path**: Use absolute paths or paths relative to project root
3. **Check settings location**: Project vs user-level settings
4. **Restart session**: Hooks are loaded at session start

### Permission Denied

```bash
chmod +x ./skills/self-improving-supply-chain/scripts/activator.sh
chmod +x ./skills/self-improving-supply-chain/scripts/error-detector.sh
chmod +x ./skills/self-improving-supply-chain/scripts/extract-skill.sh
```

### Script Not Found

If using relative paths, ensure you're in the correct directory or use absolute paths:

```json
{
  "command": "/absolute/path/to/skills/self-improving-supply-chain/scripts/activator.sh"
}
```

### Too Much Overhead

If the activator feels intrusive:

1. **Use minimal setup**: Only UserPromptSubmit, skip PostToolUse
2. **Add matcher filter**: Only trigger for supply chain-related prompts:

```json
{
  "matcher": "inventory|supplier|forecast|shipment|warehouse|procurement|logistics",
  "hooks": [...]
}
```

## Hook Output Budget

The activator is designed to be lightweight:
- **Target**: ~50-100 tokens per activation
- **Content**: Structured supply chain-specific reminder, not verbose instructions
- **Format**: XML tags for easy parsing

## Security Considerations

- Hook scripts run with the same permissions as the agent
- Scripts only output text; they don't modify files or run commands
- Error detector reads `CLAUDE_TOOL_OUTPUT` environment variable
- Treat `CLAUDE_TOOL_OUTPUT` as potentially sensitive; do not log verbatim
- All scripts are opt-in
- Recommended default: enable `UserPromptSubmit` only; add `PostToolUse` when you want supply chain disruption detection
- No credentials, payment tokens, or procurement transaction permissions are required by this skill
- This skill does not place orders, execute purchases, or call external commerce APIs

## Disabling Hooks

To temporarily disable without removing configuration:

1. Comment out in settings
2. Or delete the settings file — hooks won't run without configuration
