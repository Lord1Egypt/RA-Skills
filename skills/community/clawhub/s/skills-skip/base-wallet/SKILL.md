---
name: base-wallet
description: |
  🔐 Base Wallet - Multi-Chain RPC Support
  
  Create and manage wallets on Base chain (Ethereum-compatible).
  
  Networks:
  - Base Mainnet (8453): https://mainnet.base.org
  - Ethereum (1): https://eth.llamarpc.com
  - Arbitrum (42161): https://arb1.arbitrum.io/rpc
  - BSC (56): https://bsc-dataseed.bnbchain.org
  - Polygon (137): https://polygon-rpc.com
  - And 12+ more chains in /root/.openclaw/workspace/rpc_list.json
  
  All RPCs: /root/.openclaw/workspace/rpc_list.json
  
metadata:
  openclaw:
    emoji: 🔐
---

# 🔐 Base Wallet

## Quick Create

```bash
cd /root/.openclaw/workspace/skills/base-wallet
node scripts/create-wallet.js --env
```

## Check Balance (Any Chain)

```bash
# Using Base RPC
node scripts/check-balance.js [ADDRESS] --rpc https://mainnet.base.org
```

## All Available RPCs

See: /root/.openclaw/workspace/rpc_list.json

| Chain | RPC |
|-------|-----|
| Base | https://mainnet.base.org |
| Ethereum | https://eth.llamarpc.com |
| Arbitrum | https://arb1.arbitrum.io/rpc |
| BSC | https://bsc-dataseed.bnbchain.org |
| Polygon | https://polygon-rpc.com |
| Tempo | https://rpc.moderato.tempo.xyz |

## Send Transaction

```javascript
const { ethers } = require('ethers');

const provider = new ethers.JsonRpcProvider('https://mainnet.base.org');
const wallet = new ethers.Wallet(process.env.PRIVATE_KEY, provider);

const tx = await wallet.sendTransaction({
  to: recipientAddress,
  value: ethers.parseEther('0.001')
});
```
