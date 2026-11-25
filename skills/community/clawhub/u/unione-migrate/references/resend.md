# Migrate from Resend to UniOne

| Resend (`POST /emails`) | UniOne (`email/send`) |
|---|---|
| `Authorization: Bearer re_…` | `X-API-KEY: …` |
| `from` = `Name <email>` | `from_name`, `from_email` |
| `to` (string or array ≤ 50, one shared message) | `recipients[]` — each gets its own copy; shared visibility via `headers.To` |
| `cc`, `bcc` | add to `recipients[]`; visible ones in `headers.CC` |
| `subject`, `html`, `text` | `subject`, `body.html`, `body.plaintext` |
| `react` | render to HTML first (`render()` of React Email), then `body.html` + `body.plaintext` |
| `template: {id, variables}` | `template_id` + `substitutions` (convert `{{{VAR}}}` to the engine syntax) |
| `reply_to` | `reply_to` |
| `headers` | `headers` (only `X-…`, `To`, `CC`) |
| `attachments[]{filename, content, path, content_type, content_id}` | `attachments[]{name, content(base64), type}`; `content_id` → `inline_attachments[]`; no `path` URLs — download and base64 them |
| `tags[]{name, value}` | `metadata` (key / value, ≤ 10) or `tags[]` (strings, ≤ 4) |
| `scheduled_at` | `options.send_at` (UTC `YYYY-MM-DD hh:mm:ss`, ≤ 24 h) |
| `Idempotency-Key` header (24 h) | `idempotence_key` field (**1 minute**) + your own sent flag |
| `POST /emails/batch` (≤ 100 different emails) | one `email/send` per different message; the same message to many: one call with ≤ 500 `recipients` |
| `onboarding@resend.dev` | the sandbox domain with confirmed addresses |
| SDK returns `{ data, error }` | UniOne SDKs throw an error (`ApiError` in Node.js, Python, Ruby, Rust; `ApiException` in PHP, Java, .NET; Go returns `*APIError`): message, kind, retryable, HTTP status, API code, the API's own message |

## Events

| Resend | UniOne status |
|---|---|
| `email.sent` | `sent` |
| `email.delivered` | `delivered` |
| `email.delivery_delayed` | `soft_bounced` |
| `email.bounced` | `hard_bounced` |
| `email.complained` | `spam` |
| `email.opened` / `email.clicked` | `opened` / `clicked` |
| `email.failed`, `email.suppressed` | the recipient is in `failed_emails` of `email/send` |
| `contact.*`, `domain.*`, `email.received` | no equivalent (no contacts or inbound API in UniOne) |

Resend signs with Svix headers (`svix-id`, `svix-timestamp`, `svix-signature`); UniOne sends `auth` (MD5) in
the body. Resend's audiences, broadcasts and inbound email have no equivalent in the UniOne Web API.
