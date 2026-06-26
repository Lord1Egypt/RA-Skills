# Document Split — Multi-Document Separation

When a single PDF contains multiple document types, use `split=true` to automatically separate them into groups. Each group is returned as a separate `choices` entry with its own `pages` range and classification result.

## Basic Split

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["UPSTAGE_API_KEY"],
    base_url="https://api.upstage.ai/v1/document-classification"
)

response = client.chat.completions.create(
    model="document-classify",
    messages=[{
        "role": "user",
        "content": [{"type": "image_url", "image_url": {"url": "https://example.com/mixed.pdf"}}]
    }],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "document-classify",
            "schema": {
                "type": "string",
                "oneOf": [
                    {"const": "invoice", "description": "Commercial invoice"},
                    {"const": "receipt", "description": "Payment receipt"},
                    {"const": "contract", "description": "Legal contract"}
                ]
            }
        }
    },
    extra_body={"split": True}
)

for choice in response.choices:
    args = choice.message.tool_calls[0].function.arguments
    print(f"Type: {args['document_type']['_value']}, Pages: {args['pages']}")
```

## Split with Additional Criteria

Provide additional `split_criteria` to tell the API how to identify boundaries beyond document type alone (e.g., unique invoice numbers).

```python
response = client.chat.completions.create(
    model="document-classify",
    messages=[{
        "role": "user",
        "content": [{"type": "image_url", "image_url": {"url": "https://example.com/mixed.pdf"}}]
    }],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "document-classify",
            "schema": {
                "type": "string",
                "oneOf": [
                    {"const": "invoice", "description": "Commercial invoice"},
                    {"const": "receipt", "description": "Payment receipt"},
                    {"const": "contract", "description": "Legal contract"}
                ]
            }
        }
    },
    extra_body={
        "split": True,
        "split_criteria": [
            {"criterion": "document_id", "description": "Unique document identifier like invoice number"}
        ]
    }
)
```

Split results are returned as separate items in the `choices` array — one per document group, each with a `pages` field indicating the page range.

---

## curl Example (Single-Document Classification)

```bash
curl -X POST "https://api.upstage.ai/v1/document-classification" \
  -H "Authorization: Bearer $UPSTAGE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "document-classify",
    "messages": [{"role": "user", "content": [{"type": "image_url", "image_url": {"url": "FILE_URL"}}]}],
    "response_format": {
      "type": "json_schema",
      "json_schema": {
        "name": "document-classify",
        "schema": {
          "type": "string",
          "oneOf": [
            {"const": "invoice", "description": "Commercial invoice"},
            {"const": "receipt", "description": "Payment receipt"},
            {"const": "contract", "description": "Legal contract"}
          ]
        }
      }
    }
  }'
```
