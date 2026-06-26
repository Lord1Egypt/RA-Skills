---
name: Sendivent
description: >
  Sendivent multi-channel notification API. Use when sending notifications via email, SMS, Slack, push, Telegram, WhatsApp, or Discord.
  Triggers on: send notification with sendivent, sendivent api, sendivent contacts, sendivent events, sendivent templates, notification api.
license: MIT
---

# Sendivent Notification API

Send multi-channel notifications, manage contacts, and configure events via REST API.

> **Using Node.js?** See the [SDK Guide](references/sdk-guide.md) for TypeScript examples with the `@appitude/sendivent` package.

**Reference:** [API Guide](references/api-guide.md) | [Official Docs](https://sendivent.com/docs)

## Prerequisites

- [ ] **Create Account** — Sign up at [sendivent.com/signup](https://sendivent.com/signup)
- [ ] **Create Application** — Dashboard > Applications > New Application
- [ ] **Get API Key** — Dashboard > API Keys > Generate ([docs](https://sendivent.com/docs/api-keys))
- [ ] **Set Environment Variable** — `export SENDIVENT_API_KEY=live_your_key_here`
- [ ] **Configure a Channel** — Set up at least one integration (email, SMS, Slack, etc.)
- [ ] **Create an Event** — Dashboard > Events > New Event (e.g. `user.welcome`)

---

## Authentication

All requests require a Bearer token in the `Authorization` header:

```
Authorization: Bearer YOUR_API_KEY
```

**Base URLs:**
- Production: `https://api.sendivent.com`
- Sandbox: `https://api-sandbox.sendivent.com`

**Key Prefixes:**
- `live_*` — Production (real deliveries)
- `test_*` — Sandbox (safe testing)

All POST/PATCH requests must include `Content-Type: application/json`.

---

## Send Notification

### Send to a single recipient

`POST /v1/send/{event}`

The `event` is the event name in the URL path (e.g. `order.confirmed`), not in the body.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `to` | `string \| object` | Yes | Recipient — email, phone, UUID, external_id, or contact object |
| `payload` | `object` | Yes | Template variables (can be `{}` if none) |
| `language` | `string` | No | Template language override (e.g. `sv`, `en`) |
| `from` | `string` | No | Sender override (must be verified) |
| `overrides` | `object` | No | Channel-specific overrides |

**Flexible `to` formats:**
```json
"to": "user@example.com"
"to": "+14155551234"
"to": "550e8400-e29b-41d4-a716-446655440000"
"to": { "email": "user@example.com", "name": "Jane", "tier": "premium" }
```

Any non-standard field in the contact object (like `tier` above) is stored in `meta` and accessible in templates as `{{contact.meta.tier}}`.

**Response:**

```json
{
  "success": true,
  "deliveries": [
    { "email": "d4e5f6a7-b8c9-4d0e-a1f2-3b4c5d6e7f8a" },
    { "sms": "a1b2c3d4-e5f6-7890-abcd-ef1234567890" }
  ]
}
```

Each entry in `deliveries` is a `{ channel: uuid }` object mapping the channel to the delivery UUID.

---

### Send to multiple recipients

`POST /v1/send/{event}`

Pass an array to `to` for personalized multi-recipient sends:

```json
{
  "to": [
    { "email": "user1@example.com", "name": "Alice", "tier": "premium" },
    { "email": "user2@example.com", "name": "Bob", "tier": "free" }
  ],
  "payload": { "company": "ACME" }
}
```

Each contact receives individually compiled templates with their specific data + shared payload.

---

### Force a specific channel

`POST /v1/send/{event}/{channel}`

Channels: `email`, `sms`, `slack`, `push`, `telegram`, `whatsapp`, `discord`

---

### Idempotency

Include `X-Idempotency-Key: your-unique-key` header to prevent duplicate sends. Replayed requests return `X-Idempotent-Replay: true`.

---

### Error response (send)

When a send fails, the response includes an `errors` array:

```json
{
  "success": false,
  "deliveries": [],
  "errors": [
    { "code": "INTEGRATION_MISSING", "message": "No email integration configured" }
  ]
}
```

---

## Contacts

### List contacts

`GET /v1/contacts`

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `limit` | `number` | No | Max 100 (default 50) |
| `offset` | `number` | No | Pagination offset |
| `search` | `string` | No | Search by email, name, or phone |

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

---

### Find contact

`GET /v1/contacts/{identifier}`

Identifier can be: email, phone, UUID, external_id, or Slack user ID.

---

### Create or upsert contact

`POST /v1/contacts`

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `email` | `string` | No* | Email address |
| `phone` | `string` | No* | Phone (E.164 format) |
| `name` | `string` | No | Display name |
| `externalId` | `string` | No | Your system's user ID |
| `avatar` | `string` | No | Avatar URL |
| `username` | `string` | No | Username |
| `slack` | `string` | No | Slack user ID |
| `telegram` | `string` | No | Telegram user ID |
| `discord` | `string` | No | Discord user ID |

*At least one identifier (email, phone, externalId) is required.

Any unknown field is automatically stored in `meta` with camelCase conversion.

---

### Update contact

`PATCH /v1/contacts/{identifier}`

Same fields as create. Only updates provided fields.

---

### Delete contact

`DELETE /v1/contacts/{identifier}`

Hard delete (GDPR compliant). Returns `{ "success": true, "deleted": true }`.

---

### Push tokens

`POST /v1/contacts/{identifier}/push-tokens` — Register token: `{ "token": "ExponentPushToken[...]" }`

`DELETE /v1/contacts/{identifier}/push-tokens` — Remove token: `{ "token": "..." }`

---

## Developer Endpoints

Read-only endpoints for inspecting events, deliveries, and integrations. Available on the customer API with standard Bearer token auth.

### List events

`GET /v1/events`

Returns all notification events for the application.

**Response:**
```json
{
  "success": true,
  "data": {
    "events": [
      { "identifier": "user.welcome", "name": "User Welcome", "channels": ["email", "slack"] }
    ]
  }
}
```

### Get event details

`GET /v1/events/{identifier}`

Returns detailed event configuration including templates and channel settings.

**Response:**
```json
{
  "success": true,
  "data": {
    "event": { "identifier": "user.welcome", "name": "User Welcome", "channels": [...], "templates": [...] }
  }
}
```

### List deliveries

`GET /v1/deliveries`

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `limit` | `number` | No | Max results (default 20) |
| `offset` | `number` | No | Pagination offset |
| `event` | `string` | No | Filter by event name |
| `channel` | `string` | No | Filter by channel |
| `status` | `string` | No | Filter by status: `pending`, `sent`, `delivered`, `failed` |

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

### Get delivery trace

`GET /v1/deliveries/{uuid}/trace`

Returns full delivery trace with timeline and content snapshot.

**Response:**
```json
{
  "success": true,
  "data": {
    "delivery": { "uuid": "...", "channel": "email", "status": "sent", ... },
    "timeline": [
      { "event": "queued", "timestamp": "2026-03-30T12:00:00Z" },
      { "event": "sent", "timestamp": "2026-03-30T12:00:01Z" }
    ]
  }
}
```

### List integrations

`GET /v1/integrations`

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `channel` | `string` | No | Filter by channel |

Returns channel integrations with secrets stripped.

**Response:**
```json
{
  "success": true,
  "data": {
    "integrations": [
      { "channel": "email", "provider": "ses", "status": "active" }
    ]
  }
}
```

---

## Webhooks

Register one webhook endpoint per application to receive delivery status events.

### Event types

- `delivery.sent` — Notification dispatched to provider
- `delivery.delivered` — Provider confirmed delivery (email only via SES)
- `delivery.failed` — Delivery failed permanently
- `delivery.bounced` — Email bounced
- `delivery.complained` — Recipient marked as spam

### Create webhook

`POST /v1/webhooks`

```json
{
  "url": "https://yourapp.com/webhooks/sendivent",
  "enabled_events": ["delivery.sent", "delivery.failed"],
  "description": "Production webhook"
}
```

Response includes `signing_secret` for HMAC-SHA256 verification.

### Other operations

- `GET /v1/webhooks` — Get webhook config
- `PATCH /v1/webhooks/{uuid}` — Update (url, enabled_events, is_active)
- `DELETE /v1/webhooks/{uuid}` — Remove webhook

### Payload format

```json
{
  "event": "delivery.sent",
  "delivery": {
    "uuid": "d4e5f6a7-...",
    "channel": "email",
    "status": "sent",
    "event_name": "order.confirmed",
    "message_id": "ses-message-id",
    "sent_at": "2026-03-30T12:00:00Z",
    "delivered_at": null,
    "error": null
  },
  "request_id": "req-uuid",
  "timestamp": "2026-03-30T12:00:00Z"
}
```

---

## Channels

Sendivent supports 7 channels. Each requires a configured integration.

| Channel | Identifier | Provider |
|---------|-----------|----------|
| Email | `email` | AWS SES, SendGrid, Brevo |
| SMS | `phone` (E.164) | AWS SNS, Cellsynt |
| Slack | `slack` (user ID) | Slack API |
| Push | `push_token` | Expo, FCM, APNs |
| Telegram | `telegram` (user ID) | Telegram Bot API |
| WhatsApp | `phone` (E.164) | WhatsApp Business API |
| Discord | `discord` (user ID) | Discord Bot API |

---

## Template Variables

Templates use Handlebars syntax. Available in all channel templates:

| Variable | Description |
|----------|-------------|
| `{{contact.name}}` | Contact display name |
| `{{contact.email}}` | Contact email |
| `{{contact.phone}}` | Contact phone |
| `{{contact.meta.fieldName}}` | Custom contact fields |
| `{{payload.key}}` | Event payload data |
| `{{app.name}}` | Application name |
| `{{sender.name}}` | Sender name |
| `{{sender.email}}` | Sender email |

**Fallback syntax:** `{{name | Guest}}` — uses "Guest" if `name` is empty.

---

## Error Handling

All errors return JSON:

```json
{
  "error": "Event 'order.shipped' not found",
  "code": "EVENT_NOT_FOUND"
}
```

| Status | Code | Description |
|--------|------|-------------|
| `400` | `VALIDATION_ERROR` | Missing or invalid parameters |
| `401` | `UNAUTHORIZED` | Invalid or missing API key |
| `402` | `QUOTA_EXCEEDED` | Contact quota exceeded — upgrade plan |
| `403` | `FORBIDDEN` | Subscription inactive or addon not enabled |
| `404` | `NOT_FOUND` | Event, contact, or resource not found |
| `409` | `CONFLICT` | Webhook endpoint already exists |
| `429` | `RATE_LIMITED` | Too many requests — retry with backoff |
| `500` | `SERVER_ERROR` | Internal error |
| `502` | `PROVIDER_ERROR` | Third-party provider failed |

### Common error codes

| Code | Description |
|------|-------------|
| `MISSING_IDENTIFIER` | Contact lacks required identifier for channel |
| `INTEGRATION_MISSING` | Channel integration not configured |
| `ADDON_NOT_ENABLED` | SMS/WhatsApp addon not on plan |
| `UNVERIFIED_SENDER` | Sender email/phone not verified |
| `INVALID_EMAIL` | Invalid email format |
| `INVALID_PHONE` | Invalid phone number (must be E.164) |
| `EVENT_NOT_FOUND` | Event name doesn't exist |

---

## Rate Limits

| Environment | Requests/Second | Daily Quota |
|-------------|-----------------|------------|
| Production | 100 | 1,000 |
| Sandbox | 10 | 150 |
