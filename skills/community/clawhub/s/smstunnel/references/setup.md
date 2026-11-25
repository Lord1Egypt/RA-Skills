# Setting up SMSTunnel for your agent

Three steps, done once by the user. The agent can guide them but must never ask for the key in the chat.

## 1. Link the phone

Install the SMSTunnel app from Google Play on the Android phone and sign in:
https://play.google.com/store/apps/details?id=io.smstunnel.app

Sign in at https://smstunnel.io on the computer with the same account. The phone appears under **Phones** (it can also be linked with the QR code from **Phones → Add phone**).

## 2. Create a key

In the dashboard (https://dashboard.smstunnel.io/apps), open **Apps → Add an app**, choose **MCP**, and copy the key. It is shown only once. Deleting it later cuts the agent off.

Two options on the key, both off by default:

- **Can also read received texts**, for `list_received_texts`. Syncing must also be turned on in the SMSTunnel app on the phone.
- **Can also look up names you saved in SMSTunnel**, for `find_contact`. It never covers the phone's contacts.

## 3. Give the agent the key and connect the server

The server is the npm package `@narcisbodea/smstunnel-mcp`, pinned here to a version you can review. It needs Node.js 20 or newer.

### OpenClaw

Keep the key in OpenClaw's environment, not in its settings: add a line `SMSTUNNEL_API_KEY=<your key>` to the `.env` file in your OpenClaw state folder (normally `~/.openclaw`), in an editor, and restart OpenClaw. Then:

```bash
openclaw mcp add smstunnel --command npx --arg -y --arg @narcisbodea/smstunnel-mcp@1.2.0 --env 'SMSTUNNEL_API_KEY=${SMSTUNNEL_API_KEY}' --approval prompt
openclaw mcp probe smstunnel
```

Keep the single quotes: OpenClaw fills in `${SMSTUNNEL_API_KEY}` when it starts the server, so the key itself is never saved in `openclaw.json`. `--approval prompt` makes OpenClaw ask you before every call on its Codex runtime, so a text can't go out without your OK there. The probe should report 9 tools.

### Hermes Agent

When Hermes loads this skill in the local CLI, it asks for `SMSTUNNEL_API_KEY` with its own secure prompt and keeps it out of the chat. Then the user runs:

```bash
hermes mcp add smstunnel --env 'SMSTUNNEL_API_KEY=${SMSTUNNEL_API_KEY}' --command npx --args -y @narcisbodea/smstunnel-mcp@1.2.0
hermes mcp test smstunnel
```

Keep the single quotes: Hermes fills in `${SMSTUNNEL_API_KEY}` when it starts the server, so the key itself isn't saved in its settings. The test should list nine tools. In a session that is already running, use `/reload-mcp`. The tools appear as `mcp_smstunnel_send_sms` and so on.

### Other hosts

Any host that runs MCP servers takes the same command and environment variable:

```json
{
  "mcpServers": {
    "smstunnel": {
      "command": "npx",
      "args": ["-y", "@narcisbodea/smstunnel-mcp@1.2.0"],
      "env": { "SMSTUNNEL_API_KEY": "<your key, or your host's reference to a secret>" }
    }
  }
}
```

On Windows, if the host can't start `npx`, use `"command": "cmd"` and `"args": ["/c", "npx", "-y", "@narcisbodea/smstunnel-mcp@1.2.0"]`.

## Check it

Ask the agent to list your phones. It should call `list_phones` and show your phone as online. Nothing is sent.

## Taking access away

Delete the key under **Apps** in the dashboard. Every agent using it stops at once.

More: https://smstunnel.io/integrations/mcp/
