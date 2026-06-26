# Sendivent API Reference

Quick reference for API endpoints, parameters, and response shapes.

---

## Base URLs

| Environment | URL | Key Prefix |
|-------------|-----|------------|
| Production | `https://api.sendivent.com` | `live_*` |
| Sandbox | `https://api-sandbox.sendivent.com` | `test_*` |

---

## Authentication

```
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

---

## Notification Endpoints

### POST /v1/send/{event}

Send a notification to one or more recipients. The event name is in the URL path.

**Request:**

```json
{
  "to": "user@example.com",
  "payload": { "orderNumber": "ORD-123" },
  "language": "en",
  "from": "billing@yourcompany.com",
  "overrides": {
    "email": { "subject": "Custom subject", "reply_to": "support@co.com" },
    "sms": { "sender_id": "MYAPP" }
  }
}
```

**Flexible `to` formats:**

| Format | Example |
|--------|---------|
| Email | `"user@example.com"` |
| Phone | `"+14155551234"` |
| UUID | `"550e8400-e29b-..."` |
| External ID | `"ext_user_123"` |
| Object | `{ "email": "...", "name": "...", "customField": "..." }` |
| Array | `[{ "email": "user1@..." }, { "email": "user2@..." }]` |

**Response (200):**

```json
{
  "success": true,
  "deliveries": [
    { "email": "d4e5f6a7-b8c9-4d0e-a1f2-3b4c5d6e7f8a" },
    { "sms": "a1b2c3d4-e5f6-7890-abcd-ef1234567890" }
  ]
}
```

Each entry in `deliveries` is a `{ channel: uuid }` object.

**Error Response:**

```json
{
  "success": false,
  "deliveries": [],
  "errors": [
    { "code": "INTEGRATION_MISSING", "message": "No email integration configured" }
  ]
}
```

### POST /v1/send/{event}/{channel}

Force delivery to a specific channel. Channels: `email`, `sms`, `slack`, `push`, `telegram`, `whatsapp`, `discord`.

### Idempotency

Header: `X-Idempotency-Key: your-unique-key`

---

## Contact Endpoints

### GET /v1/contacts

List contacts with pagination and search.

| Query Param | Type | Default | Description |
|-------------|------|---------|-------------|
| `limit` | `number` | 50 | Max 100 |
| `offset` | `number` | 0 | Pagination offset |
| `search` | `string` | — | Search email, name, phone |

**Response:**
```json
{
  "success": true,
  "data": {
    "contacts": [{ "uuid": "...", "email": "...", "name": "...", "meta": {} }],
    "total": 150,
    "limit": 50,
    "offset": 0
  }
}
```

### GET /v1/contacts/{identifier}

Find a contact by email, phone, UUID, external_id, or Slack user ID.

### POST /v1/contacts

Create or upsert a contact. At least one identifier required.

| Field | Type | Description |
|-------|------|-------------|
| `email` | `string` | Email address |
| `phone` | `string` | Phone (E.164) |
| `name` | `string` | Display name |
| `externalId` | `string` | Your user ID |
| `avatar` | `string` | Avatar URL |
| `username` | `string` | Username |
| `slack` | `string` | Slack user ID |
| `telegram` | `string` | Telegram user ID |
| `discord` | `string` | Discord user ID |

Unknown fields are stored in `meta` with camelCase conversion.

### PATCH /v1/contacts/{identifier}

Update existing contact. Only provided fields are changed.

### DELETE /v1/contacts/{identifier}

Hard delete (GDPR). Returns `{ "success": true, "deleted": true }`.

### POST /v1/contacts/{identifier}/push-tokens

Body: `{ "token": "ExponentPushToken[...]" }`

### DELETE /v1/contacts/{identifier}/push-tokens

Body: `{ "token": "..." }`

---

## Developer Endpoints

Read-only endpoints for inspecting events, deliveries, and integrations. Same Bearer token auth as other endpoints.

### GET /v1/events

List all notification events for the application.

**Response:**
```json
{
  "success": true,
  "data": {
    "events": [{ "identifier": "user.welcome", "name": "User Welcome", "channels": ["email", "slack"] }]
  }
}
```

### GET /v1/events/{identifier}

Get detailed event configuration including templates and channel settings.

### GET /v1/deliveries

List recent deliveries with filters.

| Query Param | Type | Default | Description |
|-------------|------|---------|-------------|
| `limit` | `number` | 20 | Max results |
| `offset` | `number` | 0 | Pagination offset |
| `event` | `string` | — | Filter by event name |
| `channel` | `string` | — | Filter by channel |
| `status` | `string` | — | `pending`, `sent`, `delivered`, `failed` |

**Response:**
```json
{
  "success": true,
  "data": {
    "deliveries": [...],
    "total": 42,
    "limit": 20,
    "offset": 0
  }
}
```

### GET /v1/deliveries/{uuid}/trace

Full delivery trace with timeline and content snapshot.

### GET /v1/integrations

List channel integrations (secrets stripped).

| Query Param | Type | Description |
|-------------|------|-------------|
| `channel` | `string` | Filter by channel |

**Response:**
```json
{
  "success": true,
  "data": {
    "integrations": [{ "channel": "email", "provider": "ses", "status": "active" }]
  }
}
```

---

## Webhook Endpoints

### POST /v1/webhooks

One endpoint per application. Returns `signing_secret` for HMAC-SHA256 verification.

```json
{
  "url": "https://yourapp.com/webhooks/sendivent",
  "enabled_events": ["delivery.sent", "delivery.failed"],
  "description": "Production webhook"
}
```

**Response (201):**
```json
{
  "success": true,
  "webhook": {
    "uuid": "...",
    "url": "https://...",
    "enabled_events": ["delivery.sent", "delivery.failed"],
    "is_active": true,
    "signing_secret": "whsec_...",
    "created_at": "2026-03-30T..."
  }
}
```

### GET /v1/webhooks

Get current webhook configuration.

### PATCH /v1/webhooks/{uuid}

Update: `url`, `enabled_events`, `is_active`, `description`.

### DELETE /v1/webhooks/{uuid}

Soft delete webhook endpoint.

### Webhook Event Types

| Event | When |
|-------|------|
| `delivery.sent` | Notification dispatched to provider |
| `delivery.delivered` | Provider confirmed delivery (email via SES) |
| `delivery.failed` | Delivery failed permanently |
| `delivery.bounced` | Email bounced |
| `delivery.complained` | Recipient marked as spam |

### Webhook Payload

```json
{
  "event": "delivery.sent",
  "delivery": {
    "uuid": "d4e5f6a7-...",
    "channel": "email",
    "status": "sent",
    "event_name": "order.confirmed",
    "message_id": "ses-id",
    "sent_at": "2026-03-30T12:00:00Z",
    "delivered_at": null,
    "error": null
  },
  "request_id": "req-uuid",
  "timestamp": "2026-03-30T12:00:00Z"
}
```

---

## Error Codes

| Status | Code | Description |
|--------|------|-------------|
| 400 | `VALIDATION_ERROR` | Missing or invalid parameters |
| 401 | `UNAUTHORIZED` | Invalid or missing API key |
| 402 | `QUOTA_EXCEEDED` | Contact quota reached |
| 403 | `FORBIDDEN` | Inactive subscription or addon disabled |
| 404 | `NOT_FOUND` | Resource not found |
| 409 | `CONFLICT` | Already exists (e.g. webhook) |
| 429 | `RATE_LIMITED` | Too many requests |
| 500 | `SERVER_ERROR` | Internal error |
| 502 | `PROVIDER_ERROR` | Third-party provider failed |

### Specific Codes

| Code | Description |
|------|-------------|
| `MISSING_IDENTIFIER` | Contact lacks identifier for channel |
| `INTEGRATION_MISSING` | Channel integration not configured |
| `ADDON_NOT_ENABLED` | SMS/WhatsApp not on plan |
| `UNVERIFIED_SENDER` | Sender not verified |
| `INVALID_EMAIL` | Bad email format |
| `INVALID_PHONE` | Bad phone (use E.164: +1234567890) |
| `EVENT_NOT_FOUND` | Event name doesn't exist |

### Error Response Format

```json
{
  "error": "Event 'order.shipped' not found",
  "code": "EVENT_NOT_FOUND"
}
```

---

## Channels & Identifiers

| Channel | Contact Field | Format | Example |
|---------|--------------|--------|---------|
| Email | `email` | Standard email | `user@example.com` |
| SMS | `phone` | E.164 | `+14155551234` |
| Slack | `slack` | Slack user ID | `U1234ABCD` |
| Push | `push_token` | Provider token | `ExponentPushToken[xxx]` |
| Telegram | `telegram` | Telegram user ID | `123456789` |
| WhatsApp | `phone` | E.164 | `+14155551234` |
| Discord | `discord` | Discord user ID | `123456789012345678` |

---

## Template Variables

Available in Handlebars templates across all channels:

```handlebars
{{contact.name}}              — Contact display name
{{contact.email}}             — Contact email
{{contact.phone}}             — Contact phone
{{contact.meta.fieldName}}    — Custom contact fields (camelCase)
{{payload.key}}               — Event payload data
{{app.name}}                  — Application name
{{sender.name}}               — Sender display name
{{sender.email}}              — Sender email address
{{name | Guest}}              — Fallback: "Guest" if name is empty
```

---

## Rate Limits

| Environment | Requests/Second | Daily Quota |
|-------------|-----------------|------------|
| Production | 100 | 1,000 |
| Sandbox | 10 | 150 |
