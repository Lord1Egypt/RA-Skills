---
name: waiaas-wallet
description: Self-hosted crypto wallet daemon for AI agents. Send transactions, manage DeFi positions, enforce spending limits — without exposing private keys to agents. EVM + Solana unified API. 59+ MCP tools.
metadata:
  openclaw:
    emoji: "🔐"
    homepage: "https://waiaas.ai"
    requires:
      bins: ["waiaas"]
      env: ["WAIAAS_SESSION_TOKEN"]
    install:
      - id: waiaas-cli
        kind: node
        package: "@waiaas/cli"
        bins: ["waiaas"]
        label: "Install WAIaaS CLI (source: https://github.com/minhoyoo-iotrust/WAIaaS)"
---

# WAIaaS Wallet — Self-Hosted Wallet for AI Agents

> **Your private keys should never live inside your agent process.** If your agent is compromised, the attacker gets the keys. WAIaaS separates key custody into an isolated daemon with a policy engine that limits what any agent session can do.

## What is WAIaaS?

WAIaaS (Wallet-as-a-Service for AI Agents) is a **self-hosted** local daemon that manages crypto wallets on behalf of AI agents. Unlike cloud wallet services (Coinbase CDP, Privy, Circle), WAIaaS runs entirely on your machine — no third-party API keys, no custodial risk.

### Why use WAIaaS instead of raw keypairs?

| Approach | Key exposure | Spending limits | Human approval | Kill switch |
|----------|-------------|-----------------|----------------|-------------|
| Raw keypair in agent | Agent process holds key | None | None | Kill process |
| Cloud WaaS (CDP, Privy) | Third-party holds key | Varies | Varies | API call |
| **WAIaaS** | **Isolated daemon holds key** | **Per-token, per-tx, cumulative** | **SIWE/SIWS/WalletConnect** | **Instant via Admin UI** |

### Key features

- **Self-hosted**: Local daemon, no third-party dependency
- **Policy engine**: Default-deny, token whitelist, per-token spending limits, cumulative caps
- **Owner approval**: High-value transactions require human signature (SIWE/SIWS/WalletConnect/D'CENT)
- **Multi-chain**: EVM (Ethereum, Base, Arbitrum, Polygon, Optimism) + Solana in one daemon
- **59+ MCP tools**: Wallet ops, DeFi (swap/lend/stake/bridge/perp), NFT, x402, ERC-4337, ERC-8004
- **Kill switch**: Instantly freeze any wallet from Admin UI or API
- **RPC proxy**: Use as `--rpc-url` for Forge, Hardhat, ethers.js — every tx goes through policy engine

## Quick Start

### 1. Install and start the daemon

```bash
npm install -g @waiaas/cli
waiaas init                        # Create data directory + config.toml
waiaas start                       # Start daemon (sets master password on first run)
waiaas quickset --mode mainnet     # Create wallets + MCP sessions in one step
```

The `quickset` command creates **Solana + EVM** wallets automatically, issues MCP session tokens, and outputs a ready-to-use MCP config snippet.

For testing, use `waiaas quickset --mode testnet` to create Solana Devnet + EVM Sepolia wallets.

### 2. Configure spending policies (recommended before connecting agents)

Set up spending limits and token whitelists via Admin UI at `http://127.0.0.1:3100/admin`. WAIaaS uses default-deny policy — agents cannot transact until policies are configured. This ensures human oversight before any agent gains financial capabilities.

### 3. Connect MCP server

Pass the session token via environment variable (do **not** hardcode tokens in config files):

```bash
# Set session token as environment variable
export WAIAAS_SESSION_TOKEN="<session-token-from-quickset>"

# Then configure OpenClaw MCP
openclaw config set mcpServers.waiaas.command "npx"
openclaw config set mcpServers.waiaas.args '["@waiaas/mcp"]'
openclaw config set mcpServers.waiaas.env.WAIAAS_SESSION_TOKEN "\${WAIAAS_SESSION_TOKEN}"
```

Or auto-register with all wallets:

```bash
waiaas mcp setup --all
```

> **Security note:** Store session tokens in environment variables or a secrets manager, not in plaintext config files. Session tokens are time-limited JWTs and can be revoked from the Admin UI at any time.

## Available MCP Tools (59+)

### Wallet Management
- `connect_info` — Self-discovery: wallets, policies, capabilities. **Call this first.**
- `get_balance` — Wallet balance (native + USD)
- `get_address` — Public address
- `get_assets` — All held assets (native + tokens)
- `get_wallet_info` — Chain, address, environment, networks
- `get_tokens` — Registered tokens for a network
- `resolve_asset` — Resolve CAIP-19 asset ID to metadata

### Transactions
- `send_token` — Send native (SOL/ETH) or tokens (ERC-20/SPL)
- `call_contract` — Call whitelisted smart contracts
- `approve_token` — Approve spender (requires APPROVED_SPENDERS policy)
- `send_batch` — Atomic multi-instruction transaction (Solana)
- `sign_transaction` — Sign without broadcasting
- `sign_message` — Personal sign or EIP-712 typed data
- `simulate_transaction` — Dry-run with policy evaluation, no side effects
- `encode_calldata` — Encode EVM function call to hex

### Transaction History
- `list_transactions` — Outgoing transaction history (paginated)
- `get_transaction` — Single transaction details
- `list_incoming_transactions` — Incoming transfers (paginated, filterable)
- `get_incoming_summary` — Period-based incoming summary (daily/weekly/monthly)

### DeFi (via Action Providers)
- **Swap**: Jupiter (Solana), 0x (EVM), DCent Aggregator
- **Bridge**: LI.FI cross-chain, Across Protocol
- **Lending**: Aave V3 (EVM), Kamino (Solana)
- **Staking**: Lido (ETH), Jito (SOL)
- **Yield**: Pendle yield trading
- **Perp**: Drift (Solana), Hyperliquid (10 tools)
- **Prediction**: Polymarket (8 tools)

### NFT
- `list_nfts` — List owned NFTs (ERC-721/1155/Metaplex)
- `get_nft_metadata` — NFT metadata and attributes
- `transfer_nft` — Transfer NFT (requires approval tier)

### Advanced
- `x402_fetch` — HTTP 402 automatic payment
- `wc_connect` / `wc_status` / `wc_disconnect` — WalletConnect pairing
- `build_userop` / `sign_userop` — ERC-4337 Account Abstraction
- `erc8004_*` — ERC-8004 Trustless Agent identity
- `erc8128_*` — ERC-8128 Signed HTTP Requests
- `get_rpc_proxy_url` — EVM RPC proxy for Forge/Hardhat/ethers.js
- `list_credentials` / `list_offchain_actions` — Credential vault and off-chain history

## Example Workflows

### Check balance and send tokens

```
You: What's my wallet balance?
Agent: [calls connect_info, then get_balance]
> Your wallet holds 2.5 ETH ($4,250) and 1,000 USDC on Base.

You: Send 100 USDC to 0xAlice...
Agent: [calls simulate_transaction first, then send_token]
> Simulated: 100 USDC transfer, fee ~$0.02, policy tier AUTO_SIGN.
> Transaction sent! TX: 0xabc... (confirmed in 2s)
```

### DeFi operations

```
You: Swap 500 USDC for ETH on Base
Agent: [calls action_0x_swap_quote, then action_0x_swap_execute]
> Swapped 500 USDC → 0.29 ETH via 0x aggregator. TX: 0xdef...

You: Supply 1 ETH to Aave on Arbitrum
Agent: [calls action_aave_supply]
> Supplied 1 ETH to Aave V3 on Arbitrum. Current APY: 2.1%. TX: 0xghi...
```

### x402 automatic payment

```
You: Fetch the premium API at https://api.example.com/data
Agent: [calls x402_fetch — auto-pays if 402 response]
> Paid 0.01 USDC via x402. Response: { "data": ... }
```

## Security Model

WAIaaS enforces a 3-layer security model:

1. **Session authentication**: Agents use time-limited JWT session tokens. No master password exposure.
2. **Policy engine**: Default-deny. Configure ALLOWED_TOKENS, CONTRACT_WHITELIST, SPENDING_LIMIT, RATE_LIMIT per wallet.
3. **Owner approval + Kill switch**: High-value transactions require human signature. Instant wallet freeze via Admin UI.

**Transaction tiers:**
- `AUTO_SIGN` — Within policy limits, auto-approved
- `TIME_DELAY` — Delayed execution with notification
- `APPROVAL` — Requires owner wallet signature (SIWE/SIWS/WalletConnect)
- `BLOCKED` — Denied by policy

## Links

- **Website**: https://waiaas.ai
- **GitHub**: https://github.com/minhoyoo-iotrust/WAIaaS
- **npm**: `@waiaas/cli`, `@waiaas/sdk`, `@waiaas/mcp`
- **Docker**: `waiaas/daemon:latest`
- **Admin UI**: `http://127.0.0.1:3100/admin` (after daemon start)
