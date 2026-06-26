# Example: DeFi Tokens on TRON

## User Prompt

```
Show me all the DeFi tokens on TRON — which ones are trending?
```

## Expected Workflow

1. **Resolve addresses** → Filter built-in reference list to DeFi category: SUN, JST, WIN
2. **Token Info** → `getTrc20Info(address)` × each (parallel) → Name, symbol, decimals, total supply
3. **Holders** → `getTrc20TokenHolders(address, limit=5)` × each (parallel) → Holder distribution
4. **Events** → `getEventsByContractAddress(address, limit=50)` × top 3 → Recent on-chain activity
5. **Contract Info** → `getContractInfo(address)` × each (parallel) → Deployment and settings

## Expected Output (Sample)

```
## DeFi Tokens on TRON

TRON's DeFi ecosystem is anchored by the SUN.io platform, with multiple
governance and utility tokens supporting DEX, lending, and oracle protocols.

### DeFi Token Data (on-chain)

| Token    | Symbol | Total Supply       | Top Holder Balance | Recent Events | Contract Verified |
|----------|--------|--------------------|--------------------|--------------|-------------------|
| SUN      | SUN    | 19,961,072,975     | ...                | 50           | Yes               |
| JUST     | JST    | 9,900,000,000      | ...                | 50           | Yes               |
| WINkLink | WIN    | 999,000,000,000    | ...                | 50           | Yes               |

> Note: Price and market cap data are not available via TronGrid.

### Activity Signals (from recent events)
- **SUN**: X Transfer events in last 50 logs → [active/quiet]
- **JST**: X Transfer events → [active/quiet]
- **WIN**: X Transfer events → [active/quiet]
```

## MCP Tools Used

| Tool | Call Count | Purpose |
|------|-----------|---------|
| `getTrc20Info` | 3 | Token metadata per contract |
| `getTrc20TokenHolders` | 3 | Holder distribution |
| `getEventsByContractAddress` | 3 | Recent activity signals |
| `getContractInfo` | 3 | Contract details and verification |
