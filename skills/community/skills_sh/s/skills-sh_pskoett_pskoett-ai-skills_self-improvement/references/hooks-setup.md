# Hook Setup Guide (Multi-Agent)

Configure automatic self-improvement triggers across AI coding agents. The same two scripts serve all supported agents:

- `scripts/activator.sh` — prompt-submit reminder to evaluate learnings
- `scripts/error-detector.sh` — post-tool error detection on shell commands

All supported agents deliver the hook payload as **JSON on stdin** (there is no `CLAUDE_TOOL_OUTPUT` environment variable anywhere). What differs per agent is the config file location, the event names, and whether hook output can inject context for the model:

| Agent | Config location | Prompt-submit event | Post-tool event | Can inject context? |
|-------|----------------|--------------------:|----------------:|---------------------|
| Claude Code | `.claude/settings.json` (project) or `~/.claude/settings.json` | `UserPromptSubmit` (plain stdout → context) | `PostToolUse`, matcher `Bash` (requires `additionalContext` JSON) | Yes |
| Codex CLI | `<repo>/.codex/hooks.json` or `~/.codex/hooks.json`, behind `[features] codex_hooks = true` in `config.toml` | `UserPromptSubmit` (plain stdout → developer context) | `PostToolUse`, matcher `Bash` (requires `additionalContext` JSON) | Yes |
| Copilot CLI / coding agent | `.github/hooks/*.json` (repo) or `~/.copilot/hooks/*.json` (personal) | `userPromptSubmitted` (output ignored) | `postToolUse`, no matcher (output ignored) | No — hooks are logging/policy only; use `.github/copilot-instructions.md` for the reminder |

`error-detector.sh` handles the payload differences itself: it reads `tool_response` (Claude Code / Codex) or `toolResult.textResultForLlm` plus `resultType` (Copilot), filters to shell tools in-script for agents without matchers, and emits the reminder as `hookSpecificOutput.additionalContext` JSON — a shape Claude Code and Codex both accept, and Copilot safely ignores.

## Install Location and Paths

The hook `command` must point at where the skill is actually installed:

| Install method | Script location |
|----------------|-----------------|
| `gh skill install` / `npx skills add` | `.claude/skills/self-improvement/scripts/` |
| Plugin bundle (Claude Code) | `${CLAUDE_PLUGIN_ROOT}/skills/self-improvement/scripts/` (plugin hooks only) |
| Repo vendored into project | `skills/self-improvement/scripts/` |

For Claude Code, anchor project-relative paths with `${CLAUDE_PROJECT_DIR}` — it expands to the project root regardless of working directory. Codex runs hook commands from the session `cwd`, which may be a subdirectory; resolve from the git root (`$(git rev-parse --show-toplevel)/...`) or use home-anchored paths.

## Claude Code Setup

Create `.claude/settings.json` in your project root (path shown for a `gh skill install` layout — adjust per the table above):

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PROJECT_DIR}/.claude/skills/self-improvement/scripts/activator.sh"
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
            "command": "${CLAUDE_PROJECT_DIR}/.claude/skills/self-improvement/scripts/error-detector.sh"
          }
        ]
      }
    ]
  }
}
```

Notes:

- `matcher` filters by tool name and applies to tool events like `PostToolUse`. `UserPromptSubmit` does not support matchers — it fires on every prompt.
- For user-level activation, put the same structure in `~/.claude/settings.json` with `~/.claude/skills/...` paths.
- For lower overhead, register only the UserPromptSubmit hook.

## Codex CLI Setup

Codex supports lifecycle hooks (experimental, currently not on Windows). Enable the feature flag in `~/.codex/config.toml`:

```toml
[features]
codex_hooks = true
```

Then create `<repo>/.codex/hooks.json` (loads when the project `.codex/` layer is trusted) or `~/.codex/hooks.json`:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"$(git rev-parse --show-toplevel)/.claude/skills/self-improvement/scripts/activator.sh\""
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
            "command": "\"$(git rev-parse --show-toplevel)/.claude/skills/self-improvement/scripts/error-detector.sh\"",
            "statusMessage": "Checking for command errors"
          }
        ]
      }
    ]
  }
}
```

Notes:

- Codex's `UserPromptSubmit` adds plain stdout as developer context, so `activator.sh` works unchanged.
- Codex's `PostToolUse` ignores plain stdout but accepts the same `hookSpecificOutput.additionalContext` JSON shape as Claude Code, which `error-detector.sh` emits.
- Adjust the script path to your install layout (the example assumes the skill is installed under `.claude/skills/`).

## GitHub Copilot Setup

Copilot supports hooks in `.github/hooks/*.json` (repo-wide) or `~/.copilot/hooks/*.json` (Copilot CLI personal), but hook output is **ignored** for `userPromptSubmitted` and `postToolUse` — hooks can log and enforce policy, not inject context. So for Copilot:

1. Keep the reminder in `.github/copilot-instructions.md` (this is the only channel that reaches the model):

```markdown
## Self-Improvement

After completing tasks that involved:
- Debugging non-obvious issues
- Discovering workarounds
- Learning project-specific patterns
- Resolving unexpected errors

Consider logging the learning to `.learnings/` using the format from the self-improvement skill.

For high-value learnings that would benefit other sessions, consider skill extraction.
```

2. Optionally register the detector for audit logging (its JSON output is discarded, which is harmless):

```json
{
  "version": 1,
  "hooks": {
    "postToolUse": [
      { "type": "command", "bash": "./.claude/skills/self-improvement/scripts/error-detector.sh" }
    ]
  }
}
```

## Verification

### Test Activator Hook (Claude Code / Codex)

1. Enable the hook configuration
2. Start a new session
3. Send any prompt
4. Verify you see `<self-improvement-reminder>` in the context

### Test Error Detector Hook

Standalone test with a fake Claude Code / Codex payload:

```bash
echo '{"tool_name":"Bash","tool_response":"ls: /nonexistent/path: No such file or directory"}' \
  | ./scripts/error-detector.sh
```

And with a fake Copilot payload (tool filter + failure path):

```bash
echo '{"toolName":"bash","toolResult":{"resultType":"failure","textResultForLlm":"npm ERR! missing script"}}' \
  | ./scripts/error-detector.sh
```

Expected: a JSON object containing `additionalContext` in both cases. In a live Claude Code or Codex session the reminder reaches the model on the next turn as injected context, not as visible transcript output.

### Dry Run Extract Script

```bash
./scripts/extract-skill.sh test-skill --dry-run
```

Expected output shows the skill scaffold that would be created.

## Troubleshooting

### Hook Not Triggering

1. **Check script permissions**: `chmod +x scripts/*.sh`
2. **Verify path**: confirm the path matches your install method (see Install Location and Paths) and is anchored (`${CLAUDE_PROJECT_DIR}`, git root, or absolute)
3. **Codex only**: confirm `codex_hooks = true` is set and the project `.codex/` layer is trusted
4. **Check settings location**: project vs user-level
5. **Restart session**: hooks are loaded at session start

### Permission Denied

```bash
chmod +x scripts/activator.sh scripts/error-detector.sh scripts/extract-skill.sh
```

### Too Much Overhead

Use the minimal setup (prompt-submit hook only), or edit `activator.sh` to output less text. Prompt-content filtering is not possible on any of the three agents: none of them support matchers on the prompt-submit event.

## Hook Output Budget

The activator is designed to be lightweight:
- **Target**: ~50-100 tokens per activation
- **Content**: Structured reminder, not verbose instructions
- **Format**: XML tags for easy parsing

## Security Considerations

- Hook scripts run with the agent's permissions
- The scripts only read the stdin payload and write text/JSON to stdout; they don't modify files or run project commands
- All hooks are opt-in (you must configure them explicitly)
- Codex project-local hooks only load when the project `.codex/` layer is trusted

## Disabling Hooks

Remove the relevant event key from the hooks config file, or delete the file. JSON does not support comments, so "commenting out" a section will break parsing of the whole file.
