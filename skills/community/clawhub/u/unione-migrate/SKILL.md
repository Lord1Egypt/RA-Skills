---
name: unione-migrate
description: "Use when moving email sending to UniOne from another provider — SendGrid, Mailgun, Resend, Postmark — or when the code uses their SDKs, keys or API URLs (@sendgrid/mail, mailgun.js, resend, postmark, …) or their SMTP relays (smtp.sendgrid.net, smtp.mailgun.org, smtp.postmarkapp.com): maps the send calls, SMTP settings and headers, templates, webhook events and suppressions to UniOne."
license: MIT
metadata:
  author: "UniOne"
  version: "1.1.8"
  homepage: https://docs.unione.io/en/web-api-ref
  source: https://github.com/unione-repo/unione-skills
compatibility: "Requires UNIONE_API_KEY: the UniOne API key (the account key, or a project key for project data) from https://cp.unione.io/en/, server-side only."
---

# Migrate to UniOne

| From | Reference | Detect by |
|---|---|---|
| SendGrid | [sendgrid.md](references/sendgrid.md) | `@sendgrid/mail`, `sgMail`, `sendgrid` (Python / Ruby / PHP / Go / Java / C#), `SENDGRID_API_KEY`, `api.sendgrid.com/v3/mail/send` |
| Mailgun | [mailgun.md](references/mailgun.md) | `mailgun.js`, `mailgun-js`, `mailgun` (Python / Ruby / PHP / Go / Java), `MAILGUN_API_KEY`, `api.mailgun.net/v3/<domain>/messages` |
| Resend | [resend.md](references/resend.md) | `resend` (Node.js / Python / Ruby / PHP / Go), `new Resend(`, `RESEND_API_KEY`, `api.resend.com/emails` |
| Postmark | [postmark.md](references/postmark.md) | `postmark` (Node.js / Python `postmarker` / Ruby / PHP), `ServerClient(`, `POSTMARK_SERVER_TOKEN`, `X-Postmark-Server-Token`, `api.postmarkapp.com/email` |

Find the provider by its imports, environment variables and API URLs, open its reference, and convert every send call, template and webhook handler; then run the checklist.

## Fastest switch: SMTP

If the app sends through the old provider's SMTP relay rather than its SDK, switching is a config change: put
UniOne's host and credentials (the `unione` skill, SMTP section) and keep the code. Provider-specific headers stop
working: move what they carry to the `X-UNIONE` JSON header.

| Old relay | Its own headers | In UniOne |
|---|---|---|
| `smtp.sendgrid.net`, user `apikey` | `X-SMTPAPI` (`unique_args`, `sub`) | `X-UNIONE`: `global_metadata`, `global_substitutions` |
| `smtp.mailgun.org` | `X-Mailgun-Variables` | `X-UNIONE`: `global_metadata` |
| `smtp.resend.com`, user `resend` | none | none |
| `smtp.postmarkapp.com` | `X-PM-Metadata-*`, `X-PM-Message-Stream` | `X-UNIONE`: `global_metadata`; streams → projects (`project_id` as the username) |

## Migration checklist

- [ ] Sending domain: `domain/get-dns-records`, add the verification TXT, the DKIM TXT (`v=DKIM1; k=rsa; p=` +
      `dkim`), `include:spf.unione.io` to SPF, and the CNAME `_dmarc` from the `dmarc` field unless the domain already has
      its own DMARC TXT; keep the old provider's records until the switch is done;
      `domain/validate-verification-record`, `domain/validate-dkim`.
- [ ] API key in `UNIONE_API_KEY` (account key, or a project key per client / environment).
- [ ] Install the UniOne SDK or the framework package of the project (the unione skill, installation reference).
- [ ] Map every send call (tables below); multi-recipient messages become `recipients[]` (one copy per recipient).
- [ ] SMTP apps: swap the host and credentials, move provider headers to `X-UNIONE`; webhooks and suppressions
      still need the steps below.
- [ ] Recreate templates with `template/set`, converting the syntax to `liquid` (closest to Handlebars / Mustache).
- [ ] Replace the webhook endpoint: `webhook/set`, the MD5 `auth` signature, the status mapping below.
- [ ] Import suppressions (unsubscribes, bounces, complaints) with `suppression/set` before the first send.
- [ ] Test through the sandbox domain or your own mailboxes; then switch gradually (a share of traffic first).
- [ ] Remove the old SDK, keys and DNS records when traffic is fully on UniOne.

## UniOne email/send in brief

`POST https://api.unione.io/en/transactional/api/v1/email/send.json?platform=skill`, header `X-API-KEY`, JSON body `{"message": {...}}`:
`recipients[{email, substitutions, metadata}]` (≤ 500), `from_email`, `from_name`, `subject`,
`body{html, plaintext, amp}`, `template_id`, `template_engine`, `global_substitutions`, `global_metadata`,
`tags` (≤ 4), `headers` (`X-…`, `To`, `CC`), `attachments[{type, name, content(base64)}]`, `inline_attachments`,
`reply_to`, `reply_to_name`, `track_links`, `track_read`, `idempotence_key` (1 minute), `options.send_at`
(UTC `YYYY-MM-DD hh:mm:ss`, ≤ 24 h), `options.unsubscribe_url`.
Response: `job_id`, `emails` (accepted), `failed_emails` (rejected recipients with the reason).
Webhook statuses: `sent`, `delivered`, `opened`, `clicked`, `unsubscribed`, `subscribed`, `soft_bounced`,
`hard_bounced`, `spam`.

API details and SDK install: the `unione` skill; templates: `unione-email-templates`.
