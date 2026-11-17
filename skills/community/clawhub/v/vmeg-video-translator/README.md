# VMEG Media Translation Skill

Video/audio/subtitle translation, materials and tasks, script editing, and export via VMEG Remote MCP in AI coding assistants and OpenClaw agents.

Supports **macOS / Windows / Linux**: Cursor, Claude Code, Windsurf, Codex, Gemini CLI, Antigravity, QoderWork, WorkBuddy, OpenClaw.

## Quick start

1. **Install Skill** — [references/install.md](references/install.md)
2. **Configure MCP** — `https://www.vmeg.ai/api/mcp` (OAuth or API Key; see [references/oauth.md](references/oauth.md))
3. **Connect in agent MCP settings** — Connect (OAuth) or confirm config is loaded
4. **Verify** — in Agent, say: "List my VMEG materials"

> Agents should **read only one** setup doc for the current platform.  
> Tool usage comes from **MCP server instructions**; overview: [references/tools.md](references/tools.md)

## Install

| Channel | Command |
|---------|---------|
| [skills.sh](https://skills.sh/) / Vercel | `npx skills add Pixripple/vmeg-skills --skill vmeg-media-translation -g -y` |
| [SkillsMP](https://skillsmp.com/) | Discover on site → install via `npx skills add` above |
| [ClawHub](https://clawhub.ai/) | `clawhub install vmeg-media-translation` |
| [LobeHub](https://lobehub.com/skills) | `npx -y @lobehub/market-cli skills install pixripple-vmeg-skills-vmeg-media-translation -g` |
| GitHub CLI | `gh skill install Pixripple/vmeg-skills vmeg-media-translation --agent cursor` |
| Manual | Copy this folder to your agent's `skills/` directory |

Full details: **[references/install.md](references/install.md)**

## Configure MCP

Common: [references/setup-common.md](references/setup-common.md) · Auth: [references/oauth.md](references/oauth.md) · Examples: [assets/mcp-config-examples/](assets/mcp-config-examples/)

| Method | Best for |
|--------|----------|
| OAuth | Individuals: URL in config, then **Connect** in MCP UI |
| API Key | Fixed `vmeg_sk_` secret |

## Supported platforms

| Platform | Setup (read only when Agent runs on that platform) |
|----------|-----------------------------------------------------|
| Cursor | [setup-cursor.md](references/setup-cursor.md) |
| Claude Code | [setup-claude-code.md](references/setup-claude-code.md) |
| Windsurf | [setup-windsurf.md](references/setup-windsurf.md) |
| Codex | [setup-codex.md](references/setup-codex.md) |
| Gemini CLI | [setup-gemini-cli.md](references/setup-gemini-cli.md) |
| Antigravity | [setup-antigravity.md](references/setup-antigravity.md) |
| QoderWork | [setup-qoderwork.md](references/setup-qoderwork.md) |
| WorkBuddy | [setup-workbuddy.md](references/setup-workbuddy.md) |
| OpenClaw | [setup-openclaw.md](references/setup-openclaw.md) |

## FAQ

**Where is MCP settings?**  
Search "MCP" in Command Palette / Settings, or see OpenClaw Control UI at `/settings/mcp`.

**MCP won't connect?**  
URL must be `https://www.vmeg.ai/api/mcp`; do not mix OAuth with API Key Header. See [oauth.md](references/oauth.md).

**Skill installed but Agent won't call tools?**  
Both Skill and MCP must be configured; confirm `vmeg` is connected in MCP UI.

**Local video upload (OAuth)?**  
`vmeg_initiate_material_upload` → curl PUT to presigned URL → `vmeg_complete_material_upload`. See [SKILL.md](SKILL.md) and [setup-common.md](references/setup-common.md).
