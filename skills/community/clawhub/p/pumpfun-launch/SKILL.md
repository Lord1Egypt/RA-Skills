---
name: pumpfun-launch
description: Launch tokens on pump.fun directly from your agent. Zero middleware fees — direct on-chain via pumpdotfun-sdk. Use when the user wants to create, launch, deploy, or mint a new token or memecoin on pump.fun (Solana). Handles wallet generation, IPFS metadata upload, and on-chain token creation in one command. Supports dry-run mode, encrypted wallet storage, custom images, and optional initial buy. No PumpPortal, no third-party fees. Just provide a name, ticker, description, and image.
---

# Pump.fun Token Launcher

## Setup

The skill lives at `skills/pumpfun-launch/`. First run:

```bash
cd skills/pumpfun-launch && bun install
```

## Environment

Create `.env` in the skill folder:

```
HELIUS_RPC_URL=https://mainnet.helius-rpc.com/?api-key=YOUR_KEY
WALLET_PRIVATE_KEY=base58_encoded_private_key
```

Get a free Helius key at https://dev.helius.xyz/

If `WALLET_PRIVATE_KEY` is not set, the script will generate a new wallet and save it to `.wallet.key` (encrypted with a password prompt). Fund the wallet with SOL before launching.

## Usage

```bash
cd skills/pumpfun-launch
bun run launch.ts --name "TokenName" --symbol "TKN" --description "My token" --image ./logo.png
```

### Options

| Flag | Required | Description |
|------|----------|-------------|
| `--name` | ✅ | Token name |
| `--symbol` | ✅ | Token ticker |
| `--description` | ✅ | Token description |
| `--image` | ✅ | Path to image file (PNG/JPG) or URL |
| `--buy` | ❌ | Initial buy amount in SOL (default: 0) |
| `--slippage` | ❌ | Slippage in basis points (default: 500) |
| `--priority-fee` | ❌ | Priority fee in micro-lamports (default: 250000) |
| `--dry-run` | ❌ | Simulate without sending transaction |
| `--status` | ❌ | Check status of a mint address (pass mint pubkey) |

### Check Token Status

```bash
bun run launch.ts --status <MINT_ADDRESS>
```

## ⚠️ IMPORTANT — Agent Instructions

1. **ALWAYS confirm with the user** before running the launch command. Show them the token name, symbol, description, image, and buy amount.
2. **ALWAYS use `--dry-run` first** to validate parameters before real launch.
3. **Warn the user** that this creates a REAL token on Solana mainnet and costs real SOL.
4. Launching costs ~0.02 SOL (rent + fees). Initial buy is additional.
5. On success, report the mint address and transaction signature to the user.
6. The pump.fun link will be: `https://pump.fun/<MINT_ADDRESS>`
