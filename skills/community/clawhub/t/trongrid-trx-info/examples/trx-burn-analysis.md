# Example: TRX Burn Analysis

## User Prompt

```
What's the TRX burn rate? Is TRX deflationary?
```

## Expected Workflow

1. **Total Burned** → `getBurnTrx()` → Total TRX burned to date
2. **Chain Params** → `getChainParameters()` → SR reward per block, fee structure
3. **Recent Blocks** → loop `getBlock(id_or_num)` × 20 (decrement from latest) → Recent blocks for fee sampling
4. **Block Transactions** → `getTransactionInfoByBlockNum(N)` × 20 → Fees burned per block
5. **Energy Prices** → `getEnergyPrices()` → Energy price history for burn trend
6. **Web Search** → "TRX burn rate deflationary 2026" → Historical context

## Expected Output (Sample)

```
## TRX Burn Analysis

### Current Burn Stats
- Total TRX Burned (All Time): 16,234,567,890 TRX
- Percentage of Genesis Supply Burned: 16.2%
- Value of Burned TRX: ~$3.7B (at current price)

### Daily Burn Estimate
From analysis of the latest 20 blocks:
- Average Fees per Block: 156.2 TRX
- Average Burn per Block: ~140.5 TRX (90% fee burn ratio)
- Estimated Daily Burn: ~4,046,400 TRX (~$922,000/day)

### Daily Issuance (SR Block Rewards)
- Block Reward: 16 TRX per block
- Blocks per Day: ~28,800
- Daily Issuance: 460,800 TRX

### Net Supply Change
- Daily Burn:       -4,046,400 TRX
- Daily Issuance:   +460,800 TRX
- Net Daily Change: -3,585,600 TRX ✅ DEFLATIONARY

### Annualized
- Annual Burn:       ~1,476,936,000 TRX (~1.48B)
- Annual Issuance:   ~168,192,000 TRX (~168M)
- Net Annual Change: ~-1,308,744,000 TRX (~-1.3B)
- Annual Deflation Rate: ~1.5%

### Burn Drivers
1. **USDT Transfers** (~60% of burns): Energy fees from TRC-20 transfers
2. **DeFi Activity** (~25%): Smart contract calls on SunSwap, JustLend
3. **Account Creation** (~5%): New account activation fees
4. **Other Operations** (~10%): Staking, voting, TRC-10 transfers

### Is TRX Deflationary?
**Yes.** TRX has been consistently deflationary since Proposal #54 enabled
fee burning. The daily burn rate (~4M TRX) far exceeds daily issuance
(~460K TRX), resulting in a ~1.5% annual supply reduction. Higher network
activity increases the burn rate further, making TRX more deflationary
during periods of high usage.
```

## MCP Tools Used

| Tool | Call Count | Purpose |
|------|-----------|---------|
| `getBurnTrx` | 1 | Total burned TRX |
| `getChainParameters` | 1 | Fee structure |
| `getBlock` | 20 | Recent blocks (loop, decrement `id_or_num`) |
| `getTransactionInfoByBlockNum` | 20 | Fees per block |
| `getEnergyPrices` | 1 | Energy price trend |
