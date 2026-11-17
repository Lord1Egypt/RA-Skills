# Deliverability — how to make good mailings

Delivering to the inbox is 20% API and 80% sender behavior. This file is the
"good mailings" playbook to embed into any integration.

## The three pillars

### 1. Authentication (one-time DNS work)

- **SPF, DKIM, DMARC** configured on the sender domain — see [setup.md](setup.md).
- Verify by sending to your own Gmail/Outlook and reading the original headers:
  you want `spf=pass`, `dkim=pass`, `dmarc=pass`.
- Gmail/Yahoo bulk-sender rules effectively **require** SPF+DKIM+DMARC and
  one-click unsubscribe for anyone sending at volume. Treat them as mandatory.

### 2. List hygiene (continuous, automate it)

- **Only send to people who opted in.** Purchased/scraped lists destroy the
  account: they are full of spam traps and dead addresses, and moderation will
  block the account.
- **Before every send**: check `GET /smtp/unsubscribe/search?email=...` (or keep a
  local mirror of the blocklist synced daily via `GET /smtp/unsubscribe`).
- **Daily**: pull `GET /smtp/bounces/day`; delete hard bounces (nonexistent
  mailbox) from your database permanently; retry soft bounces (full mailbox,
  temporary) a limited number of times, then drop.
- **Honor unsubscribes instantly**: when a user opts out in your app, call
  `POST /smtp/unsubscribe` so SendPulse also blocks them.
- SendPulse monitors your bounce and spam-complaint rates and **restricts SMTP
  accounts that exceed thresholds**. Keep bounce rate under ~2–3% and complaints
  under ~0.1% — if you're above, stop and clean the list before sending more.
- For old/unknown lists, validate addresses first (SendPulse has an Email
  Verifier service) instead of "sending to see what bounces".

### 3. Reputation & volume (be predictable)

- **Warm up** new domains and dedicated IPs: start at tens–hundreds of emails/day
  to your most engaged recipients, roughly double every few days over 2–4 weeks.
  A brand-new domain blasting 100k emails on day one goes straight to spam.
- **Send at a steady cadence** — mailbox providers distrust volume spikes.
- Your plan also caps **emails per hour**; queue and spread large batches instead
  of firing them at once.
- Use a **subdomain** for sending (e.g. `mail.yourbrand.com`) so transactional
  reputation is isolated from your root domain.
- Separate **transactional** and **marketing** streams (different
  subdomains/senders) — a bad promo campaign must not sink password-reset emails.

## Content rules

- **Always send a `text` part** with the HTML.
- Working `From` address on your domain; a recognizable sender name.
- Subject: no ALL CAPS, no `!!!`, no spam-bait ("FREE $$$", "Act now"); say what
  the email actually is.
- Balanced HTML: not one giant image, no shortened URLs (bit.ly), links pointing
  to your own domain, total size well under 100 KB.
- Include a physical address and an **unsubscribe link** in the footer for
  anything non-transactional (legal requirement: CAN-SPAM/GDPR).
- Test rendering (the `sendpulse-template-skill` or any email-HTML guide covers
  responsive/dark-mode markup).

## Monitoring — close the loop

- **Webhooks** ([webhooks.md](webhooks.md)) for real-time delivered/opened/
  clicked/bounce/spam events; feed them back into your database.
- Watch the SMTP statistics dashboard weekly: delivery rate, opens, bounces,
  complaints per domain (Gmail vs Outlook vs others) — a drop at one provider
  points at reputation with that provider.
- Register the domain with Google Postmaster Tools and Microsoft SNDS for
  provider-side reputation data.

## Pre-flight checklist for a new integration

- [ ] SPF+DKIM+DMARC pass on a self-test email
- [ ] Recipients are opt-in; source of the list is known
- [ ] Blocklist check before send is implemented
- [ ] Daily bounce sync implemented; hard bounces deleted
- [ ] In-app unsubscribe wired to `POST /smtp/unsubscribe`
- [ ] Text part present; footer has unsubscribe + address (non-transactional)
- [ ] Volume ramp-up plan for the first month
- [ ] Webhooks or daily status polling in place
