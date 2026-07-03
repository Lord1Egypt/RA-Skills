# Telegram Instant Messenger Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `telegram-instant-messenger`

x402 availability: not enabled for this product.

## `get_updates`

Action slug: `get-updates`

Price: `2` credits

Fetch incoming updates with persisted cursor and optional media ingestion into File Manager. Returns deep link binding instructions when budget is not yet connected.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `allowed_updates` | `array` | no | Filter update types to receive, e.g. ['message','callback_query'] |
| `cursor_offset` | `integer` | no | Relative offset from cursor-derived start. Negative values look older; positive values skip newer. |
| `ingest_expiration_days` | `integer` | no | File Manager expiration in days for ingested files (1-7). |
| `ingest_files_to_manager` | `boolean` | no | When true, download Telegram photo/document files from returned updates and upload them into AgentPMT File Manager. |
| `ingest_max_files` | `integer` | no | Maximum number of files to ingest from one get_updates response. |
| `limit` | `integer` | no | Maximum number of updates to retrieve (1-100). Default: 100 |
| `mark_as_read` | `boolean` | no | Persist highest unread update_id as read. Defaults to true when unread_only=true. |
| `offset` | `integer` | no | Explicit Telegram update_id offset (absolute). Overrides cursor-derived start when provided. |
| `timeout` | `integer` | no | Long polling timeout in seconds (0-60). Default: 30 |
| `unread_only` | `boolean` | no | When true, return only updates newer than the stored read cursor. |

Sample parameters:

```json
{
  "allowed_updates": [
    "example allowed update"
  ],
  "cursor_offset": 1,
  "ingest_expiration_days": 7,
  "ingest_files_to_manager": true,
  "ingest_max_files": 10,
  "limit": 100,
  "mark_as_read": true,
  "offset": 1
}
```

Generated JSON parameter schema:

```json
{
  "allowed_updates": {
    "description": "Filter update types to receive, e.g. ['message','callback_query']",
    "items": {
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "cursor_offset": {
    "description": "Relative offset from cursor-derived start. Negative values look older; positive values skip newer.",
    "required": false,
    "type": "integer"
  },
  "ingest_expiration_days": {
    "default": 7,
    "description": "File Manager expiration in days for ingested files (1-7).",
    "maximum": 7,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "ingest_files_to_manager": {
    "description": "When true, download Telegram photo/document files from returned updates and upload them into AgentPMT File Manager.",
    "required": false,
    "type": "boolean"
  },
  "ingest_max_files": {
    "default": 10,
    "description": "Maximum number of files to ingest from one get_updates response.",
    "maximum": 25,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "limit": {
    "default": 100,
    "description": "Maximum number of updates to retrieve (1-100). Default: 100",
    "maximum": 100,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "mark_as_read": {
    "description": "Persist highest unread update_id as read. Defaults to true when unread_only=true.",
    "required": false,
    "type": "boolean"
  },
  "offset": {
    "description": "Explicit Telegram update_id offset (absolute). Overrides cursor-derived start when provided.",
    "required": false,
    "type": "integer"
  },
  "timeout": {
    "default": 30,
    "description": "Long polling timeout in seconds (0-60). Default: 30",
    "maximum": 60,
    "minimum": 0,
    "required": false,
    "type": "integer"
  },
  "unread_only": {
    "description": "When true, return only updates newer than the stored read cursor.",
    "required": false,
    "type": "boolean"
  }
}
```

## `send_document`

Action slug: `send-document`

Price: `2` credits

Send a document to the budget's bound Telegram chat via URL/file_id/base64 or File Manager file_id.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `caption` | `string` | no | Document caption (max 1024 characters) |
| `disable_notification` | `boolean` | no | Send message silently (users receive without sound). Default: false |
| `document` | `string` | no | Document as a URL, Telegram file_id, or base64-encoded data. |
| `document_file_id` | `string` | no | AgentPMT File Manager file_id to send as document (alternative to document). |
| `filename` | `string` | no | Document filename. Required when sending base64 document data. |
| `message_thread_id` | `integer` | no | Topic ID for group chats with topics enabled (optional) |
| `parse_mode` | `string` | no | Caption formatting mode: HTML, Markdown, or MarkdownV2 |
| `protect_content` | `boolean` | no | Protect content from forwarding and saving. Default: false |

Sample parameters:

```json
{
  "caption": "example caption",
  "disable_notification": true,
  "document": "example document",
  "document_file_id": "example document file id",
  "filename": "example filename",
  "message_thread_id": 1,
  "parse_mode": "HTML",
  "protect_content": true
}
```

Generated JSON parameter schema:

```json
{
  "caption": {
    "description": "Document caption (max 1024 characters)",
    "required": false,
    "type": "string"
  },
  "disable_notification": {
    "description": "Send message silently (users receive without sound). Default: false",
    "required": false,
    "type": "boolean"
  },
  "document": {
    "description": "Document as a URL, Telegram file_id, or base64-encoded data.",
    "required": false,
    "type": "string"
  },
  "document_file_id": {
    "description": "AgentPMT File Manager file_id to send as document (alternative to document).",
    "required": false,
    "type": "string"
  },
  "filename": {
    "description": "Document filename. Required when sending base64 document data.",
    "required": false,
    "type": "string"
  },
  "message_thread_id": {
    "description": "Topic ID for group chats with topics enabled (optional)",
    "required": false,
    "type": "integer"
  },
  "parse_mode": {
    "description": "Caption formatting mode: HTML, Markdown, or MarkdownV2",
    "enum": [
      "HTML",
      "Markdown",
      "MarkdownV2"
    ],
    "required": false,
    "type": "string"
  },
  "protect_content": {
    "description": "Protect content from forwarding and saving. Default: false",
    "required": false,
    "type": "boolean"
  }
}
```

## `send_message`

Action slug: `send-message`

Price: `2` credits

Send a text message to the budget's bound Telegram chat (shared AgentPMT bot).

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `disable_notification` | `boolean` | no | Send message silently (users receive without sound). Default: false |
| `message_thread_id` | `integer` | no | Topic ID for group chats with topics enabled (optional) |
| `parse_mode` | `string` | no | Text formatting mode: HTML, Markdown, or MarkdownV2 |
| `protect_content` | `boolean` | no | Protect content from forwarding and saving. Default: false |
| `reply_markup` | `object` | no | Inline keyboard markup for interactive buttons. |
| `text` | `string` | yes | Message text (max 4096 characters). Required. |

Sample parameters:

```json
{
  "disable_notification": true,
  "message_thread_id": 1,
  "parse_mode": "HTML",
  "protect_content": true,
  "reply_markup": {},
  "text": "example text"
}
```

Generated JSON parameter schema:

```json
{
  "disable_notification": {
    "description": "Send message silently (users receive without sound). Default: false",
    "required": false,
    "type": "boolean"
  },
  "message_thread_id": {
    "description": "Topic ID for group chats with topics enabled (optional)",
    "required": false,
    "type": "integer"
  },
  "parse_mode": {
    "description": "Text formatting mode: HTML, Markdown, or MarkdownV2",
    "enum": [
      "HTML",
      "Markdown",
      "MarkdownV2"
    ],
    "required": false,
    "type": "string"
  },
  "protect_content": {
    "description": "Protect content from forwarding and saving. Default: false",
    "required": false,
    "type": "boolean"
  },
  "reply_markup": {
    "description": "Inline keyboard markup for interactive buttons.",
    "required": false,
    "type": "object"
  },
  "text": {
    "description": "Message text (max 4096 characters). Required.",
    "required": true,
    "type": "string"
  }
}
```

## `send_photo`

Action slug: `send-photo`

Price: `2` credits

Send a photo to the budget's bound Telegram chat via URL/file_id/base64 or File Manager file_id.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `caption` | `string` | no | Photo caption (max 1024 characters) |
| `disable_notification` | `boolean` | no | Send message silently (users receive without sound). Default: false |
| `message_thread_id` | `integer` | no | Topic ID for group chats with topics enabled (optional) |
| `parse_mode` | `string` | no | Caption formatting mode: HTML, Markdown, or MarkdownV2 |
| `photo` | `string` | no | Photo as a URL, Telegram file_id, or base64-encoded data. |
| `photo_file_id` | `string` | no | AgentPMT File Manager file_id to send as photo (alternative to photo). |
| `protect_content` | `boolean` | no | Protect content from forwarding and saving. Default: false |

Sample parameters:

```json
{
  "caption": "example caption",
  "disable_notification": true,
  "message_thread_id": 1,
  "parse_mode": "HTML",
  "photo": "example photo",
  "photo_file_id": "example photo file id",
  "protect_content": true
}
```

Generated JSON parameter schema:

```json
{
  "caption": {
    "description": "Photo caption (max 1024 characters)",
    "required": false,
    "type": "string"
  },
  "disable_notification": {
    "description": "Send message silently (users receive without sound). Default: false",
    "required": false,
    "type": "boolean"
  },
  "message_thread_id": {
    "description": "Topic ID for group chats with topics enabled (optional)",
    "required": false,
    "type": "integer"
  },
  "parse_mode": {
    "description": "Caption formatting mode: HTML, Markdown, or MarkdownV2",
    "enum": [
      "HTML",
      "Markdown",
      "MarkdownV2"
    ],
    "required": false,
    "type": "string"
  },
  "photo": {
    "description": "Photo as a URL, Telegram file_id, or base64-encoded data.",
    "required": false,
    "type": "string"
  },
  "photo_file_id": {
    "description": "AgentPMT File Manager file_id to send as photo (alternative to photo).",
    "required": false,
    "type": "string"
  },
  "protect_content": {
    "description": "Protect content from forwarding and saving. Default: false",
    "required": false,
    "type": "boolean"
  }
}
```
