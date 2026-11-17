# SGL Grid — Laya / System One

Laya is the open-source System One model served on SGL Grid as `convaiinnovations/laya`.
Use it for typed decisions, scoring, and compact no-output-language answers. It is not a chat
completion model; do not call it through `/v1/chat/completions`.

## Consumer API

Base URL: `https://grid.x402compute.cc`

List System One models:

```bash
curl "https://grid.x402compute.cc/v1/models?type=systemone" \
  -H "X-API-Key: $COMPUTE_API_KEY"
```

Call Laya with prepaid credits:

```bash
curl -X POST https://grid.x402compute.cc/v1/systemone \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $COMPUTE_API_KEY" \
  -d '{
    "model": "convaiinnovations/laya",
    "state": {
      "ticket": "Enterprise customer cannot access billing exports",
      "customer_tier": "enterprise"
    },
    "questions": {
      "route": {
        "type": "choice",
        "instructions": "Choose the best team to handle this ticket.",
        "criteria": {
          "billing": "Billing, invoice, refund, or account credit issue.",
          "support": "Product defect or technical troubleshooting.",
          "sales": "Expansion, pricing, or contract discussion."
        }
      },
      "urgency": {
        "type": "score",
        "instructions": "Score urgency from 0 to 1.",
        "criteria": ["customer blocked", "money at risk", "security risk"]
      },
      "summary": {
        "type": "noul",
        "instructions": "Return a concise action summary."
      }
    }
  }'
```

Typical response:

```json
{
  "object": "systemone.result",
  "model": "convaiinnovations/laya",
  "answers": {
    "route": { "type": "choice", "choice": "billing", "confidence": 0.83 },
    "urgency": { "type": "score", "score": 0.7 },
    "summary": { "type": "noul", "value": "Route to billing ops and mark as high priority." }
  },
  "usage": { "input_tokens": 178, "output_tokens": 0, "cost_usd": 0.000001 }
}
```

Per-request x402 also works: omit `X-API-Key`, accept the `402 Payment Required`, sign the
`X-Payment`, and resend the same request.

## Private Laya

There are two privacy levels:

- Plain `/v1/systemone`: the orchestrator validates and routes plaintext, then sends work only to
  attested confidential nodes. This is private at the node/runtime layer, not end-to-end private from
  the caller to the node.
- Private System One: reserve a node with `POST /v1/systemone/reserve`, encrypt locally to the node's
  X25519 key, submit the sealed payload to `POST /v1/systemone`, and receive a sealed result. In this
  mode the orchestrator sees ciphertext, the node decrypts locally, and Laya runs inside the node's
  local runtime boundary.

Use private System One when the caller needs end-to-end encrypted Laya. Use the normal endpoint for
simple API-key or x402 calls where orchestrator-side plaintext validation is acceptable.

## Limits and Types

- Model id: `convaiinnovations/laya`
- Aliases: `laya`, `laya-system-one`, `systemone-laya`
- Question types: `choice`, `score`, `noul`
- Max state: 64 KiB
- Max questions: 32
- Max criteria per question: 64
- Max input context: 16,384 tokens
- Max request body: 256 KiB
- Max response body: 1 MiB
- Billing: input-only, currently $0.01 per 1M input tokens plus platform minimum charge

`choice` questions require a criteria object with at least two options. `score` questions require a
non-empty criteria array. `noul` questions require instructions and may return a string, number, or
boolean value.

## Operator Path

Desktop app path: Singularity Node app v1.7.4 or newer → Models → System One → Laya. The app manages
a local loopback Laya sidecar at `127.0.0.1:8765`, then starts the normal SGL node service with
`--systemone-sidecar-url`.

CLI fallback for operators:

```bash
python3 -m venv ~/.sgl-laya
~/.sgl-laya/bin/pip install "laya[serve]"
LAYA_DEVICE=cpu LAYA_PRELOAD=1 ~/.sgl-laya/bin/laya-serve --host 127.0.0.1 --port 8765

sgl login --models convaiinnovations/laya
sgl attest
sgl service install \
  --model-name convaiinnovations/laya \
  --systemone-sidecar-url http://127.0.0.1:8765 \
  --max-jobs 1
```

Keep the sidecar on loopback. Do not expose it on `0.0.0.0`; the grid node service is the public
lane, billing gate, attestation gate, and scheduler.
