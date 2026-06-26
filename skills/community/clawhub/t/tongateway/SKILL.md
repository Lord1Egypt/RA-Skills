---
name: agent-gateway
description: Agent Gateway — 16 tools for TON blockchain. Wallet info, transfers, jettons, NFTs, .ton DNS, prices, DEX orders, and autonomous agent wallets. Package: @tongateway/mcp
---

# Agent Gateway

Agent Gateway gives you 16 tools to interact with TON blockchain. Check balances, view tokens/NFTs, send transfers, resolve .ton names, place DEX orders, and deploy autonomous agent wallets.

**MCP package:** `@tongateway/mcp` (install via `npx -y @tongateway/mcp`)

## Authentication

If you get "No token configured" errors, authenticate first:

1. Call `auth.request` — you'll get a one-time link
2. Ask the user to open the link and connect their wallet
3. Call `auth.get_token` with the authId — you'll get a token
4. All other tools now work. Token persists across restarts.

## Tools

### Wallet

| Tool | Params | Description |
|------|--------|-------------|
| `wallet.info` | — | Wallet address, TON balance, account status |
| `wallet.jettons` | — | All token balances (USDT, NOT, DOGS, etc.) |
| `wallet.transactions` | `limit?` (number) | Recent transaction history |
| `wallet.nfts` | — | NFTs owned by the wallet |

### Transfers (Safe — requires wallet approval)

| Tool | Params | Description |
|------|--------|-------------|
| `transfer.request` | `to`, `amountNano`, `payload?`, `stateInit?` | Queue a TON transfer for owner approval |
| `transfer.status` | `id` | Check status: pending, confirmed, rejected, expired |
| `transfer.pending` | — | List all pending transfer requests |

### Lookup

| Tool | Params | Description |
|------|--------|-------------|
| `lookup.resolve_name` | `domain` | Resolve .ton domain to address. ALWAYS use before transfer when user gives a .ton name |
| `lookup.price` | `currencies?` | TON price in USD/EUR/etc. |

### DEX (open4dev order book)

| Tool | Params | Description |
|------|--------|-------------|
| `dex.create_order` | `fromToken`, `toToken`, `amount`, `price` | Place a limit order. Price is human-readable (e.g. 20 = "1 USDT = 20 AGNT") |
| `dex.pairs` | — | List available trading pairs |

### Agent Wallet (Autonomous — NO approval needed)

| Tool | Params | Description |
|------|--------|-------------|
| `agent_wallet.deploy` | — | Deploy a dedicated wallet contract. WARNING: agent can spend funds without approval |
| `agent_wallet.transfer` | `walletAddress`, `to`, `amountNano` | Send TON directly from agent wallet |
| `agent_wallet.info` | `walletAddress?` | Balance, seqno, status. Omit address to list all |

### Auth

| Tool | Params | Description |
|------|--------|-------------|
| `auth.request` | `label?` | Generate a one-time auth link |
| `auth.get_token` | `authId` | Retrieve token after user connects wallet |

## Amount conversion

Amounts are in **nanoTON**: 1 TON = 1,000,000,000 nanoTON

| TON | nanoTON |
|-----|---------|
| 0.1 | 100000000 |
| 0.5 | 500000000 |
| 1 | 1000000000 |
| 10 | 10000000000 |

**Token decimals:** TON/NOT/DOGS/BUILD/AGNT/PX/CBBTC = 9 decimals. USDT/XAUT0 = 6 decimals.

## Usage examples

### Check wallet and tokens

```
wallet.info()
→ Address: 0:9d43...0c02, Balance: 823.18 TON, Status: active

wallet.jettons()
→ USDT: 107.79, NOT: 3,186,370.60, BUILD: 45,277.57
```

### Send TON to .ton domain

```
lookup.resolve_name({ domain: "alice.ton" })
→ alice.ton → 0:83df...31a8

transfer.request({ to: "0:83df...31a8", amountNano: "500000000" })
→ Transfer request created. Approve in your wallet app.
```

### Place a DEX order

```
dex.create_order({ fromToken: "NOT", toToken: "TON", amount: "10000", price: 0.000289 })
→ Order placed on open4dev DEX. Approve in your wallet app.
```

### Autonomous transfer (no approval)

```
agent_wallet.deploy()
→ Agent Wallet deployed at EQCT1...

agent_wallet.transfer({ walletAddress: "EQCT1...", to: "0:abc...", amountNano: "500000000" })
→ Transfer executed. No approval needed.
```

## Important

- **Safe mode (default):** You request transfers, the wallet owner approves on their phone
- **Autonomous mode:** Agent wallet — agent signs directly, no approval. Only use when user explicitly asks
- **Requests expire in 5 minutes** if not approved
- **Always use `lookup.resolve_name`** when the user gives a .ton domain
- **Token persists** in `~/.tongateway/token` across restarts

## Security

See [SECURITY.md](https://github.com/tongateway/mcp/blob/main/SECURITY.md) for full security model details.

## Links

- Website: https://tongateway.ai
- API docs: https://api.tongateway.ai/docs
- MCP package: https://www.npmjs.com/package/@tongateway/mcp
- GitHub: https://github.com/tongateway/mcp
