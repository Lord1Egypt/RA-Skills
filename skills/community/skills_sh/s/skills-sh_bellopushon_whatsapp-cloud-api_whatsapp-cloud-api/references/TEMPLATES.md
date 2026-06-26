# WhatsApp Cloud API - Message Templates

## Template Categories

| Category           | Purpose                                                    |
| ------------------ | ---------------------------------------------------------- |
| **Marketing**      | Promotions, offers, product announcements                  |
| **Utility**        | Order confirmations, shipping updates, account notifications |
| **Authentication** | OTP codes, verification                                    |

## Template Lifecycle

```
PENDING → APPROVED → REJECTED (or DISABLED)
```

- Templates must be submitted for review before use.
- Meta reviews templates and either approves or rejects them.
- Approved templates can later be disabled by Meta if they violate policies.

## Creating Templates

**Endpoint:** `POST /{WABA_ID}/message_templates`

```json
{
  "name": "order_confirmation",
  "language": "en_US",
  "category": "utility",
  "components": [
    {
      "type": "header",
      "format": "text",
      "text": "Order {{1}}"
    },
    {
      "type": "body",
      "text": "Hi {{1}}, your order #{{2}} has been confirmed. Total: ${{3}}"
    },
    {
      "type": "footer",
      "text": "Thank you for your purchase"
    },
    {
      "type": "buttons",
      "buttons": [
        {
          "type": "URL",
          "text": "Track Order",
          "url": "https://example.com/track/{{1}}"
        }
      ]
    }
  ]
}
```

## Sending Templates

**Endpoint:** `POST /{phone-number-id}/messages`

```json
{
  "messaging_product": "whatsapp",
  "to": "+18091234567",
  "type": "template",
  "template": {
    "name": "order_confirmation",
    "language": { "code": "en_US" },
    "components": [
      {
        "type": "header",
        "parameters": [
          { "type": "text", "text": "ORD-12345" }
        ]
      },
      {
        "type": "body",
        "parameters": [
          { "type": "text", "text": "John" },
          { "type": "text", "text": "ORD-12345" },
          { "type": "text", "text": "49.99" }
        ]
      },
      {
        "type": "button",
        "sub_type": "url",
        "index": 0,
        "parameters": [
          { "type": "text", "text": "ORD-12345" }
        ]
      }
    ]
  }
}
```

## Header Types

| Format       | Description                                              |
| ------------ | -------------------------------------------------------- |
| `text`       | Plain text header with optional variable placeholders    |
| `image`      | Image header (requires media ID or link in parameters)   |
| `video`      | Video header (requires media ID or link in parameters)   |
| `document`   | Document header (requires media ID or link in parameters)|

## Button Types in Templates

| Type             | Behavior                                                    |
| ---------------- | ----------------------------------------------------------- |
| `URL`            | Opens a URL with an optional dynamic suffix                 |
| `PHONE_NUMBER`   | Initiates a phone call to the specified number              |
| `QUICK_REPLY`    | Returns a button payload in the webhook when tapped         |
| `COPY_CODE`      | Copies a code to the clipboard (e.g., coupon codes)         |
| `OTP`            | Delivers a one-time password (authentication templates only)|
