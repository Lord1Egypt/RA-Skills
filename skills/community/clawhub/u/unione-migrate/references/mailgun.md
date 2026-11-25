# Migrate from Mailgun to UniOne

| Mailgun (`POST /v3/<domain>/messages`, form data) | UniOne (`email/send`, JSON) |
|---|---|
| Basic auth `api:<key>` | `X-API-KEY: …` |
| `from` = `Name <email>` | `from_name`, `from_email` |
| `to` (comma-separated) | `recipients[]` — each gets its own copy |
| `cc`, `bcc` | add to `recipients[]`; visible ones in `headers.To` / `headers.CC` |
| `recipient-variables` + `%recipient.name%` | `recipients[].substitutions` + `{{name}}` |
| `subject`, `html`, `text`, `amp-html` | `subject`, `body.html`, `body.plaintext`, `body.amp` |
| `template` + `t:variables` / `h:X-Mailgun-Variables` | `template_id` + substitutions (`template_engine: "liquid"` for Handlebars templates) |
| `o:tag` | `tags[]` (≤ 4) |
| `v:<name>` / `h:X-Mailgun-Variables` | `metadata` / `global_metadata` |
| `o:deliverytime` (RFC 2822) | `options.send_at` (UTC `YYYY-MM-DD hh:mm:ss`, ≤ 24 h) |
| `o:tracking-clicks`, `o:tracking-opens` | `track_links`, `track_read` |
| `attachment`, `inline` (multipart files) | `attachments[]`, `inline_attachments[]` with base64 `content` |
| `h:Reply-To` | `reply_to` |
| `h:X-…` | `headers` |
| `o:testmode` | the sandbox domain with confirmed addresses |
| EU region `api.eu.mailgun.net` | the UniOne host of the account's region (see the unione skill) |

Mailgun's `to` with several addresses and no recipient variables shows all of them to everyone; in UniOne list
them in `recipients[]` and, if they must see each other, in `headers.To`.

## Events

| Mailgun | UniOne status |
|---|---|
| `accepted` | `sent` |
| `delivered` | `delivered` |
| `failed` (`severity: temporary`) | `soft_bounced` |
| `failed` (`severity: permanent`) | `hard_bounced` |
| `opened` / `clicked` | `opened` / `clicked` |
| `unsubscribed` | `unsubscribed` |
| `complained` | `spam` |

Mailgun signs with HMAC-SHA256 of `timestamp + token`; UniOne sends `auth` (MD5) in the body.
