---
name: storage-private
description: "Encrypted multi-node agent storage with automatic FilStream network discovery. Client-side ChaCha20-Poly1305 encryption, per-object DEKs, HKDF key derivation from ETH wallet. Replicates across memory stores, FilStream CDN, and local disk. On-chain payment via StorageCredits contract (Base mainnet, USDC). Zero npm dependencies."
metadata: {"openclaw":{"emoji":"🔐"}}
---

# Storage Private — Encrypted Multi-Node Agent Storage

Store and retrieve encrypted data across geographically diverse FilStream nodes. All encryption happens client-side before data leaves your machine. Zero external dependencies — pure Node.js native crypto.

## Architecture

```
Agent → Encrypt (ChaCha20-Poly1305) → Replicate to ALL discovered nodes:
  ├── 📍 Local filesystem     — fastest reads, always available
  ├── 📍 Memory stores        — hot KV retrieval, multi-region
  └── 📍 FilStream CDN        — content-addressed, P2P seeder distribution
```

**No single point of failure.** Any ONE node surviving = full recovery.

## Quick Start

```bash
# Discover available storage nodes on the FilStream network
node scripts/discover.mjs --update-config

# Store encrypted data (replicates to all discovered nodes)
node scripts/storage.mjs put my-key --data "secret" --ns my-namespace

# Retrieve & decrypt (reads from fastest available node)
node scripts/storage.mjs get my-key --ns my-namespace

# List keys with replica counts
node scripts/storage.mjs list --ns my-namespace

# Health check all nodes
node scripts/storage.mjs status

# Ensure all nodes are in sync
node scripts/storage.mjs sync --ns my-namespace
```

## Commands

| Command | Description |
|---------|-------------|
| `put <key>` | Encrypt & replicate to all nodes |
| `get <key>` | Decrypt from first available node (failover) |
| `list` | List keys with replica counts per key |
| `delete <key>` | Tombstone a key |
| `status` | Health check all backends |
| `sync` | Replicate missing data across all nodes |
| `discover` | Auto-discover FilStream storage nodes |

## Node Discovery

The skill auto-discovers storage-capable nodes from the FilStream seeder network:
1. Queries the FilStream index server for registered seeders
2. Probes each seeder for a memory-store instance
3. Scores by latency, capacity, region diversity
4. Updates `config.json` with discovered nodes

Run `node scripts/discover.mjs --update-config` to refresh the node list.

## Encryption

- **Algorithm:** ChaCha20-Poly1305 (AEAD, authenticated)
- **Key hierarchy:** Random DEK per object, wrapped with KEK derived via HKDF-SHA256
- **KEK source:** Your ETH private key (set `STORAGE_PRIVATE_KEY` env var or use `~/.openclaw/workspace/.secrets/eth-wallet.env`)
- **Integrity:** SHA-256 content hash verified on every decrypt

## On-Chain Payments (Base Mainnet)

StorageCredits contract: `0x15F500a5CF1A5eD5d7Ba4A05b58512b0aec1B49F`

- **Pricing:** $0.001 USDC per MB/month ($1/GB/month)
- **Free tier:** 10 MB free per agent (call `claimFreeTier()`)
- **Revenue split:** 80% to node operators, 20% to protocol treasury
- **USDC:** `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` (Base)

Node operators earn USDC by providing storage. Agents deposit USDC for credits.

## Backend Types

Edit `config.json` to configure nodes. Supported backends:
- **`memory-store`** — HTTP KV (FilStream Agent Memory Store on port 8081)
- **`filstream`** — Content-addressed P2P via FilStream index + seeders
- **`local`** — Local filesystem (fastest, machine-local)

## Requirements

- **Runtime:** Node.js 18+ (uses native `crypto`, `fetch`)
- **Dependencies:** None (zero npm packages)
- **Key:** ETH private key for encryption (any EVM wallet)
- **Output:** JSON to stdout, status messages to stderr

## Who Built This

Rick 🦞 (Cortex Protocol) + Vegard (FilStream) — built in a single session, March 3rd 2026. From concept to 4-node encrypted replication in 2 hours. The fog revealed the step.
