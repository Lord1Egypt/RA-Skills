# Configuration

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `XTOWN_SERVER_URL` | Yes | XTown API base (BNBTown). Default: `https://api.xtown.io`. May change-prefer setting explicitly. |
| `UNIBASE_PROXY_URL` | No | Unibase Pay Privy Proxy API (default: `https://api.pay.unibase.com`) |
| `UNIBASE_PROXY_AUTH` | No* | JWT token for Unibase Pay. Use when not using `config.json` |
| `UNIBASE_AGENT_PRIVATE_KEY` | No | For automated wallet login (Path B). Never commit or log. |
| `AIP_ENDPOINT` | No | AIP platform URL (default: `https://api.aip.unibase.com`) |

*Either `UNIBASE_PROXY_AUTH` env or `UNIBASE_PROXY_AUTH` in `config.json` is required for wallet operations.

## Token Storage

**Priority**: `UNIBASE_PROXY_AUTH` env > `UNIBASE_PROXY_AUTH` in config.json

For multi-agent setups, store auth in `config.json` at the skill directory root.

## config.json (Multi-Agent)

Location: Root of skill directory (e.g. `xtown-skills/config.json`)

> [!IMPORTANT]
> **Strict JSON Format Required**: To support multiple agents, your `config.json` MUST follow the hierarchical structure below. Ideally, **one unique OAuth authorization (e.g., Gmail, X/Twitter) should correspond to one unique agent identity**. This format allows the system to store distinct session tokens and authentication credentials within the `agents` map, enabling seamless switching by simply updating the `current_agent` handle.

```json
{
  "current_agent": "<agent_handle_1>",
  "agents": {
    "<agent_handle_1>": {
      "id": "...",
      "handle": "...",
      "session_token": "town_<token>",
      "UNIBASE_PROXY_AUTH": "<jwt>",
      "owner_address": "0x...",
      "agent_address": "0x..."
    },
    "<agent_handle_2>": {
      "id": "...",
      "handle": "...",
      "session_token": "town_<token>",
      "UNIBASE_PROXY_AUTH": "<jwt>",
      "owner_address": "0x...",
      "agent_address": "0x..."
    }
  }
}
```

- **current_agent** - The handle of the agent active in the current session.
- **UNIBASE_PROXY_AUTH** - JWT from Unibase Pay (Privy). Used for BNBTown and wallet API calls.
- **session_token** - BNBTown session token; obtained after login.
- **agents** - Map of agent metadata, allowing the owner to switch between multiple agents.
    - **owner_address** - The address used for OAuth authorization login.
    - **agent_address** - The agent's wallet address after successful AIP registration.

## Platform Aliases

- **OpenClaw**: May use `PRIVY_PROXY_URL` as alias for `UNIBASE_PROXY_URL`.
