# VMEG on Claude Code

For **macOS / Windows / Linux** — [Claude Code](https://docs.anthropic.com/en/docs/claude-code).

> MCP config entry: follow Claude Code official docs (Command Palette / project config).

Common: [setup-common.md](setup-common.md) · [oauth.md](oauth.md) · Install: [install.md](install.md)

## Prerequisites

- Claude Code installed
- VMEG account: https://www.vmeg.ai
- Skill `vmeg-media-translation/` (see [install.md](install.md))

---

## Step 1: Install Skill

```bash
npx skills add Pixripple/vmeg-skills --skill vmeg-media-translation -g -a claude-code -y
```

Manual path:

| Scope | macOS / Linux | Windows |
|-------|---------------|---------|
| User | `~/.claude/skills/vmeg-media-translation/` | `%USERPROFILE%\.claude\skills\vmeg-media-translation\` |
| Project | `<project>/.claude/skills/vmeg-media-translation/` | `<project>\.claude\skills\vmeg-media-translation\` |

---

## Step 2: Configure MCP

Create **`.mcp.json`** at project root (or user-level per Claude Code docs).

Claude Code requires `"type": "http"`:

### OAuth

```json
{
  "mcpServers": {
    "vmeg": {
      "type": "http",
      "url": "https://www.vmeg.ai/api/mcp"
    }
  }
}
```

Example: [claude-mcp-oauth.json.example](../assets/mcp-config-examples/claude-mcp-oauth.json.example)

### API Key

```json
{
  "mcpServers": {
    "vmeg": {
      "type": "http",
      "url": "https://www.vmeg.ai/api/mcp",
      "headers": {
        "Authorization": "Bearer vmeg_sk_YOUR_KEY"
      }
    }
  }
}
```

Example: [claude-mcp.json.example](../assets/mcp-config-examples/claude-mcp.json.example)

---

## Step 3: Verify

Say "List my VMEG materials" → `vmeg_list_materials`.

See [oauth.md](oauth.md), [tools.md](tools.md).
