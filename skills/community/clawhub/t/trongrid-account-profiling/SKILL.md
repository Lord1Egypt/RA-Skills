---
name: trongrid-account-profiling
description: "Analyze any TRON account's assets, token holdings, staking, voting, energy/bandwidth, and transaction patterns. Use when a user asks about a TRON address, wants to check wallet balance, analyze account activity, track whale wallets, or look up what an address holds. Covers TRX balance, TRC-20/TRC-10 tokens, resource usage, delegation, voting rewards, transaction history, and DeFi participation."
metadata:
  version: "1.0.0"
  mcp-server: trongrid
---

# Account Profiling

Build a comprehensive profile of any TRON account covering asset holdings, resource status, staking/voting behavior, transaction patterns, and investment preferences.

# MCP Server
- **Prerequisite**: [TronGrid MCP Guide](https://developers.tron.network/reference/mcp-api)

## Instructions

### Step 1: Validate the Address

Call `validateAddress` with the target address. If invalid, inform the user and ask for correction before proceeding.

### Step 2: Fetch Account Fundamentals

Run these calls in parallel for speed:

1. `getAccount` — TRX balance, TRC-10 holdings (assetV2), creation time, permissions, frozen balances (Stake 1.0 & 2.0), vote info
2. `getAccountResource` — Energy/bandwidth limits, usage, delegated resources, staked TRX amounts
3. `getAccountNet` — Free and staked bandwidth details

### Step 3: Fetch Token Holdings

1. `getTrc20Balance` — All TRC-20 token balances
2. For significant holdings, call `getTrc20Info` with contract addresses to resolve token names, symbols, and decimals
3. TRC-10 assets are already in the `getAccount` response (assetV2 field)

### Step 4: Analyze Staking & Voting

1. `getDelegatedResourceAccountIndexV2` — List of addresses this account delegates to / receives from
2. `getDelegatedResourceV2` — Detailed delegation amounts for specific pairs
3. `getReward` — Unclaimed voting rewards
4. Extract vote list from `getAccount` response to show which SRs the account votes for

### Step 5: Examine Transaction History

1. `getAccountTransactions` — Recent transaction history (use `limit` and `order_by` params)
2. `getAccountTrc20Transactions` — TRC-20 transfer history
3. `getInternalTransactions` — Contract-triggered internal transfers

Analyze patterns: frequency, common types (transfers/contract calls/staking), most-interacted addresses, average value.

### Step 6: Identify DeFi Participation

From transaction history, identify interactions with known DeFi protocols (SunSwap, JustLend, SunIO, etc.) and categorize as DEX trades, liquidity provision, lending/borrowing, or yield farming.

### Step 7: Compile Account Profile

Present findings in this format:

```
## Account Profile: [address]

### Overview
- Created: [date]
- Account Type: [Regular/Contract/SR]
- Total Asset Value: ~$[estimated USD value]

### TRX Holdings
- Available: [amount] TRX
- Staked (Energy): [amount] TRX
- Staked (Bandwidth): [amount] TRX

### Token Holdings
| Token | Balance | Value (USD) |
|-------|---------|-------------|
| USDT  | X,XXX   | $X,XXX      |

### Resources
- Energy: [used]/[total] ([X%] utilized)
- Bandwidth: [used]/[total] ([X%] utilized)

### Voting & Staking
- Votes Cast: [total]
- Voting For: [SR list]
- Unclaimed Rewards: [amount] TRX

### Activity Analysis
- Recent Activity (30d): [count] transactions
- Primary Activities: [transfer/contract call/staking]
- Most Interacted Contracts: [list]

### Account Classification
- Type: [Whale/Active Trader/HODLer/DeFi User/Developer/Inactive]
- Activity Trend: [Increasing/Stable/Decreasing]
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Invalid address | Malformed TRON address | Ask user to verify the address format (T-prefix, 34 chars) |
| Empty account | Address exists but never activated | Inform user this address has no on-chain activity |
| No TRC-20 data | Account has no TRC-20 tokens | Skip token section, note "No TRC-20 holdings found" |
| API timeout | TronGrid rate limit or network issue | Retry the specific failed call; partial results are still useful |

## Examples

- [Check account balance and holdings](examples/check-account-balance.md)
- [Analyze a whale account](examples/analyze-whale-account.md)
