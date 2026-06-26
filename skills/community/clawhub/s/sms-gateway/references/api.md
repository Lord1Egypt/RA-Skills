# SMS Gateway API Reference

Base URL: `http://192.168.50.69:8080` (your local instance)

Authentication: HTTP Basic Auth (username:password)

## Endpoints

### Send SMS
```
POST /message
```
Request body:
```json
{
  "phoneNumbers": ["+41787008998"],
  "textMessage": {"text": "Hello!"},
  "withDeliveryReport": true
}
```

Response:
```json
{
  "id": "VdHHQ3nlNwDZ-W9SNuLzm",
  "state": "Pending",
  "phoneNumber": "+41787008998",
  "text": "Hello!",
  "createdAt": "2024-01-15T10:30:00Z"
}
```

### Check Message Status
```
GET /message/{id}
```

### List Messages
```
GET /messages?limit=10
```

### Health Check
```
GET /health/live
GET /health/ready
GET /health
```

### Webhooks
```
GET    /webhooks
POST   /webhooks        {"event": "sms:received", "url": "https://example.com"}
DELETE /webhooks/{event}
```

Webhook events:
- `sms:received` — Incoming SMS
- `sms:delivered` — Delivery confirmation
- `system:ping` — Health ping

## States
- `Pending` — Queued for sending
- `Sent` — Sent to carrier
- `Delivered` — Confirmed delivery
- `Failed` — Failed to send
