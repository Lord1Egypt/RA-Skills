# Veritier - Python Agent Trust Gate Examples

Runnable Python examples for the **Veritier API**. They gate a tool call before an agent runs it, extract claims from text, fact-check them against evidence, and scan documents for tampering.

📦 **API Docs:** [veritier.ai/docs](https://veritier.ai/docs) · 📐 **OpenAPI:** [api.veritier.ai/openapi.json](https://api.veritier.ai/openapi.json) · 🔑 **Get your free key:** [veritier.ai/register](https://veritier.ai/register)

---

## Prerequisites

- **Python 3.10+**
- A free Veritier API key ([register here](https://veritier.ai/register))

```bash
pip install -r requirements.txt
cp ../.env.example .env
# Edit .env: VERITIER_API_KEY, optionally VERITIER_TEST_KEY
```

---

## Examples

### Quickstart

| Script | Description | Run |
|--------|-------------|-----|
| [extract_text.py](quickstart/extract_text.py) | Extract falsifiable claims (no verification) | `python quickstart/extract_text.py` |
| [verify_text.py](quickstart/verify_text.py) | Fact-check claims against live web evidence | `python quickstart/verify_text.py` |
| [validate_document.py](quickstart/validate_document.py) | Authenticity scan (`document_url` / `extracted_text`) | `python quickstart/validate_document.py` |
| [attest_action.py](quickstart/attest_action.py) | Fail-closed `POST /v1/attest_action` | `python quickstart/attest_action.py` |
| [reconstruct_credential.py](quickstart/reconstruct_credential.py) | Public GET + JWKS + optional revoke | `python quickstart/reconstruct_credential.py crc_...` |
| [test_integration.py](quickstart/test_integration.py) | Zero-quota extract/verify/validate/attest/credentials | `python quickstart/test_integration.py` |

### Use cases

| Script | Description | Run |
|--------|-------------|-----|
| [verify_article_url.py](use-cases/verify_article_url.py) | Verify claims from a web page URL | `python use-cases/verify_article_url.py <URL>` |
| [hallucination_audit.py](use-cases/hallucination_audit.py) | Catch LLM hallucinations before they reach users | `python use-cases/hallucination_audit.py` |
| [disinformation_shield.py](use-cases/disinformation_shield.py) | Screen user content for false claims | `python use-cases/disinformation_shield.py` |
| [private_references.py](use-cases/private_references.py) | Verify against your own documents | `python use-cases/private_references.py` |
| [batch_verify.py](use-cases/batch_verify.py) | Batch-process with rate-limit handling | `python use-cases/batch_verify.py` |
| [gate_tool_call.py](use-cases/gate_tool_call.py) | Attest, then only proceed on `decision=allow` | `python use-cases/gate_tool_call.py` |
| [informational_credential.py](use-cases/informational_credential.py) | `action_id` on verify (not fail-closed) | `python use-cases/informational_credential.py` |

### Webhooks

| Script | Description | Run |
|--------|-------------|-----|
| [webhook_receiver.py](webhooks/webhook_receiver.py) | Verifies HMAC-SHA256 signatures and dedupes on `Idempotency-Key`, including `type: attestation` deliveries | `python webhooks/webhook_receiver.py` |

### MCP

| Script | Description | Run |
|--------|-------------|-----|
| [mcp/veritier_mcp_proxy.py](mcp/veritier_mcp_proxy.py) | Local stdio proxy for clients that need a subprocess | started by your MCP client |
| [mcp/veritier_mcp_test.py](mcp/veritier_mcp_test.py) | Exercises every tool through the proxy | `python mcp/veritier_mcp_test.py` |

See [`mcp/README.md`](mcp/) for the client configuration.

---

## API endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/extract` | POST | Extract claims without verifying |
| `/v1/verify` | POST | Extract + verify. Optional `action_id` mints an informational credential |
| `/v1/validate` | POST | Authenticity scan (`document_url`, `document_base64`, or `extracted_text`) |
| `/v1/attest_action` | POST | Looks the action up in a system of record. Returns `allow`, `block`, or `escalate`, all with HTTP 200 |
| `/v1/credentials/{id}` | GET | Reconstructs a Claim Credential. No API key, retained 400 days |
| `/v1/credentials/.well-known/jwk` | GET | Ed25519 public keys, current and previous |
| `/v1/credentials/{id}/revoke` | POST | Lets the issuer revoke a credential. The public GET still returns 200, with `revoked: true` |

---

## Need help?

- **Full docs:** [veritier.ai/docs](https://veritier.ai/docs)
- **Live OpenAPI:** [api.veritier.ai/openapi.json](https://api.veritier.ai/openapi.json)
- **MCP:** [`mcp/`](mcp/)
- **JavaScript:** [`javascript/`](../javascript/)
