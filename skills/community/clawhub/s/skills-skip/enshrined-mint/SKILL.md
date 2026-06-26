---
name: enshrined-mint
description: |
  🔷 Enshrined Exchange - Stablecoin Swap on Tempo
  
  Contract: 0xdec0000000000000000000000000000000000000
  RPC: https://rpc.moderato.tempo.xyz
  
  Features:
  - Swap between stablecoins (USDC ↔ USDe)
  - Instant execution via orderbook
  - Low fees, optimal pricing
  
  Tokens on Tempo:
  - USDC: 0x20C0...0000
  - USDe: 0x20C0...0001
  - pathUSD: 0x20C0...0002
  
  Use when: user wants to swap stablecoins on Tempo.
  
metadata:
  openclaw:
    emoji: 🔷
---

# 🔷 Enshrined Exchange - Stablecoin Swap

## Swap USDC → USDe

```bash
cd /root/.openclaw/workspace/skills/enshrined-mint
PRIVATE_KEY=0x... node swap.js --amount 100 --from USDC --to USDe
```

## Swap USDe → USDC

```bash
cd /root/.openclaw/workspace/skills/enshrined-mint
PRIVATE_KEY=0x... node swap.js --amount 100 --from USDe --to USDC
```

## Check Balance

```bash
cd /root/.openclaw/workspace/skills/enshrined-mint
PRIVATE_KEY=0x... node check_balance.js
```

## Contract Info

| Item | Value |
|------|-------|
| Network | Tempo (Chain 4217) |
| RPC | https://rpc.moderato.tempo.xyz |
| Exchange | 0xdec0...0000 |
| USDC | 0x20C0...0000 |
| USDe | 0x20C0...0001 |
| pathUSD | 0x20C0...0002 |

## Scripts

| Script | Description |
|--------|-------------|
| swap.js | Swap stablecoins |
| check_balance.js | Check token balances |
| mint_usde.js | Mint USDe (legacy) |
