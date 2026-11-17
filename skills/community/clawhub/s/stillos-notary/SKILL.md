---
name: stillos-notary
description: Verify a claim is actually TRUE against real external state (GitHub, on-chain tx, Kalshi markets, HTTP/JSON, price feeds) — not just that a receipt wasn't forged. Ed25519-signed, hash-chained, offline-verifiable. Free tier, no account required.
metadata: {"openclaw":{"requires":{"env":[]},"primaryEnv":"STILLOS_NOTARY_KEY"}}
---

# StillOS Notary — verifies the claim, not just the receipt

Most "notary"/"attestation" skills on this registry verify **receipt integrity**: was this hash signed, was this log tampered with. That answers "did someone forge the paperwork" — it does not answer "is the underlying claim actually true." This skill answers the second question: every call resolves the claim against a real external source of truth (GitHub's API, a Kalshi market's actual settlement, an on-chain transaction, a public price feed) before signing anything. If you already have a signed receipt from elsewhere and just want to check it wasn't tampered with, a local integrity-only verifier is the right tool and cheaper than this. Use this skill when you need to know the claim itself is real, not just that the record of it is intact.

## What it does

Every call resolves a claim against **real external state**, not model output, and returns an Ed25519-signed, hash-chained receipt that anyone can independently verify:

- `github_pr` — did this PR merge, close unmerged, or is it still open (api.github.com)
- `onchain_tx` — did this tx mine successfully, optional confirmation depth (eth/base/arbitrum, keyless RPC)
- `kalshi_market` — did this Kalshi market settle, and which side won
- `url_json` / `http_status` — does a public endpoint return the expected field/status
- `price_oracle` — N-source, time-sampled price consensus against a threshold

Every verdict carries `schema_version`, `action_class: read-only` (this notary never writes on your behalf), and a resolver-specific `freshness` object so you know how long the fact stays good. Full spec: https://nolawealthfinancial.com/evidence/notary-doctrine/claim-vocabulary-spec.json

## Endpoints (base: https://nolawealthfinancial.com/notary)

- `POST /claim-verdict` — commit + resolve in one call. **Free tier: 5-25/day** depending on the cost-to-fake weight of your evidence (onchain_tx=3, kalshi_market=2, github_pr=1.5, url_json=1). x402-paid at $0.25/call past the limit.
- `POST /commit` — pre-commitment receipt only, before the outcome is known. x402-paid at $0.10/call.
- `GET /verify?hash=` — independently verify any receipt hash. Always free.

## Quick start (Python)

```bash
pip install stillos
```

```python
from stillos import Notary
n = Notary(agent_id="your-agent-id")

verdict = n.verify_prediction(
    "KXBTC-26JUL resolves NO — bitcoin below 95000 at July expiry",
    ticker="KXBTC-26JUL", side="no"
)
print(verdict)             # ✓ CONFIRMED | resolver: kalshi_market | hash: ...
print(verdict.signature)   # Ed25519 — verify independently, don't trust us
```

## Quick start (raw HTTP, any language)

```bash
curl -s -X POST https://nolawealthfinancial.com/notary/claim-verdict \
  -H "Content-Type: application/json" \
  -H "X-Agent-Id: your-agent-id" \
  -d '{
    "claim": "PR #482 on openclaw/openclaw merged",
    "resolver": {"type": "github_pr", "owner": "openclaw", "repo": "openclaw", "number": 482}
  }'
```

## Offline verification (no network, no dependency on us staying up)

Every receipt this notary issues can be checked for tamper/forgery entirely offline, without trusting our server to be up or trusting us at all beyond the published signing key:

```bash
node scripts/verify_offline.cjs receipt.json
# {"valid": true, "receipt_hash": "...", "errors": []}
```

This only proves the receipt is unforged and unmodified — it does not re-check the underlying claim (that requires calling the live resolver, since the claim's truth can only be established by asking GitHub/Kalshi/chain/etc). For full hash-chain-across-all-receipts verification, see `evidence/notary-doctrine/verify_ledger.cjs` at nolawealthfinancial.com (needs network to fetch the export).

## When to reach for this vs. not

Use it when a claim needs to survive contact with a skeptical counterparty — settlement disputes, agent-to-agent handoffs, anything where "trust me" isn't good enough. Don't use it for claims that require human judgment or aren't resolvable against machine-readable state (this notary explicitly refuses that scope rather than faking it — see `epistemic_status` in the spec).
