# Security Hook Setup Guide

Configure automatic security self-improvement triggers for AI coding agents.

## Overview

Hooks can help capture security findings with minimal overhead:
- **UserPromptSubmit** (recommended): Reminder after each prompt to evaluate security findings
- **PostToolUse (Bash)** (optional): Detection when high-signal security patterns appear in command output (trusted environments only)

## Claude Code Setup

### Option 1: Project-Level Configuration

Create `.claude/settings.json` in your project root (activator-only recommended):

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "./skills/self-improving-security/scripts/activator.sh"
          }
        ]
      }
    ]
  }
}
```

### Optional: Add PostToolUse Error Detector

Enable this only when you explicitly want command-output pattern checks in trusted environments:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "./skills/self-improving-security/scripts/error-detector.sh"
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
            "command": "~/.claude/skills/self-improving-security/scripts/activator.sh"
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
            "command": "./skills/self-improving-security/scripts/activator.sh"
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
            "command": "./skills/self-improving-security/scripts/activator.sh"
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
## Security Self-Improvement

After completing tasks that involved:
- Reviewing or modifying authentication/authorization code
- Working with secrets, credentials, or environment variables
- Configuring cloud resources or network policies
- Addressing vulnerability scan findings
- Handling compliance requirements

Consider logging the finding to `.learnings/` using the security self-improvement skill format.

CRITICAL: NEVER include actual secrets, credentials, tokens, or PII in learning entries.
Always redact sensitive values before documenting.
```

## Verification

### Test Activator Hook

1. Enable the hook configuration
2. Start a new Claude Code session
3. Send any prompt
4. Verify you see `<security-improvement-reminder>` in the context

### Test Error Detector Hook

1. Enable PostToolUse hook for Bash
2. Run a command that produces security-relevant output: `curl -k https://expired.badssl.com/`
3. Verify you see `<security-finding-detected>` reminder

### Dry Run Extract Script

```bash
./skills/self-improving-security/scripts/extract-skill.sh test-skill --dry-run
```

## Troubleshooting

### Hook Not Triggering

1. **Check script permissions**: `chmod +x scripts/*.sh`
2. **Verify path**: Use absolute paths or paths relative to project root
3. **Check settings location**: Project vs user-level settings
4. **Restart session**: Hooks are loaded at session start

### Permission Denied

```bash
chmod +x ./skills/self-improving-security/scripts/activator.sh
chmod +x ./skills/self-improving-security/scripts/error-detector.sh
chmod +x ./skills/self-improving-security/scripts/extract-skill.sh
```

### Script Not Found

If using relative paths, ensure you're in the correct directory or use absolute paths:

```json
{
  "command": "/absolute/path/to/skills/self-improving-security/scripts/activator.sh"
}
```

### Too Much Overhead

If the activator feels intrusive:

1. **Use minimal setup**: Only UserPromptSubmit, skip PostToolUse
2. **Add matcher filter**: Only trigger for security-related prompts:

```json
{
  "matcher": "security|vuln|CVE|auth|permission|secret|credential|compliance",
  "hooks": [...]
}
```

## Hook Output Budget

The activator is designed to be lightweight:
- **Target**: ~80-120 tokens per activation
- **Content**: Structured reminder with security-specific guidance
- **Format**: XML tags for easy parsing

## Security Considerations

- Hook scripts run with the same permissions as Claude Code
- Scripts only output text; they do not modify files or run commands
- Error detector reads `CLAUDE_TOOL_OUTPUT` environment variable
- Treat `CLAUDE_TOOL_OUTPUT` as potentially sensitive — **never log or forward it verbatim**
- All scripts are opt-in (you must configure them explicitly)
- Recommended default: enable `UserPromptSubmit` only
- No credentials or access tokens are required by this skill

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
