# v1.8.0: Fix CC Hook duplicates, add GitHub Issues convention

## CC Hook duplicate detection fix

`wip-install` was adding duplicate PreToolUse hooks to `~/.claude/settings.json` every time it ran. After a few installs, there were 8 hooks when there should have been 2. The duplicates pointed to repo clones and `/tmp/` paths, violating the "never run tools from repo clones" rule.

The root cause: duplicate detection compared exact command strings. The same `guard.mjs` installed from different paths produced different strings, so each install added another entry.

The fix:
- Match existing hooks by tool name in the path, not exact command string
- Always prefer `~/.ldm/extensions/<tool>/guard.mjs` over source or temp paths
- If a hook for the same tool exists at a different path, update it instead of adding a duplicate

## GitHub Issues convention added to Dev Guide

We were tracking work in `ai/todos/` markdown files. Items got lost. GitHub Issues gives us tracking, cross-referencing, and visibility across agents.

Added to the public Dev Guide:
- When to use GitHub Issues vs `ai/todos/`
- Filing convention: `filed-by:<agent-id>` labels and attribution lines
- Public vs private issue routing: public issues are the front door, private issues are the workshop
- Agent ID naming convention: `[platform]-[agent]-[machine]`

Added to the private Dev Guide:
- `filed-by:cc-mini` (blue) and `filed-by:oc-lesa-mini` (purple) label details
- Org-wide deployment commands
- Incident note: Memory Crystal agent ID drift

Both labels deployed across all wipcomputer repos.
