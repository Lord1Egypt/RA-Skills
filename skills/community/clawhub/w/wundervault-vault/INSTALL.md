# Installing Wundervault Vault

## Prerequisites

- A Wundervault account — request early access via the [contact form](https://wundervault.com/contact)
- An agent configured in your Wundervault dashboard (Settings → Agents)
- Node.js / npm installed

## Step 1 — Install the MCP server

```bash
npm install -g @wundervault/mcp-server
```

Or install locally in your OpenClaw workspace:

```bash
cd ~/.openclaw/workspace
npm install @wundervault/mcp-server
```

## Step 2 — Run the onboarding script

In your Wundervault dashboard under **Settings → Agents**, create an agent and copy the setup URL (it includes the passphrase in the `#fragment`). Download the script, then run it:

```bash
curl -fsSL https://wundervault.com/onboard -o /tmp/wv-onboard.py
python3 /tmp/wv-onboard.py "https://wundervault.com/setup/agent/TOKEN#PASSPHRASE"
```

The script must be downloaded before running — pipe mode (`curl ... | python3`) is blocked. The script verifies its own ed25519 signature on startup and exits immediately if the check fails.

Pinned version, SHA-256 checksum, and the ed25519 public key for independent verification are available at [wundervault.com/install](https://wundervault.com/install).

The script will:
- Verify its own signature before doing anything else
- Decrypt your credentials locally (passphrase never sent to the server)
- Save them to `~/.wundervault/creds-{agent_name}.json`
- Auto-configure OpenClaw (`~/.openclaw/openclaw.json`) if present
- Clear any stale MCP session so the new credentials take effect immediately

## Multiple agents on the same machine

Each agent gets its own named credentials file (`~/.wundervault/creds-Byte.json`, `~/.wundervault/creds-Claude.json`, etc.). The onboarding script handles this automatically for OpenClaw.

For other clients (Claude Code, Cursor, Windsurf), set this env var in their MCP config to point at the right file:

```json
{
  "mcpServers": {
    "wundervault": {
      "command": "wundervault-mcp",
      "env": {
        "WUNDERVAULT_CREDENTIALS_FILE": "/home/youruser/.wundervault/creds-Claude.json"
      }
    }
  }
}
```

Common global MCP config locations:
- **Claude Code**: `~/.claude/mcp.json`
- **Cursor**: `~/.cursor/mcp.json`
- **Windsurf**: `~/.codeium/windsurf/mcp_config.json`

## Verify

Ask your agent:

> "List my vault secrets"

The agent should call `vault_entries_list` and show available entries.

## Self-Hosting

Wundervault is open-source and can be self-hosted. The onboarding script auto-detects the vault URL from the setup link, so no extra configuration is needed.
