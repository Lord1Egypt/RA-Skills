# Analyze Workflow Reference

The analyze workflow is the primary way to trigger cryptocurrency news analysis via HTTP API. This reference documents the three-step async pattern: create job, poll status, fetch result.

## Authentication

All analyze endpoints require Bearer token authentication:

```
Authorization: Bearer <API_KEY>
```

The `API_KEY` is configured via the `API_KEY` environment variable on the server. Requests without a valid token receive HTTP 401.

## Overview

The analyze workflow follows an asynchronous pattern:

1. **Create**: POST to `/analyze` with `hours` and `user_id` to enqueue a job
2. **Poll**: GET `/analyze/{job_id}` to check status until completion
3. **Fetch**: GET `/analyze/{job_id}/result` to retrieve the final Markdown report

The initial POST returns immediately with job metadata. It does not return the analysis report. You must poll and fetch separately.

## Creating an Analysis Job

### Endpoint

```
POST /analyze
```

### Required Parameters

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `hours` | integer | `> 0` | Analysis time window in hours. Values below server minimum return HTTP 400. Values above maximum are capped to the configured limit (default 24h) and the response includes a `warning` field. |
| `user_id` | string | `^[A-Za-z0-9_-]{1,128}$` | Requesting user identifier. Server trims whitespace before validation. |

### Example Request

```bash
curl -X POST "https://news.tradao.xyz/analyze" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"hours": 1, "user_id": "my_agent_01"}'
```

### Success Response (HTTP 202 Accepted)

```json
{
  "success": true,
  "job_id": "analyze_job_2f205899562a4104868384e65f81c8c1",
  "status": "queued",
  "time_window_hours": 1,
  "status_url": "/analyze/analyze_job_2f205899562a4104868384e65f81c8c1",
  "result_url": "/analyze/analyze_job_2f205899562a4104868384e65f81c8c1/result",
  "warning": null
}
```

Response headers include:

- `Location`: Path to status endpoint
- `Retry-After`: Recommended polling interval in seconds (typically 5)

### Validation Errors

| Condition | HTTP Status | Notes |
|-----------|-------------|-------|
| Missing `user_id` | 422 | FastAPI validation error with field location |
| Invalid `user_id` (spaces, punctuation, non-ASCII, >128 chars) | 422 | Must match `^[A-Za-z0-9_-]{1,128}$` |
| `hours <= 0` | 422 | Positive integer required |
| `hours` below server minimum | 400 | Configurable minimum (default 1) |

Example validation error:

```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "user_id"],
      "msg": "Field required",
      "input": {"hours": 1}
    }
  ]
}
```

## Polling Job Status

### Endpoint

```
GET /analyze/{job_id}
```

### Example Request

```bash
curl -H "Authorization: Bearer ${API_KEY}" \
  "https://news.tradao.xyz/analyze/analyze_job_2f205899562a4104868384e65f81c8c1"
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | `true` only when `status` is `completed` |
| `job_id` | string | The job identifier |
| `status` | string | Current job state (see Job States below) |
| `time_window_hours` | integer | Hours requested (after server caps applied) |
| `created_at` | string (ISO 8601) | Job creation timestamp |
| `started_at` | string (ISO 8601) or null | When execution began |
| `completed_at` | string (ISO 8601) or null | When execution finished |
| `items_processed` | integer | Number of news items analyzed |
| `error` | string or null | Error message if failed |
| `result_available` | boolean | `true` when status is `completed` or `failed` |

### Response Examples

**Running job:**

```json
{
  "success": false,
  "job_id": "analyze_job_2f205899562a4104868384e65f81c8c1",
  "status": "running",
  "time_window_hours": 1,
  "created_at": "2026-03-28T12:00:00+00:00",
  "started_at": "2026-03-28T12:00:03+00:00",
  "completed_at": null,
  "items_processed": 0,
  "error": null,
  "result_available": false
}
```

Note: `success: false` during `running` or `queued` states is expected. Use the `status` field as the source of truth, not the `success` boolean.

**Completed job:**

```json
{
  "success": true,
  "job_id": "analyze_job_2f205899562a4104868384e65f81c8c1",
  "status": "completed",
  "time_window_hours": 1,
  "created_at": "2026-03-28T12:00:00+00:00",
  "started_at": "2026-03-28T12:00:03+00:00",
  "completed_at": "2026-03-28T12:01:15+00:00",
  "items_processed": 25,
  "error": null,
  "result_available": true
}
```

## Fetching the Result

### Endpoint

```
GET /analyze/{job_id}/result
```

### Example Request

```bash
curl -H "Authorization: Bearer ${API_KEY}" \
  "https://news.tradao.xyz/analyze/analyze_job_2f205899562a4104868384e65f81c8c1/result"
```

### Behavior by Job State

| Job State | HTTP Status | Response |
|-----------|-------------|----------|
| `queued` or `running` | 200 | Job metadata with empty `report` |
| `completed` | 200 | Full result with Markdown `report` |
| `failed` | 200 | Job metadata with `error` field set |
| Job not found | 404 | Error detail |

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | `true` only when job completed successfully |
| `job_id` | string | The job identifier |
| `status` | string | Final job state |
| `report` | string | Markdown-formatted analysis report (empty if not completed) |
| `items_processed` | integer | Number of news items analyzed |
| `time_window_hours` | integer | Hours analyzed |
| `error` | string or null | Error message if job failed |

### Completed Result Example

```json
{
  "success": true,
  "job_id": "analyze_job_2f205899562a4104868384e65f81c8c1",
  "status": "completed",
  "report": "# Crypto News Analysis Report\n\n## Executive Summary...",
  "items_processed": 25,
  "time_window_hours": 1,
  "error": null
}
```

## Job States

Jobs progress through the following states:

| State | Description | Terminal |
|-------|-------------|----------|
| `queued` | Job created, waiting for execution slot | No |
| `running` | Actively analyzing news items | No |
| `completed` | Analysis finished successfully | Yes |
| `failed` | Analysis failed with error | Yes |

State transitions: `queued` -> `running` -> (`completed` or `failed`)

## Complete Workflow Example

```bash
#!/bin/bash

API_KEY="your-api-key"
BASE_URL="https://news.tradao.xyz"
USER_ID="my_agent_01"

# 1. Create the job
CREATE_RESPONSE=$(curl -sS -X POST "${BASE_URL}/analyze" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d "{\"hours\":1,\"user_id\":\"${USER_ID}\"}")

JOB_ID=$(echo "${CREATE_RESPONSE}" | sed -n 's/.*"job_id":"\([^"]*\)".*/\1/p')
echo "Created job: ${JOB_ID}"

# 2. Poll until completion
while true; do
  STATUS_RESPONSE=$(curl -sS \
    -H "Authorization: Bearer ${API_KEY}" \
    "${BASE_URL}/analyze/${JOB_ID}")

  STATUS=$(echo "${STATUS_RESPONSE}" | sed -n 's/.*"status":"\([^"]*\)".*/\1/p')
  echo "Status: ${STATUS}"

  if [ "${STATUS}" = "completed" ]; then
    # 3. Fetch the result
    curl -sS \
      -H "Authorization: Bearer ${API_KEY}" \
      "${BASE_URL}/analyze/${JOB_ID}/result"
    break
  fi

  if [ "${STATUS}" = "failed" ]; then
    echo "Job failed"
    exit 1
  fi

  sleep 5
done
```

## Key Gotchas

1. **The initial POST does not return the report**: Always poll status and fetch result separately. The 202 response only confirms job acceptance.

2. **Hours is required**: Unlike the Telegram `/analyze` command which can auto-calculate a time window, the HTTP API requires explicit `hours` in every request.

3. **User ID has strict validation**: Must be 1-128 characters, alphanumeric plus underscores and hyphens only. No spaces, no special characters, no Unicode.

4. **Success field semantics**: The `success` boolean in status and result responses reflects job completion state, not HTTP success. It is `false` while the job is `queued` or `running`. Check the `status` field for the actual job state.

5. **HTTP 202 means accepted**: On the create endpoint, 202 means "accepted and processing". The result endpoint always returns HTTP 200 (with an empty `report` field while the job is still running). Note: some older documentation may mention 202 for the result endpoint, but the current implementation returns 200 for all job states; 404 is only returned when the job ID does not exist.

6. **Header case sensitivity**: Cloudflare and some proxies lowercase header names. The `Location` and `Retry-After` headers may appear as `location` and `retry-after`.

7. **Hours capping**: If you request more hours than the server allows (`max_analysis_window_hours`, default 24), the request succeeds but `time_window_hours` in the response reflects the capped value, not your original request. A `warning` field in the response describes the truncation when it occurs.

8. **User isolation**: Each `user_id` has isolated deduplication context. The same user calling analyze twice will see deduplication of previously reported items. Different users do not share context.

## Updating

Keep this reference aligned with:

- `crypto_news_analyzer/api_server.py` for endpoint implementation details
- `crypto_news_analyzer/domain/models.py` for `JobStatus` enum values
- `tests/test_api_server.py` for contract test coverage

When the live API behavior diverges from this document, the code and tests take precedence.
