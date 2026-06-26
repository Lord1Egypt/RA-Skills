# Example: Analyze a Whale Account

## User Prompt

```
Analyze the wallet TLsV52sRDL79HXGGm9yzwKibb6BeruhUzy — what does it hold,
how active is it, and is it a whale?
```

## Expected Workflow

1. **Validate Address** → `validateAddress("TLsV52sRDL79HXGGm9yzwKibb6BeruhUzy")` → Confirm valid
2. **Account Info** → `getAccount("TLsV52sRDL79HXGGm9yzwKibb6BeruhUzy")` → TRX balance, frozen assets, votes
3. **Resources** → `getAccountResource("TLsV52sRDL79HXGGm9yzwKibb6BeruhUzy")` → Energy/bandwidth limits
4. **TRC-20 Balances** → `getTrc20Balance("TLsV52sRDL79HXGGm9yzwKibb6BeruhUzy")` → Token holdings
5. **Token Metadata** → `getTrc20Info("TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t,...")` → Token names & decimals
6. **Delegation** → `getDelegatedResourceV2(from, to)` → Resources delegated/received
7. **Rewards** → `getReward("TLsV52sRDL79HXGGm9yzwKibb6BeruhUzy")` → Unclaimed rewards
8. **Transactions** → `getAccountTransactions("TLsV52sRDL79HXGGm9yzwKibb6BeruhUzy", limit=50)` → Recent activity
9. **TRC-20 Transfers** → `getAccountTrc20Transactions("TLsV52sRDL79HXGGm9yzwKibb6BeruhUzy", limit=50)` → Token transfers

## Expected Output (Sample)

```
## Account Profile: TLsV52sRDL79HXGGm9yzwKibb6BeruhUzy

### Overview
- Created: 2019-06-15
- Account Type: Regular
- Total Asset Value: ~$2,450,000

### TRX Holdings
- Available TRX: 5,200,000
- Staked TRX (Energy): 3,000,000
- Staked TRX (Bandwidth): 500,000
- Total TRX: 8,700,000

### Token Holdings
| Token | Balance      | Value (USD)   |
|-------|-------------|---------------|
| USDT  | 1,200,000   | $1,200,000    |
| USDC  | 350,000     | $350,000      |
| SUN   | 50,000      | $25,000       |

### Resources
- Energy: 12,500/580,000 (2.2% utilized)
- Bandwidth: 200/5,000 (4.0% utilized)
- Delegated to Others: 100,000 TRX (Energy)

### Voting & Staking
- Votes Cast: 3,500,000
- Voting For: SR_Alpha (2,000,000), SR_Beta (1,500,000)
- Unclaimed Rewards: 1,250 TRX
- Estimated Annual Yield: ~4.2%

### Activity Analysis
- Recent Activity (30d): 45 transactions
- Primary Activities: TRC-20 transfers, staking operations
- Most Interacted Contracts: USDT (TR7N...), SunSwap

### Account Classification
- Type: Whale
- Risk Profile: Conservative (mostly stablecoins + staking)
- Activity Trend: Stable
```

## MCP Tools Used

| Tool | Call Count | Purpose |
|------|-----------|---------|
| `validateAddress` | 1 | Verify address format |
| `getAccount` | 1 | Core account data |
| `getAccountResource` | 1 | Resource usage |
| `getTrc20Balance` | 1 | Token balances |
| `getTrc20Info` | 1 | Token metadata |
| `getDelegatedResourceV2` | 1 | Delegation info |
| `getReward` | 1 | Unclaimed rewards |
| `getAccountTransactions` | 1 | Transaction history |
| `getAccountTrc20Transactions` | 1 | TRC-20 transfers |
