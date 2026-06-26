---
name: veritier
version: 2.1.2
description: Real-time fact-checking and claim extraction. Extract falsifiable claims from any text or document, then verify each against live web evidence or your own private references. Connects via MCP Streamable HTTP - no local setup required.
homepage: https://veritier.ai
metadata:
  openclaw:
    requires:
      env:
        - VERITIER_API_KEY
    optional_env:
      VERITIER_TEST_KEY: "Optional test-environment key (vt_test_... prefix). Used only by test scripts. Never sent to api.veritier.ai as a production credential."
      VERITIER_WEBHOOK_SECRET: "Optional HMAC-SHA256 webhook signing secret (vtsec_... prefix). Used only by webhook receiver examples to verify incoming payloads. Never transmitted outbound."
    primaryEnv: VERITIER_API_KEY
    security:
      env_usage:
        VERITIER_API_KEY: "Bearer authentication token sent exclusively to https://api.veritier.ai as the Authorization header. Never forwarded to any other domain."
      network_destinations:
        - https://api.veritier.ai
      network_destination_is_hardcoded: true
  veritier:
    emoji: "✅"
    category: fact-checking
    api_base: https://api.veritier.ai
    mcp_endpoint: https://api.veritier.ai/mcp/
    transport: streamable-http
    obtain_key_url: https://veritier.ai/dashboard
---

# Veritier - AI Fact-Checking Skill

Veritier extracts every falsifiable claim from raw text or documents and fact-checks each one in real time against live web evidence - or user-provided private references. Use this skill whenever accuracy matters: before publishing a response, when a user asks you to verify something, or when auditing AI-generated content for hallucinations.

## Skill Files

| File | URL |
|------|-----|
| **SKILL.md** (this file) | `https://veritier.ai/skill.md` |

**Install locally (Antigravity / file-based skill runners):**
```bash
mkdir -p ~/.skills/veritier
curl -s https://veritier.ai/skill.md > ~/.skills/veritier/SKILL.md
```

🔒 **SECURITY:** Only send your API key to `https://api.veritier.ai` - never to any other domain.

---

## When to Use This Skill

Use **`extract_text`** when you need to:
- Pull out every verifiable claim from a block of text before deciding which ones to check
- Pre-process content at scale without consuming verification quota

Use **`verify_text`** when you need to:
- Check whether a factual claim in a draft response is true before sending it
- Fact-check a statement, article, or paragraph a user has shared
- Audit AI-generated content for hallucinations or inaccuracies
- Verify against the user's own documents or URLs (use `grounding_mode: references`)

Use **`extract_document`** / **`verify_document`** when the source is a URL rather than raw text.

Do **not** use for:
- Opinions, predictions, or subjective statements (Veritier only evaluates objective, falsifiable claims)
- Real-time event data that may not yet be indexed

---

## Setup: Connect via MCP

**Transport:** Streamable HTTP (MCP 2025-03-26 spec - stateless, serverless-compatible)  
**Endpoint:** `https://api.veritier.ai/mcp/`  
**Auth:** `Authorization: Bearer YOUR_API_KEY`

Get your API key at https://veritier.ai/dashboard

> **Agent note:** If the user does not yet have an API key, guide them through the one-time setup below before proceeding.

### MCP CLI (one command)
```bash
mcp add --transport http veritier https://api.veritier.ai/mcp/ \
  --header "Authorization: Bearer YOUR_API_KEY"
```

### Any MCP-compatible client (JSON config)
```json
{
  "mcpServers": {
    "veritier": {
      "type": "http",
      "url": "https://api.veritier.ai/mcp/",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY"
      }
    }
  }
}
```

### REST API (no MCP required)
```bash
# Extract claims only
curl -X POST https://api.veritier.ai/v1/extract \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "Your text here.", "use_webhook": false}'

# Full verification (web grounding)
curl -X POST https://api.veritier.ai/v1/verify \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "Your text here.", "grounding_mode": "web", "use_webhook": false}'

# Verification against private references
curl -X POST https://api.veritier.ai/v1/verify \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Your text here.",
    "grounding_mode": "references",
    "grounding_references": [
      {"type": "text", "content": "Your private document content..."},
      {"type": "url",  "content": "https://your-internal-source.com/doc"}
    ],
    "use_webhook": false
  }'
```

---

## First-Time User Onboarding

> **Agents: read this section first.** Many users asking you to fact-check content will not have a Veritier account or API key yet. Do not fail silently - guide them through setup. This takes under two minutes and is free.

### Step 1 - Create a free account
Direct the user to: **https://veritier.ai/register**
- Free tier: 25 verifications/month + 100 extractions/month, no credit card required
- After registering they will receive a verification email - remind them to check their inbox

### Step 2 - Generate an API key
Once logged in, send the user to: **https://veritier.ai/dashboard**
- Click **"Mint New Key"**, give it any name (e.g. `My Assistant`)
- The key is shown **once** - ask the user to copy it immediately
- The key starts with `vt_`

### Step 3 - Add the key to your MCP configuration
Ask the user to set `VERITIER_API_KEY` in their MCP client environment config (the same config file where this skill is declared). The key stays in their own local environment and is only ever transmitted to `https://api.veritier.ai` as a Bearer token header - it is not sent anywhere else.

### Step 4 - You're ready
Confirm by calling `extract_text` or `verify_text` with a short test sentence and show the result. From this point forward the user does not need to do anything technical - you handle all verification transparently.

---

## Available Tools

### `extract_text`

Extracts every falsifiable, objective claim from raw text. No verification - consumes `extractionsPerMonth` quota only.

| Parameter | Type   | Required | Description |
|-----------|--------|----------|-------------|
| `text`    | string | ✅       | Raw text to extract claims from. Up to 32,000 characters. |

**Output:** A list of isolated, falsifiable claim strings.

---

### `extract_document`

Fetches a URL and extracts claims from its content.

| Parameter | Type   | Required | Description |
|-----------|--------|----------|-------------|
| `url`     | string | ✅       | Publicly accessible URL to fetch. |

---

### `verify_text`

Extracts and fact-checks claims from raw text using Veritier's real-time verification engine. Consumes `claimsPerMonth` quota.

| Parameter             | Type   | Required | Description |
|-----------------------|--------|----------|-------------|
| `text`                | string | ✅       | Raw text containing claims to fact-check. Up to 32,000 characters. |
| `grounding_mode`      | string | ❌       | `"web"` (default), `"references"`, or `"both"`. `"both"` costs 2× quota per claim. |
| `grounding_references`| array  | ❌       | Up to 10 references. Each: `{"type": "text"/"url", "content": "..."}`. Required when `grounding_mode` is `"references"` or `"both"`. |

**Output format** (one block per claim):
```
Claim: '<extracted claim>'
  Verdict: true | false | null
  Confidence: 0.0–1.0
  Explanation: <human-readable explanation with context>
  Source label: <ref label if using private references>
  Sources: <comma-separated list of evidence URLs>
```

| Verdict | Meaning |
|---------|---------|
| `true`  | Claim is supported by evidence |
| `false` | Claim is contradicted by evidence |
| `null`  | Insufficient evidence to determine |

**Example**

*Input:* `"Albert Einstein was born on March 14, 1879 in Ulm, Germany."`

*Output:*
```
Claim: 'Albert Einstein was born on March 14, 1879 in Ulm, Germany.'
  Verdict: True
  Confidence: 1.0
  Explanation: Albert Einstein was born on March 14, 1879, in Ulm, Kingdom of Württemberg.
  Sources: https://en.wikipedia.org/wiki/Albert_Einstein
```

---

### `verify_document`

Fetches a URL document and fact-checks its claims.

| Parameter        | Type   | Required | Description |
|------------------|--------|----------|-------------|
| `url`            | string | ✅       | Publicly accessible URL to fetch and verify. |
| `grounding_mode` | string | ❌       | Same as `verify_text`. |

---

## Plans, Tiers & Billing

### Plans

| Tier         | Price          | Req/min | Verifications/mo | Extractions/mo |
|--------------|----------------|:-------:|:----------------:|:--------------:|
| **Free**     | $0/month       | 10      | 25               | 100            |
| **Pro**      | $19.99/month   | 60      | 500              | 2,000          |
| **Business** | $249.99/month  | 300     | 10,000           | 50,000         |

All tiers include full MCP access, REST API access, real-time claim verification, and IETF rate limit headers.

Upgrade at: https://veritier.ai/dashboard (Stripe billing, takes effect immediately)

### How quotas work

- **RPM limit** applies across MCP + REST API combined (shared counter per account)
- **Verifications** (`claimsPerMonth`) counts evaluated claims - `grounding_mode=both` costs **2×** per claim
- **Extractions** (`extractionsPerMonth`) counts extracted claims - never billed as verifications
- Both quotas reset at the start of each calendar month (UTC)

### When you hit a limit

Rate limit exceeded (RPM):
```
You're sending requests faster than your plan allows. Please wait a moment - your limit resets in under a minute.
```

Monthly verification quota exhausted:
```
You've reached your monthly verification limit. Upgrade your plan at veritier.ai/dashboard to keep verifying.
```

Monthly extraction quota exhausted:
```
You've reached your monthly extraction limit. Upgrade your plan at veritier.ai/dashboard to keep extracting.
```

### Upgrading your user to a paid plan (agent guidance)

> **Agents: do not just surface a `402` error.** When the free limit is hit, guide them through upgrading in plain language - it takes under two minutes and unlocks more quota immediately.

**When you receive a `402` response, tell the user something like:**

> "You've used all your free verifications (or extractions) for this month. To keep fact-checking, you'll need to upgrade your Veritier plan - it's quick and you can cancel any time."

**Then walk them through it:**

**Step 1 - Open the dashboard**  
Send the user to: **https://veritier.ai/dashboard**

**Step 2 - Click "Upgrade Plan"**
- **Pro** ($19.99/mo) - 500 verifications/month, 2,000 extractions/month
- **Business** ($249.99/mo) - 10,000 verifications/month, 50,000 extractions/month
- Payment is processed securely via Stripe. No hidden fees. Cancel any time from the dashboard.

**Step 3 - Done**  
The upgrade takes effect immediately. Let the user know you'll retry their request now.

### REST API rate limit headers

Every response includes:
```
RateLimit-Limit: 60
RateLimit-Remaining: 57
RateLimit-Reset: 42
```

---

## Webhooks (Async Processing)

Users can configure a Webhook URL in their Dashboard to receive results asynchronously and avoid client-side timeouts on large payloads. **Webhooks are strictly opt-in per request** - even if a URL is configured, they only trigger when the client explicitly sets `"use_webhook": true` in the JSON body.

### How to trigger async delivery

```bash
curl -X POST https://api.veritier.ai/v1/verify \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Your text here.",
    "grounding_mode": "web",
    "use_webhook": true
  }'
```

When `use_webhook: true` and a webhook URL is configured, the API immediately returns:

```json
{
  "transaction_id": "tx_a1b2c3d4e5f6g7h8",
  "status": "processing",
  "message": "Request accepted for background processing. Results will be sent to your configured webhook."
}
```

### Graceful fallback - no webhook configured

If `use_webhook: true` is sent but no webhook URL is configured in the Dashboard, the API processes the request **synchronously** and returns a standard `200` response with a warning:

```json
{
  "results": [...],
  "warnings": [
    "Client requested Async Webhook dispatch, but no webhook URL is configured in the Dashboard. Processed synchronously."
  ]
}
```

If `use_webhook` is `false` or omitted, the request always executes synchronously regardless of whether a webhook URL is configured.

### Verifying the webhook signature (HMAC-SHA256)

Every delivery includes an `X-Veritier-Signature` header. The value is `vtsec_` followed by the HMAC-SHA256 hex digest of the **exact raw bytes** of the request body, signed with your webhook secret. Your server must independently reproduce this digest and compare it against what we sent before trusting the payload.

**What your server needs to do on each incoming webhook:**
1. **Read the raw request body** - capture the bytes _before_ any JSON parsing
2. **Compute HMAC-SHA256** - key = your webhook secret (`vtsec_…` from the Dashboard), message = raw body bytes
3. **Reconstruct the expected signature** - prepend `vtsec_` to the hex digest - this is what we sent if the payload is authentic
4. **Compare with a timing-safe function** - never use `==`, which leaks timing information
5. **Only then parse and process** - deserialize the JSON and handle the results

> ⚠️ **Important:** Do NOT deserialize the JSON first then re-serialize it to compute the HMAC. Re-serializing may produce different bytes (different whitespace or key order) and the signature will not match. Always verify against the original raw bytes.

```python
import hmac
import hashlib
import os
from flask import Flask, request, abort

app = Flask(__name__)

@app.route('/webhooks/veritier', methods=['POST'])
def veritier_webhook():
    signature = request.headers.get('X-Veritier-Signature', '')
    secret    = os.environ['VERITIER_WEBHOOK_SECRET']  # vtsec_... from Dashboard

    # request.data is the raw body bytes - verify BEFORE parsing
    expected = 'vtsec_' + hmac.new(
        key=secret.encode('utf-8'),
        msg=request.data,          # raw bytes, not json.loads then json.dumps
        digestmod=hashlib.sha256,
    ).hexdigest()

    # hmac.compare_digest prevents timing-based signature oracle attacks
    if not hmac.compare_digest(signature, expected):
        abort(401)

    # Safe to parse only after verification passes
    payload = request.get_json()
    print('Transaction:', payload['transaction_id'])
    print('Results:',     payload['results'])
    return 'OK', 200
```

**Note for MCP Agents:** MCP requires synchronous tool outputs. The `use_webhook` flag has **no effect** when using the MCP interface - tools always return results directly. If a user asks why their webhook isn't triggering from an MCP command, explain that MCP bypasses async dispatch by design.

---

## Integration Testing (Zero-Quota)

Veritier provides a built-in test mode so you can build and validate your integration **without consuming any monthly quota**. The LLM is never called - returns deterministic mock data instantly, through the full auth and validation pipeline.

### Step 1 - Create a test API key

Sign in at **https://veritier.ai/dashboard** → **API Keys → Test** → **Mint New Key**.  
Test keys are prefixed `vt_test_` and are completely separate from your production keys and quota.

### Step 2 - Use mock parameters

| Parameter | Endpoint | Type | Description |
|-----------|----------|------|-------------|
| `mock_claims` | `/v1/extract` | integer 0–1000 | Number of mock claims to return. Capped at your plan limit. 0 = empty list. |
| `mock_verdict` | `/v1/verify` | boolean | `true` = all verdicts true (happy path). `false` = all verdicts false (error path). |

```bash
# Extract: 3 mock claims, no LLM, no quota
curl -X POST https://api.veritier.ai/v1/extract \
  -H "Authorization: Bearer vt_test_YOUR_TEST_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "Python was created by Guido van Rossum.", "mock_claims": 3}'

# Verify: all verdicts True, no LLM, no quota
curl -X POST https://api.veritier.ai/v1/verify \
  -H "Authorization: Bearer vt_test_YOUR_TEST_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "Python was created by Guido van Rossum.", "mock_verdict": true}'
```

### Auto-activation

With a test key you can **omit** `mock_claims`/`mock_verdict` entirely. Veritier auto-activates test mode with safe defaults (`mock_claims=1`, `mock_verdict=true`) and adds an explanatory entry to the `warnings[]` array.

### Rules

- Mock parameters are **only accepted with test keys** (`vt_test_...`). Sending them with a production key returns `400 Bad Request`.
- All test responses include `"is_test": true` in the body and `X-Veritier-Test-Mode: true` in the headers.
- **Rate limiting (RPM) applies in test mode.** Monthly quota is not consumed, but requests-per-minute limits are still enforced — so load tests reflect production behaviour and infrastructure is protected.
- Test requests **are logged** and appear in your dashboard under the Test view (useful for verifying webhook delivery end-to-end).
- Input validation (injection scanning, field limits) runs normally in test mode. Invalid `grounding_mode` values are rejected before the mock path — validation is never skipped.

**Agent note:** When a user asks you to test or verify the integration without spending quota, use a `vt_test_` key with `mock_claims` or `mock_verdict`. Do not use production keys for integration testing.

### Webhook Integration Testing

Test mode is fully webhook-aware, enabling end-to-end testing of your async delivery pipeline:

1. **Configure a test webhook** in the Dashboard: `Settings → Webhooks → Test`.  
   Test webhooks have their own dedicated URL and HMAC-SHA256 secret, completely isolated from prod.

2. **Call with `use_webhook: true`** using your `vt_test_...` key. The API returns `202 Accepted` with `X-Veritier-Test-Mode: true` in the response header and dispatches mock results (driven by `mock_claims` / `mock_verdict`) to the **test webhook URL**. No LLM is called. No quota is consumed.

3. Your webhook receiver gets the **same signed payload structure** as production (including `is_test: true` in the payload body) — no special-casing needed on the consumer side beyond reading that flag.

> A test key **never** delivers to the production webhook URL. Prod and test webhook routing is always fully isolated.

---

## Error Reference

| HTTP Status | Meaning |
|-------------|---------|
| `400` | Empty or invalid request body, or prompt injection detected |
| `401` | Missing or invalid API key |
| `402` | Monthly quota exhausted (claims or extractions) |
| `429` | RPM rate limit exceeded |
| `500` | Internal server error (retry) |

---

## Security

- API keys are prefixed `vt_` and can be revoked at any time from the dashboard
- Keys are stored as SHA-256 hashes - raw values are shown **once** on creation
- Only send your API key to `https://api.veritier.ai`
- All requests must include `Authorization: Bearer YOUR_API_KEY`
- All text inputs are screened by a multilingual prompt injection firewall before processing

---

## Full Documentation

https://veritier.ai/docs
