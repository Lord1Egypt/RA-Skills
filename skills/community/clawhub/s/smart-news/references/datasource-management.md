# Datasource Management Reference

This document describes the HTTP API surface for managing datasources. All datasource routes require Bearer authentication.

## CRUD Routes

### POST /datasources

Creates a new datasource. Returns `201 Created` on success, `409 Conflict` if a datasource with the same type and name already exists, and `422 Unprocessable Entity` for invalid payloads.

**Request body structure:**
```json
{
  "purpose": "news|intelligence",
  "source_type": "rss|x|rest_api",
  "tags": ["tag1", "tag2"],
  "config_payload": {
    "name": "My Source",
    ...
  }
}
```

The `purpose` field determines which pipeline the datasource feeds: `news` (RSS/X/REST for content analysis) or `intelligence` (Telegram groups, V2EX for topic research). The `name` field in the top-level request must match `config_payload.name` when both are provided.

### GET /datasources

Lists all datasources sorted by purpose, source type, then name. Supports optional filtering by `purpose` and `source_type` query parameters. Returns `200 OK` with a list of datasource summaries.

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `purpose` | string | No | Filter by `news` or `intelligence` |
| `source_type` | string | No | Filter by datasource type (`rss`, `x`, etc.) |

**Response structure:**
```json
{
  "success": true,
  "datasources": [
    {
      "id": "uuid",
      "name": "My Source",
      "purpose": "news",
      "source_type": "rss",
      "tags": ["tag1"],
      "config_summary": {
        ...
      }
    }
  ]
}
```

List responses always return safe summaries. For `rest_api` datasources, sensitive fields are redacted and replaced with counts.

### DELETE /datasources/{id}

Deletes a datasource by its UUID. Returns `204 No Content` on success, `404 Not Found` if the datasource does not exist, and `409 Conflict` if the datasource has active ingestion jobs.

The delete operation will fail with `409 Conflict` if there are pending or running ingestion jobs associated with this datasource (matched by `source_type:source_name`).

## Supported Datasource Types

The API supports five datasource types: `rss`, `x`, `rest_api`, `telegram_group`, and `v2ex`.

`telegram_group` and `v2ex` feed the **hidden-channel intelligence pipeline** (raw collection → LLM extraction → canonical knowledge). They are not part of the news analysis pipeline and require the `openclaw+opencode` ingestion service with proper credentials.

### rss

RSS feed datasources crawl RSS/XML feeds.

**Required config_payload fields:**
- `name` (string, non-empty)
- `url` (string, valid HTTP/HTTPS URL)

**Optional config_payload fields:**
- `description` (string, defaults to empty string)

**Config summary in responses:**
- `url`: The RSS feed URL
- `description`: The description value

### x

X (formerly Twitter) datasources crawl X lists or timelines.

**Required config_payload fields:**
- `name` (string, non-empty)
- `url` (string, valid HTTPS URL on x.com or www.x.com)
- `type` (string, must be `"list"` or `"timeline"`)

**Config summary in responses:**
- `url`: The X URL
- `type`: Either `"list"` or `"timeline"`

### rest_api

REST API datasources fetch content from arbitrary HTTP endpoints.

**Required config_payload fields:**
- `name` (string, non-empty)
- `endpoint` (string, valid HTTP/HTTPS URL)
- `method` (string, one of: `GET`, `POST`, `PUT`, `DELETE`)
- `response_mapping` (object) with required fields:
  - `title_field` (string, non-empty)
  - `content_field` (string, non-empty)
  - `url_field` (string, non-empty)
  - `time_field` (string, non-empty)

**Optional config_payload fields:**
- `headers` (object, defaults to empty object)
- `params` (object, defaults to empty object)

**Config summary in responses:**
- `endpoint`: The API endpoint URL
- `method`: The HTTP method
- `response_mapping`: The full response mapping object
- `header_count`: Number of headers (count only, values redacted)
- `param_count`: Number of query params (count only, values redacted)

## Tag Constraints

Tags on datasources follow strict normalization and validation rules:

**Normalization:**
- Tags are converted to lowercase
- Leading and trailing whitespace is stripped
- Empty tags after trimming are discarded
- Tags are sorted alphabetically
- Duplicate tags are removed

**Limits:**
- Maximum 16 unique tags per datasource
- Each tag must be at most 32 characters after normalization

**Validation errors:**
- Exceeding 16 unique tags returns `422 Unprocessable Entity` with message: "tags cannot contain more than 16 unique values"
- Any tag exceeding 32 characters returns `422 Unprocessable Entity` with message: "each tag must be at most 32 characters"

Example: The tags `[" Markets ", "markets", "Layer2"]` normalize to `["layer2", "markets"]`.

## Safe Summaries and Secret Redaction

All datasource responses (create and list) return safe summaries instead of the full config payload. This prevents accidental exposure of sensitive credentials.

### rss and x Summaries

For RSS and X datasources, the config summary includes the URL and type-specific fields without modification.

### rest_api Redaction

For `rest_api` datasources, the following redaction rules apply:

- The `headers` object is replaced with `header_count` (integer)
- The `params` object is replaced with `param_count` (integer)
- The actual header names, parameter names, and their values are never returned
- The `endpoint`, `method`, and `response_mapping` are returned as-is (these are not secrets)

This ensures that API keys, bearer tokens, and other credentials stored in headers or params remain secret while still allowing clients to understand the datasource configuration.

Example redacted response for a rest_api datasource:
```json
{
  "id": "uuid",
  "name": "News API",
  "purpose": "news",
  "source_type": "rest_api",
  "tags": [],
  "config_summary": {
    "endpoint": "https://api.example.com/news",
    "method": "GET",
    "response_mapping": {
      "title_field": "title",
      "content_field": "body",
      "url_field": "url",
      "time_field": "published_at"
    },
    "header_count": 1,
    "param_count": 2
  }
}
```

## Delete Conflict Behavior

Deleting a datasource can fail with `409 Conflict` in the following scenarios:

**Active Ingestion Jobs:**
If there are ingestion jobs for this datasource (matched by `source_type:source_name`) with status `"pending"` or `"running"`, the delete operation is rejected.

**Error response:**
```json
{
  "detail": "Cannot delete datasource 'rss:CoinDesk' while matching ingestion jobs are active"
}
```

**Topic-Datasource Associations:**
If the datasource is associated with any intelligence topic via `intelligence_topic_datasources`, the delete operation is rejected. All associations must be removed first.

**Error response:**
```json
{
  "detail": "Datasource 'ds-uuid' is associated with 3 topic(s) and must be unbound first"
}
```

To delete a datasource with topic associations, either use the topic datasource API to remove the associations, or clear all associations for each topic before deleting the datasource.

## Intelligence Datasource Types

The following source types feed the hidden-channel intelligence pipeline. They store raw text (30-day TTL) and produce canonical knowledge entries through LLM extraction. All secrets **must** be provided via environment variables — never inlined in the config payload.

### telegram_group

Collects messages from allowlisted Telegram chats using Telethon MTProto.

**Required config_payload fields:**
- `name` (string, non-empty)
- `chat_id` (string) **or** `chat_username` (string, with `@` prefix)

**Config payload example (by username):**
```json
{
  "source_type": "telegram_group",
  "config_payload": {
    "name": "Crypto Alpha",
    "chat_username": "@cryptoalpha"
  }
}
```

**Config payload example (by chat ID):**
```json
{
  "source_type": "telegram_group",
  "config_payload": {
    "name": "Private Group",
    "chat_id": "-1001234567890"
  }
}
```

**Constraints:**
- Must provide exactly one of `chat_id` or `chat_username` — not both, not neither
- Cannot enumerate all joined chats; each datasource targets a single explicitly configured chat
- No session strings, API hashes, passwords, or tokens in the payload — those come from environment variables (`TELEGRAM_API_ID`, `TELEGRAM_API_HASH`, `TELEGRAM_STRING_SESSION`)

**Production checklist:**
1. The server must have `TELEGRAM_API_ID`, `TELEGRAM_API_HASH`, and `TELEGRAM_STRING_SESSION` set in environment
2. The Telegram account used for the session must have joined the target chat
3. The account must not have 2FA enabled unless the session was generated with it

### v2ex

Collects topics and replies from V2EX nodes using the official API.

**Required config_payload fields:**
- `name` (string, non-empty)
- `api_version` (string, `"v1"` or `"v2"`)
- `node_allowlist` (array of strings, at least one node name)

**Config payload example (v1, no auth):**
```json
{
  "source_type": "v2ex",
  "config_payload": {
    "name": "V2EX Crypto & AI",
    "api_version": "v1",
    "node_allowlist": ["crypto", "openai"]
  }
}
```

**Config payload example (v2, with PAT):**
```json
{
  "source_type": "v2ex",
  "config_payload": {
    "name": "V2EX Tech",
    "api_version": "v2",
    "node_allowlist": ["programmer"],
    "pat_env_var_name": "V2EX_PAT"
  }
}
```

**Constraints:**
- `api_version` must be `"v1"` or `"v2"` — no HTML/CSS scraping
- `node_allowlist` must be a non-empty array of non-empty strings
- v2 requires `pat_env_var_name` pointing to an environment variable (not the PAT value itself)
- v1 is public and requires no authentication
- Node names are the URL path after `/go/`, e.g. `https://www.v2ex.com/go/crypto` → `"crypto"`

**Rate limits:**
- v1: 120 requests/hour per IP (used for both topics and replies)
- v2: varies by PAT tier
- The crawler tracks `X-Rate-Limit-Remaining` headers and pauses when exhausted

## Error Reference

| Status Code | Scenario | Detail Message Pattern |
|-------------|----------|------------------------|
| 201 | Create success | N/A (returns datasource) |
| 204 | Delete success | N/A (empty body) |
| 200 | List success | N/A (returns list) |
| 401 | Missing or invalid API key | "Invalid API key" |
| 404 | Datasource not found | "Datasource not found" |
| 409 | Duplicate datasource | "Datasource 'type:name' already exists" |
| 409 | Datasource in use | "Cannot delete datasource 'type:name' while matching ingestion jobs are active" |
| 409 | Datasource associated with topics | "Datasource 'id' is associated with N topic(s) and must be unbound first" |
| 422 | Invalid payload structure | Pydantic validation error details |
| 422 | Invalid semantic payload | e.g., "x.type must be one of: list, timeline" |
| 422 | Tag limit exceeded | "tags cannot contain more than 16 unique values" |
| 422 | Tag too long | "each tag must be at most 32 characters" |
| 500 | Internal server error | Exception message |

## Updating

Keep this reference aligned with `crypto_news_analyzer/api_server.py` and `crypto_news_analyzer/datasource_payloads.py`. When the implementation changes, update this document to reflect the current validation rules, redaction behavior, and error responses.
