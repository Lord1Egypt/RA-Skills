# Veritier - JavaScript Fact-Checking Examples

Verify any claim against live web evidence with a single API call. These JavaScript examples show you how to integrate the **Veritier AI Fact-Checking API** into your Node.js applications - from basic extraction to advanced hallucination auditing.

📦 **API Docs:** [veritier.ai/docs](https://veritier.ai/docs) · 🔑 **Get your free key:** [veritier.ai/register](https://veritier.ai/register)

---

## Prerequisites

- **Node.js 18+** (uses native `fetch` - no external HTTP library needed)
- A free Veritier API key ([register here](https://veritier.ai/register))

```bash
# Install dependencies
npm install

# Set up your API key
cp ../.env.example .env
# Edit .env and replace vt_your_api_key_here with your real key
```

---

## Examples

### 🚀 Quickstart

| Script | Description | Run |
|--------|-------------|-----|
| [extract_text.mjs](quickstart/extract_text.mjs) | Extract every falsifiable claim from text (no verification) | `node quickstart/extract_text.mjs` |
| [verify_text.mjs](quickstart/verify_text.mjs) | Fact-check claims against live web evidence | `node quickstart/verify_text.mjs` |

### 📋 Use Cases

| Script | Description | Run |
|--------|-------------|-----|
| [verify_article_url.mjs](use-cases/verify_article_url.mjs) | Verify all claims from a web page URL | `node use-cases/verify_article_url.mjs <URL>` |
| [hallucination_audit.mjs](use-cases/hallucination_audit.mjs) | Catch LLM hallucinations before they reach users | `node use-cases/hallucination_audit.mjs` |
| [disinformation_shield.mjs](use-cases/disinformation_shield.mjs) | Screen user content for false claims (Truth Firewall) | `node use-cases/disinformation_shield.mjs` |
| [private_references.mjs](use-cases/private_references.mjs) | Verify against your own documents (no web search) | `node use-cases/private_references.mjs` |
| [batch_verify.mjs](use-cases/batch_verify.mjs) | Batch-process texts with rate-limit handling | `node use-cases/batch_verify.mjs` |

### 🔔 Webhooks

| Script | Description | Run |
|--------|-------------|-----|
| [webhook_receiver.mjs](webhooks/webhook_receiver.mjs) | Express server with HMAC-SHA256 signature verification | `node webhooks/webhook_receiver.mjs` |

### 🤖 MCP

| Script | Description | Run |
|--------|-------------|-----|
| [mcp_test.mjs](mcp/mcp_test.mjs) | Test MCP connectivity via remote HTTP endpoint | `node mcp/mcp_test.mjs` |

---

## API Endpoints Used

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/extract` | POST | Extract claims without verifying (cheaper) |
| `/v1/verify` | POST | Extract + verify claims against web or private references |

Both endpoints accept either `text` (raw string) or `document` (URL) as input.

---

## Response Format

Each verified claim returns:

```json
{
  "claim": "The Eiffel Tower is in Berlin.",
  "verdict": false,
  "confidence_score": 1.0,
  "explanation": "The Eiffel Tower is located in Paris, France, not Berlin.",
  "source_urls": ["https://en.wikipedia.org/wiki/Eiffel_Tower"]
}
```

| Verdict | Meaning |
|---------|---------|
| `true`  | ✅ Supported by evidence |
| `false` | ❌ Contradicted by evidence |
| `null`  | ❓ Insufficient evidence |

---

## Need Help?

- **Full docs:** [veritier.ai/docs](https://veritier.ai/docs)
- **MCP integration (JS):** See the [`mcp/`](mcp/) subfolder
- **MCP stdio proxy (Python):** See [`python/mcp/`](../python/mcp/) for the local proxy
- **Python examples:** See the [`python/`](../python/) folder
