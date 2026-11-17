# VMEG on Cursor

For **macOS / Windows / Linux** — [Cursor](https://cursor.com/).

> **MCP settings**: search **MCP** or **Tools** in Command Palette, or see [Cursor docs](https://cursor.com/docs).

Common: [setup-common.md](setup-common.md) · [oauth.md](oauth.md) · Install: [install.md](install.md)

## Prerequisites

- Cursor installed (recent version with Remote MCP + OAuth)
- VMEG account: https://www.vmeg.ai
- Skill `vmeg-media-translation/` installed (see [install.md](install.md))

---

## Step 1: Install Skill

```bash
npx skills add Pixripple/vmeg-skills --skill vmeg-media-translation -g -a cursor -y
```

Manual path:

| Scope | macOS / Linux | Windows |
|-------|---------------|---------|
| **User (recommended)** | `~/.cursor/skills/vmeg-media-translation/` | `%USERPROFILE%\.cursor\skills\vmeg-media-translation\` |
| **Project** | `<project>/.cursor/skills/vmeg-media-translation/` | `<project>\.cursor\skills\vmeg-media-translation\` |

Create `skills` directory if missing, copy folder, restart Cursor.

---

## Step 2: Configure MCP

### Config file location

| Scope | macOS / Linux | Windows |
|-------|---------------|---------|
| User (recommended) | `~/.cursor/mcp.json` | `%USERPROFILE%\.cursor\mcp.json` |
| Project | `<project>/.cursor/mcp.json` | `<project>\.cursor\mcp.json` |

Use OAuth or API Key example from [setup-common.md](setup-common.md).

OAuth example: [cursor-mcp-oauth.json.example](../assets/mcp-config-examples/cursor-mcp-oauth.json.example)  
API Key example: [cursor-mcp.json.example](../assets/mcp-config-examples/cursor-mcp.json.example)

### Connect

1. Save `mcp.json`
2. In Cursor **MCP UI** (Command Palette → search MCP), confirm **vmeg** appears
3. OAuth: click **Connect**, browser login → **select project**
4. Confirm connected and `vmeg_*` tools visible

Agent may read `~/.cursor/mcp.json` to verify user config.

---

## Step 3: Verify

Say "List my VMEG materials" → should call `vmeg_list_materials`.

---

## Troubleshooting (Cursor + VMEG)

| Symptom | Fix |
|---------|-----|
| No `.cursor/skills` | Create manually |
| No Connect button | Save `mcp.json`; check MCP logs in Output panel |
| Browser did not open | Disconnect then Connect again in MCP UI |
| Skill but no tool calls | Confirm MCP connected; use Agent mode |

More: [oauth.md](oauth.md) · [tools.md](tools.md)
