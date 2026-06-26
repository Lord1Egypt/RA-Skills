---
name: tronscan-transaction-info
description: |
  Query TRON transaction result, confirmation status, sender, resource consumption.
  Use when user asks "why did this tx fail", "tx status", "who sent it", "energy consumed", provides a tx hash, or asks about transaction details.
  Do NOT use for address balance or token holders (use tronscan-account-profiler or tronscan-token-scanner).
metadata:
  author: tronscan-mcp
  version: "1.0"
  mcp-server: https://mcp.tronscan.org/mcp
---

# Transaction Info

## Overview

| Tool | Function | Use Case |
|------|----------|----------|
| getTransactionDetail | Tx by hash | Type, confirmation, amount, energy/bandwidth |
| getTransactionList | Tx list | List with filters, sort, pagination |
| getTrc20Transfers | TRC20/721 transfers | Token transfer records |
| getTrc20TransfersWithStatus | TRC20 with status | TRC20 transfers plus tx status |
| getTrc1155Transfers | TRC1155 transfers | Multi-token transfers |
| getTransferList | TRX/TRC10 transfers | Native TRX and TRC10 transfers |
| getInternalTransactions | Internal txs | Contract internal calls |
| getTransactionStatistics | Tx statistics | Aggregate tx and token volume |
| getTransferStatistics | Transfer statistics | Transfer activity by token type |
| getExchangeTransactions | Exchange txs | Exchange-type transactions |

## Use Cases

1. **Transaction Result**: Use `getTransactionDetail` for success/fail and confirmation.
2. **Confirmation Status**: Confirmation and block info are in `getTransactionDetail`.
3. **Sender / Receiver**: Use `getTransactionDetail` for from/to; use transfer tools for token flows.
4. **Resource Consumption**: Energy and bandwidth used are in `getTransactionDetail`.
5. **Token Transfers in Tx**: Use `getTransactionDetail`; its response includes `trc20TransferInfo`, `transfersAllList`, and other tx-level transfer info.
6. **Internal Calls**: Use `getInternalTransactions` for contract internal txs.

## MCP Server

- **Prerequisite**: [TronScan MCP Guide](https://mcpdoc.tronscan.org)

## Tools

### getTransactionDetail

- **API**: `getTransactionDetail` — Get transaction detail by hash (type, confirmation, amount, energy/bandwidth)
- **Use when**: User provides a tx hash or asks "transaction status", "tx result", or "token transfers in this tx".
- **Input**: Transaction hash (txid).
- **Response**: Type, confirmed, amount, energy, bandwidth, from, to, block, `trc20TransferInfo`, `transfersAllList`, and other tx-level transfer info.
- **Units**:
  - `net_fee`, `energy_fee`, `fee_limit`: in **sun** (1 TRX = 10⁶ sun); divide by 1,000,000 to get TRX.
  - `amount_str`(TRC20): in **smallest unit**; divide by 10^decimals to get human-readable amount.
  - `contractData.amount` (TRX transfer): in **sun** (1 TRX = 10⁶ sun); divide by 1,000,000 to get TRX.

### getTransactionList

- **API**: `getTransactionList` — Get transaction list with pagination, sort, and filters
- **Use when**: User asks for "list of transactions" or "recent txs" for an address or globally.

### getTrc20Transfers / getTrc20TransfersWithStatus

- **API**: `getTrc20Transfers` — Get TRC20/TRC721 transfer records; `getTrc20TransfersWithStatus` — Get TRC20 transfers with tx status
- **Use when**: User asks for "token transfer" or "TRC20 transfer" by **address**, **contract**, or **time range**. For transfers within a single tx, use `getTransactionDetail`.

### getTrc1155Transfers

- **API**: `getTrc1155Transfers` — Get TRC1155 transfer records
- **Use when**: User asks for TRC1155 transfers by **address**, **contract**, or **time range**. For transfers within a single tx, use `getTransactionDetail`.

### getTransferList

- **API**: `getTransferList` — Get TRX and TRC10 transfer records
- **Use when**: User asks for "TRX transfer" or "TRC10 transfer" by **address**, **contract**, or **time range**. For transfers within a single tx, use `getTransactionDetail`.

### getInternalTransactions

- **API**: `getInternalTransactions` — Get smart contract internal transaction list
- **Use when**: User asks for "internal tx" or "contract internal call".

### getTransactionStatistics / getTransferStatistics

- **API**: `getTransactionStatistics` — Get transaction statistics (total tx, token tx volume, etc.); `getTransferStatistics` — Get transfer statistics by token type
- **Use when**: User asks for "tx volume" or "transfer distribution".

### getExchangeTransactions

- **API**: `getExchangeTransactions` — Get exchange-type transactions
- **Use when**: User asks for "exchange transactions" or "DEX transactions".
- **Response**: Exchange-type transaction list.

## Workflow: Transaction Investigation

> User: "Why did this tx fail?" or "Who sent it, what did it do?"

1. **tronscan-transaction-info** — Use tx hash to call `getTransactionDetail` → result, confirmation, from/to, amount, energy/bandwidth.
2. If asking about **sender or receiver**: **tronscan-account-profiler** — `getAccountDetail`(from/to address) for balance and resources; if counterparty is a contract, **tronscan-contract-analysis** — `getContractDetail`(contract address).
3. If **token transfers within the tx** are needed: `getTransactionDetail` response already includes `trc20TransferInfo`, `transfersAllList`, etc. — no need to call transfer list tools. If **internal calls** needed: `getInternalTransactions` (pass tx hash as parameter where supported).

**Data handoff**: User-provided tx hash is input for step 1. The from/to or contract address from step 1 feeds into step 2.

## Troubleshooting

- **MCP connection failed**: If you see "Connection refused", verify TronScan MCP is connected in Settings > Extensions.
- **API rate limit / 429**: TronScan API has call count and frequency limits when no API key is used. If you encounter rate limiting or 429 errors, go to [TronScan Developer API](https://tronscan.org/#/developer/api) to apply for an API key, then add it to your MCP configuration and retry.

### Invalid tx hash
Ensure the hash is a valid TRON transaction ID (64 hex chars). If tx not found, it may be pending or on a different network.

## Notes

- Always use `getTransactionDetail` first when user has a tx hash; token transfers within the tx are already in its response—no need to call `getTrc20Transfers` / `getTrc1155Transfers` / `getTransferList`.
- `getTrc20Transfers`, `getTrc1155Transfers`, `getTransferList` are for address, contract, or time-range investigation; they **do not expose tx hash filter parameters**. Do not fabricate tx-hash filter or claim filtering by tx hash.
- Energy/bandwidth in response are in the same unit as chain (energy in units, bandwidth in bytes).
- Token entries in `trc20TransferInfo` and `transfersAllList` may include risk fields such as `tokenCanShow` and `tokenLevel`. If the transacted token has `tokenCanShow: false` or `tokenLevel` of `"3"` / `"4"`, warn the user that this transaction involves a potentially risky token. See **tronscan-token-scanner** for full field semantics.
