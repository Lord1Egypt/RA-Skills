# SMTP Email Delivery Service Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `smtp-email-delivery-service`

x402 availability: not enabled for this product.

## `send`

Action slug: `send`

Price: `5` credits

Send an email via an SMTP server. Supports plain text and HTML body formats, CC/BCC recipients, file attachments (base64-encoded), and priority levels.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `attachments` | `array` | no | File attachments (max 25MB total). Each object requires filename and base64-encoded content, with optional content_type MIME type. |
| `bcc` | `array` | no | BCC (Blind Carbon Copy) recipients. Hidden from other recipients. |
| `body` | `string` | yes | Email body content. Can be plain text or HTML depending on body_type. |
| `body_type` | `string` | no | Email body format: 'plain' for plain text (default), 'html' for HTML content. |
| `cc` | `array` | no | CC (Carbon Copy) recipients. Visible to all recipients. |
| `from_email` | `string` | no | Sender email address. Defaults to the username from smtp_url. Useful when sending from a different address than the authenticated account. |
| `priority` | `string` | no | Email priority level. Sets the X-Priority header: 'low' (5), 'normal' (3), or 'high' (1). |
| `smtp_url` | `string` | yes | SMTP server URL with credentials. Format: smtp://username:password@hostname:port (STARTTLS, port 587) or smtps://username:password@hostname:port (SSL/TLS, port 465). Gmail requires an App Password. |
| `subject` | `string` | yes | Email subject line. |
| `to` | `array` | yes | Recipient email address(es). At least one is required. Can also accept a single string or comma-separated string. |

Sample parameters:

```json
{
  "attachments": [
    {
      "content": "Draft marketing copy to check for banned phrases.",
      "content_type": "Draft marketing copy to check for banned phrases.",
      "filename": "example filename"
    }
  ],
  "bcc": [
    "example bcc"
  ],
  "body": "example body",
  "body_type": "plain",
  "cc": [
    "example cc"
  ],
  "from_email": "user@example.com",
  "priority": "normal",
  "smtp_url": "https://example.com"
}
```

Generated JSON parameter schema:

```json
{
  "attachments": {
    "description": "File attachments (max 25MB total). Each object requires filename and base64-encoded content, with optional content_type MIME type.",
    "items": {
      "properties": {
        "content": {
          "description": "Base64-encoded file content.",
          "required": true,
          "type": "string"
        },
        "content_type": {
          "description": "MIME type (e.g., application/pdf). Defaults to application/octet-stream.",
          "required": false,
          "type": "string"
        },
        "filename": {
          "description": "File name with extension (e.g., report.pdf).",
          "required": true,
          "type": "string"
        }
      },
      "type": "object"
    },
    "required": false,
    "type": "array"
  },
  "bcc": {
    "description": "BCC (Blind Carbon Copy) recipients. Hidden from other recipients.",
    "items": {
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "body": {
    "description": "Email body content. Can be plain text or HTML depending on body_type.",
    "required": true,
    "type": "string"
  },
  "body_type": {
    "default": "plain",
    "description": "Email body format: 'plain' for plain text (default), 'html' for HTML content.",
    "enum": [
      "plain",
      "html"
    ],
    "required": false,
    "type": "string"
  },
  "cc": {
    "description": "CC (Carbon Copy) recipients. Visible to all recipients.",
    "items": {
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "from_email": {
    "description": "Sender email address. Defaults to the username from smtp_url. Useful when sending from a different address than the authenticated account.",
    "required": false,
    "type": "string"
  },
  "priority": {
    "default": "normal",
    "description": "Email priority level. Sets the X-Priority header: 'low' (5), 'normal' (3), or 'high' (1).",
    "enum": [
      "low",
      "normal",
      "high"
    ],
    "required": false,
    "type": "string"
  },
  "smtp_url": {
    "description": "SMTP server URL with credentials. Format: smtp://username:password@hostname:port (STARTTLS, port 587) or smtps://username:password@hostname:port (SSL/TLS, port 465). Gmail requires an App Password.",
    "required": true,
    "type": "string"
  },
  "subject": {
    "description": "Email subject line.",
    "required": true,
    "type": "string"
  },
  "to": {
    "description": "Recipient email address(es). At least one is required. Can also accept a single string or comma-separated string.",
    "items": {
      "type": "string"
    },
    "required": true,
    "type": "array"
  }
}
```
