# v0.2.0 ... Full Treatment

The 1Password plugin gets the full WIP treatment: standard SKILL.md, license compliance, reformatted README, and a new MCP server for Claude Code.

## What's New

### MCP Server for Claude Code (#10)
New `mcp-server.mjs` provides 1Password access directly from Claude Code via MCP. Uses the `op` CLI with service account token for headless access. Three tools: `op_read_secret`, `op_list_items`, `op_test`.

Register with:
```bash
claude mcp add --scope user wip-1password -- node /path/to/mcp-server.mjs
```

### SKILL.md (agentskills.io spec) (#2)
Root SKILL.md with proper frontmatter: lowercase-hyphen name, metadata block with display-name/version/homepage/author, openclaw install instructions, capability list.

### License Compliance (#4)
Dual MIT+AGPL via `wip-license-guard --from-standard`. CLA.md generated. Attribution in README.

### README Reformatted (#3)
README reformatted to WIP Computer standard via `wip-readme-format`. Technical content (quick start, agent tools, config resolution, developer guide) split to TECHNICAL.md.

## Interfaces

| Interface | File | Status |
|-----------|------|--------|
| Module | `dist/index.js` | Existing |
| OpenClaw Plugin | `openclaw.plugin.json` | Existing |
| Skill | `skills/op-secrets/SKILL.md` | Existing |
| MCP Server | `mcp-server.mjs` | **New** |
| Root Skill | `SKILL.md` | **New** |

## Closes
#2, #3, #4, #7, #10
