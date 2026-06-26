# Example: Top TRON Tokens

## User Prompt

```
What are the top tokens on TRON?
```

## Expected Workflow

1. **Resolve addresses** → Use built-in reference list (USDT, USDD, SUN, JST, WIN, BTT, USDJ)
2. **Token Info** → `getTrc20Info(address)` × each token (parallel calls) → Name, symbol, decimals, total supply
3. **Holders** → `getTrc20TokenHolders(address, limit=5)` × each token (parallel) → Top holders
4. **Activity** → `getContractTransactions(address, limit=20)` × each token (parallel) → Recent tx count
5. **TRC-10 Assets** → `getPaginatedAssetIssueList(limit=10, offset=0)` → Top TRC-10 tokens

## Expected Output (Sample)

```
## TRON Token Overview

### TRC-20 Tokens
| Token       | Symbol | Total Supply            | Top Holder Balance | Recent Txs | Category   |
|-------------|--------|-------------------------|--------------------|-----------|------------|
| Tether      | USDT   | 62,500,000,000          | 2,600,000,000,000  | 20        | Stablecoin |
| Decentralized USD | USDD | 744,014,833         | ...                | 20        | Stablecoin |
| SUN         | SUN    | 19,961,072,975          | ...                | 20        | DeFi       |
| JUST        | JST    | 9,900,000,000           | ...                | 20        | DeFi       |

> Note: Price and market cap data are not available via TronGrid.

### TRC-10 Tokens (Top by Supply)
| Token     | ID      | Total Supply            | Precision |
|-----------|---------|-------------------------|-----------|
| BitTorrent| 1002000 | 990,000,000,000,000     | 6         |
| APENFT    | 1002508 | 999,990,000,000,000     | 6         |
```

## MCP Tools Used

| Tool | Call Count | Purpose |
|------|-----------|---------|
| `getTrc20Info` | 6 | Token metadata per contract |
| `getTrc20TokenHolders` | 6 | Holder data per contract |
| `getContractTransactions` | 6 | Activity per contract |
| `getPaginatedAssetIssueList` | 1 | TRC-10 token list |
