# VAIBot Guard Checkpoint Schema (v0.1)

This is the canonical JSON object that VAIBot Guard serializes into `/api/prove` `content` for checkpoint anchoring.

```json
{
  "schema": "vaibot-guard/checkpoint@0.1",
  "ts": "2026-03-03T01:23:45.000Z",
  "sessionId": "...",
  "seq": 1,
  "count": 50,
  "root": "<merkle-root-hex>",
  "range": { "uptoEventCount": 50 },
  "reason": "count|time",
  "prevCheckpointHash": "<prev checkpoint hash>",
  "policyVersion": "0.1",
  "guardVersion": "0.1",
  "hashAlg": "sha256",
  "merkle": {
    "leaf": "sha256(\"leaf:\"+eventHash)",
    "node": "sha256(\"node:\"+left+\":\"+right)"
  },
  "hash": "<sha256(checkpoint:canonical-json-without-hash)>"
}
```

Notes:
- Checkpoint `hash` chains checkpoints together via `prevCheckpointHash`.
- The Merkle root commits to the event stream; inclusion proofs are generated separately.
