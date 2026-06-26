# Webhooks Reference

> Complete reference for WhatsApp Cloud API webhook verification, incoming message
> payloads, status updates, and processing best practices.

---

## Webhook Verification (GET)

When you configure a webhook URL in the Meta App Dashboard, Meta sends a **GET** request
to verify that your server owns the endpoint. Your server must validate the request and
respond correctly for the webhook to be registered.

### Verification Request Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| `hub.mode` | `"subscribe"` | Always set to `subscribe` for webhook setup |
| `hub.verify_token` | Your configured token | The token you defined in the App Dashboard |
| `hub.challenge` | Random string | A challenge string that must be returned |

### Verification Flow

1. Meta sends a GET request to your webhook URL with the three query parameters above.
2. Your server compares `hub.verify_token` against your stored verify token.
3. If the tokens match, return the `hub.challenge` value with HTTP status **200**.
4. If the tokens do not match, return HTTP status **403** (Forbidden).

### Implementation Example

```typescript
// GET /webhook
function verifyWebhook(req: Request, res: Response): void {
  const mode = req.query['hub.mode'];
  const token = req.query['hub.verify_token'];
  const challenge = req.query['hub.challenge'];

  if (mode === 'subscribe' && token === process.env.WEBHOOK_VERIFY_TOKEN) {
    // Verification successful — return the challenge string
    res.status(200).send(challenge);
  } else {
    // Verification failed — token mismatch
    res.status(403).send('Forbidden');
  }
}
```

> **Important:** The verify token is a secret you define yourself. It is NOT the same
> as your Graph API access token. Store it securely in environment variables.

---

## Incoming Message Webhook (POST)

When a user sends a message to your WhatsApp Business number, Meta delivers a POST
request to your webhook URL with the full message payload.

### Full Payload Structure

```json
{
  "object": "whatsapp_business_account",
  "entry": [
    {
      "id": "WHATSAPP_BUSINESS_ACCOUNT_ID",
      "changes": [
        {
          "value": {
            "messaging_product": "whatsapp",
            "metadata": {
              "display_phone_number": "16505555555",
              "phone_number_id": "PHONE_NUMBER_ID"
            },
            "contacts": [
              {
                "profile": {
                  "name": "John Doe"
                },
                "wa_id": "16315555555"
              }
            ],
            "messages": [
              {
                "from": "16315555555",
                "id": "wamid.ABC",
                "timestamp": "1683229471",
                "type": "text",
                "text": {
                  "body": "Hello"
                }
              }
            ]
          },
          "field": "messages"
        }
      ]
    }
  ]
}
```

### Payload Field Reference

| Field | Type | Description |
|-------|------|-------------|
| `object` | `string` | Always `"whatsapp_business_account"` |
| `entry[].id` | `string` | WhatsApp Business Account ID |
| `entry[].changes[].field` | `string` | Always `"messages"` for message events |
| `value.messaging_product` | `string` | Always `"whatsapp"` |
| `value.metadata.display_phone_number` | `string` | Your business phone number |
| `value.metadata.phone_number_id` | `string` | Phone Number ID used for API calls |
| `value.contacts[].profile.name` | `string` | Sender's WhatsApp profile name |
| `value.contacts[].wa_id` | `string` | Sender's canonical WhatsApp ID (E.164, no `+`) |
| `value.messages[].from` | `string` | Sender's phone number |
| `value.messages[].id` | `string` | Unique message ID (e.g., `wamid.HBgL...`) |
| `value.messages[].timestamp` | `string` | Unix timestamp (seconds) as a string |
| `value.messages[].type` | `string` | Message type (see section below) |

### Extracting the Message

```typescript
// Extract the first message from a webhook payload
function extractMessage(body: WebhookPayload) {
  const entry = body.entry?.[0];
  const changes = entry?.changes?.[0];
  const value = changes?.value;

  if (!value?.messages?.length) {
    return null; // Not a message event (could be a status update)
  }

  return {
    phoneNumberId: value.metadata.phone_number_id,
    senderName: value.contacts?.[0]?.profile?.name ?? 'Unknown',
    senderPhone: value.messages[0].from,
    messageId: value.messages[0].id,
    timestamp: value.messages[0].timestamp,
    type: value.messages[0].type,
    message: value.messages[0],
  };
}
```

---

## Message Types in Webhooks

Each incoming message has a `type` field. The message content is nested under a key
matching that type name.

### Text Message

```json
{
  "type": "text",
  "text": {
    "body": "Hello, I need help with my order"
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `text.body` | `string` | The text content of the message |

### Image Message

```json
{
  "type": "image",
  "image": {
    "id": "MEDIA_ID",
    "mime_type": "image/jpeg",
    "sha256": "HASH",
    "caption": "Check this out"
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `image.id` | `string` | Media ID — use to download via Media API |
| `image.mime_type` | `string` | MIME type (e.g., `image/jpeg`, `image/png`) |
| `image.sha256` | `string` | SHA-256 hash of the media file |
| `image.caption` | `string` | Optional caption text |

### Video Message

```json
{
  "type": "video",
  "video": {
    "id": "MEDIA_ID",
    "mime_type": "video/mp4"
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `video.id` | `string` | Media ID — use to download via Media API |
| `video.mime_type` | `string` | MIME type (e.g., `video/mp4`) |

### Audio Message

```json
{
  "type": "audio",
  "audio": {
    "id": "MEDIA_ID",
    "mime_type": "audio/ogg; codecs=opus"
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `audio.id` | `string` | Media ID — use to download via Media API |
| `audio.mime_type` | `string` | MIME type (e.g., `audio/ogg; codecs=opus`, `audio/mpeg`) |

### Document Message

```json
{
  "type": "document",
  "document": {
    "id": "MEDIA_ID",
    "filename": "invoice.pdf",
    "mime_type": "application/pdf"
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `document.id` | `string` | Media ID — use to download via Media API |
| `document.filename` | `string` | Original filename provided by the sender |
| `document.mime_type` | `string` | MIME type (e.g., `application/pdf`) |

### Location Message

```json
{
  "type": "location",
  "location": {
    "latitude": 18.4861,
    "longitude": -69.9312,
    "name": "Santo Domingo",
    "address": "Av. Winston Churchill, Santo Domingo"
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `location.latitude` | `number` | Latitude coordinate |
| `location.longitude` | `number` | Longitude coordinate |
| `location.name` | `string` | Optional location name |
| `location.address` | `string` | Optional address text |

### Contacts Message

```json
{
  "type": "contacts",
  "contacts": [
    {
      "name": { "formatted_name": "Jane Smith", "first_name": "Jane", "last_name": "Smith" },
      "phones": [{ "phone": "+18091234567", "type": "CELL" }],
      "emails": [{ "email": "jane@example.com", "type": "WORK" }]
    }
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `contacts` | `array` | Array of contact card objects |
| `contacts[].name` | `object` | Name fields (`formatted_name`, `first_name`, `last_name`) |
| `contacts[].phones` | `array` | Phone numbers with type |
| `contacts[].emails` | `array` | Email addresses with type |

### Interactive Message (Reply)

When a user taps a button or selects a list item from an interactive message you sent,
the reply arrives as an `interactive` type.

**Button Reply:**

```json
{
  "type": "interactive",
  "interactive": {
    "type": "button_reply",
    "button_reply": {
      "id": "btn_yes",
      "title": "Yes"
    }
  }
}
```

**List Reply:**

```json
{
  "type": "interactive",
  "interactive": {
    "type": "list_reply",
    "list_reply": {
      "id": "option_1",
      "title": "Option 1",
      "description": "First option description"
    }
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `interactive.type` | `string` | Either `"button_reply"` or `"list_reply"` |
| `interactive.button_reply.id` | `string` | Button ID you defined when sending |
| `interactive.button_reply.title` | `string` | Button label text |
| `interactive.list_reply.id` | `string` | List row ID you defined when sending |
| `interactive.list_reply.title` | `string` | List row title |
| `interactive.list_reply.description` | `string` | List row description |

### Button Message (Quick Reply from Template)

When a user taps a quick reply button on a **template message**, the response arrives
as a `button` type (not `interactive`).

```json
{
  "type": "button",
  "button": {
    "text": "Yes, confirm",
    "payload": "CONFIRM_ORDER_123"
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `button.text` | `string` | Button label text |
| `button.payload` | `string` | Developer-defined payload string |

> **Note:** `button` (template quick replies) and `interactive.button_reply` (interactive
> message buttons) are different types. Handle them separately.

---

## Status Update Webhooks

Status updates are delivered to the same webhook endpoint as incoming messages. They
appear in the `statuses` array instead of the `messages` array.

### Status Lifecycle

```
sent → delivered → read
                 ↘ failed
```

A message progresses through `sent` → `delivered` → `read` under normal conditions.
If delivery fails, a `failed` status is sent instead of `delivered`.

### Status Payload Structure

```json
{
  "object": "whatsapp_business_account",
  "entry": [
    {
      "id": "WHATSAPP_BUSINESS_ACCOUNT_ID",
      "changes": [
        {
          "value": {
            "messaging_product": "whatsapp",
            "metadata": {
              "display_phone_number": "16505555555",
              "phone_number_id": "PHONE_NUMBER_ID"
            },
            "statuses": [
              {
                "id": "wamid.XXX",
                "status": "delivered",
                "timestamp": "1638420000",
                "recipient_id": "16315551234",
                "conversation": {
                  "id": "CONV_ID",
                  "origin": {
                    "type": "business_initiated"
                  }
                },
                "pricing": {
                  "billable": true,
                  "pricing_model": "CBP",
                  "category": "marketing"
                }
              }
            ]
          },
          "field": "messages"
        }
      ]
    }
  ]
}
```

### Status Field Reference

| Field | Type | Description |
|-------|------|-------------|
| `statuses[].id` | `string` | The `wamid` of the original message |
| `statuses[].status` | `string` | Status value (see table below) |
| `statuses[].timestamp` | `string` | Unix timestamp (seconds) as a string |
| `statuses[].recipient_id` | `string` | Recipient phone number |
| `statuses[].conversation.id` | `string` | Conversation ID for billing |
| `statuses[].conversation.origin.type` | `string` | Who initiated: `business_initiated`, `user_initiated`, `referral_conversion` |
| `statuses[].pricing.billable` | `boolean` | Whether this conversation incurs a charge |
| `statuses[].pricing.pricing_model` | `string` | Pricing model (e.g., `"CBP"` for conversation-based pricing) |
| `statuses[].pricing.category` | `string` | Conversation category: `marketing`, `utility`, `authentication`, `service` |

### Status Values

| Status | Description |
|--------|-------------|
| `sent` | Message accepted by the WhatsApp server |
| `delivered` | Message delivered to the recipient's device |
| `read` | Recipient opened and viewed the message |
| `failed` | Message could not be delivered (see `errors` array) |
| `deleted` | Customer deleted their copy of the message |
| `warning` | Non-fatal issue occurred (see `errors` array for details) |

### Failed Status — Error Details

When a message fails, the status payload includes an `errors` array:

```json
{
  "statuses": [
    {
      "id": "wamid.XXX",
      "status": "failed",
      "timestamp": "1638420000",
      "recipient_id": "16315551234",
      "errors": [
        {
          "code": 131047,
          "title": "Re-engagement message",
          "message": "More than 24 hours have passed since the recipient last replied.",
          "error_data": {
            "details": "Recipient must message you first or use a template."
          }
        }
      ]
    }
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `errors[].code` | `number` | Error code (see ERROR-CODES.md for full reference) |
| `errors[].title` | `string` | Short error description |
| `errors[].message` | `string` | Detailed error message |
| `errors[].error_data.details` | `string` | Additional context or resolution guidance |

### Distinguishing Messages from Statuses

A webhook payload contains **either** `messages` or `statuses` — not both. Check which
array is present to determine the event type:

```typescript
function handleWebhook(body: WebhookPayload): void {
  const value = body.entry?.[0]?.changes?.[0]?.value;

  if (value?.messages?.length) {
    // Incoming message from a customer
    handleIncomingMessage(value);
  } else if (value?.statuses?.length) {
    // Status update for a message you sent
    handleStatusUpdate(value);
  }
}
```

---

## Best Practices

### 1. Return 200 Immediately, Process Asynchronously

Always return HTTP 200 to the webhook POST request **before** processing the payload.
If your server takes too long to respond (or returns an error), Meta will retry the
delivery and may eventually deactivate your webhook.

```typescript
// Correct: respond immediately, process in background
app.post('/webhook', (req, res) => {
  res.status(200).send('OK');
  processWebhookAsync(req.body); // Non-blocking
});
```

### 2. Handle Duplicate Deliveries (Idempotency)

Meta may deliver the same webhook event more than once. Use the message ID (`wamid`)
as an idempotency key to avoid processing duplicates.

```typescript
async function processMessage(message: IncomingMessage): Promise<void> {
  const alreadyProcessed = await messageStore.exists(message.id);
  if (alreadyProcessed) {
    return; // Skip duplicate
  }

  await messageStore.save(message.id);
  // Process the message...
}
```

### 3. Check Timestamps for Ordering

Webhook notifications may arrive **out of order**. A `read` status could arrive before
the corresponding `delivered` status. Use the `timestamp` field to determine the correct
chronological sequence.

```typescript
function shouldUpdateStatus(currentTimestamp: string, newTimestamp: string): boolean {
  return parseInt(newTimestamp, 10) >= parseInt(currentTimestamp, 10);
}
```

### 4. Store Message IDs for Reply Context

Save the `wamid` of incoming messages so you can reference them when sending replies,
reactions, or marking messages as read.

```typescript
// Reply to a specific message using context
const replyPayload = {
  messaging_product: 'whatsapp',
  to: senderPhone,
  type: 'text',
  context: {
    message_id: originalMessageId, // wamid of the message being replied to
  },
  text: { body: 'Thanks for your message!' },
};
```

### 5. Validate the Payload Signature

Meta signs each webhook payload with a SHA-256 HMAC using your App Secret. Always
validate the `X-Hub-Signature-256` header to confirm the request is authentic.

```typescript
import crypto from 'crypto';

function verifySignature(payload: string, signature: string, appSecret: string): boolean {
  const expectedSignature = crypto
    .createHmac('sha256', appSecret)
    .update(payload)
    .digest('hex');

  return `sha256=${expectedSignature}` === signature;
}
```

### 6. Handle All Message Types

Design your webhook handler to gracefully process every message type. If your application
does not support a specific type (e.g., location), acknowledge it rather than failing
silently.

```typescript
function routeByType(message: IncomingMessage): void {
  switch (message.type) {
    case 'text':
      handleText(message.text);
      break;
    case 'image':
    case 'video':
    case 'audio':
    case 'document':
      handleMedia(message);
      break;
    case 'interactive':
      handleInteractive(message.interactive);
      break;
    case 'button':
      handleButton(message.button);
      break;
    case 'location':
      handleLocation(message.location);
      break;
    case 'contacts':
      handleContacts(message.contacts);
      break;
    default:
      logUnsupportedType(message.type);
  }
}
```

---

## See Also

- [MESSAGING.md](MESSAGING.md) — Sending all message types
- [TEMPLATES.md](TEMPLATES.md) — Template message management
- [ERROR-CODES.md](ERROR-CODES.md) — Error codes and retry strategies
- [CONVERSATIONS.md](CONVERSATIONS.md) — Conversation windows and pricing
