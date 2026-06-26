---
name: ravi-email-send
description: Send, compose, reply, reply-all, or forward emails with HTML formatting and attachments. Do NOT use for reading incoming email (use ravi-inbox) or for credentials (use ravi-passwords or ravi-secrets).
---

# Ravi Email — Send

Compose new emails, reply to existing ones, or forward them from your Ravi email address.

> **Writing quality matters.** Before drafting email content, see the **ravi-email-writing** skill for subject lines, HTML formatting, tone, and anti-spam best practices.

## Resolving Recipients by Name

If you have the recipient's name but not their email address (e.g. "email Alice"), **use ravi-contacts first**:

```bash
# Search contacts by name
ravi contacts search "Alice"
# → Returns matches with email, phone, display_name
# If one match → use the email from the result
# If multiple matches → confirm with the user which Alice they mean
# If no matches → ask the user for the email address directly
```

## Compose a new email

```bash
ravi email compose --to "recipient@example.com" --subject "Subject" --body "<p>HTML content</p>"
```

**Arguments:**
- `--to` (required): Recipient email address
- `--subject` (required): Email subject line
- `--body` (required): Email body (HTML supported — use tags like `<p>`, `<h2>`, `<ul>` for formatting)

**Example with HTML formatting:**
```bash
ravi email compose \
  --to "user@example.com" \
  --subject "Monthly Report" \
  --body "<h2>Monthly Report</h2><p>Key findings:</p><ul><li>Revenue up 15%</li><li>Churn down 3%</li></ul>"
```

## Reply to an email

```bash
# Reply to sender only
ravi email reply <message_id> --body "<p>Reply content</p>"

# Reply to all recipients (reply-all)
ravi email reply-all <message_id> --body "<p>Reply content</p>"
```

## Forward an email

```bash
ravi email forward <message_id> --to "recipient@example.com" --body "<p>FYI — see below.</p>"
```

**Arguments:**
- `--to` (required): Recipient email address
- `--body` (required): Email body (HTML supported)

## Rate Limits

Email sending is rate-limited per user account:
- **60 emails/hour** and **500 emails/day**

On hitting a rate limit, you'll get a 429 response with a `retry_after_seconds` value. Wait that many seconds before retrying.

**Best practices for agents:**
- Avoid tight loops of email sends — batch work where possible
- On 429: parse `retry_after_seconds` from the response body, wait, then retry
- For bulk operations, add a 1-2 second delay between sends

## Important Notes

- **HTML email bodies** — the `--body` argument accepts HTML. Use tags for formatting: `<p>`, `<h2>`, `<ul>`, `<a href="...">`. No `<html>` or `<body>` wrapper needed. See **ravi-email-writing** for templates and anti-spam rules.
- **Subject for replies/forwards** — reply and forward commands auto-derive the subject from the original message (prepending `Re:` or `Fwd:`). No need to pass `--subject`.

## Full API Reference

For complete endpoint details, request/response schemas, and parameters: [Messages](https://ravi.id/docs/schema/messages.json) | [Attachments](https://ravi.id/docs/schema/attachments.json)

## Related Skills

- **ravi-contacts** — Look up a person's email address by name before sending
- **ravi-email-writing** — Subject lines, HTML templates, tone, and anti-spam best practices
- **ravi-inbox** — Read incoming email before replying or forwarding
- **ravi-identity** — Get your email address and identity name for signatures
- **ravi-feedback** — Report deliverability issues or suggest email feature improvements
