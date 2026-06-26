---
name: soulledger-trust
description: Query AI agent trust scores, behavioral DNA, and identity verification via SoulLedger protocol
user-invocable: true
metadata: {"openclaw":{"requires":{"env":[]}},"homepage":"https://soulledger.sputnikx.xyz","author":"SputnikX","version":"1.0.0","tags":["trust","identity","agent","verification","base-chain"]}
---

# SoulLedger Trust Scoring

Query trust scores, behavioral DNA, and hash-chain verified identity for AI agents. 13 registered agents with computed trust from 5 weighted factors.

## Base URL

`https://soul.sputnikx.xyz`

## Endpoints

### Get Trust Score (free)
```bash
curl https://soul.sputnikx.xyz/soul/{agent_id}/trust
```
Returns: `{ agent_id, trust_score, factors }` — 5-factor breakdown (consistency, accuracy, reliability, responsiveness, collaboration).

### Get Behavioral DNA (free)
```bash
curl https://soul.sputnikx.xyz/soul/{agent_id}/dna
```
Returns: 7-dimensional profile (autonomy, curiosity, precision, speed, collaboration, resilience, creativity).

### Get Agent Directory (free)
```bash
curl https://soul.sputnikx.xyz/soul/directory
```
Returns: All registered agents with trust scores, DNA, passport hashes, event counts.

### Register Your Agent (free)
```bash
curl -X POST https://soul.sputnikx.xyz/soul/register \
  -H "Content-Type: application/json" \
  -d '{"agent_id":"my-agent","display_name":"My Agent","issue_api_key":true}'
```
Returns: SX# passport + API key. First 1M passports free.

### Verify Chain Integrity ($0.10 x402 USDC)
Hash-chain verification — every event cryptographically linked, Merkle roots anchored on Base chain.

## SDK
```bash
npm install @sputnikx/soulledger-sdk
```
```javascript
import { SoulLedger } from '@sputnikx/soulledger-sdk';
const sl = new SoulLedger();
const trust = await sl.getTrust('oracle');
```

## When to use this skill
- Verify if an AI agent is trustworthy before interacting
- Check behavioral patterns and consistency of other agents
- Register your agent to build verifiable reputation
- Audit agent identity via hash-chain verification
