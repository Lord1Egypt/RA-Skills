# Veritier - Python Fact-Checking Examples

Verify any claim against live web evidence with a single API call. These Python examples show you how to integrate the **Veritier AI Fact-Checking API** into your applications - from basic extraction to advanced hallucination auditing.

📦 **API Docs:** [veritier.ai/docs](https://veritier.ai/docs) · 🔑 **Get your free key:** [veritier.ai/register](https://veritier.ai/register)

---

## Prerequisites

- **Python 3.10+**
- A free Veritier API key ([register here](https://veritier.ai/register))

```bash
# Install dependencies
pip install -r requirements.txt

# Set up your API key
cp ../.env.example .env
# Edit .env and replace vt_your_api_key_here with your real key
```

---

## Examples

### 🚀 Quickstart

| Script | Description | Run |
|--------|-------------|-----|
| [extract_text.py](quickstart/extract_text.py) | Extract every falsifiable claim from text (no verification) | `python quickstart/extract_text.py` |
| [verify_text.py](quickstart/verify_text.py) | Fact-check claims against live web evidence | `python quickstart/verify_text.py` |

### 📋 Use Cases

| Script | Description | Run |
|--------|-------------|-----|
| [verify_article_url.py](use-cases/verify_article_url.py) | Verify all claims from a web page URL | `python use-cases/verify_article_url.py <URL>` |
| [hallucination_audit.py](use-cases/hallucination_audit.py) | Catch LLM hallucinations before they reach users | `python use-cases/hallucination_audit.py` |
| [disinformation_shield.py](use-cases/disinformation_shield.py) | Screen user content for false claims (Truth Firewall) | `python use-cases/disinformation_shield.py` |
| [private_references.py](use-cases/private_references.py) | Verify against your own documents (no web search) | `python use-cases/private_references.py` |
| [batch_verify.py](use-cases/batch_verify.py) | Batch-process texts with rate-limit handling | `python use-cases/batch_verify.py` |

### 🔔 Webhooks

| Script | Description | Run |
|--------|-------------|-----|
| [webhook_receiver.py](webhooks/webhook_receiver.py) | Flask server with HMAC-SHA256 signature verification | `python webhooks/webhook_receiver.py` |

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

```
Claim: '<extracted claim>'
  Verdict: true | false | null
  Confidence: 0.0–1.0
  Explanation: <human-readable rationale>
  Sources: <comma-separated evidence URLs>
```

| Verdict | Meaning |
|---------|---------|
| `true`  | ✅ Supported by evidence |
| `false` | ❌ Contradicted by evidence |
| `null`  | ❓ Insufficient evidence |

---

## Need Help?

- **Full docs:** [veritier.ai/docs](https://veritier.ai/docs)
- **MCP integration:** See the [`mcp/`](mcp/) subfolder
- **JavaScript examples:** See the [`javascript/`](../javascript/) folder
