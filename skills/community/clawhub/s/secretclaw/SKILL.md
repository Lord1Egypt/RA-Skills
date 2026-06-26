---
name: secretclaw
description: Securely input API keys and sensitive values into OpenClaw without typing them in chat. Uses a local HTTP server + Cloudflare Tunnel to serve an HTTPS form. Use when registering API keys, tokens, passwords, or any sensitive config values.
---

# SecretClaw

A skill for securely inputting secret keys and sensitive values without passing them through Discord or any chat channel.

Uses a local HTTP server + Cloudflare Tunnel to serve an HTTPS form page,
then saves the submitted value via `openclaw config set`.

## When to Use

- When registering API keys, tokens, passwords, or other sensitive values
- To avoid typing secrets directly in chat
- Examples: FAL_KEY, Notion API key, OpenAI key, etc.

## Active Tunnels

→ See `workspace/TUNNELS.md` (managed automatically by the agent)

## Usage

```bash
python3 <skill_dir>/scripts/secret_server.py \
  --config-key "env.FAL_KEY" \
  --label "FAL_KEY"
```

### Parameters
- `--config-key`: openclaw config path (dot notation)
  - e.g.: `env.FAL_KEY`, `env.OPENAI_KEY`, `channels.discord.token`
- `--label`: Human-readable name displayed on the form
- `--service`: Service name recorded in TUNNELS.md (default: `secret-input`)

## Agent Execution Steps

1. Run the command below as a background exec
2. Extract the `SECRET_URL:` line from stdout → send the URL to the user
3. When `SECRET_SAVED:` appears, the value has been saved
4. Check if a gateway restart is needed (some keys require restart)

```python
# Example background exec
python3 /opt/homebrew/lib/node_modules/openclaw/skills/secret-input/scripts/secret_server.py \
  --config-key "env.FAL_KEY" \
  --label "FAL_KEY"
```

## TUNNELS.md Structure

Active tunnel info is recorded in `workspace/TUNNELS.md`.
The agent reads this file to check currently open tunnel URLs.
Entries are automatically removed when the server shuts down.

## Security

- No secret values are ever stored in chat history
- HTTPS via Cloudflare TLS (Quick Tunnel)
- One-time token embedded in URL (cryptographically random)
- Server self-destructs immediately after submission
- Uses Cloudflare Quick Tunnel (no account required; URL changes on every run)

## Notes

- If the machine reboots, the server shuts down and the Cloudflare URL becomes invalid
- To re-enter a value, simply run the skill again to generate a new URL
- TUNNELS.md only tracks currently active tunnels (not historical URLs)
