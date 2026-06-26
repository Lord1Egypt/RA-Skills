# API Services — Detailed Usage

For the summary table with base URLs, see the main SKILL.md.

---

## Super API

Real-time on-chain Super Token balances (live balance only — no history, reports, or GDA details).
For full history, GDA support, and CSV reports, use the **Balance API** instead.

`GET /super-token-balance?chain={chainId}&token={tokenAddress}&account={accountAddress}`

Returns connected/unconnected balances, net flow rate, and underlying token
details.

Wrapped by `scripts/balance.mjs` — prefer the script for one-off lookups.

[Swagger](https://superapi.kazpi.com/)

## Balance API

Base URL: `https://balances.superfluid.dev` · Read-only, no auth · mainnet + testnet

[Scalar UI](https://balances.superfluid.dev/ui) · [OpenAPI](https://balances.superfluid.dev/doc)

**What it is** — an event-sourced balance *indexer*. It reconstructs Super Token
balance state purely from on-chain log events, giving perfect accounting for ~99.9%
of accounts. Because it replays the full event history, it can return the exact
balance state at **any point in time** (pass `timestamp`), not just "now" — something
RPC and the subgraph can't do cheaply. Reach for it whenever you need history,
point-in-time balances, GDA/IDA coverage, or CSV exports.

**Balance components** — the indexer decomposes balance into distinct parts:
- `connectedBalance` — the on-chain-visible balance (matches `realtimeBalanceOfNow`):
  CFA stream balance + deposit + connected GDA member balance + approved IDA subscriber balance.
- `disconnectedBalance` — claimable-but-unclaimed amounts: disconnected GDA pool member
  balance + unapproved IDA subscriber balance.
- `deposit` — the CFA stream **buffer**: a protective reserve locked while streams are active.
- `totalBalance` = `connectedBalance` + `disconnectedBalance`.
- `availableBalance` = `totalBalance` − `deposit` (spendable liquidity after the buffer).

**Disambiguation** — choose the right API for the job:
- **Super API** — single live balance; fast, no history
- **Accounting API** — CFA + ERC-20 only; no GDA support
- **Balance API** — most comprehensive: event-sourced, point-in-time + full history,
  CFA + GDA + IDA, snapshots, reports, CSV export

### Endpoints

- `GET /v1/chains` — list supported chains (optional `network`: mainnet/testnet/all)
- `GET /v1/accounts/{account}/tokens` — all Super Tokens held by an account (`chain`, `network`)
- `GET /v1/accounts/{account}/tokens/{token}/counterparties` — all counterparties for a token (`chain`)
- `GET /v1/accounts/{account}/tokens/{token}/balance` — point-in-time balance; `chain`
  required, optional `timestamp` (omit for current). Returns `connectedBalance`,
  `disconnectedBalance`, `totalBalance`, `availableBalance`, `deposit`,
  `connectedNetFlowRate`, `maybeCriticalAt`, `timestamp`, `token`.
- `GET /v1/accounts/{account}/tokens/{token}/balance-snapshots` — historical snapshots for
  charting; `chain`, optional `startTimestamp`/`endTimestamp`/`points`. Each point carries
  `connectedBalance`, `disconnectedBalance`, `deposit`, `totalBalance`.
- `GET /v1/accounts/{account}/tokens/{token}/entries` — raw ledger entries; `chain`, optional
  `counterparty`, `startTimestamp`, `endTimestamp`, `category`, `entryType`, `limit`, `offset`, `direction`
- `GET /v1/accounts/{account}/tokens/{token}/balance-report` — aggregated report:
  required `chain`, `startDate`, `endDate`; optional `period` (daily/weekly/monthly),
  `format` (json|csv), `view` (totals|by_counterparty|by_category), `category`,
  `counterparty`, `counterpartyDetail`, `extrapolate` (boolean)
- `GET /v1/accounts/{account}/tokens/{token}/movements` — bank-statement view; cursor
  pagination (`cursor`/`limit`/`offset`/`sort`), plus filters `counterparty`,
  `startTimestamp`, `endTimestamp`, `movementType`, `category`, `direction`, `isOngoing`, `isDisconnected`

## CMS

Can return unlisted Super Tokens (not just those in the tokenlist). Can get
CoinGecko IDs for price lookups.

[Swagger](https://cms.superfluid.pro/api-docs) ·
[OpenAPI](https://cms.superfluid.pro/openapi.json) ·
[Repo](https://github.com/superfluid-org/superfluid.pro/tree/main/cms)

## Points

SUP points campaigns (Stack.so replacement). Same repo as CMS.

[API docs](https://cms.superfluid.pro/points/api-docs) ·
[OpenAPI](https://cms.superfluid.pro/points/openapi.json)

## Accounting

Splits per-second streams into chunked granularity (e.g. streamed per day).
Handles CFA and ERC-20 transfers only — **no GDA support**.
For GDA support, full history, and CSV export, use the **Balance API** instead.

[Swagger](https://accounting.superfluid.dev/v1/swagger) ·
[Repo](https://github.com/superfluid-org/accounting-api)

## Allowlist

`GET /api/allowlist/{account}/{chainId}` — check if an account is
allowlisted for automations (vesting, flow scheduling, auto-wrap).

## Whois

Resolves across ENS, AF, Farcaster, Lens, etc.
- `GET /api/resolve/{address}` — address → profile/name
- `GET /api/reverse-resolve/{handle}` — name/handle → address

GOTCHA: despite the names, `resolve` takes an address and `reverse-resolve`
takes a name.

## Token Prices

Simpler alternative to CMS for price lookups. Provides prices for all listed
SuperTokens where the token (or underlying) is known to CoinGecko.

Endpoint: `GET /v1/{canonical-network-name}/{token-address}`

[Repo](https://github.com/d10r/sf-token-prices-api/)

## Claim Programs

Returns all SUP reward programs across seasons. Each entry has `appId`,
`name`, `season`, `category`, `url`, and a nested `program.onchainInfo` with
`poolAddress`, `fundingFlowRate`, `totalAllocated`, `totalClaimed`,
`totalMembers`, and funding timestamps.

The response uses tRPC's `superjson` format (top-level `json` + `meta` keys).
Filter by `program.onchainInfo.isFundingFinished` to find active campaigns.
