# Document Parse — Async API Workflow

Use when sync limits are exceeded.

| Limit | Sync | Async |
|-------|------|-------|
| Max pages | 100 | 1000 |
| Max file size | 50 MB | 50 MB |
| Processing | inline (5-min timeout) | batched in 10-page chunks |

Async returns a `request_id`; you poll for status and download per-batch results.

## Submit Request

```bash
curl -X POST "https://api.upstage.ai/v1/document-digitization/async" \
  -H "Authorization: Bearer $UPSTAGE_API_KEY" \
  -F "document=@large.pdf" \
  -F "model=document-parse" \
  -F "output_formats=['markdown']"
```

Response:
```json
{"request_id": "uuid-here"}
```

## Check Status & Get Results

```bash
curl "https://api.upstage.ai/v1/document-digitization/requests/{request_id}" \
  -H "Authorization: Bearer $UPSTAGE_API_KEY"
```

Response includes `download_url` for each batch (available for 30 days, individual URLs expire after 15 minutes).

## List All Requests

```bash
curl "https://api.upstage.ai/v1/document-digitization/requests" \
  -H "Authorization: Bearer $UPSTAGE_API_KEY"
```

## Status Values

- `submitted`: Request received
- `started`: Processing in progress
- `completed`: Ready for download
- `failed`: Error occurred (check `failure_message`)

## Python Polling Pattern

```python
import os
import time
import requests

api_key = os.environ["UPSTAGE_API_KEY"]

# 1. Submit async request
with open("large.pdf", "rb") as f:
    r = requests.post(
        "https://api.upstage.ai/v1/document-digitization/async",
        headers={"Authorization": f"Bearer {api_key}"},
        files={"document": f},
        data={"model": "document-parse"}
    )
request_id = r.json()["request_id"]

# 2. Poll for status
while True:
    status = requests.get(
        f"https://api.upstage.ai/v1/document-digitization/requests/{request_id}",
        headers={"Authorization": f"Bearer {api_key}"}
    ).json()
    if status["status"] == "completed":
        break
    if status["status"] == "failed":
        raise RuntimeError(status.get("failure_message", "unknown failure"))
    time.sleep(5)
```

## Notes

- Results stored for 30 days
- Download URLs expire after 15 minutes (re-fetch status to get new URLs)
- Documents split into batches of up to 10 pages
