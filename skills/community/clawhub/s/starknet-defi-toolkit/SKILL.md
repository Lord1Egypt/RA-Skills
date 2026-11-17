---
name: starknet-defi-toolkit
description: Starknet L2 DeFi integration toolkit for AI agents. Reads balances, derives STRK/ETH quotes, lists Ekubo and JediSwap pools, simulates swaps, and produces a Cairo contract skeleton. Uses Starknet JSON-RPC with no API key required (free public endpoints). Works for the Cairo / Starknet ecosystem — STRK token, Ekubo concentrated liquidity AMM, JediSwap classic AMM, and Cairo 1 / Sierra contracts. Useful for: starknet defi, cairo contracts, STRK wallets, ekubo lp, jediswap router, starknet rpc, zk-rollup defi, sierra deployment, account abstraction, argent x, braavos.
version: 1.0.0
author: ssyopros.zo.computer
---

# Starknet DeFi Toolkit

Python CLI for reading on-chain Starknet state and producing realistic DeFi integrations.

## What this skill can do (working code, no promises)

- **Read ERC-20 balances** (STRK, ETH, USDC, USDR, etc.) for any Starknet address using `starknet_call` to `balanceOf`.
- **Fetch STRK / ETH quotes** in USD via CoinGecko's free public API.
- **List Ekubo concentrated liquidity pools** (TVL, fee, token0/token1).
- **List JediSwap classic pairs** with reserves.
- **Simulate** a token swap price (constant-product x*y=k and concentrated-liquidity tick model approximation).
- **Generate a Cairo 1 / Sierra contract skeleton** for a basic ERC-20 or staking contract.

## What this skill cannot do (honest limits)

- It does **not** submit signed transactions. It can read and simulate only.
- It uses public free RPCs (e.g. `https://rpc.starknet.lava.build`, `https://free-rpc.nethermind.io/mainnet-l1`). They are rate-limited; for production use a paid Alchemy/Infura/BlastAPI endpoint via `STARKNET_RPC_URL`.
- It does not custody funds. You supply the address; nothing is signed or sent.

## Install

```bash
pip install requests
```

## Usage

```bash
# Balance of STRK for a wallet
python scripts/starknet_toolkit.py balance --address 0x049d36570d4e46f48e99674bd3fcc8463... --token STRK

# Get STRK/ETH price in USD
python scripts/starknet_toolkit.py price STRK
python scripts/starknet_toolkit.py price ETH

# List Ekubo pools (TVL-ranked)
python scripts/starknet_toolkit.py pools --protocol ekubo --top 10

# Simulate a JediSwap swap
python scripts/starknet_toolkit.py simulate --protocol jediswap --amount 100 --token-in STRK --token-out USDC

# Generate a Cairo 1 ERC-20 skeleton
python scripts/starknet_toolkit.py scaffold erc20 --name MyToken --symbol MTK --decimals 18
```

Environment variables:

- `STARKNET_RPC_URL` — override the default public RPC.
- `STARKNET_NETWORK` — `mainnet` (default) or `sepolia`.
