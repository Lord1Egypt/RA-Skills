---
name: rstack-services
preamble-tier: 2
version: 1.0.0
description: |
  Registers and configures a paid service endpoint on resolved.sh. Any HTTPS endpoint
  can become a per-call agent-callable API with automatic OpenAPI + Scalar docs, x402
  payment gating, and HMAC request verification. Interviews the operator, generates the
  PUT command, outputs webhook verification boilerplate (Python and Node.js), and
  provides test commands for discovery and paid calls. Use when asked to "register my
  service", "sell API calls on resolved.sh", "set up a service endpoint", "how do I
  charge per call", or after rstack-audit reports no services configured.
allowed-tools:
  - Bash
  - AskUserQuestion
metadata:
  env:
    - name: RESOLVED_SH_API_KEY
      description: Your resolved.sh API key (aa_live_...)
      required: true
    - name: RESOLVED_SH_RESOURCE_ID
      description: Your resource UUID
      required: true
    - name: RESOLVED_SH_SUBDOMAIN
      description: Your subdomain slug
      required: true
---

# rstack-services

Turn any HTTPS endpoint into a paid, agent-callable API. resolved.sh handles payment
verification, routes the call, and auto-generates OpenAPI docs and a Scalar interface —
you just run an endpoint and set a price.

---

## Preamble (run first)

```bash
echo "API key set: $([ -n "$RESOLVED_SH_API_KEY" ] && echo yes || echo NO — required)"
echo "Resource ID: $RESOLVED_SH_RESOURCE_ID"
echo "Subdomain:   $RESOLVED_SH_SUBDOMAIN"
```

Fetch current services so you can show the operator what already exists:

```bash
curl -sf "https://resolved.sh/listing/$RESOLVED_SH_RESOURCE_ID/services" \
  -H "Authorization: Bearer $RESOLVED_SH_API_KEY" \
  -o /tmp/rstack_services.json 2>/dev/null

python3 -c "
import sys, json
d = json.load(open('/tmp/rstack_services.json'))
services = d.get('services', [])
if not services:
    print('No services registered yet.')
else:
    for s in services:
        print(f'  {s[\"name\"]} | \${s[\"price_usdc\"]}/call | {s.get(\"description\",\"(no description)\")[:60]}')
"
```

Also fetch the auto-generated OpenAPI spec to show the current state of their docs:

```bash
HTTP_STATUS=$(curl -sf -o /dev/null -w "%{http_code}" \
  "https://$RESOLVED_SH_SUBDOMAIN.resolved.sh/openapi.json" 2>/dev/null)
echo "Auto-generated OpenAPI docs: HTTP $HTTP_STATUS"
echo "Interactive docs at: https://$RESOLVED_SH_SUBDOMAIN.resolved.sh/docs"
```

Show this summary to the operator. If services already exist, ask: "You have {N} service(s) registered. Would you like to (A) add a new service, (B) update an existing service, or (C) review and improve all services?"

---

## Phase 1 — Understand the service

Ask these questions one at a time. Wait for each answer before asking the next.

**Q1:** "What is the HTTPS URL of the endpoint you want to make callable? Must be a publicly reachable HTTPS URL — not localhost, not a private IP, not an internal network address."

Validate the URL as it's entered:
- Must start with `https://`
- Must not contain: `localhost`, `127.0.0.1`, `0.0.0.0`, `192.168.`, `10.`, `172.16.`–`172.31.`
- If invalid, explain why and ask again

**Q2:** "What does a call to this service do? Describe it in one sentence — what goes in, what comes back. Example: 'Takes a wallet address, returns the last 30 DeFi transactions on Base.'"

**Q3:** "What format does the request body use? Common choices: (A) JSON, (B) Plain text, (C) Form data, (D) Binary/custom — describe it"

**Q4:** "What should each successful call cost, in USDC? Think about the value delivered per call.

Pricing guidance:
- `$0.001–$0.01` — high-frequency routing or lookup (data retrieval, classification)
- `$0.01–$0.10` — moderate compute (aggregation, enrichment, validation)
- `$0.10–$1.00` — meaningful compute or external API cost (inference, scraping, search)
- `$1.00+` — high-value output (report generation, code execution, specialized model)"

**Q5:** "Optionally: does your endpoint take longer than 30 seconds to respond? If yes, what's a realistic timeout in seconds? (5–300, default 30)"

**Q6:** "What's a short name for this service? Must be lowercase letters, numbers, and hyphens only — no spaces. Example: `wallet-txns`, `price-oracle`, `pdf-parser`."

---

## Phase 2 — Build the registration command

Using the answers from Phase 1, assemble the service body.

Determine `input_type` from Q3:
- JSON → `"application/json"`
- Plain text → `"text/plain"`
- Form data → `"application/x-www-form-urlencoded"`
- Other → ask for the MIME type string

Build the full PUT command:

```bash
curl -X PUT "https://resolved.sh/listing/$RESOLVED_SH_RESOURCE_ID/services/{name-from-Q6}" \
  -H "Authorization: Bearer $RESOLVED_SH_API_KEY" \
  -H "Content-Type: application/json" \
  -d @- <<'EOF'
{
  "endpoint_url": "{url from Q1}",
  "price_usdc": {price from Q4},
  "description": "{one-sentence description from Q2}",
  "input_type": "{mime type from Q3}"{,
  "timeout_seconds": {from Q5 if non-default}}
}
EOF
```

Show the command to the operator and ask for confirmation: "Ready to register this service? (A) Yes — register now, (B) I want to change something first"

If B: apply the change and show again.

If A: run the command and capture the response.

```bash
# Run the PUT command and save the response
curl -X PUT "https://resolved.sh/listing/$RESOLVED_SH_RESOURCE_ID/services/{name}" \
  -H "Authorization: Bearer $RESOLVED_SH_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ ... }' \
  -o /tmp/rstack_svc_response.json -w "\nHTTP %{http_code}\n"

cat /tmp/rstack_svc_response.json
```

Parse the response to extract the `webhook_secret`. This is critical for the next phase.

```bash
WEBHOOK_SECRET=$(python3 -c "
import json
d = json.load(open('/tmp/rstack_svc_response.json'))
print(d.get('webhook_secret', 'NOT FOUND'))
")
echo "webhook_secret: $WEBHOOK_SECRET"
```

---

## Phase 3 — Webhook verification boilerplate

The `webhook_secret` in the response is used to verify that incoming calls genuinely came through resolved.sh (not from anyone who discovered your endpoint URL directly). resolved.sh sets `X-Resolved-Signature: sha256=<hmac>` on every proxied request — your endpoint should verify it.

Display this message: "**Important:** Save your `webhook_secret` — it's shown once. Add it to your environment and use the code below to verify incoming calls."

**Python verification:**

```python
import hmac
import hashlib

WEBHOOK_SECRET = "{webhook_secret from response}"  # store in env, not hardcoded

def verify_resolved_signature(body: bytes, signature_header: str) -> bool:
    """
    Verify that the request came from resolved.sh.
    Call this before processing the request body.
    Returns False if the signature is missing or invalid.
    """
    if not signature_header or not signature_header.startswith("sha256="):
        return False
    expected = "sha256=" + hmac.new(
        WEBHOOK_SECRET.encode(),
        body,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature_header)

# FastAPI example
from fastapi import Request, HTTPException

@app.post("/your-endpoint")
async def handle(request: Request):
    body = await request.body()
    sig = request.headers.get("X-Resolved-Signature", "")
    if not verify_resolved_signature(body, sig):
        raise HTTPException(status_code=403, detail="Invalid signature")
    # process body...
```

**Node.js / Express verification:**

```javascript
const crypto = require('crypto');

const WEBHOOK_SECRET = process.env.WEBHOOK_SECRET; // '{webhook_secret from response}'

function verifyResolvedSignature(body, signatureHeader) {
    if (!signatureHeader || !signatureHeader.startsWith('sha256=')) return false;
    const expected = 'sha256=' + crypto
        .createHmac('sha256', WEBHOOK_SECRET)
        .update(body)
        .digest('hex');
    // Use timingSafeEqual to prevent timing attacks
    try {
        return crypto.timingSafeEqual(
            Buffer.from(expected),
            Buffer.from(signatureHeader)
        );
    } catch {
        return false;
    }
}

// Express example
app.post('/your-endpoint', express.raw({ type: '*/*' }), (req, res) => {
    const sig = req.headers['x-resolved-signature'] || '';
    if (!verifyResolvedSignature(req.body, sig)) {
        return res.status(403).json({ error: 'Invalid signature' });
    }
    // process req.body...
});
```

**Important implementation notes:**
- Read the raw request body before any parsing — parsers consume the stream
- In Express, use `express.raw()` or equivalent to get a Buffer, not the parsed object
- Store `webhook_secret` in an environment variable, never hardcode it

---

## Phase 4 — Test commands

Generate copy-pasteable test commands for both the free discovery endpoint and the paid call endpoint.

**Free discovery (no payment required):**

```bash
# Anyone can inspect your service before paying
curl https://$RESOLVED_SH_SUBDOMAIN.resolved.sh/service/{name}
```

Expected response structure:
```json
{
  "name": "{name}",
  "description": "{description}",
  "price_usdc": {price},
  "call_count": 0,
  "input_type": "{mime type}",
  "output_schema": null
}
```

**Paid call (requires x402 USDC payment header):**

```bash
# Without payment — expect 402 with payment requirements
curl -X POST https://$RESOLVED_SH_SUBDOMAIN.resolved.sh/service/{name} \
  -H "Content-Type: {input_type}" \
  -d '{"example": "request body"}'

# With payment — requires a valid PAYMENT-SIGNATURE header (x402 USDC on Base)
# See x402 payment spec: https://resolved.sh/x402-spec
```

**Auto-generated API docs (no setup required):**

```bash
# Machine-readable OpenAPI 3.1.0 spec — includes your service
curl https://$RESOLVED_SH_SUBDOMAIN.resolved.sh/openapi.json

# Interactive Scalar docs in the browser
open https://$RESOLVED_SH_SUBDOMAIN.resolved.sh/docs
```

The docs page is live immediately — share it as your developer reference.

---

## Phase 5 — Page content update (optional)

Offer to add a `## Services` section to the operator's page content so visitors and agents can discover the service from the main page.

AskUserQuestion: "Would you like me to add a Services section to your page describing this endpoint? (A) Yes, (B) No thanks"

If yes: fetch current md_content and append:

```bash
# Fetch current md_content
CURRENT=$(curl -sf "https://$RESOLVED_SH_SUBDOMAIN.resolved.sh?format=json" | \
  python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('md_content') or '')")
echo "$CURRENT"
```

Generate a Services section:

```markdown
## Services

| Service | Description | Price |
|---------|-------------|-------|
| [{name}](https://{subdomain}.resolved.sh/service/{name}) | {description} | ${price_usdc}/call |

**Endpoint:** `POST https://{subdomain}.resolved.sh/service/{name}`
**Payment:** x402 USDC on Base
**Docs:** [Interactive API reference](https://{subdomain}.resolved.sh/docs) · [OpenAPI spec](https://{subdomain}.resolved.sh/openapi.json)
```

Produce the full PUT command with the updated md_content.

---

## Completion Status

**DONE** — Service registered. Close with: "Your service is live at `POST https://{subdomain}.resolved.sh/service/{name}`. Buyers pay ${price_usdc} USDC per call via x402. Your docs are at https://{subdomain}.resolved.sh/docs. Run `/rstack-audit` to see your updated scores."

**DONE_WITH_CONCERNS** — If the webhook_secret was not captured from the response (e.g., the operator ran the command manually): "You'll need the `webhook_secret` to verify incoming calls. Retrieve it by calling `GET https://resolved.sh/listing/{resource_id}/services` and noting the webhook_secret field. If you need to rotate it, delete and re-register the service — the secret changes on each registration."

**BLOCKED** — If env vars are missing, the endpoint URL fails SSRF validation, or the PUT returns a non-200. Show the exact error from the response and explain the likely cause:
- 422 with `endpoint_url`: the URL failed SSRF validation — must be public HTTPS
- 403: API key missing or wrong
- 409: a service with that name already exists — use a different name or update with the same PUT call
