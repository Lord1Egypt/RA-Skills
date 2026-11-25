# Installing Wundervault Vault

You need a free account at [wundervault.com](https://wundervault.com), Node.js 22.23.4, 24.22.1
or 26.12.1 or newer (the October 21, 2026 security fix; the helper app won't start on an older Node),
and administrator rights on this computer. Every step:
[wundervault.com/help/computer](https://wundervault.com/help/computer).

## 1. Install the package and the helper app (administrator, once per computer)

Linux:

```bash
sudo npm install -g @wundervault/mcp-server@2
sudo sh "$(npm root -g)/@wundervault/mcp-server/packaging/install-daemon.sh"
```

`sudo` for both, because the helper app only runs a copy installed in a system folder, never one
inside your home folder.

Windows and macOS: [wundervault.com/install](https://wundervault.com/install).
The installer downloads nothing and is short enough to read first.

## 2. Pair it with your account

Run the pairing command the installer printed last. It names node and the helper app by their
full paths, for example:

```bash
sudo /opt/wundervault/current/node /opt/wundervault/current/app/bin/wundervault-agent --pair
```

Full paths, because with `sudo` a bare name could be found in a folder your agents can write.

Check that the fingerprint it shows matches the one in your vault, then confirm there.

## 3. Add the agent

In your vault, add an agent and choose this computer. You get a **message for your agent** with a
claim code in it. Paste the message into the agent's chat and it does the rest: a claim code
isn't a secret, works once, only through the helper app on this computer, for 15 minutes.

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

## 4. Check

Ask the agent: "List my vault secrets." It should call `vault_entries_list` and show what you
gave it. No secrets yet is normal until you give it some: open a secret in your vault and turn the
agent on.

## Upgrading from version 1

Version 2 moves secrets into the helper app; your account and vault carry over. Install version 2
and the helper app (steps 1-2), then **Repair** each agent in your vault and enrol it (step 3). The
steps, in full: [wundervault.com/install#upgrade-to-2](https://wundervault.com/install#upgrade-to-2).

## Updating

When a new version is out, your vault's Computers page shows **Update now**: one press updates the
helper app on that computer. What changed: [wundervault.com/changelog](https://wundervault.com/changelog);
releases are announced on X as [@wundervault1](https://x.com/wundervault1).
