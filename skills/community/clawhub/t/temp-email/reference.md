# chat-tempmail.com API Reference

Base URL: `https://chat-tempmail.com`

All endpoints require `X-API-Key` header.

---

## Email API

### GET /api/email/domains

Returns available email domains.

Response:
```json
{ "domains": ["chat-tempmail.com", "example.com"] }
```

### POST /api/emails/generate

Create a temporary email.

Body:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | Yes | Email prefix |
| expiryTime | number | Yes | Expiry in ms: 3600000 (1h), 86400000 (1d), 259200000 (3d), 0 (permanent) |
| domain | string | Yes | Email domain |

Response:
```json
{ "id": "c2c4f894-...", "email": "test@chat-tempmail.com" }
```

### GET /api/emails

List all emails. Supports `?cursor=<nextCursor>` pagination.

Response:
```json
{
  "emails": [
    { "id": "...", "address": "...", "userId": "...", "createdAt": "...", "expiresAt": "..." }
  ],
  "nextCursor": "...",
  "total": 20
}
```

### DELETE /api/emails/{emailId}

Delete an email.

Response: `{ "success": true }`

---

## Message API

### GET /api/emails/{emailId}

List messages for an email. Supports `?cursor=<nextCursor>` pagination.

Response:
```json
{
  "messages": [
    { "id": "...", "from_address": "sender@example.com", "subject": "...", "received_at": 1745224245084 }
  ],
  "nextCursor": "...",
  "total": 50
}
```

### GET /api/emails/{emailId}/{messageId}

Get message details.

Response:
```json
{
  "message": {
    "id": "...",
    "from_address": "sender@example.com",
    "subject": "...",
    "content": "Plain text content",
    "html": "<div>HTML content</div>",
    "received_at": 1745224245084
  }
}
```

### DELETE /api/emails/{emailId}/{messageId}

Delete a message.

Response: `{ "success": true }`

---

## Webhook API

### GET /api/webhook

Get webhook configuration.

Response:
```json
{ "url": "https://your-server.com/webhook", "enabled": true }
```

### POST /api/webhook

Configure webhook.

Body:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| url | string | Yes | Webhook URL (HTTP/HTTPS) |
| enabled | boolean | Yes | Enable/disable webhook |

Response: `{ "success": true }`

### Webhook Event Payload (new_message)

Headers: `Content-Type: application/json`, `X-Webhook-Event: new_message`

```json
{
  "emailId": "...",
  "messageId": "...",
  "fromAddress": "sender@example.com",
  "subject": "Test Message",
  "content": "Plain text",
  "html": "<div>HTML</div>",
  "receivedAt": "2025-01-21T08:30:45.084Z",
  "toAddress": "test@chat-tempmail.com"
}
```

Your server should return 2xx. The system may retry on failure — ensure idempotency.