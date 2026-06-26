---
name: gmail
description: Read, send, and manage Gmail emails, threads, labels, and drafts via Gmail API
author: Google
author-url: https://developers.google.com/gmail/api
version: 1.0.0
tags: ["email", "gmail", "communication", "productivity"]
metadata: {
  "requires": {
    "env": ["GMAIL_CLIENT_ID", "GMAIL_CLIENT_SECRET", "GMAIL_REFRESH_TOKEN"],
    "python_packages": ["google-api-python-client", "google-auth-httplib2", "google-auth-oauthlib"]
  }
}
---

# Gmail Skill

## Overview
Integrate with Gmail to send/receive emails, manage threads and labels, and work with drafts. Uses official Gmail API with OAuth 2.0 authentication.

## Configuration
Set these environment variables:
| Variable | Description |
|----------|-------------|
| `GMAIL_CLIENT_ID` | Google Cloud OAuth client ID |
| `GMAIL_CLIENT_SECRET` | Google Cloud OAuth client secret |
| `GMAIL_REFRESH_TOKEN` | OAuth refresh token for your Gmail account |

## Usage Examples

### Send an email
```json
{
  "tool": "gmail_send",
  "parameters": {
    "to": "recipient@example.com",
    "subject": "Meeting Reminder",
    "body": "Hi there,\n\nJust a reminder about our meeting tomorrow at 10 AM.\n\nBest regards,\nYour AI Assistant",
    "cc": ["cc@example.com"],
    "attachments": ["/workspace/documents/agenda.pdf"]
  }
}
```

### Search for emails
```json
{
  "tool": "gmail_search",
  "parameters": {
    "query": "is:unread subject:invoice after:2026-03-01",
    "max_results": 10,
    "include_body": false
  }
}
```

### Get email details
```json
{
  "tool": "gmail_get_message",
  "parameters": {
    "message_id": "msg_1234567890abcdef",
    "format": "full"
  }
}
```

### List labels
```json
{
  "tool": "gmail_list_labels"
}
```

### Modify message labels
```json
{
  "tool": "gmail_modify_labels",
  "parameters": {
    "message_id": "msg_1234567890abcdef",
    "add_labels": ["STARRED"],
    "remove_labels": ["UNREAD"]
  }
}
```

## Query Operators
Use these in the search query:
- `is:unread` - Unread messages
- `is:starred` - Starred messages
- `from:sender@example.com` - From specific sender
- `to:recipient@example.com` - To specific recipient
- `subject:keyword` - Subject contains keyword
- `after:2026/01/01` - Messages after date
- `before:2026/12/31` - Messages before date
- `has:attachment` - Messages with attachments
