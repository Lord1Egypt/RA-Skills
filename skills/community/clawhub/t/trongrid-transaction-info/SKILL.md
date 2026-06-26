---
name: trongrid-transaction-info
description: "Query and decode TRON transactions including status, confirmation, sender/receiver, resource costs, internal transactions, event logs, and failure analysis. Use when a user asks about a transaction hash, wants to check if a transaction succeeded, understand what a transaction did, or debug a failed transaction."
metadata:
  version: "1.0.0"
  mcp-server: trongrid
---

# Transaction Info

Query and intelligently decode TRON transactions — result status, confirmation, resource consumption, decoded method calls, internal transactions, event logs, and failure diagnosis.

# MCP Server
- **Prerequisite**: [TronGrid MCP Guide](https://developers.tron.network/reference/mcp-api)

## Instructions

### Step 1: Fetch Transaction Data

Run two complementary calls in parallel:

1. `getTransactionById` — Type, raw data, sender/receiver, contract parameters, signatures, timestamp, expiration
2. `getTransactionInfoById` — Result (SUCCESS/FAILED/REVERT), block number/timestamp, fee, energy/bandwidth usage, contract return value, internal txs, event logs

### Step 2: Check Confirmation Status

1. `getBlock` (no params) — Get current block height
2. Compare transaction's block number with latest block
3. `solidityGetTransactionById` — Check if confirmed by solidity node (irreversible)

Classification:
- **Confirmed (Irreversible)**: Found on solidity node
- **Confirmed (Not yet irreversible)**: In recent block, not solidified
- **Pending**: Use `getTransactionFromPending` if needed
- **Not Found**: Invalid hash or expired

### Step 3: Decode Transaction Type

| Contract Type | Description | Key Fields |
|--------------|-------------|------------|
| TransferContract | TRX transfer | from, to, amount |
| TransferAssetContract | TRC-10 transfer | from, to, asset, amount |
| TriggerSmartContract | Contract call | contract, data (method + params) |
| FreezeBalanceV2Contract | Stake 2.0 freeze | owner, amount, resource |
| UnfreezeBalanceV2Contract | Stake 2.0 unfreeze | owner, amount, resource |
| DelegateResourceContract | Resource delegation | from, to, resource, amount |
| VoteWitnessContract | SR voting | owner, votes list |
| CreateSmartContract | Contract deployment | owner, bytecode, ABI |

### Step 4: Decode Smart Contract Calls

For `TriggerSmartContract`:

1. Extract method signature (first 4 bytes of data)
2. Common signatures:
   - `a9059cbb` = `transfer(address,uint256)`
   - `095ea7b3` = `approve(address,uint256)`
   - `23b872dd` = `transferFrom(address,address,uint256)`
3. If ABI available (via `getContract`), fully decode method name, parameters, and return value
4. Decode event logs for what actually happened

### Step 5: Analyze Resource Consumption

From receipt, break down:
- **Energy**: Used amount, from staking vs. burned TRX
- **Bandwidth**: Used amount, free vs. staked
- **Fee**: Total TRX paid (divide by 1,000,000 for TRX)
- **Energy Penalty**: Over-usage penalty if applicable

### Step 6: Internal Transactions

Call `getInternalTransactionsByTxId` for:
- TRX transfers between contracts
- Contract-to-contract calls
- Token distributions in complex transactions

### Step 7: Parse Event Logs

Decode to human-readable descriptions:
- Transfer → "[amount] [token] from [A] to [B]"
- Approval → "[A] approved [B] to spend [amount]"
- Swap → "[A] swapped [X] tokenA for [Y] tokenB"

### Step 8: Compile Transaction Report

```
## Transaction: [txid]

### Status
- Result: [SUCCESS / FAILED / REVERT]
- Confirmation: [Irreversible / Confirmed / Pending]
- Block: #[number] ([timestamp])

### Participants
- From: [address]
- To: [address / contract]
- Value: [amount] TRX / [token]

### Decoded Action
[Human-readable description]
e.g., "Transferred 1,000 USDT from TXxx... to TYyy..."
e.g., "Staked 10,000 TRX for Energy (Stake 2.0)"

### Resource Costs
- Energy: [amount] (staked: [X], burned: [Y])
- Bandwidth: [amount]
- Total Fee: [amount] TRX

### Internal Transactions
| From | To | Value | Note |
|------|----|-------|------|

### Events
[Decoded event logs]

### Failure Analysis (if failed)
- Revert Reason: [decoded]
- Likely Cause: [analysis]
- Suggestion: [actionable fix]
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Transaction not found | Invalid hash, too old, or not yet broadcast | Verify hash format (64 hex chars); check pending pool with `getTransactionFromPending` |
| No receipt data | Transaction still pending | Note "Transaction pending, receipt not yet available" |
| Cannot decode method | No ABI available for contract | Show raw data hex, identify common method signatures manually |
| REVERT without reason | Contract reverted without error message | Check energy limit, parameter validity, and contract state |

## Examples

- [Check transfer status](examples/check-transfer-status.md)
- [Decode a contract call](examples/decode-contract-call.md)
