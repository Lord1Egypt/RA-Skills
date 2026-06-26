---
name: query-agent
skill: query
description: Read-only Stacks blockchain queries — account info, transaction history, block data, mempool, contract info and events, network status, and read-only contract function calls.
---

# Query Agent

This agent provides read-only access to Stacks blockchain state via the Hiro API. It covers account lookups, transaction history, block info, mempool inspection, contract metadata and events, network status, and arbitrary read-only contract function calls. No wallet unlock is required for most subcommands — `get-account-info` and `get-account-transactions` will fall back to the active wallet address if no `--address` is provided.

## Prerequisites

- No wallet unlock required for most queries
- `get-account-info` and `get-account-transactions`: either provide `--address` or have an unlocked wallet (for automatic fallback)
- `call-read-only`: sender address is optional; falls back to wallet address or the contract's own address
- `NETWORK` environment variable controls which network to query (default: testnet; use `NETWORK=mainnet` for mainnet)

## Decision Logic

| Goal | Subcommand |
|------|-----------|
| Check current STX fee estimates before sending a transaction | `get-stx-fees` — returns low/medium/high tiers |
| Look up nonce or STX balance for an address | `get-account-info --address <address>` |
| Review transaction history for an address | `get-account-transactions --address <address>` |
| Inspect a specific block by height or hash | `get-block-info --height-or-hash <value>` |
| Check what transactions are pending in the mempool | `get-mempool-info` — optionally filter by `--sender-address` |
| Get a contract's ABI, functions, and deployment info | `get-contract-info --contract-id <address.name>` |
| Stream events emitted by a contract | `get-contract-events --contract-id <address.name>` |
| Check network health and current chain tip | `get-network-status` |
| Call a read-only Clarity function on a contract | `call-read-only --contract-id <id> --function-name <name>` |

## Safety Checks

- All subcommands are read-only — no funds or state are modified
- Verify the `NETWORK` env var matches the target network before querying
- For `call-read-only`, confirm the function is truly `read-only` in the contract ABI (`get-contract-info`) before calling
- `--args` for `call-read-only` must be a JSON array of hex-encoded Clarity values; malformed input returns a parse error

## Error Handling

| Error message | Cause | Fix |
|--------------|-------|-----|
| "No Stacks address provided and wallet is not unlocked." | `get-account-info` or `get-account-transactions` called without `--address` and no active wallet | Provide `--address` or unlock wallet first |
| "Invalid --args JSON: ..." | Malformed JSON array passed to `--args` in `call-read-only` | Ensure value is a valid JSON array, e.g., `'["0x01..."]'` |
| "Error: request failed with status 404" | Contract ID or block height/hash not found on the selected network | Verify the contract ID or block value and network match |
| "Error: request failed with status 429" | Hiro API rate limit exceeded | Wait briefly and retry; set `HIRO_API_KEY` in settings to raise limits |

## Output Handling

- `get-stx-fees`: read `fees.medium.microStx` for the standard fee to use in STX transfers; `byTransactionType` has per-tx-type estimates
- `get-account-info`: read `nonce` to set the nonce for manual transaction construction; `balance.microStx` for balance checks
- `get-account-transactions`: iterate `transactions[].txId` and `transactions[].status` to check confirmation; use `explorerUrl` for human-readable links
- `get-block-info`: read `height` and `burnBlockHeight` for cross-chain correlation
- `get-mempool-info`: read `transactions[].txId` to monitor a pending transaction by tx ID
- `get-contract-info`: read `functions[]` to discover callable functions and their argument types before calling
- `get-contract-events`: read `events[]` for raw event data emitted by the contract
- `get-network-status`: read `status` ("ready" = healthy); `coreInfo.stacksTipHeight` for current block height
- `call-read-only`: read `okay` (boolean) and `result` (hex-encoded Clarity value); `cause` contains the error if `okay` is false

## Example Invocations

```bash
# Get current STX fee estimates
bun run query/query.ts get-stx-fees

# Get transaction history for an address
bun run query/query.ts get-account-transactions --address SP2JKEZC09WVMR33NMHL8TNAVRCKDCJPAYV6510R6

# Call a read-only contract function
bun run query/query.ts call-read-only --contract-id SP3K8BC0PPEVCV7NZ6QSRWPQ2JE9E5B6N3PA0KBR9.amm-pool-v2-01 --function-name get-pool-details --args '[]'
```
