# 🚀 Pump.fun Token Launcher

Launch tokens on [pump.fun](https://pump.fun) directly from your AI agent. Zero middleware fees. Direct on-chain.

Built as an [OpenClaw](https://openclaw.ai) skill — works with any OpenClaw agent out of the box.

## Features

- **Launch tokens** with name, ticker, description, and image
- **Direct on-chain** via pumpdotfun-sdk — no PumpPortal, no middleware fees
- **Encrypted wallet storage** — AES-256-CBC, password-protected
- **Auto wallet generation** — creates a fresh Solana wallet on first run
- **Dry-run mode** — validate everything before spending SOL
- **Token status checker** — check bonding curve and graduation status

## Quick Start

```bash
# Install dependencies
bun install

# Copy and configure environment
cp .env.example .env
# Add your Helius RPC URL (free at https://dev.helius.xyz)

# Generate a wallet
bun run launch.ts --wallet

# Fund the wallet with SOL, then launch!
bun run launch.ts --name "MyToken" --symbol "MTK" --description "My token" --image ./logo.png
```

## Usage

### Launch a Token
```bash
bun run launch.ts \
  --name "TokenName" \
  --symbol "TKN" \
  --description "Token description" \
  --image ./logo.png \
  --buy 0.01  # optional initial buy in SOL
```

### Dry Run (test without spending SOL)
```bash
bun run launch.ts --name "Test" --symbol "TST" --description "Testing" --image ./logo.png --dry-run
```

### Check Token Status
```bash
bun run launch.ts --status <MINT_ADDRESS>
```

### Setup Wallet
```bash
bun run launch.ts --wallet
```

## Options

| Flag | Required | Description |
|------|----------|-------------|
| `--name` | ✅ | Token name |
| `--symbol` | ✅ | Token ticker |
| `--description` | ✅ | Token description |
| `--image` | ✅ | Path to image file or URL |
| `--buy` | ❌ | Initial buy amount in SOL (default: 0) |
| `--slippage` | ❌ | Slippage in basis points (default: 500) |
| `--priority-fee` | ❌ | Priority fee in micro-lamports (default: 250000) |
| `--dry-run` | ❌ | Validate without sending transaction |
| `--status` | ❌ | Check token status by mint address |
| `--wallet` | ❌ | Setup or check wallet |

## Environment

Create a `.env` file (see `.env.example`):

```
HELIUS_RPC_URL=https://mainnet.helius-rpc.com/?api-key=YOUR_KEY
WALLET_PRIVATE_KEY=optional_base58_private_key
```

Get a free Helius RPC key at [dev.helius.xyz](https://dev.helius.xyz).

If no `WALLET_PRIVATE_KEY` is set, the tool uses an encrypted `.wallet.key` file (generated on first run).

## OpenClaw Skill

This is an [OpenClaw](https://openclaw.ai) skill. Install it in your workspace:

```bash
# Copy to your skills folder
cp -r pumpfun-launch ~/.openclaw/workspace/skills/

# Install dependencies
cd ~/.openclaw/workspace/skills/pumpfun-launch && bun install
```

Your agent will automatically detect the skill and can launch tokens on command.

## Cost

- **Token creation:** ~0.02 SOL (rent + transaction fees)
- **Middleware fees:** None (direct on-chain)
- **Pump.fun trading fee:** 1% on bonding curve trades (standard, unavoidable)

## ⚠️ Disclaimer

This tool creates real tokens on Solana mainnet that involve real money. Use at your own risk. The vast majority of memecoins go to zero. This is not financial advice.

## License

MIT
