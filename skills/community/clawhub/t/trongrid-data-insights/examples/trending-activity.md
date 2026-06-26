# Example: Trending Activity

## User Prompt

```
What is trending on TRON right now? Show me the most active contracts and tokens.
```

## Expected Workflow

1. **Recent Blocks** → loop `getBlock(id_or_num)` × 20 (decrement from latest) → Last 20 blocks with transactions
2. **Block Transactions** → `getTransactionInfoByBlockNum(N)` × 20 → Categorize by contract
3. **Latest Events** → `getEventsByLatestBlock()` → Identify Transfer events for trending tokens
4. **Contract Info** → `getContractInfo(address)` × top 5 → Contract names and details
5. **Token Info** → `getTrc20Info(contractList)` → Token metadata for top tokens
6. **Top Holders** → `getTrc20TokenHolders(address)` × top 3 → Holder data for trending tokens
7. **Web Search** → Search for TRON trending tokens → Price and volume data

## Expected Output (Sample)

```
## What's Trending on TRON

### Hot Contracts (Last 20 Blocks)
| Rank | Contract | Name         | Calls | Category   | Trend     |
|------|----------|-------------|-------|------------|-----------|
| 1    | TR7N...  | USDT        | 2,400 | Stablecoin | Steady    |
| 2    | TKcE...  | SunSwap V2  | 950   | DEX        | +15% ↑    |
| 3    | TXJg...  | JustLend    | 420   | Lending    | +8% ↑     |
| 4    | TSSz...  | SUN Token   | 280   | DeFi       | +22% ↑    |
| 5    | TPYm...  | WINkLink    | 195   | Oracle     | Steady    |

### Trending Tokens (by Transfer Volume)
| Rank | Token | Symbol | Transfers (20 blk) | Volume        |
|------|-------|--------|-------------------|---------------|
| 1    | USDT  | USDT   | 2,200             | $45,000,000   |
| 2    | USDC  | USDC   | 380               | $8,500,000    |
| 3    | SUN   | SUN    | 250               | $1,200,000    |
| 4    | JST   | JST    | 180               | $450,000      |
| 5    | BTT   | BTT    | 120               | $180,000      |

### Most Active Accounts
| Rank | Address  | Tx Count | Type     |
|------|----------|----------|----------|
| 1    | TJDa...  | 85       | Bot      |
| 2    | TLsV...  | 62       | Exchange |
| 3    | THPv...  | 45       | Whale    |

### Key Observations
- SunSwap V2 DEX activity up 15% — likely driven by new liquidity pairs
- SUN token showing increased activity (+22%) — possible governance event
- USDT continues to dominate with ~60% of all contract calls
- Bot activity accounts for ~12% of recent transactions
```

## MCP Tools Used

| Tool | Call Count | Purpose |
|------|-----------|---------|
| `getBlock` | 20 | Recent blocks (loop, decrement `id_or_num`) |
| `getTransactionInfoByBlockNum` | 20 | Transaction details |
| `getEventsByLatestBlock` | 1 | Latest events |
| `getContractInfo` | 5 | Contract names |
| `getTrc20Info` | 1 | Token metadata |
| `getTrc20TokenHolders` | 3 | Holder data |
