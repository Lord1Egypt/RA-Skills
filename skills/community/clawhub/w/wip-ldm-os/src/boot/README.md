# LDM OS Boot Sequence Hook

SessionStart hook for Claude Code. Reads boot files and injects them into the agent's context before the first user message. No dependencies. No build step.

## What It Does

Reads 9 files from the Dream Weaver Boot Sequence (SHARED-CONTEXT.md, SOUL.md, CONTEXT.md, daily logs, journals, repo-locations.md) and injects them as `additionalContext` in the SessionStart response. The agent wakes up already knowing who it is, what's happening, and where things live.

## Content Budget

~700 lines, ~3,500 tokens. Under 2% of the context window. Large files (journals, daily logs) are truncated. Missing files are skipped gracefully.

## Deploy

```bash
mkdir -p ~/.ldm/shared/boot
cp src/boot/boot-hook.mjs ~/.ldm/shared/boot/
cp src/boot/boot-config.json ~/.ldm/shared/boot/
```

Then add to `~/.claude/settings.json` inside the `hooks` object:

```json
"SessionStart": [
  {
    "matcher": "*",
    "hooks": [
      {
        "type": "command",
        "command": "node /Users/lesa/.ldm/shared/boot/boot-hook.mjs",
        "timeout": 15
      }
    ]
  }
]
```

Restart Claude Code to pick up the hook.

## Test

```bash
echo '{"session_id":"test","hook_event_name":"SessionStart"}' | node ~/.ldm/shared/boot/boot-hook.mjs
```

Should output JSON with `hookSpecificOutput.additionalContext` containing all boot content. Check stderr for the load summary.

## Config

`boot-config.json` defines paths and limits for each boot step. Uses `~` shorthand (resolved at runtime). To support a different agent (cc-air), deploy a different config alongside the same script.

## Adding a Boot Step

1. Add an entry to `boot-config.json` under `steps`
2. Set `path` (single file) or `dir` + `strategy` (directory scan)
3. Set `stepNumber`, `label`, and optionally `maxLines` and `critical`
4. The hook picks it up automatically. No code changes needed.

## Error Philosophy

Partial boot > no boot > blocked session. The hook exits 0 no matter what. Missing files are logged to stderr and skipped. The session always starts.
