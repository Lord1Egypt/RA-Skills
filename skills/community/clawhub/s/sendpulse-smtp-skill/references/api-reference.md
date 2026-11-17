# SMTP REST API reference

Base URL: `https://api.sendpulse.com`
Auth: `Authorization: Bearer <token>` on every request (see quickstart for the
OAuth flow). Content type: `application/json`.
Live documentation (source of truth): https://sendpulse.com/integrations/api/smtp?utm_source=ai-agent&utm_medium=skill&utm_campaign=ai-skills&utm_content=sendpulse-smtp-skill

## Authorization

| Method | Path | Purpose |
|---|---|---|
| — | *Settings → API → API keys* | **Single API Key (preferred)** — long-lived Bearer generated in the dashboard (up to 5 keys, revocable). No token endpoint needed. |
| POST | `/oauth/access_token` | OAuth alternative. Body: `{"grant_type":"client_credentials","client_id":"...","client_secret":"..."}`. Token TTL: 1 hour. |

## Sending

### POST `/smtp/emails` — send an email

Body — a single `email` object:

```json
{
  "email": {
    "subject": "string, required",
    "from":  {"name": "Sender Name", "email": "verified@yourdomain.com"},
    "to":   [{"name": "Recipient", "email": "user@example.com"}],
    "cc":   [{"email": "copy@example.com"}],
    "bcc":  [{"email": "hidden@example.com"}],

    "html": "BASE64-encoded HTML body",
    "text": "plain-text body (always include it)",
    "auto_plain_text": false,

    "template": {"id": 12345, "variables": {"name": "Jane", "order_id": "1234"}},

    "attachments":        {"readme.txt": "plain text file content"},
    "attachments_binary": {"invoice.pdf": "BASE64-encoded file content"}
  }
}
```

Rules:

- Provide **either** `html`(+`text`) **or** `template`. Template variables replace
  `{{placeholders}}` defined in the template stored in SendPulse.
- `html` **must be Base64-encoded**. `text` is plain.
- `to` / `cc` / `bcc` are arrays of `{name?, email}` objects.
- `from.email` must be a **verified sender**.
- `auto_plain_text: true` generates the text part from HTML automatically.

Success: `{"result": true, "id": "<message-id>"}` — persist the `id`.

### Message status & history

| Method | Path | Purpose / parameters |
|---|---|---|
| GET | `/smtp/emails/{id}` | Full info on one sent message: delivery status (`sent`, `delivered`, `bounced`, ...), opens/click tracking. |
| GET | `/smtp/emails` | List of sent messages. Query: `limit`, `offset`, `from` & `to` (date range `YYYY-MM-DD hh:mm:ss`), `sender`, `recipient`. |
| GET | `/smtp/emails/total` | Total count of sent messages. |
| POST | `/smtp/emails/info` | Bulk status: body `{"emails": ["id1", "id2", ...]}` — **max 500 ids** per call. |

## Bounces

| Method | Path | Purpose |
|---|---|---|
| GET | `/smtp/bounces/day` | Bounced emails for the last 24 h (address, reason, type). Poll daily; remove hard bounces from your own list. |
| GET | `/smtp/bounces/day/total` | Count of bounces for the last 24 h. |

## Unsubscribe list (blocklist)

Addresses on this list are never sent to; sends to them are dropped.

| Method | Path | Purpose |
|---|---|---|
| POST | `/smtp/unsubscribe` | Add addresses. Body: `{"emails": [{"email": "a@b.c", "comment": "user clicked unsubscribe"}]}` |
| DELETE | `/smtp/unsubscribe` | Remove addresses. Body: `{"emails": ["a@b.c"]}` |
| GET | `/smtp/unsubscribe` | Full unsubscribed list (`limit`, `offset`, date filters). |
| GET | `/smtp/unsubscribe/search?email=a@b.c` | **Check one address before sending** — the single most useful hygiene call. |
| POST | `/smtp/resubscribe` | Send a confirmation email asking the user to re-subscribe. Params: `email`, `sender`, `lang`. **Hard limit: 5 requests per 24 hours.** |

## Senders, domains, IPs

| Method | Path | Purpose |
|---|---|---|
| GET | `/smtp/senders` | Verified sender emails. |
| POST | `/senders` | Add a sender: `{"email": "...", "name": "..."}` → confirmation email is sent. |
| GET | `/v2/email-service/smtp/sender_domains` | Allowed sender domains. |
| POST | `/v2/email-service/smtp/sender_domains/{domain}` | Add a sender domain. |
| GET | `/smtp/ips` | Outgoing IP addresses assigned to the account. |

## Rate limits

Requests-per-minute quota depends on the pricing tier (free ≈ 1 000/min,
500 000/day; paid tiers higher). Exceeding returns **HTTP 429** — implement
exponential backoff. These are API-call limits; email-volume limits are separate
and come from your SMTP plan.

## Conventions for generated code

- Read `client_id`/`client_secret` from env vars (`SENDPULSE_API_ID`,
  `SENDPULSE_API_SECRET` are good names).
- Cache the token for ~55 min or refresh on 401.
- Log the returned message `id` next to your own entity id (order, user).
- Wrap sends in retry-on-429/5xx with backoff; do NOT retry on 4xx validation errors.
