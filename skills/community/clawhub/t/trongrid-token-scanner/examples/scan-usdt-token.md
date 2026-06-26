# Example: Scan USDT Token

## User Prompt

```
Tell me about USDT on TRON — full token analysis.
```

## Expected Workflow

1. **Token Metadata** → `getTrc20Info("TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t")` → Name, symbol, decimals
2. **Contract Info** → `getContractInfo("TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t")` → Deployer, energy settings
3. **Contract ABI** → `getContract("TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t")` → ABI for verification
4. **Top Holders** → `getTrc20TokenHolders("TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t", limit=20)` → Distribution
5. **Transactions** → `getContractTransactions("TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t", limit=100)` → Activity
6. **Events** → `getEventsByContractAddress("TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t", limit=100)` → Transfer events
7. **Web Search** → "USDT TRON market cap price" → Current market data
8. **Total Supply** → `triggerConstantContract(owner, contract, "totalSupply()")` → On-chain total supply

## Expected Output (Sample)

```
## Token Report: Tether USD (USDT)

### Basic Info
- Contract: TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t
- Standard: TRC-20
- Decimals: 6
- Issuer: THPvaUhoh2Qn2y9THCZML3H4Af3Q3A9m6r (Tether Treasury)
- Issue Date: April 16, 2019

### Supply & Market
- Total Supply: 62,500,000,000 USDT
- Circulating Supply: ~62,500,000,000 USDT
- Price: $1.0001
- Market Cap: $62.5B (TRON chain)
- 24h Volume: $18.5B (all chains)

### Holder Analysis
- Total Holders: 48,500,000+
- Top 10 Concentration: 35.2%
- Top 50 Concentration: 48.5%
- Largest Holder: TKHuVxYfT4... (12.5B USDT, 20%)

### Activity Metrics
- Daily Transactions: ~800,000
- Daily Active Addresses: ~120,000
- 7-day Trend: Stable

### Safety Score: Low Risk

- Contract Verified: Yes (ABI available, matches reference implementation)
- Holder Concentration: Medium (top 10 hold 35%, but mostly exchanges)
- Liquidity Depth: Excellent
- Red Flags: None — however note admin can blacklist addresses and pause transfers
- Issuer: Tether Limited (established, regulated entity)
```

## MCP Tools Used

| Tool | Call Count | Purpose |
|------|-----------|---------|
| `getTrc20Info` | 1 | Token metadata |
| `getContractInfo` | 1 | Contract settings |
| `getContract` | 1 | ABI verification |
| `getTrc20TokenHolders` | 1 | Top holders |
| `getContractTransactions` | 1 | Activity data |
| `getEventsByContractAddress` | 1 | Transfer events |
| `triggerConstantContract` | 1 | Total supply query |
