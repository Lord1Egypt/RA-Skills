---
name: x402-endpoint-validator
version: 1.0.0
description: "Validate x402 endpoints — test 402 responses, check Bazaar extension, verify payment schemas, confirm .well-known/x402 discovery manifests. For agents and operators who want to verify their x402 implementation works correctly."
metadata:
  openclaw:
    emoji: "✅"
    requires:
      bins: ["curl"]
    homepage: "https://www.x402.org"
---

# x402 Endpoint Validator

Test and validate x402 endpoints. Check that the 402 payment challenge is correctly configured, the Bazaar extension is present, and the .well-known discovery manifest is valid.

## What This Validates

1. **402 Response**: Does the endpoint return HTTP 402 with proper payment requirements?
2. **Payment Schema**: Is the `accepts` array valid (asset, network, payTo, amount)?
3. **Bazaar Extension**: Does the response include `extensions.bazaar` with discovery metadata?
4. **Well-Known Manifest**: Does `/.well-known/x402` exist and contain valid JSON?
5. **Crawl vs Sync**: Does the service return results in the same response or queue a job?

## Validate a Single Endpoint

```bash
# Trigger a 402 (replace URL and body with the service's expected input)
curl -s -o /dev/null -w "%{http_code}" -X POST https://service.example/services/your-endpoint/jobs \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.de"}'
```

Expected: `402`

## Inspect the Full 402 Response

```bash
curl -s -X POST https://service.example/services/your-endpoint/jobs \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.de"}' | python3 -m json.tool
```

Check these fields:

| Field | Expected | Check |
|-------|----------|-------|
| `x402Version` | `2` | Protocol version |
| `accepts[].scheme` | `"exact"` | Payment scheme |
| `accepts[].network` | `"eip155:8453"` | Base mainnet |
| `accepts[].asset` | `"0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"` | USDC contract |
| `accepts[].amount` | valid number string | In atomic units (6 decimals) |
| `accepts[].payTo` | valid address | Where to send payment |
| `accepts[].maxTimeoutSeconds` | number | Max wait for result |
| `extensions.bazaar` | present | Bazaar discovery metadata |
| `extensions.bazaar.discoverable` | `true` | Indexed on Bazaar |

## Validate Well-Known Manifest

```bash
curl -s https://service.example/.well-known/x402 | python3 -m json.tool
```

Check:
- `x402Version` = 2
- `serviceName`, `claim`, `description` are present
- `facilitator` is declared (e.g. "cdp")
- `resources` array is non-empty
- Each resource has: url, description, network, payTo, asset, amount, inputSchema

## Validate with Agentic Market

Use the official validator at https://agentic.market/validate:
1. Select HTTP method (GET/POST/etc.)
2. Enter your endpoint URL
3. Click Validate

The tool checks x402 configuration, facilitator setup, and Bazaar indexing.

## Common Issues

| Symptom | Likely Cause |
|---------|-------------|
| HTTP 200 instead of 402 | Endpoint not x402-configured |
| Missing `accepts` array | Payment schema not declared |
| Wrong asset address | USDC on Base is `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` |
| No `extensions.bazaar` | Bazaar metadata not included |
| `/.well-known/x402` returns 404 | Discovery manifest not published |
| Amount too high/low | Check atomic units (50000 = $0.05) |
| PAYMENT-SIGNATURE rejected | Wrong tx hash, amount mismatch, or expired quote |