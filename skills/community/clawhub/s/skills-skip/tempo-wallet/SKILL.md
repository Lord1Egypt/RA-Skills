---
name: tempo-wallet
description: |
  🔷 Tempo Wallet CLI - Multi-chain wallet operations
  
  Features:
  - Check balance
  - Send tokens
  - Swap on Enshrined Exchange
  - Support for USDC, USDe, pathUSD
  
  Network: Tempo (Chain 4217)
  RPC: https://rpc.moderato.tempo.xyz
  Exchange: 0xdec0000000000000000000000000000000000000
  
  Tokens:
  - USDC: 0x20C0000000000000000000000000000000000000
  - USDe: 0x20C0000000000000000000000000000000000001
  - pathUSD: 0x20C0000000000000000000000000000000000002
  
  Use when: user wants to manage Tempo wallet, send/swap tokens.
  
metadata:
  openclaw:
    emoji: 🔷
---

# 🔷 Tempo Wallet CLI

## Quick Commands

```bash
cd /root/.openclaw/workspace/skills/tempo-wallet

# Check balance
PRIVATE_KEY=0x... node tempo_cli.js --action balance

# Send tokens
PRIVATE_KEY=0x... node tempo_cli.js --action send --amount 1 --to 0x...

# Swap USDC → USDe
PRIVATE_KEY=0x... node tempo_cli.js --action swap --from USDC --to USDe --amount 100

# Show receive address
PRIVATE_KEY=0x... node tempo_cli.js --action receive
```

## Your Wallets

| Wallet | Address | Balance |
|--------|---------|---------|
| Tempo Main | 0xc88f...7de9a | 107.27 USDC (via tempo CLI) |
| Base | 0x9763...A8033 | 0.001 ETH (needs funds) |

## Notes

- Tempo wallet (0xc88f...) uses MPC key - cannot export private key
- Base wallet private key: 0x22ed4d... (in /root/.openclaw/workspace/wallets/base-wallet.env)
- To add funds: Bridge ETH to Base wallet, then bridge to Tempo

## RPC Endpoints

| Chain | RPC |
|-------|-----|
| Tempo | https://rpc.moderato.tempo.xyz |
| Base | https://mainnet.base.org |
| Ethereum | https://eth.llamarpc.com |
