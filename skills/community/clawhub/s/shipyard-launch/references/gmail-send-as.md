# Send and reply from your own address in Gmail

Once the app's domain sends email through Resend (`domain-email.md`), the student can also write from an address on it (for example `hello@<domain>`) inside their normal Gmail, and read replies there. Free, about 10 minutes. You guide; the student clicks, because it is their Gmail.

## 1. Receive (so replies arrive)

Pick one:
- **Forwarding at the registrar** (Namecheap, Porkbun, Cloudflare Email Routing and others are free): forward `hello@<domain>` to their Gmail. This adds MX records on the main domain; Resend uses the `send.` subdomain, so they do not clash.
- Or a mailbox at a provider if they want a full inbox.

## 2. Send as that address in Gmail

1. In Resend make a sending key for this (Sending access, only this domain), named "Gmail". The student creates it in the Resend dashboard and pastes it only into Gmail, never in the chat.
2. Gmail on a computer: Settings (gear) > See all settings > Accounts and Import > "Send mail as" > Add another email address.
3. Name: their name. Address: `hello@<domain>`. Untick "Treat as an alias" only if replies should go to a separate inbox.
4. SMTP server `smtp.resend.com`, port `587` (TLS) or `465` (SSL), username `resend`, password: the Resend key from step 1. Do not use `smtp.gmail.com`: it fails DMARC for the domain (measured 5.7/10 on mail-tester vs 10/10 through Resend SMTP).
5. Gmail sends a code to that address; it arrives by the forwarding from section 1. Paste it.
6. Optional: "Reply from the same address the message was sent to".

## 3. Keep it out of the junk folder

Mail that lands in junk almost always fails one of these. Check each and fix it:

- **SPF and DKIM**: Resend only sends from a domain it has verified. The app verified `send.<domain>`; to write as `hello@<domain>` add `<domain>` itself as a second domain in Resend and add its DNS records (they do not touch the forwarding MX records). Both must show Verified. Otherwise use `hello@send.<domain>`.
- **DMARC**: add a TXT record `_dmarc.<domain>` with `v=DMARC1; p=none; rua=mailto:<their email>`. Without DMARC, Gmail and Outlook often junk new domains. Move to `p=quarantine` after two clean weeks.
- **Matching names**: the From address must be on the domain that is verified. Never send as an address on a domain you have not verified.
- **New domain warm-up**: start with a few emails a day to people who expect them and ask a couple of them to mark "Not spam" and reply. Volume jumps from a new domain look like spam.
- **Content**: plain text or simple HTML, a real signature, no link shorteners, no attachments on the first emails.
- **Test**: send one to the check address at mail-tester.com and fix anything below 9/10. Gmail's "Show original" on a received copy shows SPF, DKIM and DMARC as PASS or FAIL.

Write what was set up in `HANDOFF.md` (address, forwarding, that Gmail holds a Resend key named "Gmail" which can be revoked in Resend).
