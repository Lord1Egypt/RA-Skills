---
name: web3-docs
description: |
  Up-to-date documentation and code patterns for Solidity, Foundry, Hardhat, Viem, Wagmi, ethers.js, and OpenZeppelin. Use when writing smart contracts, debugging Solidity errors, setting up a Foundry project, writing Viem/Wagmi frontend code, or asking about ERC standards, gas optimization, upgradeable contracts, or any EVM development task. Triggers on: Solidity, Foundry, Hardhat, Viem, Wagmi, ethers.js, OpenZeppelin, ERC-20, ERC-721, ERC-4626, UUPS, proxy patterns, ABI, calldata, smart contract, deploy, cast, forge, anvil, or any EVM/blockchain development question.
---

# Web3 Docs

Current patterns and references for EVM development. Covers the full stack: contracts → testing → deployment → frontend integration.

## Stack Coverage

| Layer | Tool | Reference |
|-------|------|-----------|
| Contracts | Solidity 0.8.x | `references/solidity.md` |
| Framework | Foundry (forge/cast/anvil) | `references/foundry.md` |
| Framework (alt) | Hardhat | `references/hardhat.md` |
| Standards | OpenZeppelin 5.x | `references/openzeppelin.md` |
| Standards | ERC-4626 (tokenized vaults) | `references/erc4626.md` |
| Frontend (low-level) | Viem 2.x | `references/viem.md` |
| Frontend (React) | Wagmi 2.x | `references/wagmi.md` |
| Frontend (legacy) | ethers.js 6.x | `references/ethers.md` |

## Quick Lookup

**Starting a new Foundry project:** See `references/foundry.md` → Project Setup

**Starting a Hardhat project:** See `references/hardhat.md` → Installation

**Writing an ERC-20:** See `references/openzeppelin.md` → ERC-20

**Building a yield vault (ERC-4626):** See `references/erc4626.md` → OpenZeppelin Implementation

**First depositor attack on vaults:** See `references/erc4626.md` → First Depositor Attack

**Connecting a wallet in React:** See `references/wagmi.md` → Quick Start

**Reading contract state with Viem:** See `references/viem.md` → Read Contracts

**Common Solidity errors:** See `references/solidity.md` → Error Reference

**Deploying to Optimism/Base with Hardhat:** See `references/hardhat.md` → hardhat.config.ts

## Fetch Latest Docs

`scripts/fetch-docs.js <topic>` pulls live docs from official sources when the reference files may be stale.

```bash
node scripts/fetch-docs.js solidity      # Solidity docs
node scripts/fetch-docs.js foundry       # Foundry book
node scripts/fetch-docs.js viem          # Viem docs
node scripts/fetch-docs.js wagmi         # Wagmi docs
node scripts/fetch-docs.js openzeppelin  # OZ docs
node scripts/fetch-docs.js hardhat       # Hardhat docs
node scripts/fetch-docs.js erc4626       # ERC-4626 (OZ vault docs)
```

## Gas Optimization Quick Rules

1. Use `calldata` instead of `memory` for read-only function params
2. Pack storage variables: multiple `uint128` in one slot beats two separate `uint256`
3. `unchecked` blocks for arithmetic that can't overflow (saves ~30 gas/op)
4. `immutable` > `constant` > storage for values set once
5. Events are cheaper than storage for historical data
6. Batch operations: one tx touching N items beats N txs
