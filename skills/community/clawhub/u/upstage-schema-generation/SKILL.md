---
name: upstage-schema-generation
description: Generate a JSON schema for structured document information extraction. Use this skill whenever the user asks to generate or create a schema for a document — including phrases like "스키마 생성해줘", "이 문서에서 뭘 추출할지 스키마 짜줘", "generate a schema for this document", or any request to define extraction fields for a document. Also trigger when the user provides file paths or a folder path containing documents and wants a schema generated.
model: claude-opus-4-6
---

# Upstage Schema Generation

Analyze sample documents and automatically generate a JSON schema for use with Information Extraction.

## Prerequisites

- **API Key**: `UPSTAGE_API_KEY` environment variable is required. Get your key at [console.upstage.ai](https://console.upstage.ai).

## Two Modes

| Mode | When to use | Latency |
|------|-------------|---------|
| **API mode** | Default. Fast schema generation via Upstage endpoint. | Low |
| **VLM mode** (`claude-opus-4-6`) | When the user wants careful, hand-tuned schemas with precise extraction rules and table-aware design. | High |

## API Mode (Default)

**Endpoint**: `POST https://api.upstage.ai/v1/information-extraction/schema-generation`

```python
import os
import json
import requests
import base64

api_key = os.environ["UPSTAGE_API_KEY"]

with open("document.pdf", "rb") as f:
    b64 = base64.b64encode(f.read()).decode()

response = requests.post(
    "https://api.upstage.ai/v1/information-extraction/schema-generation",
    headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    json={
        "model": "information-extract",
        "messages": [
            {"role": "system", "content": "Generate schema for this invoice document."},
            {"role": "user", "content": [
                {"type": "image_url", "image_url": {"url": f"data:application/pdf;base64,{b64}"}}
            ]}
        ]
    }
)

schema = json.loads(response.json()["choices"][0]["message"]["content"])
print(json.dumps(schema, indent=2))
```

> **Note**: The API model is `information-extract` (not `schema-generate`). The `system` message can guide the schema focus (e.g., "Generate schema about bank_name."). Up to 3 sample images can be provided in the user message.

## VLM Mode

For carefully designed schemas with precise extraction rules, follow the 4-step VLM workflow.

- **Workflow**: Read `references/vlm-workflow.md` (parameter gathering, document reading, property list, JSON schema conversion)
- **Design rules**: Read `references/schema-design.md` (key naming, descriptions, table handling, blank/duplicate handling)

## Output Files

- **Default**: write generated schema to `<system-temp>/<input-stem>.schema.json` (e.g., `/tmp/invoice.schema.json`). For inline input with no source file, use `<system-temp>/<timestamp>-schema.json`.
- **Override**: if the user specifies an output path, use it.
- **Always print the resolved absolute path** in your response so the user can locate the file.

## Related Skills

- Generated schema → use directly as `response_format` in `upstage-information-extraction`
- If documents need pre-sorting → classify with `upstage-document-classification` first, then generate per-category schemas
- For multi-API pipelines → see `upstage-builder`
