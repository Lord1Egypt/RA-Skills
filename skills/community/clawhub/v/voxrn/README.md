# openclaw-skill-voxrn

OpenClaw skill that adds the [Voxrn](https://voxrn.com) telephony platform as a tool surface for any OpenClaw-bridged chat.

## What you get

After installing this skill the agent has these tools available:

| Tool | What it does |
|---|---|
| `call.place` | Place an outbound phone call |
| `call.list_active` | List currently-active calls |
| `call.end` | Hang up a call by SID |
| `transcript.stream` | Subscribe to live captions |
| `message.send` | Send an SMS |
| `contact.search` | Search workspace contacts |
| `contact.upsert` | Create or update a contact |
| `balance.check` | Read the workspace balance |

## Install (once it's on ClawHub)

```bash
openclaw skills install voxrn
```

## Install from this repo (local / dev)

```bash
openclaw skills install file:./openclaw-skill-voxrn
```

This copies the skill into `~/.openclaw/workspace/skills/voxrn/` and registers `voxrn` as an outbound MCP server in your OpenClaw config.

## Configure

Mint a Voxrn API key at `/enterprise/dashboard/agents → API keys`, then:

```bash
openclaw config secrets set voxrn_api_key vxk_...
```

Or, if you prefer plain env vars in your shell rc:

```bash
export VOXRN_API_KEY="vxk_..."
export VOXRN_BASE_URL="https://voxrn.com"  # optional
```

Restart the OpenClaw daemon so the new MCP server is picked up:

```bash
openclaw daemon restart
```

## Verify

```bash
openclaw mcp show voxrn
openclaw skills check
```

You should see `voxrn` in the registered MCP servers list and `voxrn` reported as "ok" by the skill checker.

## Usage

From any bridged channel (Slack, Telegram, iMessage, Discord, etc.):

> call Atlas Plumbing and ask about Thursday morning

> text Mina the meeting moved to 2pm

> what's my Voxrn balance

## License

MIT
