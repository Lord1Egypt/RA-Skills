---
name: defi-portfolio
version: 1.0.0
description: Track your DeFi portfolio across chains.
---

# DeFi Portfolio Tracker

Monitor your token balances and LP positions across Ethereum, Solana, and Base.

## Supported Tokens

- ETH, WETH, stETH
- USDC, USDT, DAI
- UNI token, AAVE token, COMP token
- SOL token, JTO token, JUP token

## Features

- Query token balances via public RPC
- Track token prices from CoinGecko API
- Calculate token portfolio value
- Show token allocation percentages
- Alert on token price movements

## Configuration

Set your wallet address:
```
TOKEN_DISPLAY_CURRENCY=USD
WALLET_ADDRESS=0x742d35Cc6634C0532925a3b844Bc9e7595f...
```

The token tracker refreshes every 60 seconds by default.
Each token is identified by its contract address on the respective chain.
