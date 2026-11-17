---
name: veritier
version: 3.4.2
description: Agent Trust Gate for tool calls. Agents should not act without a gate and evidence. attest_action looks the action up in a system of record - npm, PyPI, CourtListener, SEC EDGAR, the U.S. Code, or a policy corpus you supply - and blocks the call if the record isn't there. Each decision is a reconstructable, revocable Ed25519-signed workpaper (Claim Credential), not a certificate of truth. Also extracts and verifies claims and scans documents. Connects over MCP Streamable HTTP, so there is nothing to install.
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
    category: agent-trust-gate, fact-checking, document-validation
    api_base: https://api.veritier.ai
    mcp_endpoint: https://api.veritier.ai/mcp/
    transport: streamable-http
    obtain_key_url: https://veritier.ai/dashboard
---

# Veritier — Agent Trust Gate

Agents should not act on a claim without a gate and evidence. Veritier's **Agent Trust Gate** (`attest_action`) looks the action up in a system of record — npm, PyPI, CourtListener, SEC EDGAR, the U.S. Code, or a policy corpus you supply — and blocks the call if the record isn't there. Each gate decision is recorded as a **Claim Credential**: a reconstructable, revocable Ed25519-signed workpaper that proves what was checked. It is proof of the gate decision, not a certificate of truth.

The same API can extract and verify claims against live web evidence or references you supply, and scan PDFs and images for signs of manipulation. Use those when you need an evidence check or a hallucination audit — they never fail-close. `attest_action` is the control that can stop the agent.

Reach for this skill right before the agent runs a tool call, before you publish an answer, when you are auditing AI-generated text, or when a user hands you a document you have no reason to trust.

## Skill Files

| File | URL / path |
|------|------------|
| **SKILL.md** (this file) | `https://veritier.ai/skill.md` (this repo: [`SKILL.md`](SKILL.md)) |
| Examples README | `https://veritier.ai/README.md` (this repo: [`README.md`](README.md)) |
| Live OpenAPI (API v2.2.0) | [`https://api.veritier.ai/openapi.json`](https://api.veritier.ai/openapi.json) |
| Interactive API docs | [`https://api.veritier.ai/docs`](https://api.veritier.ai/docs) |
| Stdio MCP proxy | `https://veritier.ai/veritier_mcp_proxy.py` (this repo: [`python/mcp/veritier_mcp_proxy.py`](python/mcp/veritier_mcp_proxy.py)) |
| Stdio MCP test | `https://veritier.ai/veritier_mcp_test.py` (this repo: [`python/mcp/veritier_mcp_test.py`](python/mcp/veritier_mcp_test.py)) |
| REST + webhook samples | [`python/`](python/) and [`javascript/`](javascript/) |

**Install locally (Antigravity / file-based skill runners):**
```bash
mkdir -p ~/.skills/veritier
curl -s https://veritier.ai/skill.md > ~/.skills/veritier/SKILL.md
```

🔒 **SECURITY:** Only send your API key to `https://api.veritier.ai` - never to any other domain.

---

## When to Use This Skill

**`attest_action`** is the Agent Trust Gate — the one that can stop the agent. Use it when a tool call depends on a record actually existing: an npm or PyPI package, a court opinion, an SEC filing, a section of the U.S. Code, or a policy corpus you supply. It returns a decision and a signed workpaper (Claim Credential) before the agent proceeds. A `block` decision means the call must not run. Verify never fail-closes; attest does.

**`extract_text`** pulls the checkable claims out of a block of text so you can decide which ones are worth verifying. Extraction draws down a separate monthly allowance from verification, so it is the inexpensive way to triage a large body of content.

Reach for **`verify_text`** when you need an evidence check (supporting, not a gate):
- A claim in a draft response has to be checked before you send it
- A user has shared a statement, article, or paragraph and wants to know whether it holds up
- AI-generated content needs an audit for hallucinations
- The claim should be checked against the user's own documents rather than the open web. Set `grounding_mode` to `references` and pass the material in `grounding_references`.

`action_id` is optional on verify. Passing it mints an informational Claim Credential for the record — a signed workpaper of what was checked, not a gate. Verdicts do not change and nothing is blocked, because verify never fail-closes.

**`extract_document`** and **`verify_document`** do the same work when the source is a URL rather than raw text. `verify_document` takes the same optional `action_id`.

**`validate`** scans a PDF or image for signs of tampering. Run it before you trust the text you pull out of a document a user handed you.

Do **not** use Veritier for:
- Opinions, predictions, or subjective statements. It only evaluates claims that can be proven true or false.
- Real-time event data that may not be indexed yet
- Fail-closing on the result of `verify_text`. Use `attest_action` when the call has to be gated.
- Treating a Claim Credential as a certificate of truth, a judicial finding, or a discharge of duty

---

## Setup: Connect via MCP

**Transport:** Streamable HTTP, following the MCP 2025-03-26 spec  
**Endpoint:** `https://api.veritier.ai/mcp/`  
**Auth:** `Authorization: Bearer YOUR_API_KEY`

The transport is stateless, so it runs happily on serverless clients. Get your API key at https://veritier.ai/dashboard

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

# Optional: mint an informational credential (does not fail-close)
curl -X POST https://api.veritier.ai/v1/verify \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "Your text here.", "action_id": "tool_call_abc"}'

# Fail-closed attestation (REST: procedure required; text XOR document)
curl -X POST https://api.veritier.ai/v1/attest_action \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"action_id": "tool_call_abc", "text": "npm install lodash", "procedure": "package_exists"}'

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

> **Agents: read this section first.** Many users asking you to gate a tool call or verify claims will not have a Veritier account or API key yet. Do not fail silently - guide them through setup. This takes under two minutes and is free.

### Step 1 - Create a free account
Direct the user to: **https://veritier.ai/register**
- Free tier: 25 verifications/month + 100 extractions/month, no credit card required
- After registering they will receive a verification email - remind them to check their inbox

### Step 2 - Generate an API key
Once logged in, send the user to: **https://veritier.ai/dashboard**
- Click **"Create Key"**, give it any name (e.g. `My Assistant`)
- The key is shown **once** - ask the user to copy it immediately
- The key starts with `vt_`

### Step 3 - Add the key to your MCP configuration
Ask the user to set `VERITIER_API_KEY` in the environment config of their MCP client, which is the same file where this skill is declared. The key stays in their own environment and travels only to `https://api.veritier.ai`, as a Bearer token header. It goes nowhere else.

### Step 4 - You're ready
Confirm by calling `extract_text` or `verify_text` with a short test sentence and show the result. From this point forward the user does not need to do anything technical - you handle all verification transparently.

---

## Available Tools

### `extract_text`

Pulls every falsifiable claim out of raw text. Nothing is checked against evidence, and the call draws down `extractionsPerMonth` only.

| Parameter | Type   | Required | Description |
|-----------|--------|----------|-------------|
| `text`    | string | ✅       | Raw text to extract claims from. Up to 32,000 characters. |

**Output:** A list of isolated, falsifiable claim strings.

---

### `extract_document`

Fetches a URL and pulls the claims out of whatever it finds there.

| Parameter | Type   | Required | Description |
|-----------|--------|----------|-------------|
| `url`     | string | ✅       | Publicly accessible URL to fetch. |

---

### `verify_text`

Extracts the claims in a block of text and checks each one against evidence, returning a verdict, a confidence score, and the sources behind it. Every evaluated claim draws down `claimsPerMonth`.

| Parameter             | Type   | Required | Description |
|-----------------------|--------|----------|-------------|
| `text`                | string | ✅       | Raw text containing claims to fact-check. Up to 32,000 characters. |
| `grounding_mode`      | string | ❌       | `"web"` (default), `"references"`, or `"both"`. `"both"` costs 2× quota per claim. |
| `grounding_references`| array  | ❌       | Up to 10 references. Each: `{"type": "text"/"url", "content": "..."}`. Required when `grounding_mode` is `"references"` or `"both"`. |
| `action_id`           | string | ❌       | If set, mint an informational Claim Credential. Does not change verdicts and does not fail-close. |

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

Fetches a document at a URL and fact-checks the claims inside it.

| Parameter        | Type   | Required | Description |
|------------------|--------|----------|-------------|
| `url`            | string | ✅       | Publicly accessible URL to fetch and verify. |
| `grounding_mode` | string | ❌       | Same as `verify_text`. |
| `action_id`      | string | ❌       | Same as `verify_text`. Informational credential; verify is not fail-closed. |

---

### `validate`

Scans a document for signs that it has been altered. The scan reads the file's metadata, looks for visual manipulation, and cross-references the facts it finds against web evidence. It draws down `validationsPerMonth` only.

| Parameter         | Type    | Required | Description |
|-------------------|---------|----------|-------------|
| `url`             | string  | ❌       | Publicly accessible URL to fetch. Required if `document_base64` is not provided. |
| `document_base64` | string  | ❌       | Base64 string of the file. Required if `url` is not provided. |

---

### `attest_action`

Looks a tool call up in a named system of record before the agent runs it — the Agent Trust Gate — and returns a decision together with a signed workpaper (Claim Credential). The credential is reconstructable, revocable Ed25519 proof of the gate decision, not a certificate of truth. Each material claim draws down one unit of `claimsPerMonth`. This is a gate rather than a fact-checker, so it does not replace `verify_text`.

REST `POST /v1/attest_action` and the MCP `attest_action` tool share decisions and procedures, but **their request fields are not the same**. Do not flatten them into one schema.

#### REST: `POST /v1/attest_action`

Source of truth: live OpenAPI [`AttestActionRequest`](https://api.veritier.ai/openapi.json) (API v2.2.0). Interactive docs: https://api.veritier.ai/docs

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `action_id` | string | ✅ | Caller's identifier for the tool call. Bound into the credential. |
| `procedure` | string | ✅ | Named lookup. **Required on REST — there is no default.** See the procedure table below. |
| `text` | string | XOR | Raw action payload (up to 32,000 characters). Provide **`text` or `document`, not both**. |
| `document` | object | XOR | `{ "type": "text" \| "url" \| "base64", "content": "...", "file_name"? }`. Same XOR as extract/verify. |
| `grounding_references` | array | ❌ | Required when `procedure` is `policy_ground`. Up to 10 items of `{ "type", "content", "file_name"? }`. Ignored for the other procedures. REST has **no** `reference_text` field. |
| `on_null` | string | ❌ | What to do when a material claim cannot be resolved either way: `"block"` (default) or `"escalate"`. A claim that comes back false always blocks. |
| `mock_decision` | string | ❌ | `"allow"` or `"block"`. Returns a signed credential without running the lookup, and consumes no quota. Accepted on a test key or an Engine dashboard JWT. Production API keys are rejected. Test keys auto-activate `allow` when the field is omitted; a JWT does not. |
| `deep_audit` | bool | ❌ | After a `block` or `escalate`, wait for a web verify workpaper. The decision does not change and the extra claim units are billed. Skipped on `allow` and in mock mode. |
| `tool` | object | ❌ | Optional `{ "name", "payload_json"? }`. Hashed into the credential, never executed. REST and Engine only. |
| `run_validate` | bool | ❌ | If true and a URL or base64 document is present, run forensic authenticity first. `fraudulent` or `suspicious` blocks. REST and Engine only. |
| `use_webhook` | bool | ❌ | If true and a Dashboard webhook is configured, return 202 after the procedure completes, then POST the signed result. REST only. |

#### MCP: `attest_action` tool

Hosted MCP (`https://api.veritier.ai/mcp/`) and the stdio proxy. Always synchronous: `use_webhook` has no effect.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `action_id` | string | ✅ | Caller's identifier for the tool call. Bound into the credential. |
| `text` | string | ✅ | Action payload. **MCP is text-only** — there is no `document` argument. |
| `procedure` | string | ❌ | Named lookup. **Defaults to `"package_exists"` when omitted** (Python default on the MCP tool). |
| `reference_text` | string | ❌ | **MCP-only alias.** Required when `procedure` is `policy_ground`. The MCP layer wraps this string into a single text `GroundingReference` before `compose_claims`. Do **not** send `reference_text` on REST — use `grounding_references` there. |
| `on_null` | string | ❌ | `"block"` (default) or `"escalate"`. A claim that comes back false always blocks. |
| `mock_decision` | string | ❌ | `"allow"` or `"block"`. Test key (`vt_test_...`) only on MCP. Test keys auto-activate `allow` when omitted. |
| `deep_audit` | bool | ❌ | Same meaning as REST. Works on both MCP and REST. |

`run_validate`, `document`, `tool`, and `grounding_references` are REST and Engine only. MCP does not accept those fields.

| Procedure | Checks |
|-----------|--------|
| `package_exists` | The package is published on npm or PyPI. |
| `citation_exists` | The case exists in CourtListener, and any quoted passage actually appears in the matched opinion. This is the public record, not Westlaw. |
| `filing_exists` | The filing is on SEC EDGAR. |
| `statute_exists` | The section exists in the U.S. Code or the Internal Revenue Code, via Cornell LII. |
| `policy_ground` | The action is supported by the corpus you supply. REST: `grounding_references`. MCP: `reference_text` (wrapped into one text grounding reference). |

| `decision` | What it means | What the agent should do |
|------------|---------------|--------------------------|
| `allow` | The record was found and it matches the action. | Run the tool call. |
| `block` | The record is missing, or a material claim is contradicted. | Refuse the call and tell the user what was missing. |
| `escalate` | A material claim could not be resolved and `on_null` is `"escalate"`. | Hand the decision to a human. |

All three decisions come back as HTTP 200. A `block` is the gate doing its job, not a failed request.

**Output:** the `decision`, the material claims behind it, `credential.id`, and a `credential.verify_url` of the form `https://veritier.ai/c/crc_…`. An `execution` block carries the `mode`, the `input_sha256` of what was attested, and the signing `kid`.

Anyone can reconstruct the signed workpaper with `GET https://api.veritier.ai/v1/credentials/{id}`, and no API key is needed to do it. Credentials stay retrievable for 400 days. Signatures are Ed25519 and are checked against the JWKS at `GET https://api.veritier.ai/v1/credentials/.well-known/jwk`, which publishes the current and previous keys. The issuer can revoke a credential with `POST https://api.veritier.ai/v1/credentials/{id}/revoke` using the key that minted it. The public GET keeps working afterwards and reports `revoked: true`. The workpaper is proof of the gate decision, not a certificate of truth.

---

## Plans, Tiers & Billing

### Plans

| Tier           | Price          | Req/min | Verifications/mo | Extractions/mo | Validations/mo |
|----------------|----------------|:-------:|:----------------:|:--------------:|:--------------:|
| **Free**       | $0/month       | 10      | 25               | 100            | 5 |
| **Pro**        | $19.99/month   | 60      | 500              | 2,000          | 100 |
| **Business**   | $249.99/month  | 300     | 10,000           | 50,000         | 2,000 |
| **Enterprise** | Contact us     | Custom  | Custom           | Custom         | Custom |

Self-serve tiers (Free, Pro, Business) get the same capabilities: MCP access, the REST API, the Agent Trust Gate, live claim verification, and IETF-standard rate limit headers. Only the allowances differ. Enterprise is custom quotas and contract terms — contact us at https://veritier.ai.

Upgrade at https://veritier.ai/dashboard. Billing runs through Stripe and the new plan applies immediately.

### How quotas work

- The requests-per-minute limit is one counter per account, shared across MCP and the REST API.
- `claimsPerMonth` counts evaluated claims. Setting `grounding_mode` to `both` costs two units per claim, and `attest_action` spends one unit per material claim.
- `extractionsPerMonth` counts extracted claims and is never billed as a verification.
- `validationsPerMonth` counts authenticity scans and is never billed as an extraction or a verification.
- Every quota resets at the start of the calendar month, UTC.

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

> **Agents: do not just hand the user a raw quota error.** When someone runs out of free verifications, walk them through upgrading in plain language. It takes under two minutes and the larger allowance is available right away.

**When the API reports that the monthly quota is exhausted, tell the user something like:**

> "You've used all your free verifications (or extractions) for this month. To keep gating tool calls and verifying claims, you'll need to upgrade your Veritier plan - it's quick and you can cancel any time."

**Then walk them through it:**

**Step 1 - Open the dashboard**  
Send the user to: **https://veritier.ai/dashboard**

**Step 2 - Click "Upgrade Plan"**
- **Pro** ($19.99/mo) - 500 verifications/month, 2,000 extractions/month
- **Business** ($249.99/mo) - 10,000 verifications/month, 50,000 extractions/month
- **Enterprise** — Contact us at https://veritier.ai for custom quotas
- Payment is processed securely via Stripe on self-serve plans. No hidden fees. Cancel any time from the dashboard.

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

A webhook URL configured in the Dashboard lets Veritier return results asynchronously, which keeps a large payload from timing out on the client. Webhooks are opt-in on every request. Configuring the URL is not enough on its own: the client has to set `"use_webhook": true` in the JSON body before anything is dispatched.

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

With `use_webhook: true` and a URL configured, extract, verify, and validate return `202 Accepted` straight away, with a transaction ID in the body:

```json
{
  "transaction_id": "tx_a1b2c3d4e5f6g7h8"
}
```

`POST /v1/attest_action` also answers `202`, with one difference: the named procedure runs to completion before the response is sent, so the body already carries `decision` and `credential_id`. The signed delivery that follows uses `"type": "attestation"` and puts the full workpaper under `results`.

```json
{
  "transaction_id": "tx_a1b2c3d4e5f6g7h8",
  "decision": "block",
  "credential_id": "crc_…",
  "verify_url": "https://veritier.ai/c/crc_…",
  "action_id": "tool_call_abc"
}
```

### Graceful fallback - no webhook configured

If `use_webhook: true` is sent but no webhook URL is configured in the Dashboard, the request runs synchronously and the results come back as usual, with a warning attached:

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

Every delivery includes an `X-Veritier-Signature` header. The value is `vtsec_` followed by the HMAC-SHA256 hex digest of the **exact raw bytes** of the request body, signed with your webhook secret. Your server has to reproduce that digest itself and compare it with the one we sent before it trusts anything in the payload.

Retries reuse the same `Idempotency-Key` and `X-Veritier-Idempotency-Key`, and every delivery carries `X-Veritier-Transaction-Id`, so a receiver can recognise a duplicate. For attestations the idempotency key takes the form `attestation:{action_id}:{transaction_id}`. Deliveries whose payload has an `action_id` also repeat it in an `X-Veritier-Action-Id` header. The signature covers the body and nothing else.

**What your server needs to do on each incoming webhook:**
1. **Read the raw request body** - capture the bytes _before_ any JSON parsing
2. **Check Idempotency-Key** - retries send the same key (`attestation:{action_id}:{transaction_id}` for attest) so your receiver can ignore duplicates
3. **Compute HMAC-SHA256** - key = your webhook secret (`vtsec_…` from the Dashboard), message = raw body bytes
4. **Reconstruct the expected signature** - prepend `vtsec_` to the hex digest - this is what we sent if the payload is authentic
5. **Compare with a timing-safe function** - never use `==`, which leaks timing information
6. **Only then parse and process** - deserialize the JSON and handle the results

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

    # Retries send the same Idempotency-Key / X-Veritier-Idempotency-Key
    # (attest: attestation:{action_id}:{transaction_id}). HMAC is over the body only.

    # Safe to parse only after verification passes
    payload = request.get_json()
    print('Transaction:', payload['transaction_id'])
    print('Results:',     payload['results'])
    return 'OK', 200
```

**Note for MCP Agents:** MCP requires synchronous tool outputs. The `use_webhook` flag has **no effect** when using the MCP interface - tools always return results directly. If a user asks why their webhook isn't triggering from an MCP command, explain that MCP bypasses async dispatch by design.

---

## Integration Testing (Zero-Quota)

Test mode lets you build and check an integration without spending any monthly quota. A test key runs the full authentication and validation path and returns fixed mock data straight away. The model is never called.

### Step 1 - Create a test API key

Sign in at **https://veritier.ai/dashboard** → **API Keys → Test** → **Create Key**.  
Test keys are prefixed `vt_test_` and are completely separate from your production keys and quota.

### Step 2 - Use mock parameters

| Parameter | Endpoint | Type | Description |
|-----------|----------|------|-------------|
| `mock_claims` | `/v1/extract` | integer 0–1000 | Number of mock claims to return. Capped at your plan limit. 0 = empty list. |
| `mock_verdict` | `/v1/verify` | boolean | `true` = all verdicts true (happy path). `false` = all verdicts false (error path). |
| `mock_validation` | `/v1/validate` | boolean | `true` = authentic document. `false` = fraudulent document. |
| `mock_decision` | `/v1/attest_action` | string | `allow` or `block`. Signed credential. No registry lookup or LLM. Test keys auto-activate allow when omitted. The Engine playground may send this on a dashboard JWT without auto-activating. Production API keys still need `vt_test_`. |

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

With a test key you can leave out `mock_claims`, `mock_verdict`, `mock_validation`, and `mock_decision` altogether. Veritier turns test mode on with safe defaults of one claim, a true verdict, an authentic document, and an `allow` decision, then explains what it did in the `warnings[]` array. A dashboard JWT in the Engine does not auto-activate, so omitting `mock_decision` there runs the live procedure.

### Rules

- A production API key that sends mock parameters is rejected with `400 Bad Request`. Keys prefixed `vt_test_` accept every `mock_*` field, and switch test mode on by themselves when the fields are absent. The Engine playground can send `mock_decision` on a dashboard JWT without auto-activating, and setting the playground toggle to Off drops the field. `mock_claims`, `mock_verdict`, and `mock_validation` stay test-key only.
- Every test response carries `"is_test": true` in the body and `X-Veritier-Test-Mode: true` in the headers.
- **Requests-per-minute limits still apply in test mode.** Your monthly quota goes untouched, but the rate limiter behaves exactly as it does in production, so a load test tells you something real.
- Test requests are logged and show up under the Test view in your dashboard, which is the easiest way to watch a webhook delivery end to end.
- Input validation runs as normal in test mode, including injection scanning and field limits. An invalid `grounding_mode` is rejected before the mock path is reached.

**Agent note:** When a user asks you to test an integration without spending quota, use a `vt_test_` key together with `mock_claims`, `mock_verdict`, `mock_validation`, or `mock_decision`. Never reach for a production key to do it. The Engine playground can send `mock_decision` on a dashboard session, and switching that toggle to Off drops the field so the named procedure runs for real.

### Webhook Integration Testing

Test mode understands webhooks, so you can exercise the whole async path before any of it touches production:

1. **Configure a test webhook** in the Dashboard: `Settings → Webhooks → Test`.  
   Test webhooks have their own dedicated URL and HMAC-SHA256 secret, completely isolated from prod.

2. **Call with `use_webhook: true`** using your `vt_test_` key. You get back `202 Accepted` with `X-Veritier-Test-Mode: true` in the headers, and whatever mock results your `mock_*` parameters asked for are dispatched to the **test webhook URL**. No model is called and no quota is spent. An attestation response also carries `decision` and `credential_id`.

3. Your receiver gets the same signed payload structure it would get in production, with `is_test: true` added to the body. Reading that flag is the only special case your consumer needs.

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

- Product docs: https://veritier.ai/docs
- Live OpenAPI (API v2.2.0): https://api.veritier.ai/openapi.json
- Interactive API: https://api.veritier.ai/docs
