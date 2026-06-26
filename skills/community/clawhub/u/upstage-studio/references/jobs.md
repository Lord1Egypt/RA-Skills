# Responses & Jobs API

## POST /v2/responses — Create Job

```json
{
  "model": "agt_xxx",
  "input": [
    {
      "role": "user",
      "content": [
        { "type": "input_file", "file_id": "file_xxx" },
        { "type": "input_text", "text": "Analyze this document" }
      ]
    }
  ],
  "config_id": "cfg_xxx",
  "background": false,
  "include": ["last"],
  "metadata": {}
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `model` | string | Yes | Agent ID (`agt_xxx`) or preset agent name (`schema-generate`, `class-generate`, `schema-update`) |
| `input` | array | Yes | Input items (>=1) |
| `config_id` | string | No | Config ID. Uses Agent's default Config if omitted |
| `background` | bool | No | Background mode. Auto-true for `agt_` prefix |
| `include` | array | No | `"last"` (default, last step only) or `"all"` (all steps) |
| `text` | object | No | Override step `text.format` at request time. For preset agents, this is the only way to provide schemas or instructions |
| `metadata` | object | No | Additional metadata |

**File input methods (choose one):**

| Method | Fields | Example |
|--------|--------|---------|
| file_id | `"file_id": "file_xxx"` | Reference an already-uploaded file |
| file_url | `"file_url": "https://..."` | Auto-download and register from URL |
| file_data | `"file_data": "data:application/pdf;base64,..."`, `"filename": "doc.pdf"` | Direct Base64 upload |

**Caching:** Identical file combination + identical step settings → reuses previous results (7-day TTL).

## Response

```json
{
  "id": "job_xxx",
  "object": "response",
  "status": "completed",
  "model": "agt_xxx",
  "output": [
    {
      "type": "message",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "...",
          "step_id": "step_xxx",
          "step_index": 0
        }
      ]
    }
  ],
  "usage": { "input_tokens": 0, "output_tokens": 0, "total_tokens": 0 },
  "metadata": { "source": "api", "cached": "false" },
  "created_at": 1700000000
}
```

## Background Response (`background: true`)

Returns immediately:

```json
{ "id": "job_xxx", "status": "in_progress", ... }
```

Then poll with `GET /v2/responses/job_xxx`.

---

## GET /v2/responses/{job_id} — Get Job

| Parameter | Default | Description |
|-----------|---------|-------------|
| `include` | `"last"` | `"last"` — last step only. `"all"` — all steps |

**Response:** Same Response schema as above.

Cache info is in `metadata.cached` (`"true"` / `"false"` string).

## DELETE /v2/responses/{job_id} — Delete Job

```json
{ "id": "job_xxx", "object": "job", "deleted": true }
```

## GET /v2/agents/{agent_id}/jobs — List Agent Jobs

| Parameter | Type | Description |
|-----------|------|-------------|
| `source` | string | Filter by Job source (`"studio"`, `"api"`) |
| `config_id` | string | Filter by Config ID |
| `include` | string[] | Output include options (see below) |
| `after`, `before`, `limit`, `order` | - | Pagination |

**`include` parameter:**

| Value | Description |
|-------|-------------|
| (omitted) | No output included |
| `output` | All step results included |
| `output:parse` | document-parse results only |
| `output:classify` | document-classify results only |
| `output:extract` | information-extract results only |
| `output:instruct` | instruct results only |

Multiple values allowed: `include[]=output:classify&include[]=output:extract`

**Response (JobItem schema):**

```json
{
  "object": "list",
  "data": [
    {
      "id": "job_xxx",
      "config_id": "cfg_xxx",
      "external_config_id": "1",
      "status": "completed",
      "error": null,
      "files": [{"id": "file_xxx", "name": "invoice.pdf"}],
      "cached": false,
      "expires_at": null,
      "metadata": {"source": "api"},
      "output": null,
      "created_at": 1700000000,
      "updated_at": 1700000000
    }
  ],
  "first_id": "job_aaa",
  "last_id": "job_zzz",
  "has_more": false
}
```

## Job Status

| Status | Description |
|--------|-------------|
| `in_progress` | Processing |
| `completed` | Done. Results in `output` |
| `failed` | Failed. Error details in `error` |

## Job Execution Errors

The `error` field of a `failed` Job:

```json
{
  "code": "extract_error",
  "message": "The document is too long to process. Please reduce the number of pages or split into smaller documents."
}
```

**Error Codes:**

| Code | Description | Recommended Action |
|------|-------------|-------------------|
| `parse_error` | Document parsing failed | Try a different format or re-upload |
| `preprocess_error` | Document preprocessing failed | Check if the file is corrupted |
| `classify_error` | Classification failed | Retry |
| `extract_error` | Extraction failed | Reduce pages or simplify schema |
| `instruct_error` | Instruct step failed | Retry |
| `tool_execution_error` | Tool execution error | Retry |
| `server_error` | Internal server error | Retry; contact support if persistent |
| `job_timeout_error` | Processing timeout (1 hour) | Reduce pages or split document |

**Common Error Messages and Actions:**

| Message | Cause | Action |
|---------|-------|--------|
| Too many requests. Please try again later. | API rate limit | Wait and retry |
| Request timed out. Please try again later. | LLM response delay | Retry |
| The document is too long to process. Please reduce the number of pages or split into smaller documents. | Document exceeds model limit | Reduce pages or split |
| The model returned an incomplete response. Please retry, or reduce the number of pages if the issue persists. | Incomplete LLM response | Retry or reduce pages |
| This document exceeds the 50-page limit for Enhanced mode. Please switch to Standard mode, which supports up to 1,000 pages for larger files. | Enhanced mode limit | Switch to standard mode |
| No text elements were detected in the input file. | No text in document | Use a document containing text |

## Caching

Same files + same step settings → reuses previous results (7-day TTL).

| `cached` Value | Meaning |
|----------------|---------|
| `true` | All steps served from cache |
| `false` | At least one step was actually executed |

---

## Stats API

### GET /v2/stats/jobs — Job Statistics

| Parameter | Type | Description |
|-----------|------|-------------|
| `source` | string | Filter by Job source |
| `is_custom` | boolean | `true`: custom agents, `false`: built-in |
| `agent_id` | string | Filter by Agent |
| `config_id` | string | Filter by Config |
| `since` | datetime | Jobs created after (ISO 8601) |

**Response:**

```json
{
  "jobs": {
    "in_progress": 42,
    "completed": 1500,
    "failed": 23,
    "cached": 350
  }
}
```

Returns statistics for the authenticated user's Jobs.
