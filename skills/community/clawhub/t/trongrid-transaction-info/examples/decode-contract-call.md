# Example: Decode a Contract Call

## User Prompt

```
What happened in this transaction?
bd32eef7469d57011a092c59c745cab1e49c501e9f0ac15c580656f9ead1e319
```

## Expected Workflow

1. **Transaction Details** → `getTransactionById("bd32eef7...")` → Raw data, contract type
2. **Transaction Receipt** → `getTransactionInfoById("bd32eef7...")` → Result, logs, fees
3. **Confirmation** → `solidityGetTransactionById("bd32eef7...")` → Check finality
4. **Contract ABI** → `getContract(contractAddress)` → ABI for decoding method + events
5. **Internal Txs** → `getInternalTransactionsByTxId("bd32eef7...")` → Internal transfers
6. **Events** → `getEventsByTransactionId("bd32eef7...")` → Decoded events

## Expected Output (Sample)

```
## Transaction Report

### Overview
- Transaction ID: bd32eef7469d57011a092c59c745cab1e49c501e...
- Status: SUCCESS ✅
- Confirmation: Confirmed (Irreversible)
- Block: #70,118,200 (2026-03-11 08:45:12 UTC)
- Type: Smart Contract Call (TriggerSmartContract)

### Participants
- From: TJmmqjb1DK9TTZbQXzRQ2AuA94z4gKAPFh
- Contract: TKcEU8ekq2ZoFzLSGFYCUY6aocJBX9X31b (SunSwap V2 Router)

### Transaction Decoded
Swapped 5,000 TRX for ~420.5 USDT on SunSwap V2.

Method: swapExactETHForTokens(uint256,address[],address,uint256)
- minAmountOut: 415,000,000 (415 USDT minimum)
- path: [WTRX → USDT]
- recipient: TJmmqjb1DK9TTZbQXzRQ2AuA94z4gKAPFh
- deadline: 1741686432

### Resource Consumption
- Energy Used: 85,420 (from staking: 50,000, burned TRX: 35,420)
- Bandwidth Used: 580 (staked: 580)
- Total Fee: 14.88 TRX (energy burn)

### Internal Transactions
| # | From        | To           | Value      | Note          |
|---|-------------|-------------|------------|---------------|
| 1 | TJmm...     | TKcE...(Router) | 5,000 TRX | Swap input    |
| 2 | TKcE...(Router) | TPai...(Pair) | 5,000 TRX | Route to pool |
| 3 | TPai...(Pair) | WTRX      | 5,000 TRX  | Wrap TRX      |

### Event Logs
1. Transfer(from=TPair..., to=TJmm..., value=420500000)
   → 420.5 USDT sent to user
2. Swap(sender=TKcE..., amount0In=5000000000, amount1Out=420500000)
   → Pool swap: 5,000 TRX in, 420.5 USDT out
3. Sync(reserve0=12500000000000, reserve1=1050000000000)
   → Pool reserves updated
```

## MCP Tools Used

| Tool | Call Count | Purpose |
|------|-----------|---------|
| `getTransactionById` | 1 | Raw transaction data |
| `getTransactionInfoById` | 1 | Receipt, fees, logs |
| `solidityGetTransactionById` | 1 | Finality check |
| `getContract` | 1 | ABI for decoding |
| `getInternalTransactionsByTxId` | 1 | Internal transfers |
| `getEventsByTransactionId` | 1 | Decoded events |
