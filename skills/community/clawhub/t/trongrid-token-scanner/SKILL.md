---
name: trongrid-token-scanner
description: "Deep analysis of any specific TRC-20 or TRC-10 token on TRON including supply, price, holder distribution, contract details, activity metrics, and safety assessment. Use when a user asks about a specific token, wants to check token legitimacy, analyze holder concentration, verify token safety, or perform token due diligence."
metadata:
  version: "1.0.0"
  mcp-server: trongrid
---

# Token Scanner

In-depth analysis of any specific TRC-20 or TRC-10 token — supply, market data, holder distribution, contract details, transaction activity, and safety scoring.

# MCP Server
- **Prerequisite**: [TronGrid MCP Guide](https://developers.tron.network/reference/mcp-api)

## Instructions

### Step 1: Identify the Token

- **TRC-20**: Identified by contract address (e.g., `TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t` for USDT)
- **TRC-10**: Identified by numeric token ID or name

### Step 2: Fetch Token Metadata

**TRC-20** (run in parallel):
1. `getTrc20Info` — Name, symbol, decimals, standard, total supply
2. `getContractInfo` — Deployer, energy settings, creation time
3. `getContract` — ABI (for standard compliance check), bytecode

**TRC-10**:
1. `getAssetByIdentifier` or `getAssetByName` — Name, abbreviation, total supply, precision, issuer, issue time, URL, frozen supply

### Step 3: Analyze Holder Distribution

For TRC-20, call `getTrc20TokenHolders`:
- Top holders and balances
- Concentration: what % do top 10/50/100 holders control
- Identify if whale addresses are exchanges or known entities

### Step 4: Examine Activity

1. `getContractTransactions` — Recent contract interactions, transaction patterns
2. `getEventsByContractAddress` — Transfer events, approvals, etc.
3. Analyze: daily volume, active addresses, organic vs. bot patterns

### Step 5: Fetch Market Data

Web search for off-chain data:
- Price (USD, BTC), 24h volume, market cap, FDV
- Exchange listings, price trends

### Step 6: Safety Assessment

Evaluate across dimensions:

| Dimension | Check | Tool |
|-----------|-------|------|
| Contract verified | ABI available? | `getContract` |
| Holder concentration | Top 10 hold >80%? | `getTrc20TokenHolders` |
| Liquidity | Volume vs. market cap ratio | Web search |
| Permissions | mint/pause/blacklist functions? | ABI analysis |
| Activity | Organic or artificial patterns? | `getContractTransactions` |

### Step 7: Compile Token Report

```
## Token Report: [Name] ([Symbol])

### Basic Info
- Contract/ID: [address or ID]
- Standard: TRC-20 / TRC-10
- Decimals: [X]
- Issuer: [address]
- Issue Date: [date]

### Supply & Market
- Total Supply: [amount]
- Price: $[X.XXXX]
- Market Cap: $[X.XX M/B]
- 24h Volume: $[X.XX M]

### Holders
- Total: [count]
- Top 10 Concentration: [X.X%]
- Largest Holder: [address] ([X.X%])

### Activity
- Daily Transactions: ~[count]
- 7-day Trend: [increasing/stable/decreasing]

### Safety Score: [Low/Medium/High Risk]
- Contract Verified: [Yes/No]
- Holder Concentration: [Low/Medium/High]
- Liquidity: [Good/Fair/Poor]
- Red Flags: [list if any]
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Token not found | Invalid contract address or token ID | Ask user to verify; suggest searching by name with `getAssetByName` |
| No holders data | New token or API limitation | Note "Holder data unavailable", continue with other metrics |
| ABI unavailable | Unverified contract | Flag as risk factor, proceed with transaction-based analysis |
| TRC-10 name collision | Multiple TRC-10 tokens share same name | Use `getAssetByIdentifier` with numeric ID instead |
| No market data | Unlisted token | Report on-chain data only, note "Not listed on price aggregators" |

## Examples

- [Scan USDT token on TRON](examples/scan-usdt-token.md)
- [Token safety check](examples/token-safety-check.md)
