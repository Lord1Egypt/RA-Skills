---
name: satgate
version: 2.0.0
description: Manage your API's economic firewall from the terminal. Mint tokens, check status, validate tokens, wrap agent commands. The server-side counterpart to lnget.
homepage: https://satgate.io
---

# SatGate CLI

SatGate CLI manages API access and token governance for the agent economy. Use it when you need to control what agents can access, mint capability tokens, and run agents through SatGate's budget-enforced proxy.

**They're the wallet. We're the register.**

If the agent needs to *pay* for L402 APIs, install `lnget` from Lightning Labs. SatGate is for the *server side* — enforcement, attribution, and governance.

## Setup

Run `scripts/configure.sh` for interactive setup, or `satgate-cli init` to configure via the CLI directly.

```bash
# Interactive CLI setup (connects to SatGate Cloud)
satgate-cli init
```

Or set environment variables:

```bash
# For SatGate Cloud
export SATGATE_CLOUD_URL=https://cloud.satgate.io
export SATGATE_API_KEY=sg_your_api_key
```

Always run `satgate-cli status` first to confirm you're connected to the right tenant.

## Safety Rules

1. **Check target first** — run `satgate-cli status` before any operation to verify tenant and plan.
2. **Validate before trusting** — use `satgate-cli token validate` to verify any token.
3. **Wrap agents for enforcement** — use `satgate-cli wrap` to route agent traffic through SatGate.

## Commands

### Interactive setup
```bash
satgate-cli init    # Configure Cloud URL, API key, validate, save to ~/.satgate/config.json
```

### Check gateway status
```bash
satgate-cli status    # Tenant info, plan, request count, blocked count, total spend, active agents
```

### Mint a token for an agent
```bash
# Mint via Identity Provider → SatGate Mint exchange
satgate-cli mint --subject "my-agent"

# With custom audience
satgate-cli mint --subject "my-agent" --audience "satgate"
```

The mint flow: CLI gets a JWT from the configured Identity Provider, then exchanges it with SatGate Mint for a macaroon token with embedded policy and budget.

### Validate a token
```bash
satgate-cli token validate <macaroon-token>
```

### Wrap an agent command through SatGate proxy
```bash
# Run any command with SatGate as HTTP proxy — injects token automatically
satgate-cli wrap --token <macaroon> -- python my_agent.py
satgate-cli wrap --token <macaroon> --gateway https://gw.example.com -- node agent.js
satgate-cli wrap --token <macaroon> -- curl https://api.openai.com/v1/chat/completions
```

The wrap command starts a local HTTP proxy that injects the SatGate Bearer token into every outbound request. Set `SATGATE_TOKEN` env var as an alternative to `--token`.

### Version
```bash
satgate-cli version    # Show version, commit, build date
```

## Common Workflows

**"New agent needs API access"**
→ `satgate-cli mint --subject "agent-name"`

**"Is the gateway healthy?"**
→ `satgate-cli status`

**"Run an agent through SatGate"**
→ `satgate-cli wrap --token <token> -- python my_agent.py`

**"Verify a token is valid"**
→ `satgate-cli token validate <token>`

## MCP Bridge (for Cursor / Claude Code)

To connect MCP clients like Cursor or Claude Code to SatGate's budget-enforced proxy, use the npm bridge:

```json
{
  "mcpServers": {
    "satgate": {
      "command": "npx",
      "args": ["-y", "satgate-mcp-bridge"],
      "env": {
        "SATGATE_URL": "https://satgate-mcp-saas.fly.dev",
        "SATGATE_TOKEN": "your-token-here"
      }
    }
  }
}
```

Get your token from [cloud.satgate.io/cloud/mcp/connect](https://cloud.satgate.io/cloud/mcp/connect).

## Pairing with lnget

SatGate (server-side) + lnget (client-side) = complete agent commerce stack.

- **lnget**: Agents pay for L402-gated APIs automatically
- **SatGate CLI**: Operators mint tokens, validate access, wrap agent commands

An agent using `lnget` hits your SatGate-protected endpoint → SatGate enforces the budget and attributes the cost.
