---
name: unione-email-best-practices
description: "Use when building email features on UniOne or fixing delivery: emails going to spam, bounces and complaints, SPF/DKIM/DMARC for spf.unione.io, domain warm-up, bulk sender rules, tracking domain and dedicated IP, consent and unsubscribes (GDPR, CAN-SPAM, CASL), double opt-in, list hygiene, which transactional emails an app needs and how to keep them out of unsubscribes, retries and idempotency, accessible emails."
license: MIT
metadata:
  author: "UniOne"
  version: "1.1.8"
  homepage: https://docs.unione.io/en/web-api-ref
  source: https://github.com/unione-repo/unione-skills
---

# Email best practices for UniOne

```
[Signup form] → [Validation] → [Double opt-in] → [Consent stored]
                                                       ↓
[Suppression check] ← [Queue + idempotent send] → UniOne email/send
                                                       ↓
                               [Webhooks: delivered / bounced / spam / unsubscribed]
                                                       ↓
                                       [Suppressions + list hygiene]
```

| Need to… | See |
|---|---|
| Set up SPF / DKIM / DMARC, fix spam placement, warm up a domain | [deliverability.md](references/deliverability.md) |
| Consent, unsubscribes and the laws of the market | [compliance.md](references/compliance.md) |
| Plan the transactional emails of an app | [transactional-emails.md](references/transactional-emails.md) |
| Retries, idempotency, queues, webhooks | [sending-reliability.md](references/sending-reliability.md) |
| Bounces, complaints, suppressions, inactive recipients | [list-management.md](references/list-management.md) |

## Start here

- **New app:** plan the emails ([transactional-emails.md](references/transactional-emails.md)), authenticate the
  domain ([deliverability.md](references/deliverability.md)), then send.
- **Spam problems:** authentication first, then complaints and bounces, then content.
- **Marketing email:** consent and unsubscribe ([compliance.md](references/compliance.md)) before the first campaign;
  a separate subdomain or project for marketing.
- **Production readiness:** queue + idempotence + webhooks ([sending-reliability.md](references/sending-reliability.md)).
- **Transactional and marketing on one account:** separate projects, or an own unsubscribe URL for transactional
  mail — otherwise a marketing unsubscribe blocks password resets
  ([transactional-emails.md](references/transactional-emails.md)).

API details: the `unione` skill; HTML and accessibility: `unione-email-templates`.
