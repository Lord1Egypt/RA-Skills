---
name: stx-agent
skill: stx
description: Stacks L2 STX token and smart contract operations — check balances, transfer STX, broadcast transactions, call and deploy Clarity contracts, and check transaction status.
---

# STX Agent

This agent handles Stacks L2 STX token operations and Clarity smart contract interactions using the Hiro API. Balance and status queries work without a wallet. Transfer, contract call, contract deploy, and broadcast operations require an unlocked wallet.

## Prerequisites

- For `get-balance` and `get-transaction-status`: no wallet required — just a Stacks address or txid
- For `transfer`, `call-contract`, `deploy-contract`, `broadcast-transaction`: wallet must be unlocked (`bun run wallet/wallet.ts unlock`)
- For fee estimation: network access to Hiro API is required

## Decision Logic

| Goal | Subcommand |
|------|-----------|
| Check STX balance | `get-balance` — pass `--address` or relies on active wallet |
| Send STX to an address | `transfer` — requires `--recipient` and `--amount` in micro-STX |
| Call a write function on a contract | `call-contract` — requires contract address, name, function name, and optional args |
| Deploy a new Clarity contract | `deploy-contract` — requires `--contract-name` and `--code-body` |
| Submit a pre-signed transaction | `broadcast-transaction` — requires `--signed-tx` hex string |
| Check if a transaction confirmed | `get-transaction-status` — requires `--txid` |

## Safety Checks

- Before `transfer`: verify the sender's STX balance covers amount + estimated fee (run `get-balance` first)
- Before `call-contract` with `--post-condition-mode allow`: understand that this permits any asset movement; prefer `deny` (default) with explicit post conditions
- Before `deploy-contract`: verify the Clarity source compiles locally (`clarinet check`) before deploying to avoid wasted fees
- All write operations are irreversible once confirmed — confirm amount, recipient, and contract details before submitting
- Use `get-transaction-status` to confirm a transaction completed before taking dependent actions

## Error Handling

| Error message | Cause | Fix |
|--------------|-------|-----|
| "No Stacks address provided and wallet is not unlocked." | `get-balance` called without `--address` and no active wallet | Provide `--address` or run `wallet unlock` first |
| "Wallet is locked" | Wallet session expired or not yet unlocked | Run `bun run wallet/wallet.ts unlock --password <password>` |
| "insufficient funds" | STX balance too low for amount + fee | Check balance with `get-balance`, reduce amount or wait for funds |
| "Invalid --args JSON" | Malformed JSON passed to `--args` | Ensure `--args` is a valid JSON array string |
| "Invalid --post-conditions JSON" | Malformed JSON passed to `--post-conditions` | Check JSON array format against SKILL.md examples |
| "ConflictingNonceInMempool" | Prior transaction still pending with same nonce | Wait for pending transaction to confirm, then retry |

## Output Handling

- `get-balance`: read `balance.microStx` for raw value, `balance.stx` for human-readable; use `explorerUrl` for verification
- `transfer`: extract `txid` and pass to `get-transaction-status` to confirm; `from` and `recipient` confirm sender and destination
- `call-contract`: extract `txid` for status tracking; `contract` field confirms which contract was called
- `deploy-contract`: extract `contractId` (format: `<address>.<name>`) for subsequent `call-contract` invocations
- `broadcast-transaction`: extract `txid` to track the pre-signed transaction
- `get-transaction-status`: check `status` field — `"success"` means confirmed; `"pending"` means still in mempool

## Example Invocations

```bash
# Check STX balance for the active wallet
bun run stx/stx.ts get-balance

# Transfer 2 STX to another address
bun run stx/stx.ts transfer --recipient SP2... --amount 2000000

# Call a Clarity contract function with typed arguments
bun run stx/stx.ts call-contract --contract-address SP2... --contract-name my-contract --function-name transfer --args '[{"type":"uint","value":100}]'
```
