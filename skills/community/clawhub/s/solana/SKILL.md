---
name: Solana
description: Assist with Solana transactions, token accounts, priority fees, and program interactions.
metadata: {"clawdbot":{"emoji":"◎","os":["linux","darwin","win32"]}}
---

## Rent and Account Creation
- Every Solana account must hold a minimum SOL balance (~0.00089 SOL for basic accounts) to be rent-exempt — accounts below this get deleted
- Sending SOL to a new address that has never received anything will fail if the amount doesn't cover rent-exempt minimum
- Token accounts require separate rent deposits — each new token type a wallet holds costs ~0.002 SOL to create
- Close unused token accounts to recover rent: `spl-token close` returns the SOL to owner

## Token Accounts (SPL Tokens)
- Unlike Ethereum, Solana wallets don't automatically hold tokens — each token needs an Associated Token Account (ATA) created first
- First-time token transfers must create the recipient's ATA — sender pays ~0.002 SOL account creation fee
- "Account not found" error usually means the ATA doesn't exist yet, not that the wallet is invalid
- One wallet can have multiple ATAs for the same token (non-associated) — always use the ATA address for standard transfers

## Transaction Fees and Priority
- Base fee is ~0.000005 SOL (5000 lamports) per signature — much cheaper than Ethereum
- Priority fee = compute units × price in micro-lamports — set via `SetComputeUnitPrice` instruction
- During congestion (NFT mints, popular DEX), transactions without priority fees get dropped, not queued
- Default compute unit limit is 200k per instruction — complex programs may need `SetComputeUnitLimit` to increase

## Transaction Lifecycle
- Solana transactions expire after ~60 seconds (based on blockhash age) — no permanent mempool like Bitcoin/Ethereum
- "Dropped" means tx was never included and expired. "Failed" means it was included but reverted. Completely different outcomes
- If transaction shows "confirmed" but not "finalized", wait — finalized means 31+ confirmations and is irreversible
- Preflight simulation catches most errors before broadcast — disable with `skipPreflight: true` only if you know why

## Common Error Messages
- "Insufficient funds for rent" — account would drop below rent-exempt minimum after transaction
- "Account not found" — the account doesn't exist on-chain (never created or was closed)
- "Blockhash not found" — transaction expired, need fresh blockhash and re-sign
- "Program failed to complete" — smart contract error, check logs with `solana confirm -v <txid>`

## RPC and APIs
- Public RPCs (api.mainnet-beta.solana.com) have strict rate limits — production apps need paid RPC (Helius, QuickNode, Triton)
- `getRecentPrioritizationFees` RPC gives current priority fee market — essential for landing txs during congestion
- Solscan.io and Solana.fm are the main block explorers — both show decoded instruction data
- For token metadata (name, symbol, image), query Metaplex on-chain or use Helius/SimpleHash APIs

## Wallet and Security
- Phantom, Solflare, Backpack are the main wallets — each has slightly different transaction simulation UI
- "Approve" prompts in Solana can drain entire wallet if malicious — read the simulation carefully
- Burner wallets are common practice for minting/airdrops — never connect main wallet to unknown sites
- Unlike Ethereum's infinite approvals, most Solana programs take tokens directly — no separate revoke step needed
