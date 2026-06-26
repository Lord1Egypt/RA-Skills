# Example: Check Account Balance

## User Prompt

```
What is the balance of TUoHaVjx7n5xz8LwPRDckgFrDWhMhuSuJM?
```

## Expected Workflow

1. **Validate** → `validateAddress("TUoHaVjx7n5xz8LwPRDckgFrDWhMhuSuJM")`
2. **Account Info** → `getAccount("TUoHaVjx7n5xz8LwPRDckgFrDWhMhuSuJM")` → TRX balance + TRC-10 tokens
3. **TRC-20 Balances** → `getTrc20Balance("TUoHaVjx7n5xz8LwPRDckgFrDWhMhuSuJM")` → Token holdings
4. **Token Names** → `getTrc20Info(contractList)` → Resolve token symbols and decimals

## Expected Output (Sample)

```
## Account Profile: TUoHaVjx7n5xz8LwPRDckgFrDWhMhuSuJM

### TRX Holdings
- Available: 15,230.456 TRX (~$3,500)
- Staked: 0 TRX
- Total: 15,230.456 TRX

### Token Holdings
| Token | Balance    | Value (USD) |
|-------|-----------|-------------|
| USDT  | 5,000.00  | $5,000      |
| WIN   | 120,000   | $12         |

### Resources
- Energy: 0/0 (no staking)
- Bandwidth: 600/600 (free bandwidth only)

### Account Classification
- Type: Small holder
- Activity Trend: Low
```

## MCP Tools Used

| Tool | Call Count | Purpose |
|------|-----------|---------|
| `validateAddress` | 1 | Verify format |
| `getAccount` | 1 | TRX balance + TRC-10 |
| `getTrc20Balance` | 1 | TRC-20 tokens |
| `getTrc20Info` | 1 | Token metadata |
