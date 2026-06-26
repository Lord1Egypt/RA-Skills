# XFlows CLI Complete Command Reference

## wallet create

Create a new EVM wallet. Saved to `~/.xflows/wallets/<name>.json`.

| Flag | Required | Description |
|------|----------|-------------|
| `--name <name>` | Yes | Wallet name (used as filename) |
| `--encrypt` | No | Encrypt private key with a password |
| `--password <pw>` | No | Encryption password (prompted if `--encrypt` set without it) |
| `--private-key <key>` | No | Import existing private key instead of generating |

## wallet list

List all saved wallets with address, encryption status, and creation date. No flags.

## wallet show

Show wallet address and private key.

| Flag | Required | Description |
|------|----------|-------------|
| `--name <name>` | Yes | Wallet name |
| `--password <pw>` | No | Password for encrypted wallets |

## wallet balance

Check native token balance on a chain. Use `--name` for a local wallet or `--address` to query any address without a wallet.

| Flag | Required | Description |
|------|----------|-------------|
| `--name <name>` | One of `--name` or `--address` | Wallet name |
| `--address <addr>` | One of `--name` or `--address` | Query any address (no wallet needed) |
| `--chain-id <id>` | Yes | Chain ID to query |
| `--password <pw>` | No | Password for encrypted wallets |
| `--rpc <url>` | No | Custom RPC URL |

## wallet token-balance

Check ERC20 token balance on a specific chain. Auto-detects token decimals and symbol from the contract. Use `--name` for a local wallet or `--address` to query any address without a wallet.

| Flag | Required | Description |
|------|----------|-------------|
| `--name <name>` | One of `--name` or `--address` | Wallet name |
| `--address <addr>` | One of `--name` or `--address` | Query any address (no wallet needed) |
| `--chain-id <id>` | Yes | Chain ID to check balance on |
| `--token <address>` | Yes | ERC20 token contract address |
| `--decimals <n>` | No | Token decimals (auto-detected from contract if omitted) |
| `--password <pw>` | No | Password for encrypted wallets |
| `--rpc <url>` | No | Custom RPC URL |

## wallet delete

| Flag | Required | Description |
|------|----------|-------------|
| `--name <name>` | Yes | Wallet name |
| `--force` | No | Skip confirmation prompt |

## chains

List supported chains.

| Flag | Required | Description |
|------|----------|-------------|
| `--chain-id <id>` | No | Filter by chain ID |
| `--quix` | No | QUiX-supported chains only |

## tokens

List supported tokens.

| Flag | Required | Description |
|------|----------|-------------|
| `--chain-id <id>` | No | Filter by chain ID |
| `--quix` | No | QUiX-compatible tokens only |

## pairs

List bridgeable token pairs.

| Flag | Required | Description |
|------|----------|-------------|
| `--from-chain <id>` | Yes | Source chain ID |
| `--to-chain <id>` | No | Destination chain ID |

## bridges

List available bridges (wanbridge, quix). No flags.

## dexes

List available DEX aggregators (wanchain, rubic). No flags.

## rpc

List all pre-configured RPC endpoints. No flags.

## quote

Get cross-chain swap estimate.

| Flag | Required | Description |
|------|----------|-------------|
| `--from-chain <id>` | Yes | Source chain ID |
| `--to-chain <id>` | Yes | Destination chain ID |
| `--from-token <addr>` | Yes | Source token address (`0x0...0` for native) |
| `--to-token <addr>` | Yes | Destination token address |
| `--from-address <addr>` | Yes | Sender address |
| `--to-address <addr>` | Yes | Receiver address |
| `--amount <amount>` | Yes | Human-readable amount (e.g., `1.5`) |
| `--bridge <name>` | No | `wanbridge` or `quix` |
| `--dex <name>` | No | `wanchain` or `rubic` |
| `--slippage <value>` | No | Max slippage (e.g., `0.01` = 1%) |
| `--id <id>` | No | Request tracking identifier |

**Response key fields:** `amountOut`, `amountOutMin`, `workMode` (1-6), `nativeFees[]`, `tokenFees[]`, `approvalAddress`, `priceImpact`.

## send

Build, sign, and broadcast a cross-chain transaction.

| Flag | Required | Description |
|------|----------|-------------|
| `--wallet <name>` | Yes | Wallet name for signing |
| `--from-chain <id>` | Yes | Source chain ID |
| `--to-chain <id>` | Yes | Destination chain ID |
| `--from-token <addr>` | Yes | Source token address |
| `--to-token <addr>` | Yes | Destination token address |
| `--to-address <addr>` | Yes | Recipient address |
| `--amount <amount>` | Yes | Amount to swap |
| `--password <pw>` | No | Password for encrypted wallet |
| `--bridge <name>` | No | Force specific bridge |
| `--dex <name>` | No | Force specific DEX |
| `--slippage <value>` | No | Max slippage |
| `--rpc <url>` | No | Override source chain RPC |
| `--gas-limit <limit>` | No | Custom gas limit |
| `--dry-run` | No | Preview without sending |

**Process:** Quote -> BuildTx -> ERC-20 Approve (if needed) -> Sign & Send -> Wait for receipt.

The `--from-address` is automatically set to the wallet's address.

## transfer

Send native tokens (ETH/BNB/WAN/etc.) on the same chain. This is a simple same-chain transfer, not a cross-chain operation.

| Flag | Required | Description |
|------|----------|-------------|
| `--wallet <name>` | Yes | Wallet name for signing |
| `--chain-id <id>` | Yes | Chain ID to send on |
| `--to <address>` | Yes | Recipient address |
| `--amount <amount>` | Yes | Amount to send (human-readable, e.g., `0.1`) |
| `--password <pw>` | No | Password for encrypted wallet |
| `--rpc <url>` | No | Override default RPC endpoint |
| `--gas-limit <limit>` | No | Custom gas limit |
| `--dry-run` | No | Preview without sending |

**Process:** Load wallet -> Build tx -> Sign & Send -> Wait for receipt.

Supports Wanchain gas price enforcement (chainId 888).

## transfer-token

Send ERC20 tokens on the same chain. Auto-detects token decimals and symbol from the contract.

| Flag | Required | Description |
|------|----------|-------------|
| `--wallet <name>` | Yes | Wallet name for signing |
| `--chain-id <id>` | Yes | Chain ID to send on |
| `--token <address>` | Yes | ERC20 token contract address |
| `--to <address>` | Yes | Recipient address |
| `--amount <amount>` | Yes | Amount to send (human-readable, e.g., `100`) |
| `--decimals <n>` | No | Token decimals (auto-detected from contract if omitted) |
| `--password <pw>` | No | Password for encrypted wallet |
| `--rpc <url>` | No | Override default RPC endpoint |
| `--gas-limit <limit>` | No | Custom gas limit |
| `--dry-run` | No | Preview without sending |

**Process:** Load wallet -> Read token decimals/symbol -> Check balance -> Send transfer() -> Wait for receipt.

Supports Wanchain gas price enforcement (chainId 888).

## status

Check cross-chain transaction status.

| Flag | Required | Description |
|------|----------|-------------|
| `--hash <hash>` | Yes | Source chain tx hash |
| `--from-chain <id>` | Yes | Source chain ID |
| `--to-chain <id>` | Yes | Destination chain ID |
| `--from-token <addr>` | Yes | Source token address |
| `--to-token <addr>` | Yes | Destination token address |
| `--from-address <addr>` | Yes | Sender address |
| `--to-address <addr>` | Yes | Receiver address |
| `--amount <amount>` | Yes | Amount that was swapped |
| `--bridge <name>` | No | Bridge that was used |
| `--poll` | No | Keep polling until terminal status |
| `--interval <seconds>` | No | Polling interval (default: 15) |

**Response key fields:** `statusCode`, `statusMsg`, `receiveAmount`, `sourceHash`, `destinationHash`, `swapHash`, `refundHash`, `workMode`, `timestamp`.
