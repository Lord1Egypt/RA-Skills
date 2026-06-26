---
name: tronscan-account-profiler
description: |
  Query TRON wallet-type address total assets, token holdings, DeFi participation, energy/bandwidth, votes, tx/transfer count.
  Use when user asks "what assets does this address have", "address balance", "recent activity", or provides a TRON address for profiling.
  If the core question is contract identification, verification status, or popular methods, immediately switch to tronscan-contract-analysis.
  Do NOT use for single token details or holder distribution (use tronscan-token-scanner); tx hash details (use tronscan-transaction-info).
metadata:
  author: tronscan-mcp
  version: "1.0"
  mcp-server: https://mcp.tronscan.org/mcp
---

# Account Profiler

## Overview

| Tool | Function | Use Case |
|------|----------|----------|
| getAccountDetail | Account detail | Balance, tx count, bandwidth/energy, votes |
| getAccountTokens | Account tokens | Tokens held by address |
| getTokenAssetOverview | Asset overview | Holdings and total value |
| getParticipatedProjects | Participated projects | DeFi participation |
| getAccountAnalysis | Daily analysis | Daily balance, transfer, energy, bandwidth, tx stats |
| getAccountList | Account list | All accounts with balance, votes, tx count |
| getAccountResource | Stake 1.0 resources | Freeze records, bandwidth, energy (Stake 1.0) |
| getAccountResourceV2 | Stake 2.0 resources | Staking records, delegated bandwidth/energy (Stake 2.0) |
| getAccountsWithHoldingTrx | TRX holder count | Number of accounts holding TRX over time |
| getAccountTag | Account tags | Exchange/project/risk tags for an address |
| getAccountTokenBigAmount | Large token txs | Large token transactions for an address |
| getAccountTransferAmount | Transfer flow | Incoming/outgoing fund distribution for an address |
| getRelatedAccount | Related accounts | Related addresses and transaction data |
| getWalletTokens | Wallet tokens | Tokens and collectibles held in wallet |
| getWalletTrc20Transfers | Wallet TRC20 transfers | TRC20 transfer records for a wallet |
| getApprovalList | Approval list | Token approvals granted to contracts |
| getApprovalChangeRecords | Approval changes | Historical approval changes for a contract |
| getUnfreezableAmount | Unfreezable TRX | Amount of TRX available for unfreezing |
| getFreezeResource | TRX staking rate | TRX staking rate data over time |

## Workflow: Wallet Address Profiling

> User: "What assets does this address have? Any recent activity?"

1. **tronscan-account-profiler** — `getAccountDetail` → balance, tx count, bandwidth/energy, votes.
2. **tronscan-account-profiler** — `getAccountTokens` + `getTokenAssetOverview` for holdings and total value; optionally `getParticipatedProjects` for DeFi participation.
3. If **recent transactions** needed: **tronscan-transaction-info** — call `getTransactionList` with the address.

**Data handoff**: Same TRON address used as account parameter across all steps.

## MCP Server

- **Prerequisite**: [TronScan MCP Guide](https://mcpdoc.tronscan.org)

## Tools

### getAccountDetail

- **API**: `getAccountDetail` — Get account details (balance, tx count, bandwidth/energy, votes)
- **Use when**: User asks for "address balance", "account info", or basic wallet stats.
- **Input**: Account address.

### getAccountTokens

- **API**: `getAccountTokens` — Get tokens held by an address
- **Use when**: User asks for "tokens in this wallet" or "what does this address hold".
- **Input**: Account address.

### getTokenAssetOverview

- **API**: `getTokenAssetOverview` — Get asset holdings and total value
- **Use when**: User asks for "total assets" or "portfolio value".
- **Input**: Account address.

### getParticipatedProjects

- **API**: `getParticipatedProjects` — Get DeFi projects participated in
- **Use when**: User asks for "DeFi participation" or "which protocols is this address using".
- **Input**: Account address.

### getAccountAnalysis

- **API**: `getAccountAnalysis` — Get daily analysis (balance changes, transfer count, energy, bandwidth, tx count) for an account
- **Use when**: User asks for "account activity over time", "daily transfers", or "historical balance".
- **Input**: `address`, `type`, `startTimestamp`, `endTimestamp` (all required, timestamps in milliseconds).

### getAccountList

- **API**: `getAccountList` — Get account list with balance, voting power, tx count
- **Use when**: User asks for "top accounts", "richest addresses", or "account rankings".
- **Input**: Optional `start`, `limit`, `sort`.

### getAccountResource

- **API**: `getAccountResource` — Get Stake 1.0 resource info (freeze records, bandwidth, energy)
- **Use when**: User asks for "staking resources", "bandwidth/energy breakdown", or "freeze records" on Stake 1.0.
- **Input**: `address` (required); optional `type`, `resourceType`.

### getAccountResourceV2

- **API**: `getAccountResourceV2` — Get Stake 2.0 resource info (staking records, delegated bandwidth/energy)
- **Use when**: User asks for "Stake 2.0 resources", "delegated energy", or "staking details".
- **Input**: `address` (required); optional `type`, `resourceType`.

### getAccountsWithHoldingTrx

- **API**: `getAccountsWithHoldingTrx` — Get number of accounts holding TRX over time
- **Use when**: User asks for "how many wallets hold TRX" or "TRX holder count trend".
- **Input**: Optional `days`.

### getAccountTag

- **API**: `getAccountTag` — Get tags for an account (exchange, project, risk labels)
- **Use when**: User asks for "address label", "is this address an exchange?", or "risk tags".
- **Input**: `address` (required).

### getAccountTokenBigAmount

- **API**: `getAccountTokenBigAmount` — Get large token transactions for an address
- **Use when**: User asks for "large transfers for this address" or "whale activity".
- **Input**: `address`, `relatedToken`, `types` (all required); optional filters.

### getAccountTransferAmount

- **API**: `getAccountTransferAmount` — Get incoming/outgoing fund distribution for an address
- **Use when**: User asks for "fund flow", "where does money go", or "transfer distribution".
- **Input**: `address` (required); optional `direction`, `relatedToken`, `startTime`, `endTime`.

### getRelatedAccount

- **API**: `getRelatedAccount` — Get related accounts and transaction data
- **Use when**: User asks for "related addresses", "counterparties", or "who does this address transact with".
- **Input**: `address` (required); optional filters (up to 100 records).

### getWalletTokens

- **API**: `getWalletTokens` — Get tokens and collectibles in a wallet
- **Use when**: User asks for "wallet contents", "NFTs held", or "all assets in wallet".
- **Input**: `address` (required); optional `assetType` (all | assets | collectibles).

### getWalletTrc20Transfers

- **API**: `getWalletTrc20Transfers` — Get TRC20 transfer records for a wallet
- **Use when**: User asks for "TRC20 transfers" for a specific token and address.
- **Input**: `address`, `trc20Id` (both required); optional pagination and filters. Note: start+limit ≤ 10000.

### getApprovalList

- **API**: `getApprovalList` — Get token approvals granted by an address to contracts
- **Use when**: User asks for "what has this address approved?", "token allowances", or "approval risk".
- **Input**: `address` (required); optional `type`, `relatedId`.

### getApprovalChangeRecords

- **API**: `getApprovalChangeRecords` — Get historical approval changes for a contract
- **Use when**: User asks for "approval history" for a specific contract.
- **Input**: `contractAddress` (required); optional `fromAddress`, `toAddress`.

### getUnfreezableAmount

- **API**: `getUnfreezableAmount` — Get amount of TRX available for unfreezing
- **Use when**: User asks for "how much TRX can I unfreeze" or "unfreezable TRX".
- **Input**: `address` (required).

### getFreezeResource

- **API**: `getFreezeResource` — Get TRX staking rate data
- **Use when**: User asks for "TRX staking rate" or "staking APY trend".
- **Input**: Optional `startDay`, `endDay` (yyyy-MM-dd).

## Troubleshooting

- **MCP connection failed**: If you see "Connection refused", verify TronScan MCP is connected in Settings > Extensions.
- **API rate limit / 429**: TronScan API has call count and frequency limits when no API key is used. If you encounter rate limiting or 429 errors, go to [TronScan Developer API](https://tronscan.org/#/developer/api) to apply for an API key, then add it to your MCP configuration and retry.

### Invalid address
Ensure the address is a valid TRON base58 format (starts with T). For contract analysis, use **tronscan-contract-analysis** skill instead.

## Notes

- When `getAccountTokens`, `getTokenAssetOverview`, or `getWalletTokens` returns token holdings, each token item may include risk fields such as `tokenCanShow` and `tokenLevel`. If any held token has `tokenCanShow: false` or `tokenLevel` of `"3"` (Suspicious) / `"4"` (Unsafe), flag it to the user — the wallet may be holding risky or spam tokens. See **tronscan-token-scanner** for full field semantics and judgment order.

