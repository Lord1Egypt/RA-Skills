---
name: xflows-bridge
description: "Cross-chain bridge operations using the xflows CLI (Wanchain XFlows). Use when the user wants to: (1) create or manage crypto wallets for cross-chain use, (2) query supported chains, tokens, pairs, bridges, or DEXes, (3) get cross-chain swap quotes and fee estimates, (4) send cross-chain transactions between EVM chains, (5) track cross-chain transaction status and completion, (6) send native tokens (ETH/BNB/WAN) on the same chain, (7) send ERC20 tokens on the same chain, (8) check balance of any address (no wallet needed). Triggers on: cross-chain, bridge, swap tokens between chains, xflows, Wanchain, WanBridge, QUiX, move/transfer tokens from Ethereum/BSC/Polygon/Arbitrum/Optimism/Avalanche/Wanchain to another chain, bridge ETH/BNB/USDC/USDT, transfer ETH, send tokens, ERC20 transfer, check balance, query address balance."
---

# XFlows Cross-Chain Bridge

Operate the `xflows` CLI to perform cross-chain bridge transactions via the Wanchain XFlows protocol, as well as same-chain native token and ERC20 token transfers.

## Prerequisites

Ensure `xflows` is installed: `npm install -g xflows`. Verify with `xflows --version`.

## Core Workflow

For any cross-chain transfer, follow this sequence:

1. **Wallet** -- Ensure a wallet exists (`xflows wallet list`), create if needed
2. **Discover** -- Find supported chains, tokens, and pairs for the route
3. **Quote** -- Get estimated output and fees
4. **Send** -- Execute with `--dry-run` first, then for real
5. **Track** -- Monitor status until completion

## Command Quick Reference

See [references/commands.md](references/commands.md) for complete flag details.

### Wallet Management

```bash
xflows wallet create --name <n>                                    # new wallet
xflows wallet create --name <n> --encrypt --password <pw>          # encrypted
xflows wallet create --name <n> --private-key 0x...                # import key
xflows wallet list                                                 # list all
xflows wallet show --name <n> [--password <pw>]                    # show key
xflows wallet balance --name <n> --chain-id <id> [--password <pw>] # balance (own wallet)
xflows wallet balance --address <addr> --chain-id <id>             # balance (any address)
xflows wallet token-balance --name <n> --chain-id <id> --token <addr> [--decimals <n>] [--password <pw>] [--rpc <url>] # ERC20 balance (own wallet)
xflows wallet token-balance --address <addr> --chain-id <id> --token <addr> [--decimals <n>] [--rpc <url>] # ERC20 balance (any address)
xflows wallet delete --name <n> --force                            # delete
```

### Query Routes

```bash
xflows chains [--chain-id <id>] [--quix]          # supported chains
xflows tokens [--chain-id <id>] [--quix]          # supported tokens
xflows pairs --from-chain <id> [--to-chain <id>]  # bridgeable pairs
xflows bridges                                     # available bridges
xflows dexes                                       # available DEXes
xflows rpc                                         # configured RPC endpoints
```

### Quote

```bash
xflows quote \
  --from-chain <id> --to-chain <id> \
  --from-token <addr> --to-token <addr> \
  --from-address <addr> --to-address <addr> \
  --amount <amount> \
  [--bridge wanbridge|quix] [--slippage 0.01] [--dex wanchain|rubic]
```

### Send Transaction

```bash
xflows send \
  --wallet <name> [--password <pw>] \
  --from-chain <id> --to-chain <id> \
  --from-token <addr> --to-token <addr> \
  --to-address <addr> --amount <amount> \
  [--bridge wanbridge|quix] [--slippage 0.01] [--dry-run] [--gas-limit <n>] [--rpc <url>]
```

### Transfer (Same-Chain Native Token)

```bash
xflows transfer --wallet <name> --chain-id <id> --to <addr> --amount <amount> \
  [--password <pw>] [--rpc <url>] [--gas-limit <n>] [--dry-run]
```

### Transfer Token (Same-Chain ERC20)

```bash
xflows transfer-token --wallet <name> --chain-id <id> \
  --token <addr> --to <addr> --amount <amount> \
  [--decimals <n>] [--password <pw>] [--rpc <url>] [--gas-limit <n>] [--dry-run]
```

- Auto-detects token decimals and symbol from the contract (or use `--decimals` to override)
- Checks token balance before sending

### Track Status

```bash
xflows status \
  --hash <txHash> \
  --from-chain <id> --to-chain <id> \
  --from-token <addr> --to-token <addr> \
  --from-address <addr> --to-address <addr> \
  --amount <amount> \
  [--poll --interval 10]
```

## Key Concepts

### Token Addresses

- Native tokens (ETH, BNB, MATIC, WAN, etc.): `0x0000000000000000000000000000000000000000`
- ERC-20 tokens: find via `xflows tokens --chain-id <id>`

### Common Chain IDs

| Chain | ID | Chain | ID |
|-------|----|-------|----|
| Ethereum | 1 | Arbitrum | 42161 |
| BSC | 56 | Optimism | 10 |
| Polygon | 137 | Base | 8453 |
| Avalanche | 43114 | Wanchain | 888 |

### Query Any Address Balance

Both `wallet balance` and `wallet token-balance` support `--address` to query any address without needing a local wallet:

```bash
# Check any address's ETH balance
xflows wallet balance --address 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045 --chain-id 1

# Check any address's USDC balance
xflows wallet token-balance --address 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045 \
  --chain-id 1 --token 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48
```

Provide either `--name` (local wallet) or `--address` (any address). When `--address` is used, no wallet file or password is needed.

### Encrypted Wallets

When a wallet was created with `--encrypt`, every command that uses the private key (`send`, `transfer`, `transfer-token`, `wallet show`, `wallet balance`) requires `--password <pw>`.

### Wanchain Gas Rule

Sending from Wanchain (chainId 888) automatically enforces minimum gasPrice of 1 gwei. No manual action needed.

### Status Codes

| Code | Meaning | Terminal? |
|------|---------|-----------|
| 1 | Success | Yes |
| 2 | Failed | Yes |
| 3 | Processing | No |
| 4/5 | Refunded | Yes |
| 6 | Trusteeship (manual intervention) | Yes |
| 7 | Risk transaction (AML flagged) | Yes |

## Patterns

### Find a Token Address

```bash
xflows tokens --chain-id 1 | jq '.data[] | select(.tokenSymbol == "USDC")'
```

### Safe Execution (always dry-run first)

```bash
# Preview
xflows send --wallet alice --from-chain 1 --to-chain 56 \
  --from-token 0x0000000000000000000000000000000000000000 \
  --to-token 0x0000000000000000000000000000000000000000 \
  --to-address 0xRecipient --amount 0.1 --dry-run

# Execute (remove --dry-run)
xflows send --wallet alice --from-chain 1 --to-chain 56 \
  --from-token 0x0000000000000000000000000000000000000000 \
  --to-token 0x0000000000000000000000000000000000000000 \
  --to-address 0xRecipient --amount 0.1
```

### Same-Chain Native Transfer

```bash
# Send 0.1 ETH on Ethereum
xflows transfer --wallet alice --chain-id 1 --to 0xRecipient --amount 0.1

# Dry run first
xflows transfer --wallet alice --chain-id 1 --to 0xRecipient --amount 0.1 --dry-run
```

### Same-Chain ERC20 Transfer

```bash
# Send 100 USDC on Ethereum (auto-detect decimals)
xflows transfer-token --wallet alice --chain-id 1 \
  --token 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48 \
  --to 0xRecipient --amount 100

# Specify decimals manually
xflows transfer-token --wallet alice --chain-id 1 \
  --token 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48 \
  --to 0xRecipient --amount 100 --decimals 6
```

### Poll Until Complete

```bash
xflows status --hash 0xTxHash \
  --from-chain 1 --to-chain 56 \
  --from-token 0x0000000000000000000000000000000000000000 \
  --to-token 0x0000000000000000000000000000000000000000 \
  --from-address 0xSender --to-address 0xReceiver \
  --amount 0.1 --poll --interval 10
```
