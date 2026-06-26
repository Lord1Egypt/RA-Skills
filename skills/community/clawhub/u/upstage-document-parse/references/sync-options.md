# Document Parse — Sync API Detail

## Full Parameter Reference

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model` | string | required | Use `document-parse` (latest) or `document-parse-nightly` |
| `document` | file | required | Document file to parse |
| `mode` | string | `standard` | `standard` (text-focused), `enhanced` (complex tables/images), `auto` |
| `ocr` | string | `auto` | `auto` (images only) or `force` (always OCR) |
| `output_formats` | string | `['html']` | `text`, `html`, `markdown` (array format) |
| `coordinates` | boolean | `true` | Include bounding box coordinates |
| `base64_encoding` | string | `[]` | Elements to base64: `["table"]`, `["figure"]`, etc. |
| `chart_recognition` | boolean | `true` | Convert charts to tables (Beta) |
| `merge_multipage_tables` | boolean | `false` | Merge tables across pages (Beta, max 20 pages if true) |

## Mode Selection

- **`standard`**: text-focused, fastest, default for clean PDFs
- **`enhanced`**: complex tables/images, slower but more accurate
- **`auto`**: API decides per page

## Common Variations

### Extract Markdown

```bash
curl -X POST "https://api.upstage.ai/v1/document-digitization" \
  -H "Authorization: Bearer $UPSTAGE_API_KEY" \
  -F "document=@report.pdf" \
  -F "model=document-parse" \
  -F "output_formats=['markdown']"
```

### Enhanced Mode for Complex Documents

```bash
curl -X POST "https://api.upstage.ai/v1/document-digitization" \
  -H "Authorization: Bearer $UPSTAGE_API_KEY" \
  -F "document=@complex.pdf" \
  -F "model=document-parse" \
  -F "mode=enhanced" \
  -F "output_formats=['html', 'markdown']"
```

### Force OCR for Scanned Documents

```bash
curl -X POST "https://api.upstage.ai/v1/document-digitization" \
  -H "Authorization: Bearer $UPSTAGE_API_KEY" \
  -F "document=@scan.pdf" \
  -F "model=document-parse" \
  -F "ocr=force"
```

### Extract Table Images as Base64

```bash
curl -X POST "https://api.upstage.ai/v1/document-digitization" \
  -H "Authorization: Bearer $UPSTAGE_API_KEY" \
  -F "document=@invoice.pdf" \
  -F "model=document-parse" \
  -F "base64_encoding=['table']"
```

## LangChain Integration

```python
from langchain_upstage import UpstageDocumentParseLoader

loader = UpstageDocumentParseLoader(
    file_path="document.pdf",
    output_format="markdown",
    ocr="auto"
)
docs = loader.load()
```

## Notes

- Server-side timeout: 5 minutes per request (sync API)
- Standard documents process in ~3 seconds
- Sync limits: max 100 pages, max 50 MB
- Use async API for documents > 100 pages, > 50 MB, or when sync would time out (see `async-workflow.md`)
