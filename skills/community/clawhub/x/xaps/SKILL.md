---
name: xaps
description: Audit agent value moves before sign or settle. Payers attach X-XAPS-Receipt; counterparties independently clear. Advisory receipt, not insurance — XAPS does not execute or warrant the transfer.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    envVars:
      - name: XAPS_AGENT_KEY
        required: false
        description: Payer key for POST /verify. Required only when this agent signs or pays. Not needed to clear another agent's receipt.
      - name: XAPS_API_URL
        required: false
        description: Tollbooth base URL. Default https://api.xaps.network
    emoji: "🛡️"
    homepage: https://github.com/APMC1/xaps-sdk
---

# XAPS — pre-execution audit for value moves

XAPS is a live Tollbooth. It does not wrap x402 or hold funds. It issues a portable receipt **before** an agent signs, pays, or settles.

- Payers **attach** `X-XAPS-Receipt`.
- Payees and facilitators **clear** that id themselves (no agent key).
- Refuse value unless `clear` is true, `use_case` is `value_move`, and amount / pay_to / resource match **this** 402.

External cost (Tollbooth, not this skill): about $0.01 per approved payer audit. Register at `POST https://api.xaps.network/agents/register`.

The fee buys an attested decision (`APPROVED` / `REJECTED`) over a `payload_hash`. It is not insurance, not custody, not settlement, and not a warranty that the action is safe. XAPS does not sign, send, or settle the value. A wrong call is a wrong opinion; the agent that executes still owns the loss. Independent `clear` only proves this receipt exists, is `value_move`, and matches this 402 — not that the payment is good.

## When to use

Use this skill when the agent is about to:

- sign or retry an x402 payment (`wrapFetchWithPayment`, `X-Payment`)
- send, sign, or submit a wallet/tx
- settle or fulfill paid work from another agent

Do **not** use it for GitHub issues, docs, or read-only lookup.

## Payer — audit then attach

Requires `XAPS_AGENT_KEY`. Fail closed if status is not `APPROVED`.

```bash
BASE="${XAPS_API_URL:-https://api.xaps.network}"
RECEIPT="$(curl -sS -X POST "$BASE/verify" \
  -H "Content-Type: application/json" \
  -H "X-Agent-Key: $XAPS_AGENT_KEY" \
  -d "{\"payload\":{\"action\":\"sign_x402_payment\",\"use_case\":\"value_move\",\"amount\":AMOUNT,\"pay_to\":\"PAY_TO\",\"resource\":\"RESOURCE_URL\"}}")"
```

Proceed only when `audit.status` is `APPROVED`. Put `receipt_id` on header `X-XAPS-Receipt`. No receipt → no sign.

Python:

```python
from xaps import XapsClient, XapsRejectedError
receipt = XapsClient(base_url="https://api.xaps.network").audit(
    action="sign_x402_payment",
    use_case="value_move",
    amount=float(AMOUNT),
)
if receipt["audit"]["status"] != "APPROVED":
    raise XapsRejectedError(receipt["audit"].get("beta_attack", "REJECTED"), receipt=receipt)
# attach receipt["receipt_id"] as X-XAPS-Receipt
```

## Payee / facilitator — clear independently

No agent key. Call this on the counterparty, not the payer.

```bash
BASE="${XAPS_API_URL:-https://api.xaps.network}"
curl -sS -X POST "$BASE/receipts/clear" \
  -H "Content-Type: application/json" \
  -d "{\"receipt_id\":\"RECEIPT_ID\",\"require_use_case\":\"value_move\",\"amount\":AMOUNT,\"pay_to\":\"PAY_TO\",\"resource\":\"RESOURCE_URL\"}"
```

Refuse unless `clear` is true. Mismatched amount / pay_to / resource fail closed.

Python:

```python
from xaps import require_value_clearance
require_value_clearance(receipt_id, amount=AMOUNT, pay_to=PAY_TO, resource=RESOURCE_URL)
```

## References

- Node: https://api.xaps.network
- Agent card: https://api.xaps.network/.well-known/xaps-agent-card.json
- SDK: https://github.com/APMC1/xaps-sdk (`independent_clearance`, `require_value_clearance`)
- MCP: `io.github.APMC1/xaps`
