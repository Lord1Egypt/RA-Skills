# VAIBot Guard Receipt Schema (v0.1)

This is the canonical JSON object that VAIBot Guard serializes into `/api/prove` `content`.

## Receipt object (top-level)

The receipt is a single object model that can represent both precheck and finalize stages.
In steady-state, finalize receipts SHOULD include `intent`, `decision`, and `result`.

```json
{
  "schema": "vaibot-guard/receipt@0.1",
  "kind": "exec",
  "runId": "run_...",
  "sessionId": "...",
  "ts": "2026-03-03T01:23:45.000Z",
  "policyVersion": "0.1",
  "risk": { "risk": "low|high", "reason": "..." },
  "intent": { "tool": "system.run", "action": "exec", "command": "/usr/bin/uname", "cwd": ".", "args": ["-a"] },
  "decision": { "decision": "allow|deny|approve", "reason": "...", "approvalId": "appr_..." },
  "result": { "code": 0, "signal": null },
  "audit": { "hash": "...", "prevHash": "..." },
  "precheckAudit": { "hash": "...", "prevHash": "..." },
  "prove": { "ok": true, "contentHash": "...", "txHash": "...", "url": "..." }
}
```

Notes:
- `prove` is optional and is only present when VAIBot API anchoring is enabled and the `/prove` call succeeds.
- `audit` refers to the local hash-chained audit event emitted by the guard service.

## Mapping to `/api/prove`

- `content`: JSON.stringify(receipt)
- `contentType`: `application/json`
- `encoding`: `utf-8`
- `metadata`: small indexable keys (e.g. `runId`, `sessionId`, `kind`, `schema`)
- `idempotencyKey`: `runId`
