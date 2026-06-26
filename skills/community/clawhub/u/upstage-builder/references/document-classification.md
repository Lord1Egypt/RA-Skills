<!-- Source: https://console.upstage.ai/api/docs/for-agents/raw -->
# Document Classification API

## 5. Document Classification API

Classify documents into user-defined categories. This API uses OpenAI SDK compatible interface.

### Endpoint

```
POST https://api.upstage.ai/v1/document-classification
```

**Note:** Use OpenAI SDK with `base_url="https://api.upstage.ai/v1/document-classification"`

### Request Body (JSON)

| Parameter         | Type    | Required | Description                                                                                                                                                                                             |
| ----------------- | ------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `model`           | string  | Yes      | Use `document-classify`                                                                                                                                                                                 |
| `messages`        | array   | Yes      | Array with exactly one user message containing one `image_url` content. Only `role: "user"` is allowed.                                                                                                 |
| `response_format` | object  | Yes      | Class definitions with `json_schema`                                                                                                                                                                    |
| `split`           | boolean | No       | Split multi-document files into separate items in `choices`. Default: false                                                                                                                             |
| `split_criteria`  | array   | No       | Additional criteria for splitting. Array of objects with `criterion` (string) and `description` (string). Example: `[{"criterion": "card_id", "description": "The id that indicates each unit card."}]` |

### Limitations

- **Max pages:** 100 pages per file
- **Max file size:** 50MB
- **Max pixels per page:** 200,000,000 pixels (for non-image files, pixels are calculated after converting to images at 150 DPI)
- **Max classes:** 1,000 class definitions
- **Min classes:** 1 class required
- **Duplicate handling:** Classes with duplicate `const` names are ignored

### Available Models

| Model Alias                 | Description                                  |
| --------------------------- | -------------------------------------------- |
| `document-classify`         | Production model for document classification |
| `document-classify-nightly` | Experimental nightly (not for production)    |

### Example Request (curl)

```bash
curl -X POST https://api.upstage.ai/v1/document-classification \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "document-classify",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "image_url",
            "image_url": {
              "url": "https://example.com/document.jpg"
            }
          }
        ]
      }
    ],
    "response_format": {
      "type": "json_schema",
      "json_schema": {
        "name": "document-classify",
        "schema": {
          "type": "string",
          "oneOf": [
            {"const": "invoice", "description": "Commercial invoice with itemized charges"},
            {"const": "receipt", "description": "Purchase receipt with transaction details"},
            {"const": "contract", "description": "Legal agreement or contract"},
            {"const": "others", "description": "Other document types"}
          ]
        }
      }
    }
  }'
```

### Python Example (OpenAI SDK - Recommended)

```python
import base64
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_API_KEY",
    base_url="https://api.upstage.ai/v1/document-classification"
)

def encode_img_to_base64(img_path):
    with open(img_path, 'rb') as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

filepath = "./document.png"
base64_data = encode_img_to_base64(filepath)

response = client.chat.completions.create(
    model="document-classify",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:application/octet-stream;base64,{base64_data}"}
                }
            ]
        }
    ],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "document-classify",
            "schema": {
                "type": "string",
                "oneOf": [
                    {"const": "invoice", "description": "Commercial invoice with itemized charges"},
                    {"const": "receipt", "description": "Purchase receipt with transaction details"},
                    {"const": "contract", "description": "Legal agreement or contract"},
                    {"const": "others", "description": "Other document types"}
                ]
            }
        }
    }
)
classification = response.choices[0].message.content
```

### Python Example (Document Split)

When processing a file containing multiple documents of different types (e.g., a PDF with an invoice, ID cards, and a receipt):

```python
# Document Split: Separate multiple documents in a single file
response = client.chat.completions.create(
    model="document-classify",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:application/octet-stream;base64,{base64_data}"}
                }
            ]
        }
    ],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "document-classify",
            "schema": {
                "type": "string",
                "oneOf": [
                    {"const": "invoice", "description": "Commercial invoice"},
                    {"const": "id_card", "description": "ID card or identification document"},
                    {"const": "receipt", "description": "Purchase receipt"},
                    {"const": "others", "description": "Other document types"}
                ]
            }
        }
    },
    extra_body={
        "split": True,
        "split_criteria": [
            {"criterion": "document_id", "description": "Unique identifier for each document"}
        ]
    }
)

# Process each split document group
for choice in response.choices:
    doc_type = choice.message.content
    if choice.message.tool_calls:
        args = choice.message.tool_calls[0].function.arguments
        if isinstance(args, str):
            import json
            args = json.loads(args)
        pages = args.get("pages", [])
        print(f"Document type: {doc_type}, Pages: {pages}")
```

### Example Response

```json
{
  "id": "iex-AQZoWf2p5j6TO-AE",
  "object": "chat.completion",
  "model": "document-classify-260304",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "invoice"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 951,
    "completion_tokens": 2,
    "total_tokens": 953
  }
}
```

### Example Response (with split=true)

When `split=true`, multiple document groups are returned as separate items in the `choices` array. Each choice includes `pages` and optional `split_criteria_info` in the `tool_calls`:

```json
{
  "id": "chatcmpl-...",
  "object": "chat.completion",
  "model": "document-classify-260304",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "invoice",
        "tool_calls": [
          {
            "id": "call_...",
            "type": "function",
            "function": {
              "name": "additional_values",
              "arguments": {
                "document_type": {"_value": "invoice", "confidence_score": 0.99},
                "pages": [1, 2],
                "split_criteria_info": {"document_id": "INV-001"}
              }
            }
          }
        ]
      },
      "finish_reason": "stop"
    },
    {
      "index": 1,
      "message": {
        "role": "assistant",
        "content": "receipt",
        "tool_calls": [
          {
            "id": "call_...",
            "type": "function",
            "function": {
              "name": "additional_values",
              "arguments": {
                "document_type": {"_value": "receipt", "confidence_score": 0.95},
                "pages": [3],
                "split_criteria_info": {"document_id": "REC-001"}
              }
            }
          }
        ]
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 200,
    "completion_tokens": 150,
    "total_tokens": 350
  }
}
```

### Response Processing

```python
# Extract classification result
classification = response.choices[0].message.content  # "invoice"
```

### Getting Confidence Score

The response includes confidence scores via a `tool_calls` function named `additional_values`:

```python
# Get confidence score from tool_calls (function name: additional_values)
if response.choices[0].message.tool_calls:
    tool_call = response.choices[0].message.tool_calls[0]
    # tool_call.function.name == "additional_values"
    # arguments may be a JSON string or dict depending on SDK version
    args = tool_call.function.arguments
    if isinstance(args, str):
        import json
        args = json.loads(args)

    # Structure: {"document_type": {"_value": "invoice", "confidence_score": 1.0}, "pages": [...], "split_criteria_info": {...}}
    confidence = args["document_type"]["confidence_score"]

    # When split=true, also includes:
    # - pages: list of page numbers for this document group
    # - split_criteria_info: values for each split criterion (if split_criteria was provided)
```

### Class Definition Best Practices

Follow these recommendations for better classification accuracy:

| Guideline                        | Description                                                                        |
| -------------------------------- | ---------------------------------------------------------------------------------- |
| **Clear label names**            | Use concrete, non-overlapping names (e.g., `invoice`, `receipt`, `contract`)       |
| **Differentiating descriptions** | State key criteria in 1-2 sentences and add decision rules for borderline cases    |
| **Use examples (optional)**      | Brief include/exclude examples help with ambiguous cases                           |
| **Manage label count**           | Too many labels can confuse the model. Start with core labels and expand gradually |
| **Consistent format**            | Keep label casing and separators (lowercase, hyphen/underscore) consistent         |

**Class Design Restrictions:**

- Maximum 1,000 class definitions
- Minimum 1 class required
- Classes with duplicate `const` names are ignored

---

