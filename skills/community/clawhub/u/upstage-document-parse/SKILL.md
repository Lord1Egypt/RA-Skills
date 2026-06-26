---
name: upstage-document-parse
description: "Parse documents (PDF, images, DOCX, PPTX, XLSX, HWP) into layout-aware markdown/HTML with tables, figures, headings, and bounding boxes using Upstage Document Parse API. Use when user asks to convert documents to markdown/HTML, preserve layout/tables, or analyze document structure — '이 PDF를 마크다운으로 변환해줘', '문서 구조 분석해줘', '표/레이아웃 그대로 추출해줘', 'parse this PDF to markdown'. DO NOT use for plain text-only extraction with word coordinates — use upstage-ocr instead. DO NOT use for schema-driven field extraction (specific values like invoice total) — use upstage-information-extraction instead."
homepage: https://console.upstage.ai/api/document-digitization/document-parsing
---

# Upstage Document Parse

Convert documents into structured HTML/Markdown. Recognizes layout elements such as tables, images, equations, and charts with bounding box coordinates.

## Quick Start

```python
import os
import requests

with open("report.pdf", "rb") as f:
    response = requests.post(
        "https://api.upstage.ai/v1/document-digitization",
        headers={"Authorization": f"Bearer {os.environ['UPSTAGE_API_KEY']}"},
        files={"document": f},
        data={"model": "document-parse", "output_formats": "['markdown']"}
    )
print(response.json()["content"]["markdown"])
```

**API Key**: Always use `os.environ["UPSTAGE_API_KEY"]`. Get your key at [console.upstage.ai](https://console.upstage.ai).

## Supported Formats

JPEG, PNG, BMP, PDF (up to 1000 pages with async), TIFF, HEIC, DOCX, PPTX, XLSX, HWP, HWPX

## Sync vs Async

| Mode | Endpoint | Max pages | Max file size | Notes |
|------|----------|-----------|---------------|-------|
| **Sync** | `/v1/document-digitization` | 100 | 50 MB | Result returned in response (5 min server timeout). Best for ≤ 100 pages and quick turnaround. |
| **Async** | `/v1/document-digitization/async` | 1000 | 50 MB | Returns `request_id`; processed in 10-page batches. Use when document exceeds sync limits or sync would time out. |

Decision rule:
- ≤ 100 pages **and** expected to finish within 5 min → sync.
- 100 pages, scanned/complex content, or batch jobs → async.

For async submit/poll workflow, see `references/async-workflow.md`.

## Key Parameters (Sync)

| Parameter | Default | Common Values |
|-----------|---------|---------------|
| `model` | required | `document-parse` |
| `output_formats` | `['html']` | `['markdown']`, `['html', 'markdown']` |
| `mode` | `standard` | `enhanced` (complex tables), `auto` |
| `ocr` | `auto` | `force` (always OCR scanned PDFs) |
| `coordinates` | `true` | `false` to omit bounding boxes |

For full parameter reference and curl variations (enhanced mode, force OCR, base64 table images, LangChain integration), see `references/sync-options.md`.

## Response Structure

```json
{
  "api": "2.0",
  "model": "document-parse-251217",
  "content": {
    "html": "<h1>...</h1>",
    "markdown": "# ...",
    "text": "..."
  },
  "elements": [
    {
      "id": 0,
      "category": "heading1",
      "content": { "html": "...", "markdown": "...", "text": "..." },
      "page": 1,
      "coordinates": [{"x": 0.06, "y": 0.05}, ...]
    }
  ],
  "usage": { "pages": 1 }
}
```

### Element Categories

`paragraph`, `heading1`, `heading2`, `heading3`, `list`, `table`, `figure`, `chart`, `equation`, `caption`, `header`, `footer`, `index`, `footnote`

## Output Files

- **Default**: write to `<system-temp>/<input-stem>.parsed.<ext>` where `<ext>` matches `output_formats` (`md` or `html`). Example: `/tmp/report.parsed.md`. Use `tempfile.gettempdir()` for cross-platform code.
- **Override**: if the user specifies an output path, use it.
- **Always print the resolved absolute path** in your response so the user can locate the file.

## Tips

- Use `mode=enhanced` for complex tables, charts, images
- Use `mode=auto` to let API decide per page
- Use async API for documents > 100 pages, > 50 MB, or when sync would exceed the 5-min timeout (async caps at 1000 pages)
- Use `ocr=force` for scanned PDFs or images
- `merge_multipage_tables=true` combines split tables (max 20 pages with enhanced mode)
- Standard documents process in ~3 seconds; sync API timeout is 5 minutes

## Detailed References

| File | Content |
|------|---------|
| `references/sync-options.md` | Full sync parameter reference, mode selection, curl variations, LangChain |
| `references/async-workflow.md` | Async submit/poll/status, Python polling pattern, retention rules |
