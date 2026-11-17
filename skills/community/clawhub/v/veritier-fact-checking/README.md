# ✅ Veritier — Agent Trust Gate API Examples

**Agents should not act without a gate and evidence.**

Veritier is the **Agent Trust Gate**. Before an agent runs a tool call, `attest_action` looks it up in a system of record — npm, CourtListener, EDGAR, the U.S. Code, or a policy corpus you supply — and blocks the call if the record isn't there. Each decision is a **Claim Credential**: a reconstructable, revocable Ed25519-signed workpaper that proves what the gate checked. It is not a certificate of truth.

The same API also extracts and verifies claims in text, PDFs, and images against live web evidence or your own private references, and returns a verdict, a confidence score, and its sources. That path never fail-closes. Use it as supporting evidence — including hallucination audits — not as the control plane.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://python.org)
[![Node.js 18+](https://img.shields.io/badge/Node.js-18%2B-brightgreen.svg)](https://nodejs.org)
[![Veritier API](https://img.shields.io/badge/API-veritier.ai-purple.svg)](https://veritier.ai)

🌐 [Website](https://veritier.ai) · 📖 [Documentation](https://veritier.ai/docs) · 📐 [OpenAPI](https://api.veritier.ai/openapi.json) · 🔑 [Get Free API Key](https://veritier.ai/register) · 📊 [Dashboard](https://veritier.ai/dashboard)

---

## ⚡ 30-Second Quickstart

Get your free API key at [veritier.ai/register](https://veritier.ai/register), then:

<table>
<tr>
<th>Python</th>
<th>JavaScript</th>
</tr>
<tr>
<td>

```python
import httpx

response = httpx.post(
    "https://api.veritier.ai/v1/verify",
    headers={
        "Authorization": "Bearer YOUR_API_KEY",
        "Content-Type": "application/json",
    },
    json={"text": "The Eiffel Tower is in Berlin."},
)

for claim in response.json()["results"]:
    print(f"{claim['verdict']}: {claim['claim']}")
    # False: The Eiffel Tower is in Berlin.
```

</td>
<td>

```javascript
const res = await fetch("https://api.veritier.ai/v1/verify", {
  method: "POST",
  headers: {
    Authorization: "Bearer YOUR_API_KEY",
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    text: "The Eiffel Tower is in Berlin.",
  }),
});

const { results } = await res.json();
results.forEach((c) => console.log(`${c.verdict}: ${c.claim}`));
// false: The Eiffel Tower is in Berlin.
```

</td>
</tr>
</table>

---

## 📁 What's Inside

Every example here runs as-is in **Python** or **JavaScript**, and the MCP scripts wire the same tools into an AI agent. The agent-facing instructions live in [`SKILL.md`](SKILL.md), which is also served at `https://veritier.ai/skill.md`. This README is served at `https://veritier.ai/README.md`.

### Python Examples → [`python/`](python/)

| Example | Description |
|---------|-------------|
| [extract_text.py](python/quickstart/extract_text.py) | Extract claims from text without verifying |
| [verify_text.py](python/quickstart/verify_text.py) | Verify claims against live web evidence |
| [validate_document.py](python/quickstart/validate_document.py) | Authenticity scan (`document_url` / `extracted_text`) |
| [attest_action.py](python/quickstart/attest_action.py) | Fail-closed action attestation |
| [reconstruct_credential.py](python/quickstart/reconstruct_credential.py) | Public reconstruct, JWKS, optional revoke |
| [test_integration.py](python/quickstart/test_integration.py) | Zero-quota extract / verify / validate / attest / credentials |
| [verify_article_url.py](python/use-cases/verify_article_url.py) | Fact-check all claims from a web page |
| [hallucination_audit.py](python/use-cases/hallucination_audit.py) | Catch LLM hallucinations before they reach users |
| [disinformation_shield.py](python/use-cases/disinformation_shield.py) | Screen content for false claims - truth firewall |
| [private_references.py](python/use-cases/private_references.py) | Verify against your own documents (no web search) |
| [batch_verify.py](python/use-cases/batch_verify.py) | Batch-process texts with rate-limit handling |
| [gate_tool_call.py](python/use-cases/gate_tool_call.py) | Attest, then only proceed on `decision=allow` |
| [informational_credential.py](python/use-cases/informational_credential.py) | Optional `action_id` on verify (not fail-closed) |
| [webhook_receiver.py](python/webhooks/webhook_receiver.py) | HMAC-signed webhooks + `Idempotency-Key` |

### JavaScript Examples → [`javascript/`](javascript/)

| Example | Description |
|---------|-------------|
| [extract_text.mjs](javascript/quickstart/extract_text.mjs) | Extract claims from text without verifying |
| [verify_text.mjs](javascript/quickstart/verify_text.mjs) | Verify claims against live web evidence |
| [validate_document.mjs](javascript/quickstart/validate_document.mjs) | Authenticity scan (`document_url` / `extracted_text`) |
| [attest_action.mjs](javascript/quickstart/attest_action.mjs) | Fail-closed action attestation |
| [reconstruct_credential.mjs](javascript/quickstart/reconstruct_credential.mjs) | Public reconstruct, JWKS, optional revoke |
| [test_integration.mjs](javascript/quickstart/test_integration.mjs) | Zero-quota extract / verify / validate / attest / credentials |
| [verify_article_url.mjs](javascript/use-cases/verify_article_url.mjs) | Fact-check all claims from a web page |
| [hallucination_audit.mjs](javascript/use-cases/hallucination_audit.mjs) | Catch LLM hallucinations before they reach users |
| [disinformation_shield.mjs](javascript/use-cases/disinformation_shield.mjs) | Screen content for false claims - truth firewall |
| [private_references.mjs](javascript/use-cases/private_references.mjs) | Verify against your own documents (no web search) |
| [batch_verify.mjs](javascript/use-cases/batch_verify.mjs) | Batch-process texts with rate-limit handling |
| [gate_tool_call.mjs](javascript/use-cases/gate_tool_call.mjs) | Attest, then only proceed on `decision=allow` |
| [informational_credential.mjs](javascript/use-cases/informational_credential.mjs) | Optional `action_id` on verify (not fail-closed) |
| [webhook_receiver.mjs](javascript/webhooks/webhook_receiver.mjs) | HMAC-signed webhooks + `Idempotency-Key` |

### MCP Integration - Python → [`python/mcp/`](python/mcp/)

| File | Description |
|------|-------------|
| [veritier_mcp_proxy.py](python/mcp/veritier_mcp_proxy.py) | Stdio proxy v2.2 (includes `attest_action`) |
| [veritier_mcp_test.py](python/mcp/veritier_mcp_test.py) | Integration test - auto-detects test keys for zero-quota runs |

### MCP Integration - JavaScript → [`javascript/mcp/`](javascript/mcp/)

| File | Description |
|------|-------------|
| [mcp_test.mjs](javascript/mcp/mcp_test.mjs) | Streamable HTTP test (extract / verify / validate / attest_action) |

---

## 🛠 Available API Tools

| Tool | Endpoint | Description | Quota |
|------|----------|-------------|-------|
| **extract_text** | `POST /v1/extract` | Extract falsifiable claims from raw text | Extractions |
| **extract_document** | `POST /v1/extract` | Extract claims from a URL document | Extractions |
| **verify_text** | `POST /v1/verify` | Extract + fact-check. Optional `action_id` informational credential | Verifications |
| **verify_document** | `POST /v1/verify` | Extract + fact-check from a URL document | Verifications |
| **validate** | `POST /v1/validate` | Authenticity scan of `document_url`, `document_base64` with `file_name`, or `extracted_text` | Validations |
| **attest_action** | `POST /v1/attest_action` | Agent Trust Gate: looks the action up in a system of record and returns a decision plus a signed workpaper (Claim Credential). REST requires `procedure` and `text` **or** `document` (not both); `policy_ground` uses `grounding_references`. MCP is a separate tool schema (see below). | Verifications |
| **reconstruct** | `GET /v1/credentials/{id}` | Returns the public workpaper. No API key, retained 400 days | none |
| **jwks** | `GET /v1/credentials/.well-known/jwk` | Current and previous Ed25519 public keys | none |
| **revoke** | `POST /v1/credentials/{id}/revoke` | Lets the issuer revoke a credential. The public GET still returns 200, with `revoked: true` | none |

### Verification Response

```
Claim: 'The Eiffel Tower is located in Berlin.'
  Verdict: false
  Confidence: 1.0
  Explanation: The Eiffel Tower is located in Paris, France, not Berlin.
  Sources: https://en.wikipedia.org/wiki/Eiffel_Tower
```

| Verdict | Meaning |
|---------|---------|
| `true` | Supported by evidence |
| `false` | Contradicted by evidence |
| `null` | Insufficient evidence to determine |

### Attestation Decisions

`attest_action` answers with one of three decisions.

| Decision | Meaning | HTTP status |
|----------|---------|-------------|
| `allow` | The record was found and matches the action | 200 |
| `block` | The record is missing, or a material claim is contradicted | 200 |
| `escalate` | A material claim could not be resolved and `on_null` is `"escalate"` | 200 |

A `block` is the gate doing its job rather than a failed request, so treat it as a successful call and refuse the action. The Claim Credential is reconstructable, revocable Ed25519 proof of that decision — not a certificate of truth.

REST and MCP do **not** share one `attest_action` request schema:

| | REST `POST /v1/attest_action` | MCP `attest_action` tool |
|--|------------------------------|--------------------------|
| `procedure` | **Required** (no default) | Optional; defaults to `package_exists` |
| Input | `text` **XOR** `document` | `text` only |
| `policy_ground` corpus | `grounding_references` (`{type, content, file_name?}`) | `reference_text` (MCP-only alias, wrapped into one text grounding reference) |

Live contract: [openapi.json](https://api.veritier.ai/openapi.json) (`AttestActionRequest`, API v2.2.0). Skill details: [`SKILL.md`](SKILL.md).

Passing `action_id` to `/v1/verify` mints an informational workpaper for the record and nothing more. Verify never fail-closes.

---

## 🤖 MCP Integration (AI Agents)

Any MCP-compatible agent can reach Veritier over HTTP with nothing installed locally:

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

Clients that need a local subprocess can use the [stdio proxy](python/mcp/) instead. Either way the agent gets six tools: `extract_text`, `extract_document`, `verify_text`, `verify_document`, `validate`, and `attest_action`. Reconstructing a credential, fetching the JWKS, and revoking are REST-only operations.

## 🔑 Getting Started

1. **Register** at [veritier.ai/register](https://veritier.ai/register) - free, no credit card
2. **Confirm** the verification email
3. **Go to** [veritier.ai/dashboard](https://veritier.ai/dashboard)
4. **Click** "Create Key" - copy the `vt_` key immediately (shown once)
5. **Set** `VERITIER_API_KEY` in your environment:
   ```bash
   # Copy the template
   cp .env.example .env
   # Add your key
   ```
6. **Run** any example:
   ```bash
   # Python
   cd python && pip install -r requirements.txt
   python quickstart/verify_text.py

   # JavaScript
   cd javascript && npm install
   node quickstart/verify_text.mjs
   ```

---

## 💰 Plans

| Tier | Price | Req/min | Verifications/mo | Extractions/mo | Validations/mo |
|------|-------|:---:|:---:|:---:|:---:|
| **Free** | $0 | 10 | 25 | 100 | 5 |
| **Pro** | $19.99/mo | 60 | 500 | 2,000 | 100 |
| **Business** | $249.99/mo | 300 | 10,000 | 50,000 | 2,000 |
| **Enterprise** | Contact us | Custom | Custom | Custom | Custom |

Upgrade anytime at [veritier.ai/dashboard](https://veritier.ai/dashboard) — takes effect immediately. Enterprise is custom — [contact us](https://veritier.ai).

---

## Integration Testing (Zero-Quota)

You can build and check an integration without spending any quota. A test key runs the full authentication and validation path and returns fixed mock data. The model is never called.

### 1. Create a test key

Sign in at [veritier.ai/dashboard](https://veritier.ai/dashboard) → **API Keys → Test** → **Create Key**.  
Test keys are prefixed `vt_test_` and are completely isolated from your production quota.

### 2. Run the zero-quota integration test

```bash
export VERITIER_TEST_KEY="vt_test_your_key_here"

# Python
python python/quickstart/test_integration.py

# JavaScript
node javascript/quickstart/test_integration.mjs
```

```
OK [1/10] API connectivity confirmed
OK [2/10] Extract: 3 mock claims returned
...
OK [8/10] Attest: mock_decision=allow
OK [9/10] Public reconstruct + JWKS
OK [10/10] Issuer revoke
All integration checks passed. Zero quota was consumed.
```

### 3. Mock parameters

| Parameter | Endpoint | Description |
|-----------|----------|-------------|
| `mock_claims` | `POST /v1/extract` | Integer 0–1000. Returns that many mock claims. No LLM, no extraction quota. |
| `mock_verdict` | `POST /v1/verify` | Boolean. `true` = all verdicts true, `false` = all false. No LLM, no verification quota. |
| `mock_validation` | `POST /v1/validate` | Boolean. `true` = authentic, `false` = fraudulent. REST body uses `document_url` / `extracted_text`. |
| `mock_decision` | `POST /v1/attest_action` | `allow` or `block`. Signed credential, no lookup. Test keys auto-activate allow when omitted. |

**Rules:**
- Mock fields are accepted only on test keys. A production key that sends one is rejected with `400 Bad Request`. The Engine playground can send `mock_decision` on a dashboard JWT, but the samples in this repo authenticate with API keys.
- Test responses carry `"is_test": true` in the body and an `X-Veritier-Test-Mode: true` header.
- **Requests-per-minute limits still apply in test mode.** Your monthly quota goes untouched, but the rate limiter behaves exactly as it does in production.
- Leaving the mock parameters off a test-key request switches test mode on anyway, with defaults of one claim, a true verdict, an authentic document, and an `allow` decision.
- Test requests are logged and appear in the Test view in your dashboard.
- Input validation runs as normal, including injection scanning and field limits. An invalid `grounding_mode` is rejected before the mock path is reached.

---

## 🔒 Security

- API keys are prefixed `vt_` and stored as SHA-256 hashes, so Veritier never holds the raw value.
- You can revoke a key at any time from the dashboard.
- Only ever send your key to `https://api.veritier.ai`.
- Every input is screened for prompt injection before it reaches the verification engine.
- Webhook deliveries are signed with HMAC-SHA256 in the `X-Veritier-Signature` header. The signature covers the raw body bytes and nothing else, so it does not extend to any other header. Retries reuse the same `Idempotency-Key` and `X-Veritier-Idempotency-Key`, which lets your receiver drop duplicates.
- A Claim Credential is a public signed workpaper at `/c/:id` — reconstructable, revocable Ed25519 proof of what the gate (or an informational verify) checked. It carries no account id and no email address. The issuer can revoke it, after which the public GET still succeeds and reports `revoked: true`. It is not a certificate of truth, a judicial finding, or a discharge of duty.

---

## 🏗 Use Cases

### Gate a tool call (Agent Trust Gate)
Call `POST /v1/attest_action` before the agent runs a command, and let it proceed only on `decision=allow`. [gate_tool_call](python/use-cases/gate_tool_call.py) wires that up end to end.

### Informational workpaper on verify
Pass `action_id` to `POST /v1/verify` and you get a signed workpaper for the record without gating anything. See [informational_credential](python/use-cases/informational_credential.py).

### Fact-Check Articles
Give the verification endpoint a URL and it fetches the page for you. [verify_article_url](python/use-cases/verify_article_url.py) then checks every claim it finds there.

### Verify Against Internal Documents
With `grounding_mode: "references"`, claims are checked against material you supply and the web is never searched. [private_references](python/use-cases/private_references.py) shows how the request is put together.

### Catch LLM Hallucinations
Supporting audit, not the gate. Run AI-generated text through Veritier before it reaches a reader. [hallucination_audit](python/use-cases/hallucination_audit.py) flags the claims that turn out to be false.

### Screen user-generated content
User-generated content, news snippets, and social posts can be checked the same way. [disinformation_shield](python/use-cases/disinformation_shield.py) flags false claims. This is an evidence check, not a fail-closed gate.

### Content Moderation at Scale
Thousands of texts can go through in one pass. [batch_verify](python/use-cases/batch_verify.py) handles the throttling and backoff for you.

---

## 📄 License

The code in this repository is provided under the [MIT License](LICENSE).  
The Veritier API is a commercial service - see [veritier.ai](https://veritier.ai) for terms.
