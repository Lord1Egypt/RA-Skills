# @tongateway/mcp

[![smithery badge](https://smithery.ai/badge/tongateway/agent)](https://smithery.ai/servers/tongateway/agent)

MCP server for [Agent Gateway](https://tongateway.ai) — gives AI agents full access to the TON blockchain via Model Context Protocol.

**16 tools:** wallet info, jettons, NFTs, transactions, transfers, .ton DNS, prices, DEX orders, agent wallets, and more.

## Quick Start

### Claude Code

```bash
claude mcp add-json tongateway '{
  "command": "npx",
  "args": ["-y", "@tongateway/mcp"],
  "env": {
    "AGENT_GATEWAY_API_URL": "https://api.tongateway.ai"
  }
}' --scope user
```

### Cursor

Add to Cursor Settings → MCP Servers:

```json
{
  "mcpServers": {
    "tongateway": {
      "command": "npx",
      "args": ["-y", "@tongateway/mcp"],
      "env": {
        "AGENT_GATEWAY_API_URL": "https://api.tongateway.ai"
      }
    }
  }
}
```

### OpenClaw

```bash
openclaw config set --strict-json plugins.entries.acpx.config.mcpServers '{
  "tongateway": {
    "command": "npx",
    "args": ["-y", "@tongateway/mcp"],
    "env": {
      "AGENT_GATEWAY_API_URL": "https://api.tongateway.ai"
    }
  }
}'
```

No token needed upfront — the agent authenticates via `auth.request` (generates a one-time link, user connects wallet). Token persists in `~/.tongateway/token` across restarts.

## Tools

### Auth

| Tool | Description |
|------|-------------|
| `auth.request` | Generate a one-time link for wallet connection |
| `auth.get_token` | Retrieve token after user connects wallet |

### Wallet

| Tool | Description |
|------|-------------|
| `wallet.info` | Wallet address, TON balance, account status |
| `wallet.jettons` | All token balances (USDT, NOT, DOGS, etc.) |
| `wallet.transactions` | Recent transaction history |
| `wallet.nfts` | NFTs owned by the wallet |

### Transfers (Safe — requires wallet approval)

| Tool | Description |
|------|-------------|
| `transfer.request` | Request a TON transfer (to, amountNano, payload?, stateInit?) |
| `transfer.status` | Check transfer status by ID |
| `transfer.pending` | List all pending requests |

### Lookup

| Tool | Description |
|------|-------------|
| `lookup.resolve_name` | Resolve .ton domain to address |
| `lookup.price` | Current TON price in USD/EUR |

### DEX (open4dev order book)

| Tool | Description |
|------|-------------|
| `dex.create_order` | Place a limit order (fromToken, toToken, amount, price) |
| `dex.pairs` | List available trading pairs |

### Agent Wallet (Autonomous — no approval needed)

| Tool | Description |
|------|-------------|
| `agent_wallet.deploy` | Deploy a dedicated wallet contract for the agent |
| `agent_wallet.transfer` | Send TON directly from agent wallet |
| `agent_wallet.info` | Balance, seqno, agent key status |

## How it works

```
You: "Send 1 TON to alice.ton"

Agent: lookup.resolve_name("alice.ton") → 0:83df...
       transfer.request(to="0:83df...", amountNano="1000000000")
       → Transfer request created. Approve in your wallet app.
```

For agent wallets (autonomous mode):

```
You: "Send 0.5 TON from my agent wallet to 0:abc..."

Agent: agent_wallet.transfer(wallet, to, amount)
       → Transfer executed. No approval needed.
```

## Build from Source

If you prefer not to use `npx`, you can build and run locally:

```bash
git clone https://github.com/tongateway/mcp
cd mcp
npm install
npm run build
```

Then configure your MCP client to use the local build:

```json
{
  "mcpServers": {
    "tongateway": {
      "command": "node",
      "args": ["/path/to/mcp/dist/index.js"],
      "env": {
        "AGENT_GATEWAY_API_URL": "https://api.tongateway.ai"
      }
    }
  }
}
```

See [SECURITY.md](SECURITY.md) for the full security model.

## Links

- [tongateway.ai](https://tongateway.ai) — landing page + install guides
- [Dashboard](https://tongateway.ai/app.html) — connect wallet & manage tokens
- [API Docs](https://api.tongateway.ai/docs) — Swagger UI
- [Agent Wallet Contract](https://github.com/tongateway/ton-agent-gateway-contract) — FunC smart contract
- [Skill File](https://tongateway.ai/agent-gateway.md) — context file for AI agents
- [Smithery](https://smithery.ai/servers/tongateway/agent) — MCP marketplace listing
- [MCP HTTP Endpoint](https://tongateway.run.tools) — remote MCP transport

## License

MIT
