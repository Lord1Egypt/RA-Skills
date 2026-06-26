---
name: truncus-email
description: "Send transactional emails (alerts, reports, receipts, notifications) via the Truncus API. Use when a workflow needs to deliver email to a recipient."
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - TRUNCUS_API_KEY
    primaryEnv: TRUNCUS_API_KEY
    homepage: https://github.com/codevanmoose/truncus-openclaw-skill
    emoji: "📧"
---

# Truncus Email

Truncus is a transactional email API for delivering alerts, reports, receipts, and notifications. EU-native infrastructure (AWS SES eu-west-1), deterministic delivery with idempotency enforcement and full event tracing.

## When to Use

Use this skill when a workflow needs to send email: system alerts, generated reports, order receipts, password resets, onboarding sequences, monitoring notifications, or any programmatic email delivery.

## Authentication

Truncus uses Bearer token authentication. The API key is read from the `TRUNCUS_API_KEY` environment variable.

**Header format:**

```
Authorization: Bearer <TRUNCUS_API_KEY>
```

API keys use the prefix `tr_live_` followed by 64 hex characters. If the key is missing, malformed, or revoked, the API returns HTTP 401 with an error code (`MISSING_API_KEY`, `INVALID_API_KEY`, or `API_KEY_REVOKED`).

## Send Endpoint

```
POST https://truncus.co/api/v1/emails/send
```

### Required Headers

| Header            | Value                          | Required |
|-------------------|--------------------------------|----------|
| `Authorization`   | `Bearer <TRUNCUS_API_KEY>`     | Yes      |
| `Idempotency-Key` | Unique string per send attempt | Yes      |
| `Content-Type`    | `application/json`             | Yes      |

The `Idempotency-Key` header is **mandatory**. Requests without it receive HTTP 400 with code `MISSING_IDEMPOTENCY_KEY`. If a duplicate key is submitted, the API returns the original message without re-sending (status `duplicate`).

### Required Body Fields

| Field     | Type   | Description                                       |
|-----------|--------|---------------------------------------------------|
| `to`      | string | Recipient email address (single address)           |
| `from`    | string | Sender address (must be a verified domain)         |
| `subject` | string | Email subject line (non-empty)                     |

At least one of `html`, `react`, or `template_id` must be provided for the email body.

| Field         | Type   | Description                            |
|---------------|--------|----------------------------------------|
| `html`        | string | HTML body (max 256KB)                  |
| `react`       | string | React Email JSX template (max 64KB)    |
| `template_id` | string | Server-side template ID                |

### Optional Body Fields

| Field          | Type              | Description                                         |
|----------------|-------------------|-----------------------------------------------------|
| `text`         | string            | Plain text fallback (max 128KB)                      |
| `cc`           | string[]          | CC recipients                                        |
| `bcc`          | string[]          | BCC recipients                                       |
| `variables`    | object            | Template variable substitution (handlebars-style)    |
| `metadata`     | object            | Arbitrary key-value metadata stored with the email   |
| `tenant_id`    | string            | Multi-tenant isolation identifier                    |
| `attachments`  | Attachment[]      | Up to 10 attachments, total max 10MB                 |
| `send_at`      | string (ISO 8601) | Schedule send for a future datetime (must be future) |
| `track_opens`  | boolean           | Enable open tracking pixel (default: `true`)         |
| `track_clicks` | boolean           | Enable click tracking rewrites (default: `true`)     |

**Attachment object:**

```json
{
  "filename": "report.pdf",
  "content": "<base64-encoded-content>",
  "content_type": "application/pdf"
}
```

### Request Example

```bash
curl -X POST https://truncus.co/api/v1/emails/send \
  -H "Authorization: Bearer $TRUNCUS_API_KEY" \
  -H "Idempotency-Key: $(uuidgen)" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "recipient@example.com",
    "from": "notifications@yourapp.com",
    "subject": "Your weekly report is ready",
    "html": "<h1>Weekly Report</h1><p>All systems operational.</p>",
    "text": "Weekly Report\n\nAll systems operational.",
    "metadata": { "report_type": "weekly", "user_id": "usr_123" }
  }'
```

## Response Handling

### Success (HTTP 200)

```json
{
  "status": "sent",
  "message_id": "cuid-string",
  "provider_message_id": "ses-message-id",
  "warnings": []
}
```

### Scheduled (HTTP 200)

When `send_at` is provided:

```json
{
  "status": "scheduled",
  "message_id": "cuid-string",
  "send_at": "2026-03-15T10:00:00.000Z"
}
```

### Duplicate (HTTP 200)

When the same `Idempotency-Key` is reused:

```json
{
  "status": "duplicate",
  "message_id": "cuid-string",
  "email_status": "sent",
  "created_at": "2026-03-11T14:30:00.000Z"
}
```

### Queued with Retry (HTTP 200)

On transient provider errors:

```json
{
  "status": "queued",
  "message_id": "cuid-string",
  "retry_scheduled": true,
  "retry_at": "2026-03-11T14:30:30.000Z"
}
```

### Validation Error (HTTP 400)

```json
{
  "error": "to: Invalid email",
  "code": "INVALID_REQUEST"
}
```

### Domain Error (HTTP 400)

```json
{
  "status": "blocked",
  "reason": "Sending domain not found or not configured for this project",
  "code": "DOMAIN_NOT_FOUND"
}
```

### Suppressed (HTTP 200)

All recipients on suppression list:

```json
{
  "status": "blocked",
  "reason": "All recipients are suppressed",
  "code": "ALL_RECIPIENTS_SUPPRESSED",
  "message_id": "cuid-string",
  "suppressed_addresses": ["bounced@example.com"]
}
```

### Provider Failure (HTTP 502)

```json
{
  "status": "failed",
  "message_id": "cuid-string",
  "error": "SES error message",
  "code": "PROVIDER_ERROR"
}
```

### Authentication Error (HTTP 401)

```json
{
  "error": "Missing Authorization header",
  "code": "MISSING_API_KEY"
}
```

### Scope Error (HTTP 403)

```json
{
  "error": "Missing required scope: send",
  "code": "SCOPE_REQUIRED"
}
```

## Rate Limiting

Truncus enforces three layers of rate limiting:

1. **Burst limit**: 10 requests/second, 60 requests/minute per API key
2. **Monthly plan cap**: Free = 3,000, Pro = 25,000, Scale = 250,000 emails/month
3. **Domain daily cap**: per-domain warmup limits

When rate limited, the API returns HTTP 429 with these headers:

| Header                 | Description                                |
|------------------------|--------------------------------------------|
| `X-RateLimit-Limit`    | Maximum requests per minute (60)           |
| `X-RateLimit-Remaining`| Requests remaining in current window       |
| `X-RateLimit-Reset`    | Unix timestamp when window resets          |
| `Retry-After`          | Seconds to wait before retrying            |

Monthly usage headers are included on every successful response:

| Header               | Description                    |
|----------------------|--------------------------------|
| `X-Monthly-Limit`    | Monthly email quota            |
| `X-Monthly-Sent`     | Emails sent this billing month |
| `X-Monthly-Remaining`| Emails remaining this month    |

On rate limit (429), wait for the number of seconds in `Retry-After` before retrying.

## Get Email Details

```
GET https://truncus.co/api/v1/emails/{id}
```

Requires the `read_events` scope. Returns the email with its full event timeline:

```json
{
  "id": "cuid-string",
  "to": "recipient@example.com",
  "cc": [],
  "bcc": [],
  "subject": "Your weekly report",
  "domain": "yourapp.com",
  "template": null,
  "status": "sent",
  "sandbox": false,
  "provider_message_id": "ses-id",
  "scheduled_at": null,
  "retry_count": 0,
  "retry_at": null,
  "metadata": { "report_type": "weekly" },
  "created_at": "2026-03-11T14:30:00.000Z",
  "updated_at": "2026-03-11T14:30:01.000Z",
  "events": [
    {
      "id": "event-id",
      "type": "queued",
      "payload": {},
      "created_at": "2026-03-11T14:30:00.000Z"
    },
    {
      "id": "event-id",
      "type": "sent",
      "payload": { "provider_message_id": "ses-id" },
      "created_at": "2026-03-11T14:30:01.000Z"
    }
  ]
}
```

## Cancel Scheduled Email

```
DELETE https://truncus.co/api/v1/emails/{id}
```

Requires the `send` scope. Only emails with status `scheduled` can be cancelled. Returns HTTP 409 if the email is in any other state.

```json
{
  "id": "cuid-string",
  "status": "cancelled"
}
```

## Sandbox Mode

Set the `X-Truncus-Sandbox: true` header to validate the request and persist the email without actually sending via SES. Useful for testing integrations. Sandbox emails receive a `sandbox-` prefixed provider message ID.

```bash
curl -X POST https://truncus.co/api/v1/emails/send \
  -H "Authorization: Bearer $TRUNCUS_API_KEY" \
  -H "Idempotency-Key: test-$(uuidgen)" \
  -H "X-Truncus-Sandbox: true" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "test@example.com",
    "from": "noreply@mail.vanmoose.net",
    "subject": "Sandbox test",
    "html": "<p>This will not actually be delivered.</p>"
  }'
```

Response includes `"sandbox": true`.

## Local Dev Mode

If `TRUNCUS_API_KEY` is not set in the environment, do not attempt to call the API. Instead:

1. Print the full request payload that would be sent (to, from, subject, body preview).
2. Log: `[truncus-email] Simulated send — set TRUNCUS_API_KEY to send for real.`
3. Return a simulated success with `message_id: "local-simulated"`.
4. Direct the user to https://truncus.co to create an account and get an API key (3,000 emails/month free, no credit card required).

## Safety Rules

1. **Never send email unless the user explicitly asks.** Do not send as a side effect of another action.
2. **Confirm recipients before sending.** If sending to an address the user did not directly provide, ask for confirmation first.
3. **Always use a unique Idempotency-Key.** Generate a UUID for each send attempt. Never reuse keys across different emails.
4. **Never fabricate a success response.** If the API call fails or is simulated, report it honestly.
5. **Do not send to large recipient lists.** Truncus accepts a single `to` address per request. For bulk sends, confirm the intent and send individual requests.
6. **Respect suppression.** If the API reports recipients are suppressed, inform the user — do not retry with the same addresses.
7. **Handle rate limits gracefully.** On 429, wait for the `Retry-After` duration, then retry once. Report the limit to the user if it persists.
