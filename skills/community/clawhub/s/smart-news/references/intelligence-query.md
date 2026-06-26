# Intelligence Query Reference

Topic-first intelligence HTTP API. All endpoints require Bearer authentication and manage the topic research lifecycle (create → revise → confirm → research → merge → archive).

These endpoints are synchronous — results return immediately. Do not use an async job/poll workflow for intelligence routes.

## Authentication

Send `Authorization: Bearer <API_KEY>` with every request. Missing or invalid credentials return `401 Unauthorized`.

## Topic Lifecycle

Topics progress through states: `draft` → `active` → `archived`. Only `active` topics are researched by the ingestion scheduler. Merge previews expire after 24 hours. Finding merge is available through both the HTTP API and the Telegram `/topic_merge` command.

## Deprecated Routes

The old entry-based routes (`/intelligence/entries*`, `/intelligence/discovery`, `/intelligence/labels`, `/intelligence/search`, `/intelligence/raw/*`, `/intelligence/topics/converge`) have been removed. Use only the topic-first endpoints documented below.

---

## POST /intelligence/topics

Create a new intelligence topic with an LLM-generated draft prompt.

### Request Body

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `theme` | string | Yes | 1–500 characters |
| `source_context` | object | No | Optional context for prompt generation |
| `datasource_ids` | string[] | No | Optional list of datasource IDs to associate. Omitted = no associations. |

### Status Codes

| Code | Meaning |
|------|---------|
| `201` | Topic draft created |
| `400` | Invalid theme or topic parameters |
| `401` | Missing or invalid Bearer token |
| `503` | LLM service unavailable |

### Response (201)

Returns a `TopicPromptVersionResponse`:

```json
{
  "id": "prompt-uuid",
  "intelligence_topic_id": "topic-uuid",
  "prompt_version": "v1.0",
  "prompt_text": "LLM-generated research prompt...",
  "schema_version": "v1.0",
  "status": "draft",
  "created_by": "api",
  "activated_by": null,
  "activation_notes": null,
  "created_at": "2026-05-18T10:00:00+00:00",
  "activated_at": null,
  "archived_at": null,
  "updated_at": "2026-05-18T10:00:00+00:00",
  "audit_history": []
}
```

### Example

```bash
curl -X POST "https://news.tradao.xyz/intelligence/topics" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"theme": "crypto payment channels in Telegram groups"}'
```

---

## POST /intelligence/topics/{topic_id}/revise

Revise the most recent draft prompt using LLM and user feedback. Returns a new prompt version.

### Request Body

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `feedback` | string | Yes | 1–5000 characters |

### Response

Returns a `TopicPromptVersionResponse` with the revised prompt.

### Example

```bash
curl -X POST "https://news.tradao.xyz/intelligence/topics/topic-uuid/revise" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"feedback": "Focus on stablecoin settlement, exclude NFT marketplaces"}'
```

---

## PUT /intelligence/topics/{topic_id}/prompt

Manually set or replace the topic prompt text. Context-aware behavior:
- If an active prompt exists → edits it in place (new version with same activation)
- If no active prompt → creates a draft revision

### Request Body

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `prompt_text` | string | Yes | 1–50000 characters |

### Response

Returns a `TopicPromptVersionResponse`.

### Example

```bash
curl -X PUT "https://news.tradao.xyz/intelligence/topics/topic-uuid/prompt" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"prompt_text": "Custom manual research prompt text..."}'
```

---

## POST /intelligence/topics/{topic_id}/confirm

Confirm a draft prompt version, activating it for scheduled research.

### Request Body

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `prompt_version_id` | string | Yes | Must reference a draft prompt version |
| `activation_notes` | string | No | Max 2000 characters |

### Response

Returns a `TopicPromptVersionResponse` with status `active`.

### Example

```bash
curl -X POST "https://news.tradao.xyz/intelligence/topics/topic-uuid/confirm" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"prompt_version_id": "prompt-uuid", "activation_notes": "Ready for daily research"}'
```

---

## GET /intelligence/topics

List intelligence topics with pagination and filtering.

### Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `active_only` | boolean | No | `true` | Filter to active topics only |
| `page` | integer | No | 1 | Page number (1-based) |
| `page_size` | integer | No | 20 | Items per page |

### Response (200)

```json
{
  "items": [
    {
      "id": "topic-uuid",
      "name": "Stablecoin Settlement Channels",
      "finding_count": 5,
      "updated_at": "2026-05-18T06:30:00+00:00"
    }
  ],
  "total": 12,
  "page": 1,
  "page_size": 20
}
```

### Example

```bash
curl -H "Authorization: Bearer ${API_KEY}" \
  "https://news.tradao.xyz/intelligence/topics?active_only=true&page=1&page_size=20"
```

---

## GET /intelligence/topics/{topic_id}

Get topic metadata and merge availability. Findings and prompts are available via separate endpoints below.

### Response (200)

```json
{
  "topic": {
    "id": "topic-uuid",
    "name": "Stablecoin Settlement Channels",
    "is_active": true,
    "updated_at": "2026-05-18T06:30:00+00:00"
  },
  "merge_available": false
}
```

Returns `404` if the topic ID does not exist.

### Example

```bash
curl -H "Authorization: Bearer ${API_KEY}" \
  "https://news.tradao.xyz/intelligence/topics/topic-uuid"
```

---

## GET /intelligence/topics/{topic_id}/findings

Return paginated active findings with citations. Each citation includes a `source_url` (resolved from raw items when available) for direct linking to original messages.

### Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `page` | integer | No | 1 | Page number (1-based) |
| `page_size` | integer | No | 10 | Items per page |

### Response (200)

```json
{
  "findings": [
    {
      "id": "finding-uuid",
      "intelligence_topic_id": "topic-uuid",
      "prompt_version_id": "prompt-uuid",
      "finding_payload": { /* LLM-generated structured finding */ },
      "confidence": 0.92,
      "citations": [
        {
          "message_id": "raw-uuid",
          "message_snippet": "Original message text excerpt...",
          "source": "telegram_group",
          "published_at": "2026-05-18T05:00:00+00:00",
          "source_url": "https://t.me/channel/123"
        }
      ],
      "source_finding_ids": [],
      "status": "active",
      "found_at": "2026-05-18T06:00:00+00:00",
      "created_at": "2026-05-18T06:00:00+00:00",
      "updated_at": "2026-05-18T06:00:00+00:00"
    }
  ],
  "total": 5,
  "page": 1,
  "page_size": 10
}
```

### Example

```bash
curl -H "Authorization: Bearer ${API_KEY}" \
  "https://news.tradao.xyz/intelligence/topics/topic-uuid/findings?page=1&page_size=10"
```

---

## GET /intelligence/topics/{topic_id}/prompts

Return all prompt versions and the currently active prompt for a topic.

### Response (200)

```json
{
  "current_prompt": {
    "id": "prompt-uuid",
    "intelligence_topic_id": "topic-uuid",
    "prompt_version": "v1.0",
    "prompt_text": "Research prompt text...",
    "schema_version": "v1.0",
    "status": "active",
    "created_by": "api",
    "activated_by": "api",
    "activation_notes": "Ready for daily research",
    "created_at": "2026-05-18T10:00:00+00:00",
    "activated_at": "2026-05-18T10:05:00+00:00",
    "archived_at": null,
    "updated_at": "2026-05-18T10:05:00+00:00",
    "audit_history": []
  },
  "prompt_versions": [ /* all versions, same shape as current_prompt */ ]
}
```

### Example

```bash
curl -H "Authorization: Bearer ${API_KEY}" \
  "https://news.tradao.xyz/intelligence/topics/topic-uuid/prompts"
```

---

## POST /intelligence/topics/{topic_id}/archive

Archive a topic, stopping further scheduled research runs.

### Response (200)

```json
{
  "success": true,
  "topic_id": "topic-uuid",
  "lifecycle_status": "archived",
  "updated_at": "2026-05-18T12:00:00+00:00"
}
```

Returns `404` if the topic ID does not exist.

### Example

```bash
curl -X POST "https://news.tradao.xyz/intelligence/topics/topic-uuid/archive" \
  -H "Authorization: Bearer ${API_KEY}"
```

---

## POST /intelligence/topics/{topic_id}/merge

Start an **async** merge job for active topic findings. The LLM call may take several minutes — this endpoint returns immediately with a `job_id`. Poll the status endpoint, then fetch the result once the job completes.

### Response (202)

```json
{
  "success": true,
  "job_id": "merge_job_abc123",
  "topic_id": "topic-uuid",
  "status": "queued",
  "status_url": "/intelligence/topics/topic-uuid/merge/merge_job_abc123",
  "result_url": "/intelligence/topics/topic-uuid/merge/merge_job_abc123/result"
}
```

Returns `400` if no active prompt found. Returns `404` if the topic ID does not exist. The `Location` response header points to the status URL.

### Example

```bash
curl -X POST "https://news.tradao.xyz/intelligence/topics/topic-uuid/merge" \
  -H "Authorization: Bearer ${API_KEY}"
```

---

## GET /intelligence/topics/{topic_id}/merge/{job_id}

Check the status of a merge job. Jobs progress through `queued`, `running`, `completed`, and `failed` states.

### Response (200)

```json
{
  "success": true,
  "job_id": "merge_job_abc123",
  "topic_id": "topic-uuid",
  "status": "completed",
  "created_at": "2026-06-04T10:00:00+00:00",
  "started_at": "2026-06-04T10:00:01+00:00",
  "completed_at": "2026-06-04T10:02:34+00:00",
  "error": null,
  "result_available": true
}
```

`result_available` is `true` when the job status is `completed` or `failed`. Returns `404` if the job or topic is not found.

### Example

```bash
curl -H "Authorization: Bearer ${API_KEY}" \
  "https://news.tradao.xyz/intelligence/topics/topic-uuid/merge/merge_job_abc123"
```

---

## GET /intelligence/topics/{topic_id}/merge/{job_id}/result

Retrieve the completed merge results. Only available after the job status is `completed` or `failed`.

### Response (200)

```json
{
  "success": true,
  "job_id": "merge_job_abc123",
  "topic_id": "topic-uuid",
  "status": "completed",
  "topic_name": "Stablecoin Settlement Channels",
  "source_findings_count": 5,
  "merged_findings_count": 2,
  "source_citations_count": 15,
  "merged_citations_count": 8,
  "removed_citations_count": 7,
  "summary": "Consolidated findings summary...",
  "change_summary": {}
}
```

Returns `404` if the job is not found. The endpoint returns the current job state at any time — poll status with `result_available` to detect completion. Failed jobs return `success: false` with the error in the `error` field.

### Workflow

```
POST /intelligence/topics/{id}/merge  →  202 Accepted + job_id
  ↓
GET  /intelligence/topics/{id}/merge/{job_id}  →  poll until completed/failed
  ↓
GET  /intelligence/topics/{id}/merge/{job_id}/result  →  final merge results
```

### Example

```bash
curl -H "Authorization: Bearer ${API_KEY}" \
  "https://news.tradao.xyz/intelligence/topics/topic-uuid/merge/merge_job_abc123/result"
```

---

## GET /intelligence/topics/{topic_id}/runs

Get paginated research run logs for a specific topic. Each run includes the prompt version used, execution status, findings count, and timestamps.

### Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `page` | integer | No | 1 | Page number (1-based) |
| `page_size` | integer | No | 10 | Items per page |

### Response (200)

Returns paginated list of `TopicResearchRun` objects.

### Example

```bash
curl -H "Authorization: Bearer ${API_KEY}" \
  "https://news.tradao.xyz/intelligence/topics/topic-uuid/runs?page=1&page_size=10"
```

---

## GET /intelligence/topic-runs

Get paginated research run logs across all topics. Useful for monitoring overall research activity.

### Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `page` | integer | No | 1 | Page number (1-based) |
| `page_size` | integer | No | 10 | Items per page |

### Response (200)

Returns paginated list of `TopicResearchRun` objects across all topics.

### Example

```bash
curl -H "Authorization: Bearer ${API_KEY}" \
  "https://news.tradao.xyz/intelligence/topic-runs?page=1&page_size=10"
```

---

## Status Codes

| Status | Meaning |
|--------|---------|
| `200` | Success |
| `201` | Topic draft created |
| `202` | Merge job accepted (async — poll for result) |
| `400` | Invalid parameters or merge preview error |
| `401` | Missing or invalid Bearer token |
| `404` | Topic or resource not found |
| `422` | FastAPI validation error |
| `500` | Internal server error |
| `503` | LLM service or repository not initialized |

## Notes

- Topic lifecycle endpoints are synchronous — results return immediately without polling.
- The merge endpoint (`POST /intelligence/topics/{id}/merge`) is **async**: returns 202, then poll status → get result.
- Only `active` topics receive scheduled research from the ingestion service.
- Merge previews expire after 24 hours; accepting a stale preview is rejected.
- Finding merge is available through both the async HTTP endpoint and the Telegram `/topic_merge` command. At least two active findings are required.
- Prompt lifecycle: create draft → revise (optional) → confirm → active. Manual edits via `PUT /prompt` can shortcut this.
- These endpoints exist only on `analysis-service` / `api-only` deployments. They are not available from `ingestion`.

## Updating

Canonical sources for this reference:

1. `crypto_news_analyzer/api_server.py` — route definitions and response models
2. `crypto_news_analyzer/intelligence/topic_prompts.py` — prompt workflow service
3. `crypto_news_analyzer/intelligence/topic_findings.py` — findings and merge service
4. `crypto_news_analyzer/domain/models.py` — `TopicLifecycleStatus` enum and `SafeDataSourceSummary`
5. `crypto_news_analyzer/domain/repositories.py` — `IntelligenceRepository` datasource association contract
6. `tests/intelligence/test_topic_datasource_api.py` — association API contract tests

When sources disagree, trust code over prose.
