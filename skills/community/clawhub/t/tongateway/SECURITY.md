# Security Model

## Open Source

All code is public and auditable:

- **MCP server:** https://github.com/tongateway/mcp
- **API:** https://github.com/tongateway/ton-agent-gateway-api
- **Smart contract:** https://github.com/tongateway/ton-agent-gateway-contract
- **Client/website:** https://github.com/tongateway/ton-agent-gateway-client

## No Private Keys

The token stored in `~/.tongateway/token` is a **session token (JWT)**, not a private key or seed phrase. It allows the agent to:
- Request transfers (which require wallet owner approval)
- Read wallet balances, jettons, NFTs, transactions
- Place DEX orders (which require wallet owner approval)

The token **cannot**:
- Sign transactions
- Access your private key or seed phrase
- Move funds without your explicit approval

The token can be **revoked at any time** from the [dashboard](https://tongateway.ai/app.html).

## Safe Mode (Default)

All transfers go through a **human-in-the-loop** approval flow:

1. Agent requests a transfer via the API
2. The request is sent to your wallet app (Tonkeeper, MyTonWallet, etc.) via TON Connect
3. You review the transaction details on your phone
4. You approve or reject

The agent **cannot move funds** without your explicit approval. Pending requests expire after 5 minutes if not approved.

## Autonomous Mode (Opt-in)

The `agent_wallet.deploy` and `agent_wallet.transfer` tools enable autonomous transfers **only if the user explicitly deploys an Agent Wallet**.

How it works:
- A separate smart contract (Agent Wallet) is deployed on-chain
- The user funds it with the amount they're willing to let the agent spend
- The agent gets a signing key for that specific wallet only
- The agent **cannot access the user's main wallet**

**Risk:** If the agent malfunctions or is compromised, it can spend all funds in the Agent Wallet without approval. Treat Agent Wallets as "hot wallets" — only fund them with amounts you're willing to lose.

**Mitigation:**
- Agent keys have an expiration time
- The wallet owner (admin) can revoke the agent key at any time
- The Agent Wallet is a separate contract — your main wallet is never at risk
- The smart contract is [open source and auditable](https://github.com/tongateway/ton-agent-gateway-contract)

## npx Execution

The MCP server runs locally via `npx @tongateway/mcp`. This is the standard installation method for MCP servers (same as used by Anthropic's official MCP servers).

- The package is published on npm under the [`@tongateway`](https://www.npmjs.com/package/@tongateway/mcp) scope
- The npm package is built from the [GitHub source](https://github.com/tongateway/mcp) via GitHub Actions
- You can verify the published code matches the source by comparing the npm tarball with the repository

If you prefer not to use npx, you can:
- Clone the repo and build from source: `git clone https://github.com/tongateway/mcp && cd mcp && npm install && npm run build`
- Run in a sandboxed environment (Docker, VM, etc.)

## Data Storage

| File | Contents | Purpose |
|------|----------|---------|
| `~/.tongateway/token` | JWT session token | Persists authentication across restarts |
| `~/.tongateway/wallets.json` | Agent wallet signing keys | Only created if you deploy an Agent Wallet |

Both files are created with standard file permissions and can be deleted at any time to reset the state.

## Reporting Vulnerabilities

If you find a security issue, please report it via [GitHub Issues](https://github.com/tongateway/mcp/issues) or contact us through the [website](https://tongateway.ai).
