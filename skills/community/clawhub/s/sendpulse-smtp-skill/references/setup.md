# Account & sender setup

Everything in this file happens **once**, in the SendPulse dashboard
(https://login.sendpulse.com). No email will be delivered until all steps are done.

## 1. Activate the SMTP service (moderation)

SendPulse moderates every SMTP account to protect its shared IP reputation.

1. Open **SMTP** in the dashboard.
2. Fill out the sender profile (questionnaire): what you send, how you collected
   your recipient addresses, how recipients can unsubscribe.
3. Wait for moderator approval — usually **up to 24 hours**.

Until approved, API authorization works but sending is blocked. If the account is
later blocked (e.g. for high bounce/spam rates), the dashboard shows a banner with
a contact form to request unblocking.

## 2. Add and verify a sender

1. **SMTP → Settings** → add a sender email address.
2. Rules:
   - The address must be on a **corporate domain you control**. Free mailbox
     domains (gmail.com, outlook.com, yahoo.com, mail.ru, …) are **rejected**.
   - The number of sender domains is limited by your plan.
3. SendPulse sends a **confirmation email** to that address — click the link.
4. The sender then appears in `GET /smtp/senders` and can be used in `from.email`.

Via API instead of the dashboard: `POST /senders` with `{"email": "...", "name": "..."}`
triggers the same confirmation email.

## 3. Configure DNS: SPF and DKIM

Without these, mail is technically sent but is likely to land in spam.

- **SPF** — a TXT record on your domain authorizing SendPulse servers to send on
  its behalf. Copy the exact value from *SMTP → Settings* in the dashboard
  (it is an `include:` mechanism added to your existing SPF record — a domain must
  have only ONE SPF record, merge, don't add a second).
- **DKIM** — a TXT record at `<selector>._domainkey.<yourdomain>` with a public
  key. The dashboard shows the exact host and value per verified domain.
- **DMARC** (recommended) — start with `v=DMARC1; p=none; rua=mailto:you@domain`
  to monitor, tighten to `quarantine`/`reject` once SPF/DKIM pass.

The dashboard has built-in SPF and DKIM checkers — use them to verify propagation
(DNS changes can take up to 24–48 h).

## 4. Get API credentials

- **REST API**: *Account Settings → API tab* → `ID` and `Secret`. Used for the
  OAuth `client_credentials` flow.
- **SMTP relay**: *SMTP → Settings → General* → server address, port, login,
  password. Used by PHPMailer/nodemailer/mail clients — see
  [smtp-relay.md](smtp-relay.md).

Store both as secrets (environment variables, vault). Never commit them.

## 5. Optional hardening

- **IP whitelist for the API** — restrict which IPs may call the API with your
  credentials (dashboard, API settings).
- **Dedicated IP** — for high-volume senders; isolates your reputation from other
  SendPulse customers. Requires its own warm-up (see
  [deliverability.md](deliverability.md)).
- **Webhooks** — get real-time delivery/open/click/bounce events instead of
  polling; see [webhooks.md](webhooks.md).

## Setup checklist (copy for the user)

- [ ] SMTP profile filled, moderation approved
- [ ] Sender email on own domain added and confirmed via email link
- [ ] SPF record merged into domain DNS, checker green
- [ ] DKIM record added, checker green
- [ ] DMARC record added (at least `p=none`)
- [ ] API `ID`/`Secret` (or SMTP login/password) stored as secrets
- [ ] Test email sent to yourself and inspected: headers show `spf=pass`, `dkim=pass`
