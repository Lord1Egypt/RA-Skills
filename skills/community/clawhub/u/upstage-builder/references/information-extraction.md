<!-- Source: https://console.upstage.ai/api/docs/for-agents/raw -->
# Information Extraction API

## 6. Information Extraction API

Extract structured data from documents using custom schemas. This API uses OpenAI SDK compatible interface.

### Endpoint (Synchronous)

```
POST https://api.upstage.ai/v1/information-extraction
```

**Note:** Use OpenAI SDK with `base_url="https://api.upstage.ai/v1/information-extraction"`

### Endpoint (Asynchronous - for large documents)

```
POST https://api.upstage.ai/v1/information-extraction/async
GET https://api.upstage.ai/v1/information-extraction/jobs/{job_id}
GET https://api.upstage.ai/v1/information-extraction/jobs
```

### Limitations

| API Type     | Max Pages | Max Properties | Max Schema Chars |
| ------------ | --------- | -------------- | ---------------- |
| Synchronous  | 100       | 100            | 15,000           |
| Asynchronous | 1,000     | 5,000          | 120,000          |

### Available Models

| Model Alias                   | Description                                 |
| ----------------------------- | ------------------------------------------- |
| `information-extract`         | Production model for information extraction |
| `information-extract-nightly` | Experimental nightly (not for production)   |

### Schema Design Restrictions (IMPORTANT)

When defining extraction schemas, these restrictions apply:

- Total string length of all property names and definition names **cannot exceed 10,000 characters**
- **First-level properties must be `string`, `integer`, `number`, or `array`** (object type NOT permitted at first level)
- **Nested arrays not allowed** (array cannot contain items of arrays)
- Root object must be `object` type

**Valid Schema Example:**

```json
{
  "type": "object",
  "properties": {
    "invoice_number": {"type": "string"},
    "items": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": {"type": "string"},
          "price": {"type": "number"}
        }
      }
    }
  }
}
```

**Invalid Schema Examples:**

```json
// ERROR: Object at first level
{
  "type": "object",
  "properties": {
    "vendor": {
      "type": "object",  // NOT ALLOWED at first level
      "properties": { ... }
    }
  }
}

// ERROR: Nested arrays
{
  "type": "object",
  "properties": {
    "matrix": {
      "type": "array",
      "items": {
        "type": "array",  // NOT ALLOWED - nested array
        "items": { ... }
      }
    }
  }
}
```

### Request Body (JSON)

| Parameter              | Type    | Required | Description                                                                                                               |
| ---------------------- | ------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| `model`                | string  | Yes      | Use `information-extract`                                                                                                 |
| `messages`             | array   | Yes      | Array with single user message containing image_url                                                                       |
| `response_format`      | object  | Yes      | Extraction schema with `json_schema`                                                                                      |
| `mode`                 | string  | No       | (Beta) `standard` or `enhanced`. Default: standard                                                                        |
| `location`             | boolean | No       | (Beta) Return coordinates. Default: false                                                                                 |
| `location_granularity` | string  | No       | (Beta) Coordinate detail level. See below. Default: element                                                               |
| `confidence`           | boolean | No       | (Beta) Return confidence scores (`high` or `low`). High recall (>95%), ~50% precision for low flags. Default: false       |
| `split`                | boolean | No       | (Beta) Split multi-document files. Schema-driven, page-level minimum. Results in separate `choices` items. Default: false |
| `chunking`             | object  | No       | (Beta) For large docs (30+ pages or 50+ row tables): `{"pages_per_chunk": 5}`. Default chunk size: 5 pages                |

### Example Request (curl)

```bash
curl -X POST https://api.upstage.ai/v1/information-extraction \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "information-extract",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "image_url",
            "image_url": {
              "url": "https://example.com/invoice.jpg"
            }
          }
        ]
      }
    ],
    "response_format": {
      "type": "json_schema",
      "json_schema": {
        "name": "invoice_schema",
        "schema": {
          "type": "object",
          "properties": {
            "invoice_number": {
              "type": "string",
              "description": "The invoice number"
            },
            "total_amount": {
              "type": "string",
              "description": "Total amount with currency"
            },
            "vendor_name": {
              "type": "string",
              "description": "Name of the vendor"
            }
          },
          "required": ["invoice_number", "total_amount"]
        }
      }
    }
  }'
```

### Example Response

```json
{
  "id": "iex-AQZoWf2p5j6TO-AE",
  "object": "chat.completion",
  "model": "information-extract-260304",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "{\"invoice_number\":\"INV-2024-001\",\"total_amount\":\"$1,234.56\",\"vendor_name\":\"Acme Corp\"}"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 951,
    "completion_tokens": 32,
    "total_tokens": 983
  }
}
```

### Python Example (OpenAI SDK - Recommended)

```python
import base64
import json
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_API_KEY",
    base_url="https://api.upstage.ai/v1/information-extraction"
)

def encode_img_to_base64(img_path):
    with open(img_path, 'rb') as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

filepath = "./bank_statement.png"
base64_data = encode_img_to_base64(filepath)

extraction_response = client.chat.completions.create(
    model="information-extract",
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
            "name": "document_schema",
            "schema": {
                "type": "object",
                "properties": {
                    "bank_name": {
                        "type": "string",
                        "description": "The name of bank in bank statement"
                    },
                    "total_amount": {
                        "type": "string",
                        "description": "Total amount with currency"
                    }
                }
            }
        }
    }
)

result = json.loads(extraction_response.choices[0].message.content)
print(result)
```

### Parameter Tips

| Use Case                                            | Recommended Settings                                |
| --------------------------------------------------- | --------------------------------------------------- |
| Simple invoices/receipts                            | `mode: "standard"`                                  |
| Complex tables, handwritten text, low-quality scans | `mode: "enhanced"` (additional cost)                |
| Need bounding boxes for highlighting                | `location: true`, `location_granularity: "element"` |
| Word-level highlighting                             | `location: true`, `location_granularity: "word"`    |
| Quality assurance / human review                    | `confidence: true` (flags uncertain extractions)    |
| Documents with 30+ pages or 50+ row tables          | `chunking: {"pages_per_chunk": 5}`                  |
| PDF with multiple invoices in one file              | `split: true`                                       |

### Location Granularity Options

When `location: true`, use `location_granularity` to control coordinate precision:

| Value               | Description                 | Response Contains                         |
| ------------------- | --------------------------- | ----------------------------------------- |
| `element` (default) | Element-level bounding box  | `coordinates` array                       |
| `word`              | Word-level coordinates      | `word_coordinates` array                  |
| `all`               | Both element and word level | Both `coordinates` and `word_coordinates` |

**Important:** When `location: true` or `confidence: true`, the detailed results are returned in `tool_calls` with function name `additional_values`, not in the main `content` field.

**Parsing Location/Confidence Results:**

```python
import json

# The main content still contains extracted values
result = json.loads(response.choices[0].message.content)

# Location/confidence details are in tool_calls
if response.choices[0].message.tool_calls:
    additional = json.loads(response.choices[0].message.tool_calls[0].function.arguments)
    # additional contains coordinates, page numbers, and/or confidence levels
    print(additional)
```

**Location Response Example (from tool_calls):**

```json
{
  "invoice_number": {
    "_value": "INV-2024-001",
    "page": 1,
    "coordinates": [
      {"x": 0.0745, "y": 0.1005},
      {"x": 0.2096, "y": 0.1005},
      {"x": 0.2096, "y": 0.1591},
      {"x": 0.0745, "y": 0.1591}
    ]
  }
}
```

**Confidence Response Example (from tool_calls):**

```json
{
  "invoice_number": {
    "_value": "INV-2024-001",
    "confidence": "high"
  },
  "total_amount": {
    "_value": "$1,234.56",
    "confidence": "low"
  }
}
```

### Async API Example

```python
import requests
import time
import json

api_key = "YOUR_API_KEY"
base_url = "https://api.upstage.ai/v1/information-extraction"

# Step 1: Create async job
schema = {
    "type": "object",
    "properties": {
        "invoice_number": {"type": "string", "description": "Invoice number"},
        "total": {"type": "string", "description": "Total amount"}
    }
}

with open("document1.pdf", "rb") as f1, open("document2.pdf", "rb") as f2:
    response = requests.post(
        f"{base_url}/async",
        headers={"Authorization": f"Bearer {api_key}"},
        files=[
            ("documents", f1),
            ("documents", f2)
        ],
        data={
            "model": "information-extract",
            "schema": json.dumps(schema)
        }
    )
job_id = response.json()["job_id"]

# Step 2: Poll for results
while True:
    job = requests.get(
        f"{base_url}/jobs/{job_id}",
        headers={"Authorization": f"Bearer {api_key}"}
    ).json()

    if job["status"] in ["COMPLETED", "PARTIALLY_COMPLETED"]:
        # Get results with extraction data
        results = requests.get(
            f"{base_url}/jobs/{job_id}?with_result=true",
            headers={"Authorization": f"Bearer {api_key}"}
        ).json()

        # Process each document's result
        for batch in results["batches"]:
            if batch["status"] == "COMPLETED":
                content = batch["result"]["choices"][0]["message"]["content"]
                extracted_data = json.loads(content)
                print(f"{batch['file_name']}: {extracted_data}")
        break
    elif job["status"] == "FAILED":
        raise Exception("Job failed")

    time.sleep(5)
```

### IE Async Job Status Response

```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "COMPLETED",
  "model": "information-extract-260304",
  "total_documents": 2,
  "completed_documents": 2,
  "created_at": "2024-07-01T14:47:01Z",
  "started_at": "2024-07-01T14:47:02Z",
  "completed_at": "2024-07-01T14:47:43Z",
  "batches": [
    {
      "id": 1,
      "file_name": "invoice1.pdf",
      "status": "COMPLETED",
      "failure_message": "",
      "result": {
        "id": "iex-123",
        "model": "information-extract-260304",
        "choices": [
          {
            "message": {
              "content": "{\"invoice_number\":\"INV-001\",\"total\":\"$500\"}"
            }
          }
        ],
        "usage": {
          "prompt_tokens": 951,
          "completion_tokens": 32,
          "total_tokens": 983
        }
      }
    },
    {
      "id": 2,
      "file_name": "invoice2.pdf",
      "status": "COMPLETED",
      "failure_message": "",
      "result": {
        "choices": [
          {
            "message": {
              "content": "{\"invoice_number\":\"INV-002\",\"total\":\"$750\"}"
            }
          }
        ]
      }
    }
  ]
}
```

**Status Values:** `CREATED` → `IN_PROGRESS` → `COMPLETED` | `PARTIALLY_COMPLETED` | `FAILED` | `CANCELED`

**Batch Status Values:** `CREATED` → `IN_PROGRESS` → `COMPLETED` | `FAILED`

### IE Async API Constraints

- **Supported file formats:** PDF, JPEG, PNG, BMP, TIFF, HEIC, DOCX, PPTX, XLSX (Note: HWP/HWPX not supported in async)
- **Max documents per job:** 20 documents
- **Result storage:** 30 days after completion
- **Job cancellation:** Not supported via API
- **Schema requirement:** All documents in a single job must use the same schema
- **Polling interval:** Recommended 5-10 seconds between status checks

---


---

## 7. Schema Generation API

Auto-generate extraction schemas from sample documents. Useful when you don't know what fields to extract.

### Endpoint

```
POST https://api.upstage.ai/v1/information-extraction
```

**Note:** Use OpenAI SDK with `base_url="https://api.upstage.ai/v1/information-extraction"`

### Request Body (JSON)

| Parameter  | Type   | Required | Description                                                         |
| ---------- | ------ | -------- | ------------------------------------------------------------------- |
| `model`    | string | Yes      | Use `schema-generate`                                               |
| `messages` | array  | Yes      | System message (optional) + User message with up to 3 sample images |

### When to Use

- You have sample documents but don't know the field structure
- You want AI to suggest a schema based on document content
- Bootstrapping a new extraction pipeline

### Using System Message

You can guide schema generation with a system message describing your extraction intent:

```python
messages=[
    {"role": "system", "content": "Generate a schema for extracting invoice information including line items, totals, and vendor details."},
    {"role": "user", "content": [...]}  # Sample document images
]
```

### Python Example (OpenAI SDK)

```python
import base64
import json
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_API_KEY",
    base_url="https://api.upstage.ai/v1/information-extraction"
)

def encode_img_to_base64(img_path):
    with open(img_path, 'rb') as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

# Encode sample document
base64_data = encode_img_to_base64("./sample_invoice.png")

response = client.chat.completions.create(
    model="schema-generate",
    messages=[
        {"role": "system", "content": "Generate a schema for extracting invoice information."},
        {
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": f"data:application/octet-stream;base64,{base64_data}"}}
            ]
        }
    ]
)

# Parse the generated schema
schema_str = response.choices[0].message.content
schema = json.loads(schema_str)
print(schema)
```

### Example Response

```json
{
  "id": "e1a90437-df41-45cd-acc6-a7bacbdd2a86",
  "object": "chat.completion",
  "model": "schema-generate",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "{\"type\": \"json_schema\", \"json_schema\": {\"name\": \"document_schema\", \"schema\": {\"type\": \"object\", \"properties\": {\"invoice_number\": {\"type\": \"string\"}, \"total_amount\": {\"type\": \"number\"}, \"vendor_name\": {\"type\": \"string\"}}}}}"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 1230,
    "completion_tokens": 591,
    "total_tokens": 1821
  }
}
```

### Using Generated Schema for Extraction

```python
# Use the generated schema for actual extraction
extraction_response = client.chat.completions.create(
    model="information-extract",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": f"data:application/octet-stream;base64,{base64_data}"}}
            ]
        }
    ],
    response_format=schema  # Use the generated schema
)

result = json.loads(extraction_response.choices[0].message.content)
print(result)
```

---


---

## 8. Prebuilt Information Extraction API

Extract predefined key fields from specific document types with high accuracy. Unlike universal information extraction which requires a custom schema, prebuilt extractors are fine-tuned for specific document formats (receipts, logistics documents) and achieve higher accuracy (90-95%) out of the box.

### Endpoint

```
POST https://api.upstage.ai/v1/information-extraction
```

### Available Models

| Model Alias                                      | Document Type                     | Description                                           |
| ------------------------------------------------ | --------------------------------- | ----------------------------------------------------- |
| `receipt-extraction`                             | Receipt                           | Extract store info, items, totals from paper receipts |
| `air-waybill-extraction`                         | Air Waybill (AWB)                 | Extract shipment details from air waybills            |
| `bill-of-lading-and-shipping-request-extraction` | Bill of Lading / Shipping Request | Extract logistics data from BL and SR documents       |
| `commercial-invoice-and-packing-list-extraction` | Commercial Invoice / Packing List | Extract trade data from commercial invoices and PLs   |
| `kr-export-declaration-certificate-extraction`   | Korean Export Declaration         | Extract fields from Korean export declaration forms   |

### Input Requirements

- **Supported formats:** JPEG, PNG, BMP, PDF, TIFF, HEIC, DOCX, PPTX, XLSX, HWP, HWPX
- **Maximum file size:** 50MB
- **Maximum pages per file:** 30 (pages beyond 30 are ignored)
- **Maximum pixels per page:** 100,000,000
- **Supported characters:** Alphanumeric, Hangul, Hanja (Hanzi/Kanji in beta)

### Request Body (multipart/form-data)

| Parameter  | Type   | Required | Description                                   |
| ---------- | ------ | -------- | --------------------------------------------- |
| `model`    | string | Yes      | Model alias (e.g., `receipt-extraction`)      |
| `document` | file   | Yes      | The document file to extract information from |

### Response Format

```json
{
  "mimeType": "multipart/form-data",
  "documentType": "receipt",
  "fields": [
    {
      "key": "date",
      "type": "date",
      "value": "2023-09-15",
      "confidence": 0.98,
      "id": 1,
      "refinedValue": "September 15, 2023"
    },
    {
      "key": "total",
      "type": "monetary_usd",
      "value": "150.00",
      "confidence": 0.95,
      "id": 2,
      "properties": [
        {
          "key": "subtotal",
          "value": "100.00",
          "confidence": 0.95
        }
      ]
    }
  ],
  "stored": true,
  "modelVersion": "receipt-extraction",
  "apiVersion": "1.1",
  "numBilledPages": 2,
  "metadata": {
    "pageSize": "A4",
    "totalPages": 2
  }
}
```

**Response Fields:**

| Field                 | Type    | Description                                               |
| --------------------- | ------- | --------------------------------------------------------- |
| `documentType`        | string  | Detected document type                                    |
| `fields`              | array   | Array of extracted field objects                          |
| `fields[].key`        | string  | Field name (e.g., `date`, `total`, `store.store_address`) |
| `fields[].type`       | string  | Field type (e.g., `date`, `content`, `monetary_usd`)      |
| `fields[].value`      | string  | Extracted value                                           |
| `fields[].confidence` | number  | Confidence score (0 to 1)                                 |
| `fields[].properties` | array   | Nested sub-fields (if applicable)                         |
| `numBilledPages`      | integer | Number of pages billed                                    |

### Code Examples

**curl:**

```bash
curl -X POST https://api.upstage.ai/v1/information-extraction \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -F "model=receipt-extraction" \
  -F "document=@receipt.png"
```

**Python:**

```python
import requests

url = "https://api.upstage.ai/v1/information-extraction"
headers = {"Authorization": "Bearer YOUR_API_KEY"}

files = {"document": open("receipt.png", "rb")}
data = {"model": "receipt-extraction"}
response = requests.post(url, headers=headers, files=files, data=data)

print(response.json())
```

### Filtering Specific Fields

The API returns all extracted fields. Filter the fields you need from the response:

```python
response = requests.post(url, headers=headers, files=files, data=data)
data = response.json()

# Extract specific field values
addresses = [
    field['value'] for field in data.get('fields', [])
    if field['key'] == 'store.store_address' and field['type'] == 'content'
]
print(addresses)
```

---

