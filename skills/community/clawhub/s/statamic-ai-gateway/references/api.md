# AI Gateway — API Reference

Endpoint contract for the AI Gateway tool execution interface. For tool-specific argument schemas, examples, and behavioral notes, use the `/capabilities/{tool}` endpoint — it is the source of truth.

## Site Credentials

```bash
SITE_URL=$(jq -r '.sites.SITE_NAME.base_url' ~/.config/ai-gateway/sites.json)
SITE_TOKEN=$(jq -r '.sites.SITE_NAME.token' ~/.config/ai-gateway/sites.json)
```

## Endpoints

| Method | Path                              | Purpose                                |
|--------|-----------------------------------|----------------------------------------|
| POST   | `/ai-gateway/execute`             | Execute a tool                         |
| GET    | `/ai-gateway/capabilities`        | List all tools and their enabled state |
| GET    | `/ai-gateway/capabilities/{tool}` | Full usage docs for a specific tool    |

All requests require `Authorization: Bearer {token}`. POST requires `Content-Type: application/json`.

---

## Discovery

### List all tools

```bash
curl -s -H "Authorization: Bearer $SITE_TOKEN" \
  $SITE_URL/ai-gateway/capabilities | jq .
```

Returns each tool's `enabled` state, `target_type`, and `requires_confirmation` flag.

### Get tool usage

```bash
curl -s -H "Authorization: Bearer $SITE_TOKEN" \
  $SITE_URL/ai-gateway/capabilities/entry.upsert | jq .
```

Returns: argument schema with types/required/defaults, validation rules, example request and response, allowed targets, denied fields, and behavioral notes. **Always call this before using a tool for the first time on a site.**

---

## Request Envelope

```json
{
    "tool": "string (required)",
    "arguments": { "(required, tool-specific)" },
    "request_id": "string (optional — echoed in response)",
    "idempotency_key": "string (optional — logged for dedup)",
    "confirmation_token": "string (optional — for confirming gated ops)"
}
```

## Response Envelopes

### Success

```json
{ "ok": true, "tool": "entry.upsert", "result": { "status": "created", ... }, "meta": { "request_id": "..." } }
```

### Error

```json
{ "ok": false, "tool": "...", "error": { "code": "...", "message": "...", "details": { } }, "meta": { } }
```

`error.details` is present only for `validation_failed`.

### Confirmation Required

```json
{
    "ok": false,
    "tool": "cache.clear",
    "error": { "code": "confirmation_required", "message": "..." },
    "confirmation": { "token": "...", "expires_at": "...", "operation_summary": { "tool": "...", "target": "...", "environment": "..." } },
    "meta": {}
}
```

To confirm: resend the exact same request with `"confirmation_token": "..."` added at the envelope top level. Token expires after 60s and is bound to the exact tool + arguments.

---

## Error Codes

| Code                   | HTTP | Meaning                              |
|------------------------|------|--------------------------------------|
| `unauthorized`         | 401  | Missing or invalid bearer token      |
| `forbidden`            | 403  | Target not in allowlist              |
| `tool_not_found`       | 404  | Tool name not registered             |
| `tool_disabled`        | 403  | Tool registered but not enabled      |
| `validation_failed`    | 422  | Bad envelope or tool arguments       |
| `resource_not_found`   | 404  | Target resource doesn't exist        |
| `conflict`             | 409  | Entry already exists                 |
| `rate_limited`         | 429  | Too many requests — back off         |
| `confirmation_required`| 200  | Confirmation token issued            |
| `execution_failed`     | 500  | Tool error — retry or report         |
| `internal_error`       | 500  | Server error — retry or report       |

## Constraints

- `data` must be a JSON object, never an array or primitive.
- Unknown argument keys are rejected with `validation_failed`.
- Default rate limit: 30 req/min on execute, 60 req/min on capabilities.
- Default max request body: 64KB.
- Each site has independent config — capabilities, allowlists, rate limits, and tokens are all per-site.
