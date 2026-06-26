# LDM OS v0.4.7

Three fixes from dogfood:

1. MCP registration strips `/tmp/` clone prefixes (`wip-install-wip-1password` -> `wip-1password`). Closes #54 follow-up.
2. `ldm doctor --fix` cleans stale MCP entries from `~/.claude.json` (entries with `/tmp/` paths or clone prefix names).
3. `ldm status` shows pending npm updates. Reads from installed package.json, not stale registry. Closes #34.
4. `ldm stack list` shows full contents (component and MCP server names, not just counts). Closes #60.

## Issues closed

- Closes #34
- Closes #60
