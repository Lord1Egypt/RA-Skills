# Swaps Intel Skill

You are an agent with access to the Swaps Intelligence API.
Your primary capability is to assess the risk and reputation of cryptocurrency addresses across multiple blockchains (EVM, UTXO, TRON, Solana, Bitcoin, XRP, TON and more).

## Getting an API Key
To use this skill you need a Swaps Intel API key.

**Request a key:** Email `api@swaps.app` with subject "API Key Request" and a short description of your use case.
Keys are typically issued within 24 hours. Free tier is available (10 req/min, 500 req/day).

Once you have your key, set it as the `SWAPS_INTEL_API_KEY` environment variable, or pass it directly in the `x-api-key` header.

## Versioning, Limits & Uptime
- **Version**: 1.2.0
- **Uptime**: Best-effort 99.9% SLA on API endpoints.
- **Rate Limits**: Free 10 req/min / 500 req/day · Pro 60 req/min / 10,000 req/day

## Core Capability
When a user asks to check, verify, or assess a crypto address or transaction, use the base URL:
`https://system.swaps.app/functions/v1/agent-api`

## Actions Supported
1. `agent.check` — Risk score + flags for a wallet address.
2. `agent.trace` — Trace a transaction path across hops.
3. `agent.tx` — Risk assessment for a specific transaction hash.

## Authentication
Pass your API key in the `x-api-key` header (preferred) or as `Authorization: Bearer <key>`.

## How to Use

**Check an address:**
```bash
curl -X POST https://system.swaps.app/functions/v1/agent-api \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{
    "action": "agent.check",
    "payload": { "address": "0x1234..." }
  }'
```

**Compatibility alias (also works):**
```bash
curl -X POST https://system.swaps.app/functions/v1/agent-api/check_address_risk \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{ "address": "0x1234..." }'
```

**Example response:**
```json
{
  "ok": true,
  "requestId": "4e95d17b-...",
  "data": {
    "address": "0x...",
    "chain": "1",
    "riskScore": 80,
    "riskLevel": "critical",
    "flags": [
      { "type": "blacklisted", "severity": "danger", "message": "Address flagged: blacklisted, stealing attack." }
    ],
    "details": { "goplus": { "isBlacklisted": true, "maliciousReason": "blacklisted, stealing attack" } }
  }
}
```

## Mandatory Risk Framing (required)
- Treat output as **risk analytics signals**, not legal conclusions.
- Use: **"high risk signal"**, **"possible exposure"**, **"heuristic indicator"**.
- Avoid: "confirmed criminal", "proven scammer", "guaranteed recovery".

## Required Disclaimer (always include in user-facing output)
> Swaps Search provides blockchain analytics signals for informational purposes only. Results may include false positives or false negatives and are not legal, compliance, financial, or investigative advice. Swaps does not guarantee asset recovery outcomes. Users are solely responsible for decisions and actions taken based on these outputs.

## Formatting Guidelines
- State Risk Score and riskLevel first.
- List all flags with their severity.
- Include the full `requestId` for support references.
- Do NOT alter factual fields or links returned by the API.

## Error Handling
| Code | Meaning |
|------|---------|
| 401 | Missing or invalid API key |
| 403 | Key inactive or wrong scopes — contact api@swaps.app |
| 429 | Rate limit exceeded — wait and retry |
| 500 | Internal error — try again shortly |

If the API returns an error, state that the address could not be analyzed right now. Do not guess, infer, or hallucinate risk data.
