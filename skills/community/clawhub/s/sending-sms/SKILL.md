---
name: sending-sms
description: Sends SMS messages via the Sendly API with the Node.js SDK or REST API. Handles single messages, batch sends, scheduling, conversations, and sandbox testing. Applies when sending text messages, notifications, alerts, or reminders via SMS.
---

# Sending SMS with Sendly

## Quick start

```typescript
import Sendly from "@sendly/node";

const sendly = new Sendly(process.env.SENDLY_API_KEY!);

const message = await sendly.messages.send({
  to: "+15551234567",
  text: "Your order has shipped!",
  messageType: "transactional",
});
```

## Authentication

All requests require a Bearer token. Store the API key in `SENDLY_API_KEY` env var.

- `sk_test_*` keys → sandbox mode (no real SMS sent, no credits charged)
- `sk_live_*` keys → production (real SMS on verified numbers)

## REST API

**Base URL:** `https://sendly.live/api/v1`

### Send a message

```bash
curl -X POST https://sendly.live/api/v1/messages \
  -H "Authorization: Bearer $SENDLY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"to": "+15551234567", "text": "Hello!", "messageType": "transactional"}'
```

**Required fields:** `to` (E.164 format), `text`, `messageType` (`transactional` or `marketing`)

**Optional fields:** `metadata` (object, max 4KB), `from` (sender ID)

### Response shape

```json
{
  "id": "msg_abc123",
  "to": "+15551234567",
  "text": "Hello!",
  "status": "sent",
  "segments": 1,
  "creditsUsed": 2,
  "createdAt": "2026-03-31T10:00:00Z"
}
```

### Schedule a message

```bash
curl -X POST https://sendly.live/api/v1/messages/schedule \
  -H "Authorization: Bearer $SENDLY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"to": "+15551234567", "text": "Reminder!", "messageType": "transactional", "scheduledAt": "2026-04-01T14:00:00Z"}'
```

Schedule window: 5 minutes to 5 days in the future.

### Batch send

```bash
curl -X POST https://sendly.live/api/v1/messages/batch \
  -H "Authorization: Bearer $SENDLY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"to": "+15551234567", "text": "Hello"}, {"to": "+15559876543", "text": "Hi"}], "messageType": "transactional"}'
```

Up to 10,000 recipients per batch.

### List messages

```bash
curl "https://sendly.live/api/v1/messages?limit=50" \
  -H "Authorization: Bearer $SENDLY_API_KEY"
```

Supports `limit`, `offset`, `status`, `q` (full-text search).

## Node.js SDK

```bash
npm install @sendly/node
```

```typescript
import Sendly from "@sendly/node";

const sendly = new Sendly(process.env.SENDLY_API_KEY!);

const msg = await sendly.messages.send({ to: "+15551234567", text: "Hello!", messageType: "transactional" });
const scheduled = await sendly.messages.schedule({ to: "+15551234567", text: "Later!", messageType: "transactional", scheduledAt: "2026-04-01T14:00:00Z" });
const batch = await sendly.messages.batch({ messages: [{to: "+15551234567", text: "Hi"}], messageType: "transactional" });
const list = await sendly.messages.list({ limit: 50 });
const single = await sendly.messages.get("msg_abc123");
```

## Message types

- **transactional**: OTP codes, order confirmations, appointment reminders, account alerts. Allowed 24/7.
- **marketing**: Promotions, sales, newsletters. Subject to quiet hours (9pm–8am recipient local time).

Misclassifying marketing as transactional violates TCPA.

## Sandbox testing

Use `sk_test_*` keys with magic phone numbers:

| Number | Behavior |
|---|---|
| +15005550000 | Always succeeds |
| +15005550001 | Invalid number error |
| +15005550002 | Cannot route error |
| +15005550006 | Carrier rejected |

## Credit costs

- US/CA: 2 credits per SMS ($0.02)
- International: varies by country (2–48 credits)
- 1 credit = $0.01

## Conversations API

Messages are automatically threaded into conversations. Use the conversations API for two-way messaging:

```typescript
const convos = await sendly.conversations.list({ status: "active", limit: 20 });
const replies = await sendly.conversations.suggestReplies("conv_abc123");
```

## Full reference

- API docs: https://sendly.live/docs/sms
- SDK docs: https://sendly.live/docs/sdks
- OpenAPI spec: https://sendly.live/openapi.yaml
- Sandbox docs: https://sendly.live/docs/sandbox
