# Migrate from SendGrid to UniOne

| SendGrid (`POST /v3/mail/send`) | UniOne (`email/send`) |
|---|---|
| `Authorization: Bearer SG.…` | `X-API-KEY: …` |
| `from.email`, `from.name` | `from_email`, `from_name` |
| `personalizations[].to[]` | `recipients[]` — one entry per address; each gets its own copy |
| `personalizations[].cc[]` / `bcc[]` | add to `recipients[]`; visible ones in `headers.To` / `headers.CC` |
| `personalizations[].dynamic_template_data` / `substitutions` | `recipients[].substitutions` |
| `subject` | `subject` |
| `content[]` (`text/html`, `text/plain`) | `body.html`, `body.plaintext` |
| `template_id` (`d-…`, Handlebars) | `template_id` from `template/set` + `template_engine: "liquid"` |
| `categories[]` | `tags[]` (≤ 4) |
| `custom_args` | `recipients[].metadata` / `global_metadata` (≤ 10 keys) |
| `send_at` (Unix time, ≤ 72 h) | `options.send_at` (UTC `YYYY-MM-DD hh:mm:ss`, ≤ 24 h) |
| `attachments[]{content, filename, type, disposition: inline, content_id}` | `attachments[]{type, name, content}`; inline → `inline_attachments[]{type, name: <content_id>, content}` |
| `reply_to` | `reply_to`, `reply_to_name` |
| `headers` | `headers` (only `X-…`, `To`, `CC`) |
| `tracking_settings.click_tracking` / `open_tracking` | `track_links`, `track_read` (turning off needs support) |
| `asm.group_id` (unsubscribe groups) | default unsubscribe link or `options.unsubscribe_url`; separate projects for separate lists |
| `mail_settings.sandbox_mode` | the sandbox domain with confirmed addresses |
| Response `202`, `X-Message-Id` header | `200` with `job_id`, `emails`, `failed_emails` |

Handlebars → Liquid: `{{name}}` → `{{ name }}`, `{{#if x}}…{{else}}…{{/if}}` → `{% if x %}…{% else %}…{% endif %}`,
`{{#each items}}{{this.title}}{{/each}}` → `{% for item in items %}{{ item.title }}{% endfor %}`.

## Events

| SendGrid Event Webhook | UniOne status |
|---|---|
| `processed` | `sent` |
| `delivered` | `delivered` |
| `deferred` | `soft_bounced` |
| `bounce` (`type: bounce`) | `hard_bounced` |
| `bounce` (`type: blocked`) | `soft_bounced` |
| `dropped` | the recipient is in `failed_emails` of `email/send` |
| `open` / `click` | `opened` / `clicked` |
| `spamreport` | `spam` |
| `unsubscribe` / `group_unsubscribe` | `unsubscribed` |

SendGrid signs with ECDSA (`X-Twilio-Email-Event-Webhook-Signature`); UniOne sends `auth` (MD5) in the body.
SendGrid posts an array of events; UniOne posts `{auth, events_by_user[{events[{event_name, event_data}]}]}`.

## Code (Node.js)

```javascript
// Before
import sgMail from "@sendgrid/mail";
sgMail.setApiKey(process.env.SENDGRID_API_KEY);
await sgMail.send({ to: "alex@example.com", from: "noreply@example.com", subject: "Hi", html: "<p>Hi</p>" });

// After: raw HTTP (or the UniOne Node.js SDK, see the unione skill)
const response = await fetch("https://api.unione.io/en/transactional/api/v1/email/send.json?platform=skill", {
  method: "POST",
  headers: { "Content-Type": "application/json", "X-API-KEY": process.env.UNIONE_API_KEY },
  body: JSON.stringify({ message: {
    recipients: [{ email: "alex@example.com" }],
    from_email: "noreply@example.com", subject: "Hi", body: { html: "<p>Hi</p>", plaintext: "Hi" },
  } }),
});
const result = await response.json(); // { job_id, emails, failed_emails } or { status: "error", code, message }
```
