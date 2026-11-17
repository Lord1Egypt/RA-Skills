# viralnote-skill

An agent skill that teaches Claude (and other LLM agents) to drive the **ViralNote** social media API — schedule posts, manage media, query analytics, all without writing custom integration code.

## Install

### Claude Code / Claude Desktop with the `skills` CLI

```bash
npx skills add viralnote/viralnote-skill
```

This drops the skill into `~/.claude/skills/viralnote/`. Restart Claude and the skill becomes available on demand.

### Manual install

Clone or download this repo into your skills directory:

```bash
git clone https://github.com/viralnote/viralnote-skill ~/.claude/skills/viralnote
```

### OpenClaw / ClawHub

```bash
clawhub install @howdy7/viralnote
# or: openclaw skills install @howdy7/viralnote
export VIRALNOTE_API_KEY="vnd_..."
```

For **native MCP tools** (15 tools) in OpenClaw, use HTTP MCP instead of this skill — see [viralnote.app/agents#openclaw](https://www.viralnote.app/agents#openclaw).

Publish or update on ClawHub: see [CLAWHUB.md](./CLAWHUB.md).

## Configuration

The skill expects one environment variable:

```bash
export VIRALNOTE_API_KEY="vnd_..."
```

Generate the key inside your ViralNote dashboard → **Settings → API keys**. Pick the scopes you want the agent to be able to use (`posts:read`, `posts:write`, `webhooks:read`, `webhooks:write`).

## What's inside

- `SKILL.md` — the instructions the agent reads to decide when and how to use ViralNote
- `reference/` — endpoint reference and auth notes (loaded on demand)
- `examples/` — end-to-end workflows (scheduling a post, importing media, pulling analytics)

## Usage

Once installed, just ask Claude naturally:

> "Schedule a post for tomorrow at 9am on Instagram and X with the photo I just uploaded to my library."

> "What were my best-performing posts on Pinterest in the last 30 days?"

> "Import this Dropbox file into my ViralNote library: https://..."

The agent will figure out which endpoints to call and walk you through it.

## License

MIT — see `LICENSE`. Pull requests welcome.

## Links

- ViralNote — https://viralnote.app
- API reference — https://viralnote.app/developers/docs
- OpenAPI spec — https://viralnote.app/api/v1/openapi
