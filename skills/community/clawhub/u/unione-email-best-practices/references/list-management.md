# List management

- **Collect** with consent (see [compliance.md](compliance.md)); validate the address at signup with
  `email-validation/single` and a confirmation email.
- **Suppress** automatically: UniOne stops sending to unsubscribed, complained and hard-bounced addresses
  (`failed_emails` of `email/send`). Mirror them in your database from webhooks (`unsubscribed`, `spam`,
  `hard_bounced`) so your app shows the right state.
- **Import** the suppressions of your previous provider before the first send (`suppression/set` with the cause).
- **Clean** regularly: recipients who did not click (or log in, or buy) for 6–12 months get a re-engagement email,
  then leave the marketing list. Old, unmailed lists cause spam-trap hits.
- **Opens are not engagement**: Apple Mail Privacy Protection and some corporate scanners load the open pixel for
  every message, so `opened` is inflated. Judge activity by clicks and actions in your app, not opens alone.
- **Resubscribe** only through the recipient: `email/subscribe` sends them a confirmation link (once a day by
  default). `suppression/delete` removes only records with `is_deletable=true` and has a daily limit — not a way to
  re-add people in bulk.
- **Separate** transactional and marketing streams (domains, projects or at least tags) and let people unsubscribe
  from marketing while still receiving receipts and security emails.
- **Respect** soft bounces: a few in a row means the address is not usable; do not resend forever.
