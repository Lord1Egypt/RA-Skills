<!-- Source: https://console.upstage.ai/api/docs/for-agents/raw -->
# Document Processing APIs

## Supported File Formats (Document APIs)

The following applies to Document OCR, Document Parse, Document Classification, and Information Extraction APIs:

- **Supported formats:** JPEG, PNG, BMP, PDF, TIFF, HEIC, DOCX, PPTX, XLSX, HWP, HWPX
- **Maximum file size:** 50MB
- **Maximum pixels per page:** 200,000,000

---


---

## 3. Document OCR API

Extract text from images and documents.

### Endpoint

```
POST https://api.upstage.ai/v1/document-digitization
```

### Request Body (multipart/form-data)

| Parameter  | Type   | Required | Description                                                                                        |
| ---------- | ------ | -------- | -------------------------------------------------------------------------------------------------- |
| `model`    | string | Yes      | Use `ocr`                                                                                          |
| `document` | file   | Yes      | Document file to process                                                                           |
| `schema`   | string | No       | Response format compatibility: `clova` (Clova OCR migration) or `google` (Google Vision migration) |

### Limitations

- **Max pages:** 100 pages per file
- **Max file size:** 50MB
- **Max pixels per page:** 200,000,000
- **Supported character sets:** Alphanumeric, Hangul, Hanja (full support). Katakana, Hiragana (partial). Hanzi, Kanji (beta)
- **Text size:** Optimized for text under 30% of page size. Larger text may cause errors.

### Example Request

```bash
curl -X POST https://api.upstage.ai/v1/document-digitization \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -F "model=ocr" \
  -F "document=@/path/to/document.pdf"
```

### Python Example

```python
import requests

with open("document.pdf", "rb") as f:
    response = requests.post(
        "https://api.upstage.ai/v1/document-digitization",
        headers={"Authorization": "Bearer YOUR_API_KEY"},
        files={"document": f},
        data={"model": "ocr"}
    )
result = response.json()
```

### Example Response

```json
{
  "apiVersion": "1.1",
  "confidence": 0.98,
  "mimeType": "multipart/form-data",
  "modelVersion": "ocr-250904",
  "numBilledPages": 1,
  "stored": true,
  "metadata": {
    "pages": [
      {"height": 1600, "page": 1, "width": 1200}
    ]
  },
  "text": "Full document text...",
  "pages": [
    {
      "id": 0,
      "confidence": 0.97,
      "width": 1200,
      "height": 1600,
      "text": "Page text...",
      "words": [
        {
          "id": 0,
          "text": "Invoice",
          "confidence": 0.95,
          "boundingBox": {
            "vertices": [
              {"x": 50, "y": 75},
              {"x": 150, "y": 75},
              {"x": 150, "y": 100},
              {"x": 50, "y": 100}
            ]
          }
        }
      ]
    }
  ]
}
```

### Response Fields

| Field                         | Description                                   |
| ----------------------------- | --------------------------------------------- |
| `apiVersion`                  | API version (major.minor format)              |
| `confidence`                  | Document-level confidence score (0-1)         |
| `mimeType`                    | MIME type of the input file                   |
| `modelVersion`                | Model version used for processing             |
| `numBilledPages`              | Number of pages charged                       |
| `stored`                      | Whether input was stored (true/false)         |
| `metadata`                    | Document metadata including page dimensions   |
| `text`                        | Full document text (all pages concatenated)   |
| `pages[].id`                  | Page index (0-based)                          |
| `pages[].text`                | Text content for each page                    |
| `pages[].width`               | Page width in pixels                          |
| `pages[].height`              | Page height in pixels                         |
| `pages[].confidence`          | Page-level confidence score (0-1)             |
| `pages[].words`               | Array of recognized words                     |
| `pages[].words[].id`          | Word index within page                        |
| `pages[].words[].text`        | Recognized text                               |
| `pages[].words[].confidence`  | Word-level confidence score (0-1)             |
| `pages[].words[].boundingBox` | Bounding box with vertices (x, y coordinates) |

### Parameter Tips

| Use Case                     | Recommended Settings |
| ---------------------------- | -------------------- |
| Default usage                | `model: "ocr"`       |
| Migration from Clova OCR     | `schema: "clova"`    |
| Migration from Google Vision | `schema: "google"`   |

---


---

## 4. Document Parse API

Convert documents to structured HTML or Markdown with layout detection.

### Endpoint (Synchronous)

```
POST https://api.upstage.ai/v1/document-digitization
```

### Endpoint (Asynchronous - for large documents)

```
POST https://api.upstage.ai/v1/document-digitization/async
GET https://api.upstage.ai/v1/document-digitization/requests/{request_id}
GET https://api.upstage.ai/v1/document-digitization/requests
```

### Limitations

| API Type     | Max Pages | Notes                                 |
| ------------ | --------- | ------------------------------------- |
| Synchronous  | 100       | First 100 pages processed if exceeded |
| Asynchronous | 1,000     | Batched in 10-page chunks             |

### Request Body (multipart/form-data)

| Parameter                | Type    | Required | Description                                                                                                                                                |
| ------------------------ | ------- | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `model`                  | string  | Yes      | Use `document-parse` or `document-parse-nightly`                                                                                                           |
| `document`               | file    | Yes      | Document file to process                                                                                                                                   |
| `mode`                   | string  | No       | `standard`, `enhanced`, or `auto`. Default: `standard`. Note: `enhanced` and `auto` modes require `document-parse-260128` or later. See Mode Options below |
| `output_formats`         | string  | No       | JSON array: `["text"]`, `["html"]`, `["markdown"]`, or any combination. Default: `["html"]`                                                                |
| `ocr`                    | string  | No       | `auto`: OCR only for images; digital-born PDFs use embedded text. `force`: Convert all files to images and always perform OCR. Default: `auto`             |
| `coordinates`            | boolean | No       | Return bounding boxes. Default: true                                                                                                                       |
| `chart_recognition`      | boolean | No       | Convert charts to tables. Default: true. Note: Always enabled when `mode=enhanced` (parameter ignored)                                                     |
| `merge_multipage_tables` | boolean | No       | Merge tables across pages. Default: false. Note: Max 20 pages when `mode=enhanced`                                                                         |
| `base64_encoding`        | string  | No       | Categories to return as base64 images. Any layout category allowed: `["table"]`, `["figure"]`, `["equation"]`, etc.                                        |

### Example Request

```bash
curl -X POST https://api.upstage.ai/v1/document-digitization \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -F "model=document-parse" \
  -F "document=@/path/to/document.pdf" \
  -F 'output_formats=["html", "markdown"]'
```

### Async API Example

```python
import requests
import time

api_key = "YOUR_API_KEY"

# Step 1: Submit async request
with open("large_document.pdf", "rb") as f:
    response = requests.post(
        "https://api.upstage.ai/v1/document-digitization/async",
        headers={"Authorization": f"Bearer {api_key}"},
        files={"document": f},
        data={"model": "document-parse"}
    )
request_id = response.json()["request_id"]

# Step 2: Poll for results
while True:
    status = requests.get(
        f"https://api.upstage.ai/v1/document-digitization/requests/{request_id}",
        headers={"Authorization": f"Bearer {api_key}"}
    ).json()

    if status["status"] == "completed":
        # Download results from batch download_urls
        for batch in status["batches"]:
            if batch["status"] == "completed":
                result = requests.get(batch["download_url"]).json()
                print(f"Pages {batch['start_page']}-{batch['end_page']}: processed")
        break
    elif status["status"] == "failed":
        raise Exception(status["failure_message"])

    time.sleep(5)
```

### Async Status Response

```json
{
  "id": "e7b1b3b0-1b3b-4b3b-8b3b-1b3b3b3b3b3b",
  "status": "completed",
  "model": "document-parse",
  "failure_message": "",
  "total_pages": 28,
  "completed_pages": 28,
  "batches": [
    {
      "id": 0,
      "model": "document-parse-260128",
      "status": "completed",
      "failure_message": "",
      "download_url": "https://...",
      "start_page": 1,
      "end_page": 10,
      "requested_at": "2024-07-01T14:47:01Z",
      "updated_at": "2024-07-01T14:47:15Z"
    },
    {
      "id": 1,
      "model": "document-parse-260128",
      "status": "completed",
      "failure_message": "",
      "download_url": "https://...",
      "start_page": 11,
      "end_page": 20,
      "requested_at": "2024-07-01T14:47:01Z",
      "updated_at": "2024-07-01T14:47:13Z"
    }
  ],
  "requested_at": "2024-07-01T14:47:01Z",
  "completed_at": "2024-07-01T14:47:43Z"
}
```

**Status Values:** `submitted` → `started` → `completed` | `failed`

**Batch Status Values:** `scheduled` → `started` → `completed` | `failed` | `retrying`

### Async API Important Notes

- **download_url expiration:** Each `download_url` is valid for **15 minutes** after issuance. Re-fetch the request status to get a fresh URL.
- **Result storage:** Results are stored for **30 days** after completion.
- **Queue behavior:** Async API uses queue-based batch processing. During peak hours, jobs may wait up to **72 hours** before processing starts. Status `scheduled` or `started` during this time is normal.

### Async Request History Response

`GET /v1/document-digitization/requests` returns a list of all async requests:

```json
{
  "requests": [
    {
      "id": "e7b1b3b0-1b3b-4b3b-8b3b-1b3b3b3b3b3b",
      "status": "completed",
      "model": "document-parse",
      "requested_at": "2024-07-01T14:47:01Z",
      "completed_at": "2024-07-01T14:47:43Z"
    },
    {
      "id": "a1b2c3d4-5e6f-7a8b-9c0d-1e2f3a4b5c6d",
      "status": "started",
      "model": "document-parse",
      "requested_at": "2024-07-01T15:00:00Z",
      "completed_at": null
    }
  ]
}
```

### Example Response (Sync)

```json
{
  "apiVersion": "1.1",
  "model": "document-parse-260128",
  "elements": [
    {
      "id": 1,
      "category": "paragraph",
      "page": 1,
      "content": {
        "text": "This is a paragraph.",
        "html": "<p>This is a paragraph.</p>",
        "markdown": "This is a paragraph."
      },
      "coordinates": [
        {"x": 0.125, "y": 0.225},
        {"x": 0.425, "y": 0.225},
        {"x": 0.425, "y": 0.325},
        {"x": 0.125, "y": 0.325}
      ]
    }
  ],
  "content": {
    "text": "Full document text...",
    "html": "<html>...</html>",
    "markdown": "..."
  },
  "usage": {
    "pages": 5
  }
}
```

### Element Categories

`paragraph`, `table`, `figure`, `chart`, `header`, `footer`, `caption`, `equation`, `heading1`, `list`, `index`, `footnote`

### Chart Recognition Details

When `chart_recognition=true`, charts are detected and converted to structured table format.

**Supported chart types:** Bar charts, Line charts, Pie charts

**Output behavior:**

- **Recognition succeeds** → category: `chart`, HTML includes `<figcaption>` (Chart Title, X-Axis, Y-Axis, Chart Type) and `<table>` with extracted data
- **Recognition fails** → category: `figure`, contains OCR text result only

**Example chart output (success):**

```json
{
  "category": "chart",
  "content": {
    "html": "<figure data-category='chart'><img data-coord=\"...\" /><figcaption><p>Chart Title: Sales Report</p><p>X-Axis: Month</p><p>Y-Axis: Revenue</p><p>Chart Type: bar</p></figcaption><table>...</table></figure>",
    "markdown": "- Chart Type: bar\n| Month | Revenue |\n|---|---|\n| Jan | $100 |",
    "text": "Chart Type: bar..."
  }
}
```

### Equation Recognition (LaTeX)

Elements with category `equation` output recognized text in **LaTeX format** within `content.html` and `content.markdown`. This enables rendering with engines like MathJax.

**Note:** `content.text` contains OCR result which may be inaccurate for equations (equation-specific recognition not applied to text output).

**Example equation output:**

```json
{
  "category": "equation",
  "content": {
    "html": "<p data-category='equation'>$$a_{n}=\\sum_{k=1}^{n}{\\frac{2k+1}{k^{2}}}$$</p>",
    "markdown": "$$a_{n}=\\sum_{k=1}^{n}{\\frac{2k+1}{k^{2}}}$$",
    "text": "an = Σ 2k+1/k²"
  }
}
```

### Coordinates Format

Coordinates are **relative values between 0 and 1**, representing the position within the page.

**To calculate absolute pixel position:**

- `absolute_x = x * page_width`
- `absolute_y = y * page_height`

Each element has 4 coordinate points defining the bounding box corners (top-left, top-right, bottom-right, bottom-left).

### Mode Options

| Mode       | Description                                                                                |
| ---------- | ------------------------------------------------------------------------------------------ |
| `standard` | Fast processing for text-heavy documents with simple tables                                |
| `enhanced` | Better handling of complex tables, charts, images, and low-quality scans (additional cost) |
| `auto`     | Automatically classifies each page as standard or enhanced and processes accordingly       |

### Input Recommendations

For best results:

- **Minimum document width:** 640 pixels
- **Minimum text size:** At least 2.5% of image height (e.g., 16px for 640px tall image)
- **Resolution:** Use high-resolution documents for better text legibility
- **Pixel calculation for non-image files:** PDF, DOCX, etc. are converted to images at 150 DPI before pixel count is calculated

### Parameter Tips

| Document Type                               | Recommended Settings                                        |
| ------------------------------------------- | ----------------------------------------------------------- |
| Text-heavy documents (articles, contracts)  | `mode: "standard"`                                          |
| Complex tables, charts, images              | `mode: "enhanced"` (additional cost)                        |
| Mixed document types                        | `mode: "auto"` (auto-classifies pages)                      |
| Scanned PDFs or images                      | `ocr: "force"`                                              |
| Digital-born PDFs                           | `ocr: "auto"` (default)                                     |
| Need table images for downstream processing | `base64_encoding: ["table"]`                                |
| Multi-page tables                           | `merge_multipage_tables: true` (max 20 pages with enhanced) |
| RAG/LLM ingestion                           | `output_formats: ["markdown"]`                              |
| Web display                                 | `output_formats: ["html"]`                                  |

---


---

## 10. Document Split API

Split a single file containing multiple document types into separate document groups using the Classification API. This is useful when a single PDF contains mixed document types (e.g., an application, ID cards, and bank statements).

Document Split is a feature of the Document Classification API, enabled by setting `split: true`.

### Endpoint

```
POST https://api.upstage.ai/v1/document-classification
```

### Request Body (JSON)

All parameters from the Document Classification API apply (see Section 5), plus:

| Parameter        | Type    | Required | Description                                                |
| ---------------- | ------- | -------- | ---------------------------------------------------------- |
| `split`          | boolean | No       | Set to `true` to enable document splitting. Default: false |
| `split_criteria` | array   | No       | Additional criteria for splitting within the same class    |

**`split_criteria` Object:**

| Field         | Type   | Description                                     |
| ------------- | ------ | ----------------------------------------------- |
| `criterion`   | string | Criterion name (e.g., `document_id`, `card_id`) |
| `description` | string | Description of the criterion for the model      |

### How Split Works

- **Without `split_criteria`**: Splits at boundaries where the document type changes based on defined classes.
- **With `split_criteria`**: Additionally splits within the same class based on the specified criteria (e.g., splitting two ID cards with different card IDs).

Non-consecutive pages of the same class and split criteria result are merged into a single document group with multiple page ranges (e.g., `[[1, 3], [6, 6]]`).

### Code Examples

**curl:**

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
            "image_url": {"url": "data:application/octet-stream;base64,BASE64_DATA"}
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
            {"const": "invoice", "description": "Commercial invoice"},
            {"const": "receipt", "description": "Purchase receipt"},
            {"const": "contract", "description": "Legal contract"},
            {"const": "others", "description": "Other"}
          ]
        }
      }
    },
    "split": true,
    "split_criteria": [
      {"criterion": "document_id", "description": "The id that indicates each unit document."}
    ]
  }'
```

**Python (OpenAI SDK):**

```python
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
                    {"const": "receipt", "description": "Purchase receipt"},
                    {"const": "contract", "description": "Legal contract"},
                    {"const": "others", "description": "Other"}
                ]
            }
        }
    },
    extra_body={
        "split": True,
        "split_criteria": [
            {"criterion": "document_id", "description": "The id that indicates each unit document."}
        ]
    }
)
```

### Response Format

Each split document group is returned as a separate item in the `choices` array:

```json
{
  "id": "chatcmpl-...",
  "object": "chat.completion",
  "created": 1714000000,
  "model": "document-classify-...",
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
                "page_ranges": [[1, 3], [6, 6]],
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
                "page_ranges": [[4, 5]],
                "split_criteria_info": {"document_id": "REC-001"}
              }
            }
          }
        ]
      },
      "finish_reason": "stop"
    }
  ]
}
```

**Response Fields (per choice):**

| Field                                    | Type   | Description                                               |
| ---------------------------------------- | ------ | --------------------------------------------------------- |
| `message.content`                        | string | Classified document type                                  |
| `additional_values.document_type._value` | string | Document type with confidence score                       |
| `additional_values.page_ranges`          | array  | Page ranges for this group (list of `[start, end]` pairs) |
| `additional_values.split_criteria_info`  | object | Values of the split criteria for this group               |

---

