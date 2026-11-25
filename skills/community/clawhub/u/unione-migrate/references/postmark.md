# Migrate from Postmark to UniOne

| Postmark (`POST /email`, `/email/withTemplate`, `/email/batch`) | UniOne (`email/send`) |
|---|---|
| `X-Postmark-Server-Token` | `X-API-KEY` (a project key is the closest to a Postmark server) |
| `From` = `Name <email>` | `from_name`, `from_email` |
| `To` (comma-separated, ≤ 50) | `recipients[]` — each gets its own copy |
| `Cc`, `Bcc` | add to `recipients[]`; visible ones in `headers.To` / `headers.CC` |
| `Subject`, `HtmlBody`, `TextBody` | `subject`, `body.html`, `body.plaintext` |
| `TemplateId` / `TemplateAlias` + `TemplateModel` (Mustachio) | `template_id` + `substitutions` (`template_engine: "liquid"`) |
| `Tag` | `tags: [Tag]` |
| `Metadata` | `metadata` / `global_metadata` (≤ 10 keys) |
| `ReplyTo` | `reply_to` |
| `Headers[]{Name, Value}` | `headers{Name: Value}` (only `X-…`, `To`, `CC`) |
| `TrackOpens`, `TrackLinks` | `track_read`, `track_links` |
| `Attachments[]{Name, Content, ContentType, ContentID}` | `attachments[]{name, content, type}`; with `ContentID` → `inline_attachments[]{name: <ContentID>, …}` |
| `MessageStream` (`outbound` / `broadcast`) | separate projects or domains per stream, `tags` |
| `/email/batch` (≤ 500 messages) | one call per different message, or one call with ≤ 500 `recipients` + substitutions |
| Response `MessageID` | `job_id` + `emails` / `failed_emails` |

Mustachio → Liquid: `{{name}}` → `{{ name }}`, `{{#each items}}{{title}}{{/each}}` →
`{% for item in items %}{{ item.title }}{% endfor %}`, `{{#if x}}` → `{% if x %}`.

## Events

| Postmark webhook | UniOne status |
|---|---|
| `Delivery` | `delivered` |
| `Bounce` (`HardBounce`) | `hard_bounced` |
| `Bounce` (`SoftBounce`, `Transient`) | `soft_bounced` |
| `SpamComplaint` | `spam` |
| `Open` / `Click` | `opened` / `clicked` |
| `SubscriptionChange` | `unsubscribed` / `subscribed` |

Postmark protects webhooks with basic auth on the URL; UniOne sends `auth` (MD5) in the body.
