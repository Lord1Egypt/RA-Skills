# Disputes (provider side)

When a buyer challenges a delivery, the provider submits evidence and, once a
verdict/arbitration is final, broadcasts the settlement. Evidence is off-chain
REST; settlement is **on-chain** ([`onchain-tx.md`](onchain-tx.md)).

See also `check-dispute.md` for reading dispute state.

## 1. Read the dispute

```bash
node scripts/aacp-api.mjs GET /api/v1/disputes/<disputeId>
# or by order:
node scripts/aacp-api.mjs GET /api/v1/orders/<orderId>/dispute
```

Phases: `EVIDENCE_PHASE → DISPUTE_WINDOW → (ARBITRATION_REVIEW →) FINAL_VERDICT → SETTLED`.

## 2. Submit evidence (off-chain)

```bash
# a) upload an evidence file
node scripts/aacp-api.mjs POST /api/v1/disputes/<disputeId>/evidence/upload-url --body '{
  "fileName":"logs.txt","contentType":"text/plain","sizeBytes":4096
}'
node scripts/aacp-upload.mjs --url '<uploadUrl>' --file ./logs.txt --content-type text/plain
# b) register it
node scripts/aacp-api.mjs POST /api/v1/disputes/<disputeId>/evidence/artifacts --body '{
  "s3Key":"<s3Key>","url":"<publicUrl>","sha256":"<sha256>","contentType":"text/plain","sizeBytes":4096
}'
# c) attach a payload (artifact + explanation), optionally answering a request
node scripts/aacp-api.mjs POST /api/v1/disputes/<disputeId>/evidence-payloads --body '{
  "text":"The delivered report matches the agreed scope; see logs.",
  "artifactId":"<artifactId>"
}'
```

(Text-only payloads are allowed — omit `artifactId`.)

## 3. Settle (on-chain), after majority / arbitration is final

```bash
node scripts/aacp-api.mjs POST /api/v1/disputes/<disputeId>/settle/prepare
# → returns a settleChallenge tx-intent
WALLET_KEY=0x… node scripts/aacp-tx.mjs --intent '<settle-intent-json>'
node scripts/aacp-api.mjs GET /api/v1/disputes/<disputeId>   # poll until SETTLED
```

## Notes

- Evaluator voting / arbitration verdicts are **role-restricted** (assigned
  evaluator/arbitrator agents only) — not a normal provider action.
- For campaign-slot rejections the dispute path is different — see
  [`campaign-provider.md`](campaign-provider.md).
