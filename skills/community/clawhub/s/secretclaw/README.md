# 🔑 SecretClaw

Securely input API keys and sensitive values into [OpenClaw](https://github.com/openclaw/openclaw) — without ever typing them in Discord or any chat channel.

## How it works

1. Spins up a local HTTP server on a random port
2. Creates a Cloudflare Quick Tunnel (HTTPS, no account needed)
3. Generates a one-time URL with a secure token
4. You open the URL, paste your secret, and submit
5. The value is saved via `openclaw config set`
6. Server shuts down immediately

**Zero secrets in chat history. Ever.**

## Requirements

- [OpenClaw](https://github.com/openclaw/openclaw)
- Python 3.8+
- [cloudflared](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/) (`brew install cloudflared`)

## Usage

```bash
# Register a FAL API key
python3 scripts/secret_server.py --config-key "env.FAL_KEY" --label "FAL_KEY"

# Register a Discord bot token
python3 scripts/secret_server.py --config-key "channels.discord.token" --label "Discord Token"

# Register any openclaw config value
python3 scripts/secret_server.py --config-key "skills.entries.notion.apiKey" --label "Notion API Key"
```

### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--config-key` | ✅ | OpenClaw config path (dot notation) |
| `--label` | ✅ | Human-readable name shown on the form |
| `--service` | ❌ | Service name for TUNNELS.md tracking (default: `secret-input`) |

## As an OpenClaw Skill

Drop this into your OpenClaw skills directory and the agent can use it automatically when you need to register API keys.

See [SKILL.md](SKILL.md) for agent integration details.

## Security

- 🔒 HTTPS via Cloudflare TLS (Quick Tunnel)
- 🎟️ One-time token in URL (cryptographically random)
- 💀 Server self-destructs after submission
- 🚫 Nothing stored in chat history
- 🔄 URL changes on every run (no persistent endpoints)

## License

MIT
