---
name: rng-provably-fair
description: Provably fair random number generation with on-chain seed anchoring — Keno, Roulette, Dice for agent entertainment
user-invocable: true
metadata: {"openclaw":{"requires":{"env":[]}},"homepage":"https://sputnikx.xyz/rng/","author":"SputnikX","version":"1.0.0","tags":["rng","random","provably-fair","gaming","casino"]}
---

# Provably Fair RNG

Cryptographically verifiable random number generation. Server seeds anchored on Base chain. Verification pipeline: seed → hash → result → proof.

## Base URL

`https://sputnikx.xyz/rng`

## Generate Random Number
```bash
curl "https://sputnikx.xyz/rng/api/generate?min=1&max=100"
```

## Verify Result
```bash
curl "https://sputnikx.xyz/rng/api/verify/{seed_hash}"
```

## Games (Orion's Lounge)
- Keno, Roulette, Dice
- House edge: 2.5-8%
- RTP: 92-97.5%
- All results verifiable on-chain

## How It Works
1. Server generates seed → SHA-256 hash published
2. Client provides client seed
3. Combined hash → deterministic result
4. Seed revealed after game → anyone can verify
5. Seed chain anchored on Base for tamper-proof audit trail
