# Transactional emails

The emails an app usually needs, and what each must contain:

| Email | Must have |
|---|---|
| Email confirmation / double opt-in | One clear button, the link's lifetime, "ignore if it was not you". |
| Password reset | A one-time link valid 15–60 minutes, no password in the email, a note to contact support if not requested. |
| One-time code (OTP) | The code in text (not an image), its lifetime; the code also in the subject or preheader only if the threat model allows. |
| Welcome | What to do first, links to help; no aggressive promotions. |
| Receipt / order confirmation | Order number, items, totals, taxes, address, support contact. |
| Shipping / status updates | Status, tracking link, expected date. |
| Security alerts (new login, changed email) | What happened, when, from where, how to secure the account. |
| Account / billing notices | The facts and the action needed, with a deadline. |

Rules:

- Send immediately (queue + worker, not inside the web request), with an `idempotence_key` per event and entity.
- Personalise with substitutions; keep one template per email type (`template/set`) instead of HTML in code.
- Track delivery with webhooks; alert when `hard_bounced` / `spam` rates rise.
- Plaintext part, accessible HTML (see the email-templates skill), the brand and a support address in every email.
- Security emails go even to unsubscribed users only if the law and your terms allow it — they are not marketing.
- **The unsubscribe link is added to every email by default, password resets included**, and a click unsubscribes
  the address from all mail of the account or project — the next password reset is rejected too. Send transactional
  and marketing mail from separate projects (their own unsubscribe lists), or give transactional email its own
  `options.unsubscribe_url` (a preferences page in your app). Removing the link (`skip_unsubscribe`) and sending to
  unsubscribed addresses (`bypass_unsubscribed`) need support approval.
