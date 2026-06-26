# ZAP1 - Zcash Attestation

Zcash attestation layer for AI agents. Every tool call, message, and policy decision anchored to a BLAKE2b Merkle tree on Zcash mainnet. Proofs verifiable on any chain.

## What it does

- 8 hooks: policy enforcement before execution, session tracking, proof checkpoints, inbound/outbound attestation
- 14 tools: attest events, verify proofs, check stats, manage API keys, decode memos, query anchors
- Every action gets a cryptographic proof anchored to Zcash
- Policy rules block restricted tools before they execute
- Periodic proof summaries injected into conversation

## Install

```
clawhub install @Zk-nd3r/zap1-zcash-attestation
```

## Configure

```json
{
  "apiUrl": "https://pay.frontiercompute.io",
  "apiKey": "your-key",
  "agentId": "my-agent"
}
```

Get a free API key: message 00zeven on Signal or visit frontiercompute.io/pricing.html

## Verify

Every attested action returns a leaf hash. Verify at:
- Browser: frontiercompute.io/verify.html
- API: pay.frontiercompute.io/verify/{leaf_hash}/check
- CLI: curl https://pay.frontiercompute.io/verify/{leaf_hash}/check

## Links

- Protocol: github.com/Frontier-Compute/zap1
- Explorer: explorer.frontiercompute.io
- Pricing: frontiercompute.io/pricing.html
- 00zeven (live agent): 00zeven.cash
