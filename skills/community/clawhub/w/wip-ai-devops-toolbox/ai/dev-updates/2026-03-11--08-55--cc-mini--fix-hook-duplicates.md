# Fix CC Hook duplicate detection in wip-install

**Date:** 2026-03-11 08:55 PST
**Author:** Claude Code (cc-mini)

## Problem

`wip-install` was adding duplicate CC Hook entries to `~/.claude/settings.json` on every install. The duplicate check compared exact command strings, but the same tool installed from different paths (repo clone, /tmp/, installed extension) produced different strings. After multiple installs, `settings.json` had 8 PreToolUse hooks when it should have had 2.

Three of the duplicate paths violated the "never run tools from repo clones" rule:
- Repo clone paths (`staff/Parker/Claude Code - Mini/repos/...`)
- Temp install paths (`/tmp/wip-install-...`)

## Fix

Changed `installClaudeCodeHook()` in `install.js`:

1. **Always prefer the installed extension path.** If `~/.ldm/extensions/<tool>/guard.mjs` exists, use that path in the hook command instead of the source path.
2. **Match by tool name, not exact command.** Existing hooks are found by checking if the command contains `/<toolName>/`, not by exact string comparison.
3. **Update instead of duplicate.** If a hook for the same tool already exists at a different path, update it to point to the installed location instead of adding a new entry.

## Files changed

- `tools/wip-universal-installer/install.js` ... `installClaudeCodeHook()` function rewritten

Closes #82
