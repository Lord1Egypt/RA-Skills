# LDM OS Boot Sequence Hook

SessionStart hook for Claude Code. Reads boot files and injects them into the agent's context before the first user message. No dependencies. No build step.

## What It Does

Reads 9 files from the Dream Weaver Boot Sequence (SHARED-CONTEXT.md, SOUL.md, CONTEXT.md, daily logs, journals, repo-locations.md) and injects them as `additionalContext` in the SessionStart response. The agent wakes up already knowing who it is, what's happening, and where things live.

## Content Budget

Large files are line-capped and stale journals are dropped to path-only lines, so the payload stays small. Missing files are skipped gracefully. The last line of every boot payload is a one-line summary (`== Boot payload: N bytes, M lines, K sections. Capped: ... Stale/path-only: ... ==`) so future slowness triage is trivial.

### Per-step line caps

Every step has a line cap. If `boot-config.json` sets `maxLines` for a step, that wins. Otherwise these code defaults apply. They live in `boot-hook.mjs`, not just the config template, because the installer preserves an existing user `boot-config.json` and never overwrites it, so a config-only change would never reach existing installs:

- `sharedContext`: 80
- `soul`: 80
- `context`: 60
- `repoLocations`: 80

When a file is truncated, the injected content ends with a marker naming the full path so the rest can be read on demand.

### Staleness cutoffs

`most-recent` steps (journals) inject the newest dated file only if it is fresh. If the newest file is older than `stalenessDays` (default 14, overridable top-level or per-step), the body is NOT injected: a single line with the file path, date, and age is emitted instead. This stops a four-month-old "most recent" journal from being re-injected every session.

`daily-logs` steps have the same guard via `dailyLogStalenessDays` (default 2). Day files are today/yesterday by construction, so this is defensive.

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

Optional keys:

- Top-level `stalenessDays` (default 14) and `dailyLogStalenessDays` (default 2): staleness cutoffs for `most-recent` and `daily-logs` steps. Per-step keys of the same name override the top-level value.
- Per-step `maxLines`: line cap for that step. Overrides the code default (see Content Budget).
- Top-level `maxTotalLines` (default 2000): hard safety cap across all steps.

## Adding a Boot Step

1. Add an entry to `boot-config.json` under `steps`
2. Set `path` (single file) or `dir` + `strategy` (directory scan)
3. Set `stepNumber`, `label`, and optionally `maxLines` and `critical`
4. The hook picks it up automatically. No code changes needed.

## Error Philosophy

Partial boot > no boot > blocked session. The hook exits 0 no matter what. Missing files are logged to stderr and skipped. The session always starts.
