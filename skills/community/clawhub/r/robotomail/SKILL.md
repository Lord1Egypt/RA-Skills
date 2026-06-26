---
name: Robotomail
description: >
  Give an AI agent a real inbox and outbound email using Robotomail.
  Use this skill when the user asks you to send email, check inbox, read messages,
  reply to email, manage mailboxes, stream inbound events via SSE, set up email webhooks,
  configure email domains, or perform any email-related task programmatically.
  Trigger words: email, mailbox, inbox, send email, receive email, mail, webhook email,
  SSE, email events, agent inbox, outbound email, email infrastructure.
license: MIT
compatibility: >
  Requires curl (or any HTTP client) and a Robotomail API key.
  Sign up at https://robotomail.com or via the API.
metadata:
  author: Robotomail
  version: 1.0.6
  website: https://robotomail.com
  openclaw:
    requires:
      env:
        - ROBOTOMAIL_API_KEY
    primaryEnv: ROBOTOMAIL_API_KEY
---

# Robotomail — Give Your AI Agent a Real Inbox

Robotomail lets an AI agent send, receive, and react to email programmatically. It is API-first email infrastructure for autonomous agents, assistants, and workflows.

Use Robotomail when you want an agent to:

- send outbound email, reminders, updates, or follow-ups
- read inbound email from a real inbox
- react to incoming email via webhooks or real-time SSE events
- reply in existing threads using normal email semantics
- use a hosted `robotomail.co` address or a custom domain

## Best-fit use cases

### 1. Agent support inbox
Give your agent a real inbox so it can classify, summarize, draft, or reply to incoming support emails.

### 2. Outbound follow-ups and reminders
Let an agent send reminders, nudges, receipts, booking confirmations, or outbound follow-ups from its own mailbox.

### 3. Real-time email triggers
Subscribe to inbound email events with webhooks or SSE so your agent can wake up and act immediately.

## Fast start

If the user is new to Robotomail, the fastest path is:

1. Sign up at `https://robotomail.com` or create an account via `POST /v1/signup`
2. Create or list a mailbox with `GET /v1/mailboxes` or `POST /v1/mailboxes`
3. Send a test email with `POST /v1/mailboxes/{id}/messages`
4. Read inbound email with `GET /v1/mailboxes/{id}/messages?direction=INBOUND`
5. Subscribe to inbound events via webhook or SSE

> **New accounts start inert.** A fresh `POST /v1/signup` returns an API key, but the account owner must verify the signup email **and** add a card (a 3-day Developer trial, no charge until it ends) before the key works — until then product calls (steps 2–5) return `402 PAYMENT_REQUIRED`. Call `POST /v1/billing/upgrade` for a checkout URL and share it with the owner.

## Authentication

All requests require an API key in the `Authorization` header:

```
Authorization: Bearer <ROBOTOMAIL_API_KEY>
```

**Base URL:** `https://api.robotomail.com`

If the user doesn't have an API key yet, they can sign up at https://robotomail.com or you can create an account via `POST /v1/signup`.

## Quick Reference — What Can I Do?

| Task | Method | Endpoint |
|---|---|---|
| Send an email | POST | `/v1/mailboxes/{id}/messages` |
| List inbox messages | GET | `/v1/mailboxes/{id}/messages?direction=INBOUND` |
| Read a specific message | GET | `/v1/mailboxes/{id}/messages/{msgId}` |
| List conversation threads | GET | `/v1/mailboxes/{id}/threads` |
| Read a thread | GET | `/v1/mailboxes/{id}/threads/{tid}` |
| List mailboxes | GET | `/v1/mailboxes` |
| Create a mailbox | POST | `/v1/mailboxes` |
| Add a custom domain | POST | `/v1/domains` |
| Verify domain DNS | POST | `/v1/domains/{id}/verify` |
| Set up a webhook | POST | `/v1/webhooks` |
| Stream events with SSE | GET | `/v1/events` |
| Upload an attachment | POST | `/v1/attachments` (multipart) |
| Download an attachment | GET | `/v1/attachments/{id}` |
| Check account & usage | GET | `/v1/account` |

For full endpoint details including request/response schemas, read `references/api-reference.md`.

## Webhooks vs SSE

Use **webhooks** when Robotomail should push events to your public HTTPS endpoint.

Use **SSE** when the agent wants a live event stream over a single long-lived connection, for example when running a local listener or agent loop.

If the user says things like "stream inbound mail", "listen for new messages", or "real-time inbox events", prefer SSE.

## Decision Tree — Common Tasks

### "Send an email"

1. List mailboxes: `GET /v1/mailboxes` — find the mailbox to send from
2. Send: `POST /v1/mailboxes/{id}/messages` with `to`, `subject`, `bodyText` (and optionally `bodyHtml`)
3. To reply to an existing message, include `inReplyTo` with the original message's `messageId` header value

### "Check my inbox" / "Read my email"

1. List mailboxes: `GET /v1/mailboxes`
2. Fetch inbound messages: `GET /v1/mailboxes/{id}/messages?direction=INBOUND`
3. Read a specific message: `GET /v1/mailboxes/{id}/messages/{msgId}`

### "Reply to an email"

1. Read the original message to get its `messageId` field
2. Send reply: `POST /v1/mailboxes/{id}/messages` with `inReplyTo` set to the original's `messageId` value
3. Threading is automatic — the reply joins the same thread

### "Set up email for a new domain"

1. Add domain: `POST /v1/domains` with `{"domain": "example.com"}`
2. Read the `dnsRecords` from the response — tell the user to configure these at their DNS provider
3. After DNS is configured, verify: `POST /v1/domains/{id}/verify`
4. Once verified, create a mailbox: `POST /v1/mailboxes` with `{"address": "agent", "domainId": "<id>"}`

### "Set up a webhook for incoming email"

1. Create webhook: `POST /v1/webhooks` with `url` and `events: ["message.received"]`
2. Save the `secret` from the response, it is shown only once
3. Verify deliveries with `X-Robotomail-Signature` header (HMAC-SHA256 of payload using secret)

See `references/webhook-verification.md` for signature verification code.

### "Listen for incoming email in real time" / "Use SSE"

1. Connect to `GET /v1/events`
2. Filter or react to `message.received`, `message.delivered`, `message.bounced`, and `message.complaint`
3. Use SSE when the agent wants a live stream instead of public webhook delivery

### "Send an email with an attachment"

1. Upload the file: `POST /v1/attachments` (multipart/form-data, field name `file`, max 25MB)
2. Note the returned attachment `id`
3. Send the message with `attachments: ["<attachment-id>"]`

### "Read an inbound email's attachments" / "Handle inline images"

Inbound messages with attachments expose them on two surfaces with **different shapes**. Pick the right one for your access pattern — do not assume REST responses contain ready-to-use download URLs.

1. **Webhook / SSE `message.received` payload** — `data.attachments[]` is delivered with a ready-to-use `download_url` field (presigned R2 URL, valid 24h from publish time) on each attachment, alongside `id`, `filename`, `content_type`, `size_bytes`, and `content_id`. Field names are snake_case. Fetch each file directly — no Authorization header needed:
   ```
   for att in event.data.attachments:
       bytes = HTTP_GET(att.download_url)
       save_to(att.filename, bytes)
   ```
2. **REST `GET /v1/mailboxes/{id}/messages` and `GET /v1/mailboxes/{id}/messages/{msgId}`** — `attachments[]` contains **metadata only** (`id`, `filename`, `contentType`, `sizeBytes`, `contentId`), no URL field. To download, call `GET /v1/attachments/{id}` for each attachment id and use the `url` field on that response. Field names are camelCase. This is also how you refresh an expired `download_url` from an old webhook/SSE replay.

**Inline images:** when an attachment's `content_id` (snake_case in webhook/SSE) or `contentId` (camelCase in REST) is non-null, the attachment is referenced in `body_html` / `bodyHtml` as `<img src="cid:<content_id>">`. Rewrite each `cid:` reference to a real downloadable URL before passing the HTML to a renderer or vision model. From a webhook/SSE payload (where `download_url` is already on the attachment):
```
for att in event.data.attachments where att.content_id is not None:
    body_html = body_html.replace(f"cid:{att.content_id}", att.download_url)
```
From a REST message read, fetch a presigned URL per inline attachment first:
```
for att in message.attachments where att.contentId is not None:
    url = GET(f"/v1/attachments/{att.id}").url
    bodyHtml = bodyHtml.replace(f"cid:{att.contentId}", url)
```

**Drop limits:** if a message has more than 20 attachments, or any single attachment exceeds 25 MB, the payload includes `attachments_dropped: true` and `attachments_dropped_reason: "size" | "count" | "both"`. The message itself is still delivered, but the over-limit attachments are not stored. Tell the user if you see this flag.

## Key Constraints

- **Daily send limits:** 500/day (Developer), up to 2,000/day on higher tiers, per mailbox — resets at midnight UTC
- **Monthly send limits:** 15,000/month (Developer), unlimited (Growth, Scale) per mailbox
- **Velocity limits:** 30 messages/min per mailbox, 60 messages/min per account — returns `429` if exceeded
- **Bounce rate:** Must stay below 3% over a 7-day rolling window (minimum 50 messages). Exceeding this auto-suspends the mailbox.
- **Complaint rate:** Must stay below 0.05% over a 7-day rolling window (minimum 50 messages). Exceeding this auto-suspends the mailbox.
- **Attachment size:** Max 25MB per file
- **Storage:** 10GB (Developer), 25GB (Growth), 100GB (Scale)
- **Plans start at $19/mo (Developer):** 10 mailboxes on `robotomail.co` plus custom domains; Growth and Scale add more

If a send returns `429`, the mailbox has hit its daily/monthly limit or velocity limit. Tell the user and suggest slowing down or upgrading to a higher tier.

## Error Handling

All errors return `{"error": "message"}` with standard HTTP status codes:

- `401` — Missing or invalid API key
- `403` — Account suspended or scoped key accessing a restricted resource. When suspended, response includes `{ "suspended": true, "reason": "bounce_rate_exceeded" }`. Tell the user to contact support@robotomail.com.
- `404` — Resource not found
- `429` — Rate limit, velocity limit, or send quota exceeded
- `413` — Attachment too large

## Tips

- Always use `bodyText` for the plain-text version. Add `bodyHtml` only when rich formatting is needed.
- Use threads (`GET /v1/mailboxes/{id}/threads/{tid}`) to see full conversation history before replying.
- When listing messages, use `since` parameter (ISO-8601) to fetch only recent messages.
- Suppression list (`GET /v1/suppressions`) contains bounced/complained addresses — check before sending to addresses that previously failed.
