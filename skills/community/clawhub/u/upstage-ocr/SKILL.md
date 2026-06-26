---
name: upstage-ocr
description: "Extract plain text with word-level bounding box coordinates from images and scanned documents using Upstage OCR API. Use when user asks to OCR a document, extract raw text from an image/scan, or get text coordinates — '이미지에서 텍스트만 뽑아줘', 'OCR 돌려줘', 'extract text with coordinates'. DO NOT use for layout-aware extraction (tables, figures, markdown/HTML conversion) — use upstage-document-parse instead. DO NOT use for schema-driven field extraction (invoice number, total amount) — use upstage-information-extraction instead."
homepage: https://console.upstage.ai/api/document-digitization/ocr
---

# Upstage OCR

Extract word-level text with bounding box coordinates from images and scanned documents.

## Quick Start

```python
import os
import requests

response = requests.post(
    "https://api.upstage.ai/v1/document-digitization",
    headers={"Authorization": f"Bearer {os.environ['UPSTAGE_API_KEY']}"},
    files={"document": open("scan.pdf", "rb")},
    data={"model": "ocr"}
)
result = response.json()
print(result["pages"][0]["text"])
```

**API Key**: Always use `os.environ["UPSTAGE_API_KEY"]`. Get your key at [console.upstage.ai](https://console.upstage.ai).

---

## Endpoints

| Mode | Endpoint | Max pages | Max file size |
|------|----------|-----------|---------------|
| **Sync** | `POST /v1/document-digitization` | 100 | 50 MB |
| **Async** | `POST /v1/document-digitization/async` | 1000 | 50 MB |

- **Request format**: `multipart/form-data`
- **Sync**: returns the result in the response body (timeout 5 min).
- **Async**: returns a `request_id`; poll status and download per-batch results (batches of 10 pages).

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `model` | string | Yes | `ocr` (alias: `ocr-250904`) |
| `document` | file | Yes | Document file to process |
| `schema` | string | No | `clova` or `google` (for migration) |

## Limits

| Item | Sync | Async |
|------|------|-------|
| Max pages | 100 | 1000 |
| Max file size | 50 MB | 50 MB |
| Max pixels/page | 200,000,000 | 200,000,000 |

Pick **sync** for ≤ 100 pages and quick (≤ 5 min) processing. Pick **async** for documents up to 1000 pages, when you can poll, or when the sync timeout would be hit.

## Supported Formats

JPEG, PNG, BMP, PDF, TIFF, HEIC, DOCX, PPTX, XLSX, HWP, HWPX

## Supported Languages

- **Full support**: Alphabets, Korean, Chinese characters
- **Partial support**: Katakana, Hiragana
- **Beta**: Simplified Chinese

## Response Structure

```json
{
  "api": "2.0",
  "model": "ocr-250904",
  "pages": [
    {
      "id": 0,
      "text": "Full extracted text",
      "words": [
        {
          "id": 0,
          "text": "word",
          "bounding_box": {
            "vertices": [
              {"x": 0.12, "y": 0.05},
              {"x": 0.25, "y": 0.05},
              {"x": 0.25, "y": 0.08},
              {"x": 0.12, "y": 0.08}
            ]
          },
          "confidence": 0.98
        }
      ]
    }
  ],
  "usage": {"pages": 1}
}
```

## Usage Examples

### Sync — Basic OCR

```bash
curl -X POST "https://api.upstage.ai/v1/document-digitization" \
  -H "Authorization: Bearer $UPSTAGE_API_KEY" \
  -F "document=@/path/to/image.jpg" \
  -F "model=ocr"
```

### Sync — Python (Extract Text with Coordinates)

```python
import os
import requests

def ocr_document(file_path):
    with open(file_path, "rb") as f:
        response = requests.post(
            "https://api.upstage.ai/v1/document-digitization",
            headers={"Authorization": f"Bearer {os.environ['UPSTAGE_API_KEY']}"},
            files={"document": f},
            data={"model": "ocr"}
        )
    result = response.json()

    for page in result["pages"]:
        print(f"=== Page {page['id']} ===")
        print(page["text"])
        for word in page["words"]:
            print(f"  [{word['confidence']:.2f}] {word['text']} @ {word['bounding_box']}")

    return result
```

### Async — Submit, Poll, Download

Use the async endpoint for documents up to 1000 pages. Documents are processed in batches of 10 pages; results are stored for 30 days, individual download URLs expire after 15 minutes.

```bash
# 1. Submit
curl -X POST "https://api.upstage.ai/v1/document-digitization/async" \
  -H "Authorization: Bearer $UPSTAGE_API_KEY" \
  -F "document=@large.pdf" \
  -F "model=ocr"
# → {"request_id": "uuid-here"}

# 2. Poll status
curl "https://api.upstage.ai/v1/document-digitization/requests/{request_id}" \
  -H "Authorization: Bearer $UPSTAGE_API_KEY"
```

Status values: `submitted`, `started`, `completed`, `failed` (check `failure_message`). The completed response includes a `download_url` per batch — fetch each and concatenate `pages` to reconstruct the full document.

```python
import os
import time
import requests

api_key = os.environ["UPSTAGE_API_KEY"]
base = "https://api.upstage.ai/v1/document-digitization"

with open("large.pdf", "rb") as f:
    r = requests.post(
        f"{base}/async",
        headers={"Authorization": f"Bearer {api_key}"},
        files={"document": f},
        data={"model": "ocr"},
    )
request_id = r.json()["request_id"]

while True:
    status = requests.get(
        f"{base}/requests/{request_id}",
        headers={"Authorization": f"Bearer {api_key}"},
    ).json()
    if status["status"] == "completed":
        break
    if status["status"] == "failed":
        raise RuntimeError(status.get("failure_message", "unknown failure"))
    time.sleep(5)

# status["batches"] contains per-batch download_url entries
pages = []
for batch in status.get("batches", []):
    data = requests.get(batch["download_url"]).json()
    pages.extend(data["pages"])
```

## Output Files

- **Default**: write to `<system-temp>/<input-stem>.ocr.json` (e.g., `/tmp/receipt.ocr.json`). Use `tempfile.gettempdir()` for cross-platform code.
- **Override**: if the user specifies an output path, use it.
- **Always print the resolved absolute path** in your response so the user can locate the file.

## Tips

- For documents > 100 pages, switch to the **async endpoint** (up to 1000 pages). Sync rejects oversized documents.
- Sync server timeout is 5 minutes — if a sync request times out, retry on `/async`.
- Async results live for 30 days; per-batch `download_url`s expire after 15 minutes (re-fetch status to refresh).
- Low scan quality will result in lower `confidence` values. Pre-processing images can help.
- Coordinates are returned as normalized ratios (0–1).
- OCR extracts text only. If you need structured HTML/Markdown output, use Document Parse instead.
