# Example: Check Transfer Status

## User Prompt

```
Did my transaction go through?
Hash: 7c2d4206c03a883dd9066d620335dc1be272a8dc733cfa3f6d10308faa37facc
```

## Expected Workflow

1. **Transaction Details** → `getTransactionById("7c2d4206...")` → Type, sender, receiver, amount
2. **Transaction Receipt** → `getTransactionInfoById("7c2d4206...")` → Status, fees, block
3. **Confirmation Check** → `solidityGetTransactionById("7c2d4206...")` → Irreversibility
4. **Current Block** → `getBlock()` (no params) → Block height comparison
5. **Internal Txs** → `getInternalTransactionsByTxId("7c2d4206...")` → Internal transfers
6. **Events** → `getEventsByTransactionId("7c2d4206...")` → Emitted events

## Expected Output (Sample)

```
## Transaction Report

### Overview
- Transaction ID: 7c2d4206c03a883dd9066d620335dc1be272a8dc...
- Status: SUCCESS ✅
- Confirmation: Confirmed (Irreversible)
- Block: #70,120,345 (2026-03-11 09:15:00 UTC)
- Type: TRC-20 Token Transfer

### Participants
- From: TUoHaVjx7n5xz8LwPRDckgFrDWhMhuSuJM
- To: TLsV52sRDL79HXGGm9yzwKibb6BeruhUzy
- Contract: TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t (USDT)

### Transaction Decoded
Transferred 1,000.000000 USDT from TUoHa... to TLsV5... via the USDT contract.

Method: transfer(address,uint256)
- Recipient: TLsV52sRDL79HXGGm9yzwKibb6BeruhUzy
- Amount: 1,000,000,000 (1,000 USDT, 6 decimals)

### Resource Consumption
- Energy Used: 14,631 (from staking: 14,631, burned: 0)
- Bandwidth Used: 345 (free: 345, staked: 0)
- Total Fee: 0 TRX (fully covered by staked resources)

### Event Logs
1. Transfer(from=TUoHa..., to=TLsV5..., value=1000000000)
   → 1,000 USDT transferred successfully
```

## MCP Tools Used

| Tool | Call Count | Purpose |
|------|-----------|---------|
| `getTransactionById` | 1 | Transaction details |
| `getTransactionInfoById` | 1 | Receipt & fees |
| `solidityGetTransactionById` | 1 | Confirmation status |
| `getBlock` | 1 | Current block height (no params) |
| `getInternalTransactionsByTxId` | 1 | Internal transfers |
| `getEventsByTransactionId` | 1 | Event logs |
