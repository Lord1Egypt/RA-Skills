---
name: x402-bazaar
description: "x402 Bazaar protocol guide for AgentPMT — implement the HTTP 402 two-step handshake, sign EIP-3009 TransferWithAuthorization, route through the AgentPMT facilitator, and settle USDC payments on Base. Use when building agent-to-agent commerce that follows the x402 standard."
version: 1.0.2
homepage: https://www.agentpmt.com/external-agent-api
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/external-agent-api"}}
---

# x402 Bazaar

## Freshness

Last updated: `2026-06-09`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

Use this skill when building or debugging the x402 payment flow for AgentPMT credit purchases and agent-to-agent commerce.

## Overview

x402 turns HTTP 402 into a machine-payable protocol. AgentPMT uses it to let an external wallet buy USDC-denominated credits, then spend those credits on marketplace tools and workflows.

## Handshake

1. Send a purchase request without payment.
2. Read the HTTP 402 response and the `PAYMENT-REQUIRED` header.
3. Decode the requirements, including payee, amount, token, chain, validity window, and nonce.
4. Sign an EIP-3009 `TransferWithAuthorization` for USDC on Base.
5. Retry the same purchase with `PAYMENT-SIGNATURE`.

```python
purchase = {
    "wallet_address": wallet_address,
    "credits": 500,
    "payment_method": "x402",
}
first = requests.post("https://www.agentpmt.com/api/external/credits/purchase", json=purchase, timeout=30)
if first.status_code == 402:
    payment_required = first.headers["PAYMENT-REQUIRED"]
    signed_header = "<base64 signed EIP-3009 authorization>"
    paid = requests.post(
        "https://www.agentpmt.com/api/external/credits/purchase",
        json=purchase,
        headers={"PAYMENT-SIGNATURE": signed_header},
        timeout=30,
    )
    paid.raise_for_status()
```

## Signature Contract

Use the returned x402 fields exactly. The authorization value, validity window, and nonce must match the server challenge. Do not reuse a nonce.

## AgentPMT Endpoints

| Purpose | Endpoint |
|---|---|
| Create wallet | `POST https://www.agentpmt.com/api/external/agentaddress` |
| Buy credits | `POST https://www.agentpmt.com/api/external/credits/purchase` |
| Create session | `POST https://www.agentpmt.com/api/external/auth/session` |
| List tools | `GET https://www.agentpmt.com/api/external/tools` |
| Invoke tool with credits or direct x402 | `POST https://www.agentpmt.com/api/external/tools/{productSlug}/actions/{actionSlug}/invoke` |

## EIP-191 Requests After Payment

After credits settle, balance calls and tool calls use wallet-signed EIP-191 messages.

Balance uses the scoped message with an empty payload:

```text
agentpmt-external
wallet:{wallet_lowercased}
session:{session_nonce}
request:{request_id}
action:balance
product:-
payload:
```

Tool invocation uses the path-bound message:

```text
agentpmt-external
wallet:{wallet_lowercased}
session:{session_nonce}
request:{request_id}
method:POST
path:/external/tools/{productSlug}/actions/{actionSlug}/invoke
payload:{payload_hash}
```

For a called URL like `https://www.agentpmt.com/api/external/tools/google-drive/actions/list-files/invoke`, prefer signing `path:/external/tools/google-drive/actions/list-files/invoke`. Do not sign the host or a query string. AgentPMT also accepts bounded `/api`, raw-action-slug, and trailing-slash variants only when they resolve to the same product/action.

`payload_hash` is SHA-256 over the exact action `parameters` object. Canonical JSON recursively sorts object keys and uses no whitespace; AgentPMT accepts both JS raw UTF-8 serialization and Python escaped serialization (`json.dumps(parameters, sort_keys=True, separators=(",", ":"), ensure_ascii=True)`). Do not hash wrapper fields like `wallet_address`, `session_nonce`, `request_id`, or `signature`.

## Error Handling

| Status | Meaning | Recovery |
|---|---|---|
| 400 | Invalid request or schema mismatch | Rebuild the request from the endpoint schema. |
| 401 `EXTERNAL_SIGNATURE_SESSION_NONCE_INVALID` | Session nonce is unknown | Create a new session nonce and sign again with a fresh request_id. |
| 401 `EXTERNAL_SIGNATURE_SESSION_NONCE_EXPIRED` | Session nonce expired | Create a new session nonce and sign again with a fresh request_id. |
| 401 `EXTERNAL_SIGNATURE_MALFORMED` | Signature could not be recovered | Rebuild the EIP-191 signature from `expected_message`; do not change parameters after hashing. |
| 401 `EXTERNAL_SIGNATURE_WALLET_MISMATCH` | Signature recovered a different wallet | Use `expected_message`, `expected_wallet`, `recovered_wallet_for_expected_message`, accepted path candidates, and accepted payload hash forms to correct wallet casing, key selection, path, or canonical JSON. |
| 402 | Payment required or insufficient credits | Complete the x402 payment flow. |
| 409 `EXTERNAL_SIGNATURE_REQUEST_REPLAY` | Replay or duplicate request | Generate a fresh request_id and retry once. |
| 500 | Platform or facilitator error | Retry later with a fresh request_id. |

## Related Skills

- Agent Payment: ../agent-payment
- Agent Tool Marketplace: ../agent-tool-marketplace
- AgentPMT marketplace: https://www.agentpmt.com
