---
name: temp-email
description: Manage temporary email addresses and messages using the chat-tempmail.com API. Use when the user wants to create disposable emails, check inbox messages, or manage webhooks.
allowed-tools: Bash(curl *), Read
---

# Temporary Email Skill

You manage temporary email addresses via the chat-tempmail.com REST API.

## Authentication

All requests require the `X-API-Key` header. The API key should be in the environment variable `TEMP_EMAIL_API_KEY`.

If the variable is not set, ask the user to provide their API key.

Use this in every curl call:
```
-H "X-API-Key: $TEMP_EMAIL_API_KEY"
```

## Base URL

```
https://chat-tempmail.com
```

## Available Operations

### 1. Get Available Domains
```bash
curl -s https://chat-tempmail.com/api/email/domains -H "X-API-Key: $TEMP_EMAIL_API_KEY"
```

### 2. Create Email
```bash
curl -s -X POST https://chat-tempmail.com/api/emails/generate \
  -H "X-API-Key: $TEMP_EMAIL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "<prefix>", "expiryTime": <ms>, "domain": "<domain>"}'
```
Expiry options: 3600000 (1h), 86400000 (1d), 259200000 (3d), 0 (permanent).

### 3. List Emails
```bash
curl -s "https://chat-tempmail.com/api/emails" -H "X-API-Key: $TEMP_EMAIL_API_KEY"
```
Supports `?cursor=<nextCursor>` for pagination.

### 4. Delete Email
```bash
curl -s -X DELETE "https://chat-tempmail.com/api/emails/<emailId>" -H "X-API-Key: $TEMP_EMAIL_API_KEY"
```

### 5. Get Messages
```bash
curl -s "https://chat-tempmail.com/api/emails/<emailId>" -H "X-API-Key: $TEMP_EMAIL_API_KEY"
```
Supports `?cursor=<nextCursor>` for pagination.

### 6. Get Message Details
```bash
curl -s "https://chat-tempmail.com/api/emails/<emailId>/<messageId>" -H "X-API-Key: $TEMP_EMAIL_API_KEY"
```

### 7. Delete Message
```bash
curl -s -X DELETE "https://chat-tempmail.com/api/emails/<emailId>/<messageId>" -H "X-API-Key: $TEMP_EMAIL_API_KEY"
```

### 8. Get Webhook Config
```bash
curl -s https://chat-tempmail.com/api/webhook -H "X-API-Key: $TEMP_EMAIL_API_KEY"
```

### 9. Configure Webhook
```bash
curl -s -X POST https://chat-tempmail.com/api/webhook \
  -H "X-API-Key: $TEMP_EMAIL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "<webhook_url>", "enabled": true}'
```

## Guidelines

- Always use `-s` flag with curl to suppress progress output.
- Parse JSON responses and present results in a readable format to the user.
- When creating an email, if the user doesn't specify a domain, fetch available domains first and use the first one.
- When creating an email, default to 1 hour expiry unless the user specifies otherwise.
- For paginated results, automatically fetch next pages if the user wants all results.
- For full API details, see [reference.md](reference.md).
