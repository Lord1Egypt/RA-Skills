# Deliverability

## Authentication (required by Gmail, Yahoo and Microsoft)

| Record | What to do |
|---|---|
| SPF | One TXT record per domain: `v=spf1 include:spf.unione.io ~all` (merge with your other senders into one record; at most 10 DNS lookups). |
| DKIM | TXT `<selector>._domainkey` = `v=DKIM1; k=rsa; p=` + the `dkim` field of `domain/get-dns-records` (the selector is on the domain page of the control panel, e.g. `us`), then `domain/validate-dkim`. |
| Verification | The TXT record from `domain/get-dns-records`, then `domain/validate-verification-record`. |
| DMARC | Add the CNAME `_dmarc` → the `dmarc` field of `domain/get-dns-records` (UniOne publishes the policy), unless the domain already has its own DMARC TXT record: then keep it (e.g. `_dmarc.example.com TXT "v=DMARC1; p=none; rua=mailto:dmarc@example.com"`, moving to `p=quarantine` / `p=reject` once reports show only your legitimate mail). |

The `From` domain must align with the DKIM / SPF domain. Use a subdomain per stream (`mail.example.com` for
transactional, `news.example.com` for marketing) so a marketing problem does not block password resets.

## Reputation

- **Warm up** a new domain: start with the most engaged recipients and a few hundred emails a day, roughly double
  the volume every few days while bounces and complaints stay low.
- Keep the **complaint rate below 0.1%** (never reach 0.3%) and hard bounces below 2%.
- Send only to people who asked for the mail; never buy or scrape lists. Validate addresses at signup
  (`email-validation/single`) and remove `hard_bounced` / `spam` addresses (UniOne suppresses them automatically).
- Bulk senders (5,000+ emails a day to Gmail, Yahoo or Outlook.com) must have SPF, DKIM and DMARC (at least
  `p=none`) aligned with the `From` domain; Microsoft junks or rejects non-compliant bulk mail to Outlook.com since
  May 2025. Gmail and Yahoo also require one-click unsubscribe (`List-Unsubscribe` + `List-Unsubscribe-Post`,
  RFC 8058) honoured within two days; UniOne's default unsubscribe handles it.
- Watch the mailbox providers' postmaster tools: Google Postmaster Tools, Yahoo Sender Hub, Microsoft SNDS.

## UniOne infrastructure

- **Tracking domain**: with `track_links` / `track_read` on, links and the open pixel go through a UniOne domain
  by default. A tracking domain of your own (a CNAME like `click.example.com`, added in the control panel https://cp.unione.io/en/, section
  "Tracking domains") keeps the links on your domain, which mailbox providers and recipients trust more.
- **Shared vs dedicated IP**: under a few hundred thousand emails a month, or with irregular volume, stay on the
  shared pool — it is warmed up and watched. A dedicated IP pays off with steady high volume, needs its own warm-up
  and takes all the reputation of your mail alone. `custom_backend_id` of `email/send` picks the backend (IP pool
  and tracking domain) per message, e.g. one for transactional and one for marketing.
- **Global unavailability list**: UniOne does not send to addresses that hard-bounced or complained with other
  senders either (`failed_emails`). `bypass_global` overrides it only with support approval — mailing those
  addresses is what spam traps and blocklists catch.
- **Projects** (enabled by support) have their own domains, webhooks, templates and unsubscribe lists: the cleanest
  way to keep marketing complaints and unsubscribes away from transactional mail.

## Content

- A recognisable `from_name`, a working `reply_to` (not a `noreply@` that bounces replies), a clear subject without
  spam triggers (ALL CAPS, "!!!", "free"), a preheader that continues the subject.
- HTML with a plaintext part, a reasonable text-to-image ratio, no URL shorteners, links to your own domain.
- The physical address of the sender in marketing email.
- Optional, once DMARC is at `p=quarantine` / `p=reject`: BIMI shows your logo in Gmail, Yahoo and Apple Mail
  (needs a verified mark certificate for Gmail).

## When mail goes to spam

1. Check SPF, DKIM, DMARC and the domain status (`domain/list`).
2. Look at `soft_bounced` / `hard_bounced` with `delivery_info.destination_response` in webhooks or event dumps.
3. Check complaints (`spam` events) and the postmaster tools.
4. Separate marketing from transactional, slow down, send only to engaged recipients.
