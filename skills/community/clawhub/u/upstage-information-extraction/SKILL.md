---
name: upstage-information-extraction
description: "Extract specific named fields from documents using Upstage Information Extraction API with custom JSON schemas (sync/async) or prebuilt models for receipts, invoices, waybills, bills of lading. Use when user wants named values like '청구액', '주문번호', invoice total, supplier name — '영수증에서 금액이랑 날짜 뽑아줘', '인보이스 필드 추출해줘', 'extract invoice number and amount', 'pull structured data from receipts'. DO NOT use for plain text extraction without a schema — use upstage-ocr. DO NOT use for full document layout/markdown conversion — use upstage-document-parse. For schema design help, pair with upstage-schema-generation."
homepage: https://console.upstage.ai/api/information-extraction
---

# Upstage Information Extraction

Extract structured data from documents using custom JSON schemas. Also supports prebuilt models for receipts, invoices, and trade documents.

## Quick Start

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["UPSTAGE_API_KEY"],
    base_url="https://api.upstage.ai/v1/information-extraction"
)

response = client.chat.completions.create(
    model="information-extract",
    messages=[{
        "role": "user",
        "content": [{"type": "image_url", "image_url": {"url": "https://example.com/invoice.pdf"}}]
    }],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "invoice_schema",
            "schema": {
                "type": "object",
                "properties": {
                    "invoice_number": {"type": "string", "description": "Invoice ID"},
                    "total_amount": {"type": "string", "description": "Total amount with currency"},
                    "date": {"type": "string", "description": "Invoice date in YYYY-MM-DD"}
                }
            }
        }
    }
)
print(response.choices[0].message.content)
```

**API Key**: Always use `os.environ["UPSTAGE_API_KEY"]`. Get your key at [console.upstage.ai](https://console.upstage.ai).

---

## Endpoints

| Mode | Endpoint |
|------|----------|
| Sync | `POST https://api.upstage.ai/v1/information-extraction` |
| Async | `POST https://api.upstage.ai/v1/information-extraction/async` |
| Status | `GET https://api.upstage.ai/v1/information-extraction/jobs/{job_id}` |

- **OpenAI SDK compatible**: Set `base_url` to `https://api.upstage.ai/v1/information-extraction`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `model` | string | Yes | `information-extract` or `information-extract-nightly` |
| `messages` | array | Yes | Single user message with `image_url` |
| `response_format` | object | Yes | Extraction schema (JSON Schema format) |
| `mode` | string | No | `standard` (default) or `enhanced` |
| `location` | boolean | No | Return coordinates (default: false) |
| `confidence` | boolean | No | Return confidence scores (default: false) |
| `split` | boolean | No | Split multi-document files (default: false) |

## Limits

| Item | Sync | Async |
|------|------|-------|
| Max pages | 100 | 1,000 |
| Max properties | 100 | 5,000 |
| Max schema chars | 15,000 | 120,000 |

## Schema Rules

- Top-level properties: only `string`, `integer`, `number`, `array` allowed (no objects)
- No nested arrays
- Total character length of all property names must be under 10,000
- For automatic schema generation, use `upstage-schema-generation` skill

## Response Structure

```json
{
  "choices": [
    {
      "message": {
        "content": "{\"invoice_number\": \"INV-001\", \"total_amount\": \"$1,234.56\", \"date\": \"2026-01-15\"}"
      }
    }
  ],
  "usage": {"prompt_tokens": 500, "completion_tokens": 50}
}
```

`content` is a JSON string. Parse with `json.loads()`.

---

## Prebuilt Models

Ready-to-use models that require no schema definition.

| Model | Document Type |
|-------|--------------|
| `receipt-extraction` | Receipts |
| `air-waybill-extraction` | Air waybills |
| `bill-of-lading-and-shipping-request-extraction` | Bills of lading / shipping requests |
| `commercial-invoice-and-packing-list-extraction` | Commercial invoices / packing lists |
| `kr-export-declaration-certificate-extraction` | Korean export declaration certificates |

### Prebuilt Usage Example

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["UPSTAGE_API_KEY"],
    base_url="https://api.upstage.ai/v1/information-extraction"
)

response = client.chat.completions.create(
    model="receipt-extraction",
    messages=[{
        "role": "user",
        "content": [{"type": "image_url", "image_url": {"url": "https://example.com/receipt.jpg"}}]
    }]
)
print(response.choices[0].message.content)
```

Prebuilt models are called without `response_format`.

---

## Async Processing (Large Documents)

```python
import os
import time
import requests

api_key = os.environ["UPSTAGE_API_KEY"]
headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

# 1. Submit async job
response = requests.post(
    "https://api.upstage.ai/v1/information-extraction/async",
    headers=headers,
    json={
        "model": "information-extract",
        "messages": [{"role": "user", "content": [{"type": "image_url", "image_url": {"url": "FILE_URL"}}]}],
        "response_format": {"type": "json_schema", "json_schema": {"name": "schema", "schema": {...}}}
    }
)
job_id = response.json()["id"]

# 2. Poll for results
while True:
    status = requests.get(
        f"https://api.upstage.ai/v1/information-extraction/jobs/{job_id}",
        headers=headers
    ).json()
    if status["status"] == "completed":
        print(status["choices"][0]["message"]["content"])
        break
    time.sleep(5)
```

## Output Files

- **Default**: write extracted JSON to `<system-temp>/<input-stem>.extracted.json` (e.g., `/tmp/invoice.extracted.json`). Use `tempfile.gettempdir()` for cross-platform code.
- **Override**: if the user specifies an output path, use it.
- **Always print the resolved absolute path** in your response so the user can locate the file.

## Tips

- `enhanced` mode improves accuracy on complex tables/images but is slower.
- Set `confidence: true` to get per-field confidence scores for quality filtering.
- Schema design is critical for extraction quality. Use `upstage-schema-generation` skill for automatic generation.
- `split: true` is useful when a single file contains multiple documents.
