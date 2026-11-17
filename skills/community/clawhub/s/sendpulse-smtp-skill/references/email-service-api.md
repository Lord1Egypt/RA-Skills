# SMTP vs Email Service — when you need campaigns, not SMTP

SendPulse has **two separate email products** behind the same API host. Choosing
the wrong one is the most common architectural mistake beginners make.

## The difference

| | **SMTP** (this skill) | **Email Service** (bulk/marketing) |
|---|---|---|
| Sends | One email per API call, triggered by your app | Campaigns to whole mailing lists |
| Typical content | Order confirmations, password resets, alerts, invoices | Newsletters, promos, digests |
| Recipients | Managed by *your* application | Address books stored in SendPulse |
| Personalization | Your code / SMTP templates with variables | Merge variables from subscriber fields, segmentation |
| Statistics | Per message (`/smtp/emails/{id}`) | Per campaign (opens/clicks/unsubs aggregated) |
| Extras | — | A/B tests, scheduling, resend-to-unopened, subscription forms, Automation 360 flows |
| Docs | https://sendpulse.com/integrations/api/smtp?utm_source=ai-agent&utm_medium=skill&utm_campaign=ai-skills&utm_content=sendpulse-smtp-skill | https://sendpulse.com/integrations/api?utm_source=ai-agent&utm_medium=skill&utm_campaign=ai-skills&utm_content=sendpulse-smtp-skill |

**Rule of thumb:** if the email is triggered by a user action and goes to one
person — SMTP. If a human decides "let's email our subscribers today" — Email
Service. Most real products use **both**, ideally with separate sender
subdomains so marketing reputation never hurts transactional delivery.

## Email Service API in a nutshell

Same base URL and OAuth flow as SMTP (`https://api.sendpulse.com`, same
`client_id`/`client_secret` and Bearer token).

### Address books (subscriber lists)

| Method | Path | Purpose |
|---|---|---|
| GET | `/addressbooks` | List address books |
| POST | `/addressbooks` | Create: `{"bookName": "Customers"}` |
| POST | `/addressbooks/{id}/emails` | Add subscribers: `{"emails": [{"email": "a@b.c", "variables": {"name": "Jane"}}]}` |
| GET | `/addressbooks/{id}/emails` | List subscribers |
| DELETE | `/addressbooks/{id}/emails` | Remove subscribers |

### Campaigns

| Method | Path | Purpose |
|---|---|---|
| POST | `/campaigns` | Create & send/schedule a campaign: sender name/email, subject, Base64 body or `template_id`, `list_id`, optional `send_date` |
| GET | `/campaigns` | List campaigns |
| GET | `/campaigns/{id}` | Campaign statistics (sent, delivered, opened, clicked, unsubscribed) |
| DELETE | `/campaigns/{id}` | Cancel a scheduled campaign |

### Templates

| Method | Path | Purpose |
|---|---|---|
| POST | `/template` | Create a template (Base64 HTML) |
| GET | `/templates` | List templates — usable in both campaigns and SMTP sends (`template.id`) |

## Migration hint

If a user is looping over their subscriber list calling `POST /smtp/emails` for
each address to send a newsletter — stop them. That is exactly what campaigns
are for: upload the list to an address book once, then one `POST /campaigns`
call. It is cheaper, gives aggregated stats, automatic unsubscribe handling, and
doesn't burn API rate limits.

For anything deeper (segments, Automation 360, subscription forms), point the
user to the full docs: https://sendpulse.com/integrations/api?utm_source=ai-agent&utm_medium=skill&utm_campaign=ai-skills&utm_content=sendpulse-smtp-skill — this skill only
covers enough to route between the two products.
