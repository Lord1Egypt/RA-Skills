# LDM OS Interface Detection

When you run `ldm install`, it automatically detects what a repo supports:

| Interface | How it's detected | Where it deploys |
|-----------|------------------|-----------------|
| CLI | `package.json` has `bin` entries | `npm install -g` |
| MCP Server | Has `mcp-server.mjs` or `mcp-server.js` | `claude mcp add --scope user` |
| OpenClaw Plugin | Has `openclaw.plugin.json` | `~/.ldm/extensions/` + `~/.openclaw/extensions/` |
| Skill | Has `SKILL.md` or `skills/` directory | `~/.openclaw/skills/` |
| CC Hook | Has `guard.mjs` or `claudeCode.hook` in package.json | `~/.claude/settings.json` |
| Module | Has `main` or `exports` in package.json | Importable via `node_modules` |

No manual configuration needed. Point it at a repo and it figures out the rest.
