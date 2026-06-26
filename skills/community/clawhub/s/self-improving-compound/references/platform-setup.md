# Platform setup

This skill is portable, but automation differs by environment.

## Manual use (works everywhere)

The safest baseline is manual activation:
1. determine the workspace root
2. run `python3 scripts/learnings.py --root /path/to/workspace <command>`
3. promote or extract only after the pattern is proven

## Claude Code / Claude-style hook configs

Example prompt-start reminder:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "/absolute/path/to/self-improving-compound/hooks/activator.sh"
          }
        ]
      }
    ]
  }
}
```

Example error reminder:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "/absolute/path/to/self-improving-compound/hooks/error-detector.sh"
          }
        ]
      }
    ]
  }
}
```

## Codex / other skills-aware CLIs

Use the same manual workflow unless your client supports equivalent command hooks.

## GitHub Copilot

When hooks are unavailable, add a compact reminder to `.github/copilot-instructions.md`:

```markdown
## Self-improvement
After solving non-obvious issues or learning project-specific conventions, consider logging the durable lesson to `learning/` and promoting proven rules into shared memory.
```

## OpenClaw

OpenClaw-specific notes:
- Set `OPENCLAW_WORKSPACE` so `--root` is optional.
- Keep `learning/` in the workspace root by default, not the skill directory.
- Set `SELF_IMPROVING_LEARNING_ROOT` only when several workspaces should share one lesson store.
- The `hooks/activator.sh` and `hooks/error-detector.sh` scripts are workspace-root aware.
- Bundled shell helpers require bash; POSIX `sh`-only hosts should call the Python CLI directly.
