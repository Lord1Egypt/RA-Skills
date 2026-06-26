# Vorim AI — OpenClaw Skill

Identity, permissions, trust scores, and audit trails for your OpenClaw agent.

## Install

### Option 1: Copy the skill

Copy the `SKILL.md` file to your OpenClaw skills directory:

```bash
# Global (all workspaces)
mkdir -p ~/.openclaw/skills/vorim
cp SKILL.md ~/.openclaw/skills/vorim/

# Or workspace-specific
mkdir -p ./skills/vorim
cp SKILL.md ./skills/vorim/
```

### Option 2: Add the MCP server

Add Vorim's MCP server to your OpenClaw config:

```bash
mcporter add vorim --command "npx @vorim/mcp-server" --env VORIM_API_KEY=agid_sk_live_...
```

Or manually add to your MCP configuration:

```json
{
  "mcpServers": {
    "vorim": {
      "command": "npx",
      "args": ["-y", "@vorim/mcp-server"],
      "env": {
        "VORIM_API_KEY": "agid_sk_live_..."
      }
    }
  }
}
```

## Setup

1. Get a free API key at [vorim.ai](https://vorim.ai/login)
2. Set the environment variable: `VORIM_API_KEY=agid_sk_live_...`
3. On first use, the agent will register itself with Vorim and save its agent ID

## What It Does

Once installed, your OpenClaw agent will:

- **Check permissions** before taking sensitive actions (shell commands, emails, payments)
- **Log every action** with a tamper-proof audit trail
- **Verify its identity** when interacting with external services
- **Build a trust score** (0-100) based on behavioral history

## 17 MCP Tools Available

| Category | Tools |
|----------|-------|
| Identity | register, get, list, update, revoke |
| Permissions | check, grant, list, revoke |
| Audit | emit event, export signed bundle |
| Trust | verify trust score |
| Credentials | ephemeral agents, delegate, request token, list delegations |

## Links

- [Vorim AI](https://vorim.ai)
- [Documentation](https://vorim.ai/docs)
- [@vorim/mcp-server on npm](https://www.npmjs.com/package/@vorim/mcp-server)
- [OpenClaw](https://openclaw.ai)
