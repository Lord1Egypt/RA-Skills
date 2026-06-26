# vod_search_media_by_semantics — Detailed Parameters and Examples

> Corresponding script: `scripts/vod_search_media_by_semantics.py`
>
> Search video content imported into the knowledge base using natural language (requires prior import via `vod_import_media_knowledge.py`).

### ⚠️ Common Parameter Mistakes

| Incorrect Usage | Correct Usage | Description |
|---------|---------|------|
| `--query ...` | `--text ...` | **🚨 Use `--text` for semantic search — never `--query`; the parameter names are different** |
| `--category Video` | `--categories Video` | **🚨 Use `--categories` (plural) for media type filtering, not `--category`** |

## Parameter Reference

### Application Selection

| Parameter | Type | Required | Description |
|------|------|------|------|
| `--sub-app-id` | int | - | VOD sub-application ID (required for accounts created after 2023-12-25; can also be set via the `TENCENTCLOUD_VOD_SUB_APP_ID` environment variable); mutually exclusive with `--app-name` — **one of the two must be specified** |
| `--app-name` | string | - | Fuzzy-match a sub-application by name/description (mutually exclusive with `--sub-app-id` — **one of the two must be specified**) |

### Search Parameters

| Parameter | Type | Required | Description |
|------|------|------|------|
| `--text` / `-t` | string | ✅ | Natural language search text (**not** `--query` or `--keyword`) |
| `--limit` / `-n` | int | - | Number of results to return (default 20, range [1, 100]) |

### Filter Conditions

| Parameter | Type | Required | Description |
|------|------|------|------|
| `--categories` | string[] | - | File type filter: `Video` / `Audio` / `Image` (multiple values allowed) |
| `--tags` | string[] | - | Tag filter (matches any tag; up to 16 tags, space-separated) |
| `--persons` | string[] | - | Filter by person (matches all specified persons; up to 16) |
| `--task-types` | string[] | - | Filter by task type (multiple values allowed): `AiAnalysis.DescriptionTask`, `SmartSubtitle.AsrFullTextTask` |

### Output Control

| Parameter | Type | Description |
|------|------|------|
| `--verbose` / `-v` | flag | Display detailed information |
| `--json` | flag | Output the full response in JSON format |
| `--region` | string | Region (default `ap-guangzhou`) |
| `--dry-run` | flag | Preview request parameters without actually executing |

> ⚠️ **Prerequisite**: Media must first be imported into the knowledge base via `vod_import_media_knowledge.py import` before it can be found by semantic search.
> ⚠️ **Parameter name**: Use `--text` (`-t`) for the search text — not `--query` or `--keyword`.

---

## Usage Examples

```bash
# Basic semantic search
python scripts/vod_search_media_by_semantics.py \
    --sub-app-id 1500046806 --text "beach video with a sunset"

# Search by application name
python scripts/vod_search_media_by_semantics.py \
    --app-name "Test App" --text "footage of someone running"

# Filter by file type
python scripts/vod_search_media_by_semantics.py \
    --sub-app-id 1500046806 --text "amazing goals" --categories Video

# Filter by tag
python scripts/vod_search_media_by_semantics.py \
    --sub-app-id 1500046806 --text "amazing goals" --tags "sports" "soccer"

# Filter by person
python scripts/vod_search_media_by_semantics.py \
    --sub-app-id 1500046806 --text "interview video" --persons "Zhang San"

# Specify number of results
python scripts/vod_search_media_by_semantics.py \
    --sub-app-id 1500046806 --text "meeting video" --limit 50

# Filter by task type
python scripts/vod_search_media_by_semantics.py \
    --sub-app-id 1500046806 --text "product introduction" --task-types Ai Analysis.Description Task

# Output in JSON format
python scripts/vod_search_media_by_semantics.py \
    --sub-app-id 1500046806 --text "video containing music" --json

# Verbose mode
python scripts/vod_search_media_by_semantics.py \
    --sub-app-id 1500046806 --text "product demo" --verbose

# Preview request parameters (without executing)
python scripts/vod_search_media_by_semantics.py \
    --sub-app-id 1500046806 --text "beach video with a sunset" --dry-run
```

---

## API Interface

| Feature | API | Documentation |
|------|---------|---------|
| Semantic media search | `SearchMediaBySemantics` | https://cloud.tencent.com/document/api/266/126287 |