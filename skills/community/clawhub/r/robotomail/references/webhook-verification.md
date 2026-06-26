# Webhook Signature Verification

Robotomail signs every webhook delivery with HMAC-SHA256. Verify the signature to ensure the payload is authentic.

## How It Works

1. When you create a webhook (`POST /v1/webhooks`), the response includes a `secret` (e.g., `whsec_xxxxxxxxxxxx`). Save it — it's shown only once.
2. Each delivery includes an `X-Robotomail-Signature` header containing the HMAC-SHA256 hex digest of the raw JSON body.
3. Compute the expected signature and compare using a timing-safe comparison.

## Webhook Payload Structure

```json
{
  "event": "message.received",
  "timestamp": "2026-03-19T12:00:00Z",
  "data": {
    "message_id": "uuid",
    "mailbox_id": "uuid",
    "mailbox_address": "agent@example.com",
    "from": "sender@company.com",
    "to": ["agent@example.com"],
    "cc": [],
    "subject": "Subject line",
    "body_text": "Plain text content",
    "body_html": "<p>HTML</p>",
    "thread_id": "uuid",
    "in_reply_to": "<original-message-id> | null",
    "headers": {},
    "attachments": [
      {
        "id": "uuid",
        "filename": "document.pdf",
        "content_type": "application/pdf",
        "size_bytes": 245000,
        "url": "https://presigned-download-url..."
      }
    ],
    "received_at": "2026-03-19T12:00:00Z"
  }
}
```

## Verification Examples

### Node.js

```javascript
import crypto from "crypto";

function verifyWebhook(rawBody, signature, secret) {
  const expected = crypto
    .createHmac("sha256", secret)
    .update(rawBody)
    .digest("hex");

  return crypto.timingSafeEqual(
    Buffer.from(signature),
    Buffer.from(expected)
  );
}

// In your request handler:
const signature = req.headers["x-robotomail-signature"];
const isValid = verifyWebhook(req.rawBody, signature, process.env.WEBHOOK_SECRET);

if (!isValid) {
  return res.status(401).json({ error: "Invalid signature" });
}
```

### Python

```python
import hmac
import hashlib

def verify_webhook(raw_body: bytes, signature: str, secret: str) -> bool:
    expected = hmac.new(
        secret.encode(),
        raw_body,
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(signature, expected)

# In your request handler:
signature = request.headers.get("X-Robotomail-Signature", "")
is_valid = verify_webhook(request.data, signature, os.environ["WEBHOOK_SECRET"])

if not is_valid:
    return {"error": "Invalid signature"}, 401
```

### Go

```go
import (
    "crypto/hmac"
    "crypto/sha256"
    "encoding/hex"
)

func verifyWebhook(rawBody []byte, signature, secret string) bool {
    mac := hmac.New(sha256.New, []byte(secret))
    mac.Write(rawBody)
    expected := hex.EncodeToString(mac.Sum(nil))
    return hmac.Equal([]byte(signature), []byte(expected))
}
```

## Webhook Events

| Event | Fires when |
|---|---|
| `message.received` | Inbound email arrives in a mailbox |
| `message.sent` | Outbound email is accepted by the recipient's mail server |
| `message.delivered` | Delivery confirmed |
| `message.bounced` | Outbound email bounced |
| `message.complaint` | Recipient marked email as spam |
