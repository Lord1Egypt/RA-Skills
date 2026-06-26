---
name: agent-passport
description: Issue and verify SX# agent passports — cryptographic identity with hash-chain integrity, Merkle anchoring on Base
user-invocable: true
metadata: {"openclaw":{"requires":{"env":[]}},"homepage":"https://soulledger.sputnikx.xyz","author":"SputnikX","version":"1.0.0","tags":["passport","identity","verification","hash-chain","base"]}
---

# Agent Passport — SX# Identity

Issue cryptographic passports for AI agents. Each passport includes a unique SX# identifier, passport hash, and hash-chain verified event history. Merkle roots anchored on Base chain.

## Base URL

`https://soul.sputnikx.xyz`

## Register Agent & Get Passport (free)
```bash
curl -X POST https://soul.sputnikx.xyz/soul/register \
  -H "Content-Type: application/json" \
  -d '{"agent_id":"my-agent","display_name":"My Agent","issue_api_key":true}'
```
Returns: `{ passport: { sx_id, passport_hash }, api_key, campaign: "First 1M Free Passports" }`

## Get Passport by SX#
```bash
curl https://soul.sputnikx.xyz/soul/passport/101
```

## Get Agent Profile
```bash
curl https://soul.sputnikx.xyz/soul/{agent_id}/pulse
```
Returns: Full profile — trust, DNA, character, activity, event count.

## Verify Event Proof ($0.05 x402)
```bash
curl https://soul.sputnikx.xyz/soul/{agent_id}/proof/{event_hash}
```

## Merkle Root Verification ($0.05 x402)
```bash
curl https://soul.sputnikx.xyz/soul/merkle/verify/{root_hash}
```

## Campaign
First 1,000,000 passports are FREE. Currently issued: ~13. Get yours now.

## On-Chain Anchoring
- Every 100th event → SHA-256 Merkle root → Base chain transaction
- Verifiable on BaseScan
- Tamper-proof: changing any event invalidates the entire chain downstream
