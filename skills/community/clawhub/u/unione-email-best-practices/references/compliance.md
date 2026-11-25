# Compliance

Not legal advice: have your counsel review your flows. The rules most senders on UniOne meet:

| Law | Applies to | Key requirements |
|---|---|---|
| **GDPR** (EU / EEA, UK GDPR) | Personal data of people in the EU / UK | A lawful basis for every email (consent for marketing, recorded with time and source); a privacy notice; access and erasure on request; a data processing agreement with your ESP. |
| **ePrivacy / PECR** | Marketing email to EU / UK people | Prior opt-in consent; soft opt-in only for similar products to existing customers, with an opt-out at collection and in every email. |
| **CAN-SPAM** (US) | Commercial email to US recipients | No deceptive `From` or subject; identify ads; the sender's physical postal address; a working opt-out honoured within 10 business days. |
| **CASL** (Canada) | Commercial electronic messages to Canada | Express or implied consent (records kept); sender identification; an unsubscribe working for 60 days, honoured within 10 business days. |

## Practice

- **Double opt-in** for marketing lists: the signup sends a confirmation email; add to the list after the click.
- Store consent: address, time, source (form, page), the text the person agreed to, IP.
- Transactional email (receipts, password resets, security alerts) needs no marketing consent, but must not carry
  promotions beyond a small, non-dominant mention.
- Unsubscribe: one click, no login, works for at least 60 days; sync unsubscribes back to your database
  (`unsubscribed` webhook events, `suppression/list`).
- Delete data you no longer need; erase a person on request (also from suppression lists only when they ask to
  receive mail again — a suppression is the record that you must not mail them).
