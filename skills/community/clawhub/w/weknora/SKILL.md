---
name: weknora
description: >
  Import documents and perform knowledge retrieval via WeKnora API. Use when
  uploading files, URLs, or Markdown to a knowledge base, searching knowledge
  with hybrid retrieval (vector + keyword), or querying knowledge details.
  Triggers: (1) uploading documents to a knowledge base, (2) hybrid search
  across knowledge bases, (3) listing/querying knowledge base contents.
metadata: {"openclaw": {"requires": {"env": ["WEKNORA_API_KEY", "WEKNORA_BASE_URL"]}}}
---
# WeKnora

Knowledge base document import and retrieval through the WeKnora REST API.

## Setup


1. Get your API Key from the WeKnora web UI (account settings page)
2. Configure environment variables:

```bash
export WEKNORA_BASE_URL="https://your-server.com/api/v1"
export WEKNORA_API_KEY="sk-your-api-key"
```

> Add the above to `~/.zshrc` or `~/.bashrc` to persist across sessions.

## Credential Check

Verify credentials before any API call. Stop and prompt the user if unset.

```bash
if [ -z "$WEKNORA_BASE_URL" ] || [ -z "$WEKNORA_API_KEY" ]; then
  echo "Missing WeKnora credentials. Set WEKNORA_BASE_URL and WEKNORA_API_KEY per Setup."
  exit 1
fi
```

## API Call Template

All requests go to `$WEKNORA_BASE_URL` with a shared header set. Define a helper:

```bash
wk_api() {
  local method="$1" endpoint="$2" body="$3"
  curl -s -X "$method" "$WEKNORA_BASE_URL/$endpoint" \
    -H "X-API-Key: $WEKNORA_API_KEY" \
    -H "Content-Type: application/json" \
    -H "X-Request-ID: $(uuidgen 2>/dev/null || date +%s)" \
    ${body:+-d "$body"}
}
```

For file uploads use `curl -F` directly (multipart/form-data).

## API Decision Table

|User Intent |Endpoint |Key Params |
|---|---|---|
|List knowledge bases |`GET /knowledge-bases` |— |
|View KB details |`GET /knowledge-bases/:id` |— |
|Upload a file |`POST /knowledge-bases/:id/knowledge/file` |`file` (form-data), `enable_multimodel` |
|Import a web page |`POST /knowledge-bases/:id/knowledge/url` |`url`, `enable_multimodel` |
|Write Markdown content |`POST /knowledge-bases/:id/knowledge/manual` |`title`, `content`, `tag_id` |
|Check upload progress |`GET /knowledge/:id` |watch `parse_status` |
|Browse KB contents |`GET /knowledge-bases/:id/knowledge` |`page`, `page_size`, `tag_id` |
|Edit Markdown knowledge |`PUT /knowledge/manual/:id` |`title`, `content` |
|Delete a knowledge entry |`DELETE /knowledge/:id` |— |
|Search within a KB |`GET /knowledge-bases/:id/hybrid-search` |`query_text`, `match_count`, thresholds |
|Search across KBs |`POST /knowledge-search` |`query`, `knowledge_base_ids` |

## Common Workflows

### Upload File and Wait for Parsing

```bash
# 1. Find target KB
wk_api GET "knowledge-bases"
# -> pick kb_id from data[].id

# 2. Upload file
curl -s -X POST "$WEKNORA_BASE_URL/knowledge-bases/<kb_id>/knowledge/file" \
  -H "X-API-Key: $WEKNORA_API_KEY" \
  -F 'file=@document.pdf' -F 'enable_multimodel=true'
# -> get knowledge_id from data.id

# 3. Poll until parsed
wk_api GET "knowledge/<knowledge_id>"
# -> repeat until data.parse_status == "completed"
```

### Import URL

```bash
wk_api POST "knowledge-bases/<kb_id>/knowledge/url" \
  '{"url": "https://example.com/article", "enable_multimodel": true}'
# -> poll knowledge/:id same as file upload
```

### Write Markdown Knowledge

```bash
wk_api POST "knowledge-bases/<kb_id>/knowledge/manual" \
  '{"title": "Meeting Notes", "content": "# Q1 Review\n\nKey points..."}'
```

### Search Knowledge

```bash
# Single-KB hybrid search (vector + keyword)
wk_api GET "knowledge-bases/<kb_id>/hybrid-search" \
  '{"query_text": "deployment process", "match_count": 5}'

# Cross-KB semantic search
wk_api POST "knowledge-search" \
  '{"query": "deployment process", "knowledge_base_ids": ["kb-1", "kb-2"]}'
```

### Browse and Read KB Contents

```bash
# List knowledge entries (paginated)
wk_api GET "knowledge-bases/<kb_id>/knowledge?page=1&page_size=20"

# Get full detail of one entry
wk_api GET "knowledge/<knowledge_id>"
```

## Core Response Fields

**Knowledge Base** (`GET /knowledge-bases`): `data[]` — `id`, `name`, `description`, `type` (`document` | `faq`), `embedding_model_id`, `knowledge_count`, `chunk_count`, `is_processing`, `created_at`.

**Knowledge Entry** (`GET /knowledge/:id`): `data` — `id`, `title`, `description` (auto-generated summary), `type` (`file` | `url` | `manual`), `parse_status`, `enable_status`, `file_name`, `file_type`, `file_size`, `source` (URL origin), `created_at`, `processed_at`, `error_message`.

**Search Result** (`hybrid-search`): `data[]` — `id`, `content` (chunk text), `score` (relevance 0–1), `knowledge_id`, `knowledge_title`, `knowledge_filename`, `chunk_index`, `chunk_type` (`text` | `summary` | `image`), `match_type`, `metadata`.

**Paginated List** (`GET .../knowledge`): `data[]` + `total`, `page`, `page_size`.

## Enum Values

- `parse_status`: `pending` → `processing` → `completed` | `failed`
- `enable_status`: `enabled` | `disabled` (knowledge becomes `enabled` after successful parsing)
- `type` (knowledge): `file` (uploaded file), `url` (web import), `manual` (Markdown)
- `type` (knowledge base): `document` (standard), `faq` (FAQ pairs)
- `chunk_type`: `text` (regular chunk), `summary` (auto-generated summary), `image` (image chunk)

## Pagination

- **Offset pagination** (`GET .../knowledge`, `GET /sessions`): use `page` and `page_size` query params. Response includes `total` for calculating pages.
- **Hybrid search**: returns up to `match_count` results (no pagination; increase `match_count` for more).

## Notes

- `GET /knowledge-bases/:id/hybrid-search` uses GET method but requires a **JSON request body** — pass `-d '{...}'` with curl.
- After uploading, knowledge `enable_status` starts as `disabled` and auto-switches to `enabled` once `parse_status` reaches `completed`.
- File upload uses `multipart/form-data`, not JSON. Use `curl -F 'file=@path'`.
- `file_type` is auto-detected from the uploaded file (supports `pdf`, `docx`, `xlsx`, `pptx`, `txt`, `md`, `csv`, `html`, etc.).
- Search `score` ranges from 0 to 1; higher is more relevant. Adjust `vector_threshold` (default ~0.5) to filter low-quality matches.
- When `parse_status` is `failed`, check `error_message` field for the failure reason before retrying with `POST /knowledge/:id/reparse`.

## Error Handling

All errors return:

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable description",
    "details": "Optional extra info"
  }
}
```

|HTTP Code |Meaning |Suggested Action |
|---|---|---|
|`400` |Bad request |Check required fields and param formats |
|`401` |Unauthorized |Verify `WEKNORA_API_KEY` is correct |
|`403` |Forbidden |Confirm you have access to this resource |
|`404` |Not found |Check resource ID exists |
|`413` |Payload too large |Reduce file size or split content |
|`500` |Server error |Retry after a short delay |


