# Installing Wundervault Vault

You need a free account at [wundervault.com](https://wundervault.com), Node.js 22.23.4, 24.22.1
or 26.12.1 or newer (the October 21, 2026 security fix; the broker won't start on an older Node),
and administrator rights on this computer. Every step:
[wundervault.com/help/computer](https://wundervault.com/help/computer).

## 1. Install the package

```bash
npm install -g @wundervault/mcp-server@2
```

## 2. Install the broker (administrator, once per computer)

Linux:

```bash
sudo sh "$(npm root -g)/@wundervault/mcp-server/packaging/install-daemon.sh"
```

Windows and macOS: [wundervault.com/install](https://wundervault.com/install).
The installer downloads nothing and is short enough to read first.

## 3. Pair it with your account

Use the full paths the installer printed in its last step. They usually are:

```bash
sudo /usr/bin/node /usr/bin/wundervault-agent --pair              # Linux
sudo /usr/local/bin/node /usr/local/bin/wundervault-agent --pair  # macOS
```

Full paths, because with `sudo` a bare name could be found in a folder your agents can write.

Check that the fingerprint it shows matches the one in your vault, then confirm there.

## 4. Add the agent

In your vault, add an agent and choose this computer. You get a **message for your agent** with a
claim code in it. Paste the message into the agent's chat and it does the rest: a claim code
isn't a secret, works once, only through the broker on this computer, for 15 minutes.

Or do it yourself. Enrol, piping the code in (never as an argument):

```bash
printf '%s\n' 'WV-XXXX-XXXX' | wundervault-agent --enrol
```

Then add Wundervault to the agent's MCP settings. `WUNDERVAULT_AGENT_NAME` must match the
agent's name in your vault exactly (enrol prints it). OpenClaw:

```bash
openclaw mcp add wundervault --command wundervault-mcp --env 'WUNDERVAULT_AGENT_NAME=<name>'
```

Other clients take this block: Claude Code `~/.claude.json` (or `claude mcp add`), Cursor
`~/.cursor/mcp.json`, Windsurf `~/.codeium/windsurf/mcp_config.json`.

```json
{
  "mcpServers": {
    "wundervault": {
      "command": "wundervault-mcp",
      "env": { "WUNDERVAULT_AGENT_NAME": "<the agent's name in your vault>" }
    }
  }
}
```

The config holds no secrets. An app that starts several copies of the vault tool for one agent
(several chats, or OpenClaw's gateway and its Codex runtime) is fine: copies of one agent share
its connection.

## 5. Check

Ask the agent: "List my vault secrets." It should call `vault_entries_list` and show what you
gave it. No secrets yet is normal until you give it some: open a secret in your vault and turn the
agent on.

## Upgrading from version 1

Version 2 moves secrets into the broker; your account and vault carry over. Install version 2 and
the broker (steps 1-3), then **Repair** each agent in your vault and enrol it (step 4). The
steps, in full: [wundervault.com/install#upgrade-to-2](https://wundervault.com/install#upgrade-to-2).
