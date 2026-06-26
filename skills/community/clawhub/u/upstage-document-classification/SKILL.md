---
name: upstage-document-classification
description: "Classify documents into user-defined categories using Upstage Document Classification API. Also supports document splitting for multi-document PDFs. Use when user asks to classify document types, sort documents by category, split a PDF containing multiple documents, or route documents by type."
homepage: https://console.upstage.ai/api/document-classification
---

# Upstage Document Classification

Classify documents into user-defined categories with confidence scores. Also supports Document Split for separating multi-document PDFs into individual documents.

## Quick Start

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
        "content": [{"type": "image_url", "image_url": {"url": "https://example.com/document.pdf"}}]
    }],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "document-classify",
            "schema": {
                "type": "string",
                "oneOf": [
                    {"const": "invoice", "description": "Commercial invoice with itemized charges"},
                    {"const": "receipt", "description": "Payment receipt"},
                    {"const": "contract", "description": "Legal contract or agreement"},
                    {"const": "resume", "description": "Personal resume or CV"}
                ]
            }
        }
    }
)
print(response.choices[0].message.content)
```

**API Key**: Always use `os.environ["UPSTAGE_API_KEY"]`. Get your key at [console.upstage.ai](https://console.upstage.ai).

## Endpoint

```
POST https://api.upstage.ai/v1/document-classification
```

OpenAI SDK compatible — set `base_url` to `https://api.upstage.ai/v1/document-classification`.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `model` | string | Yes | `document-classify` or `document-classify-nightly` |
| `messages` | array | Yes | Single user message with `image_url` |
| `response_format` | object | Yes | JSON Schema defining classification categories |
| `split` | boolean | No | Enable multi-document splitting (default: false) |
| `split_criteria` | array | No | Additional splitting criteria (used with `split=true`) |

## Schema Definition (Important)

Categories are defined using `oneOf` with `const` values. The root schema type **must be `"string"`**, not `"object"`.

```json
{
  "type": "json_schema",
  "json_schema": {
    "name": "document-classify",
    "schema": {
      "type": "string",
      "oneOf": [
        {"const": "invoice", "description": "Commercial invoice"},
        {"const": "receipt", "description": "Payment receipt"},
        {"const": "other", "description": "Other document type"}
      ]
    }
  }
}
```

> **Important**: Using `enum` or `object`-based schemas will return a 400 error. The Classification API requires `oneOf` with `const`/`description` pairs.

## Response Structure

```json
{
  "choices": [{
    "message": {
      "content": "invoice",
      "tool_calls": [{
        "function": {
          "arguments": {
            "document_type": {"_value": "invoice", "confidence_score": 0.99},
            "pages": [1, 2]
          }
        }
      }]
    }
  }]
}
```

- `content`: classified category name
- `tool_calls.function.arguments.document_type._value`: classified value
- `tool_calls.function.arguments.document_type.confidence_score`: 0.0–1.0
- `tool_calls.function.arguments.pages`: page range (most useful with split mode)

## Document Split (Multi-Document PDFs)

For PDFs containing multiple document types, set `extra_body={"split": True}` to separate them into groups. Each group is returned as a separate `choices` entry. See `references/document-split.md` for the full split workflow with optional `split_criteria`.

## Output Files

- **Default (classify only)**: `<system-temp>/<input-stem>.classified.json` (e.g., `/tmp/contract.classified.json`).
- **Default (split mode)**: directory `<system-temp>/<input-stem>.split/` with one file per detected document (e.g., `page-001.invoice.pdf`).
- **Override**: if the user specifies an output path, use it.
- **Always print the resolved absolute path(s)** in your response so the user can locate the file(s).

## Tips

- Include `"other"` in your categories to handle unclassified documents.
- `split` is useful as the first step in a document processing pipeline for scanned mixed-document files.
- A common pattern: classify first → apply category-specific schemas with `upstage-information-extraction`.
- Use `confidence_score` to flag low-confidence documents for manual review.

## Detailed References

| File | Content |
|------|---------|
| `references/document-split.md` | Document split (basic + with criteria), curl example |
