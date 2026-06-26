# tellermcp

An MCP (Model Context Protocol) server that lets agents pull Teller delta-neutral opportunities, borrow pool data, loan terms, and the on-chain transactions needed to borrow or repay directly from Teller's public Delta-Neutral API.

## Features

- 🔍 **Delta-neutral scanner** – surfaces opportunities filtered by chain, asset, minimum net APR, and hard limits.
- 🏦 **Borrow pool discovery** – lists every active Teller lending pool with optional chain/token filters.
- 📐 **Per-wallet borrow terms** – computes LTV, available principal, and max borrowable USD for any wallet/pool pairing.
- 🧾 **Borrow transaction builder** – returns the full set of encoded transactions (approvals + borrow call) ready to submit on-chain.
- 📊 **Loan portfolio view** – fetches all Teller loans tied to a wallet + chain.
- 💸 **Repay helper** – builds repayment approvals + repay transactions for full or partial paydowns.

Each tool returns a short text summary plus structured JSON under `structuredContent.payload`, so consuming agents get machine-usable data without extra parsing.

## Project layout

```
agents/tellermcp/
├── README.md              # this file
├── package.json           # npm metadata + scripts
├── tsconfig.json          # TypeScript config
└── src/
    ├── index.ts           # MCP server wiring + tool registration
    ├── client.ts          # typed Teller API client
    └── types.ts           # response interfaces used by the client
```

## Requirements

- Node.js 20+ (Node 22.22.0 is available in this workspace)
- npm (ships with Node)
- Internet access to `https://delta-neutral-api.teller.org`

## Setup & usage

```bash
cd agents/tellermcp
npm install           # already run, but safe to repeat
npm run build         # optional: type-check
npm start             # launches the MCP server over stdio
```

`npm start` runs `tsx src/index.ts`, which starts an `McpServer` using `StdioServerTransport`. Point any MCP-compatible agent (e.g., mcporter/OpenClaw) at this command to expose the tools.

### Environment variables

| Variable | Default | Purpose |
| --- | --- | --- |
| `TELLER_API_BASE_URL` | `https://delta-neutral-api.teller.org` | Override for self-hosted instances or local mocks |
| `TELLER_API_TIMEOUT_MS` | `15000` | Per-request timeout for Teller API calls (ms) |

## Available tools

| Tool name | What it does | Key inputs |
| --- | --- | --- |
| `get-delta-neutral-opportunities` | Returns filtered delta-neutral arb opportunities. | `chainId`, `coin`, `limit`, `minNetAprPct` (all optional) |
| `get-borrow-pools` | Lists Teller borrow pools with optional filters. | `chainId`, `collateralTokenAddress`, `borrowTokenAddress`, `poolAddress`, `ttl` |
| `get-borrow-terms` | Computes borrow capacity for a wallet + pool. | `wallet`, `chainId`, `collateralToken`, `poolAddress` |
| `build-borrow-transactions` | Generates encoded transactions required to borrow. | `walletAddress`, `collateralTokenAddress`, `chainId`, `poolAddress`, `collateralAmount`, `principalAmount`, `loanDuration` |
| `get-wallet-loans` | Pulls all Teller loans for a wallet. | `walletAddress`, `chainId` |
| `build-repay-transactions` | Builds repayment approval + repay calls. | `bidId`, `chainId`, `walletAddress`, `amount` (optional for partial) |

Every address input is validated (checksummed or lowercase) before hitting the Teller API, and all numeric inputs are sanity-checked.

## Integrating with OpenClaw / mcporter

Add a transport entry that spawns this server via stdio, for example:

```jsonc
{
  "name": "tellermcp",
  "command": "npm",
  "args": ["start"],
  "cwd": "/data/workspace/agents/tellermcp"
}
```

Once registered, the `tellermcp` agent exposes the six tools above to any Codex/OpenClaw session.

## Next steps

- Wire authentication if Teller ships private endpoints.
- Cache hot endpoints (e.g., `/perps/delta-neutral`) if rate limits become tight.
- Extend with rollover tooling once the API exposes builder endpoints.
