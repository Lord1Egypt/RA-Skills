# Payment Methods — Cards, Bank Debits, Wallets, and Local Rails

**Read `platform` in `~/Clawic/data/stripe-api-integration/config.yaml`** (account country, presentment currencies, enabled methods) before recommending a method: availability is per account, per country and per currency, and the docs list what exists, not what this account can charge.

**Contents:** [The Only Classification That Matters](#the-only-classification-that-matters) · [Method Families](#method-families) · [Bank Debits Are Not Card Payments](#bank-debits-are-not-card-payments) · [Wallets](#wallets) · [Buy Now Pay Later](#buy-now-pay-later) · [Enabling Methods Without Rewriting the Integration](#enabling-methods-without-rewriting-the-integration) · [Choosing What to Offer](#choosing-what-to-offer) · [Refunds and Disputes by Rail](#refunds-and-disputes-by-rail)

## The Only Classification That Matters

Not "card versus alternative". **Synchronous versus asynchronous, and reusable versus single-use.**

| Property | Consequence for your code |
|---|---|
| Synchronous (cards, wallets) | Success at the end of the request; fulfill on the event and be done |
| Asynchronous (bank debits, vouchers, some bank redirects) | The intent goes to `processing` and settles later — sometimes days later; the event that matters arrives after the customer has left |
| Reusable (cards, wallets, SEPA and ACH debit with a mandate) | Can back a subscription |
| Single-use (most bank redirects, vouchers, most BNPL) | Cannot back a subscription; some convert into a reusable debit mandate |

An integration built only for synchronous methods breaks the day someone enables a bank debit, because its success path assumes the customer is still on the success page.

## Method Families

| Family | Examples | Sync? | Reusable? | Notes |
|---|---|---|---|---|
| Cards | Visa, Mastercard, Amex, and local schemes | Yes | Yes | The default rail everywhere; SCA applies in regulated markets (`sca-3ds.md`) |
| Wallets | Apple Pay, Google Pay, Link | Yes | Yes (tokenized card underneath) | Highest conversion lift on mobile; the underlying rail is still a card |
| Bank debits | SEPA Direct Debit, ACH, BACS, PAD, BECS | No | Yes, with a mandate | Cheap for large amounts, slow, reversible long after settlement |
| Bank redirects | iDEAL, Bancontact, BLIK, P24, EPS | Mostly sync | Some convert to a debit mandate | Dominant locally; iDEAL in the Netherlands is not optional |
| BNPL | Klarna, Afterpay, Affirm | Sync to you | No | The provider pays you and owns the credit risk; fees are higher |
| Vouchers and transfers | Boleto, OXXO, bank transfer | No | No | Customer pays later at a bank or shop; expect days and expiries |

## Bank Debits Are Not Card Payments

The failure model is inverted: a card fails immediately and rarely reverses; a bank debit succeeds immediately and can fail or reverse afterwards.

- **Settlement takes days, not seconds.** ACH typically settles in a handful of business days, SEPA Direct Debit similar. Treat the payment as pending until the rail's failure window has closed — shipping on "succeeded" is shipping on a promise.
- **Reversal windows are long.** A SEPA debit can be returned by the payer for weeks after collection, and an unauthorized-debit claim reaches back much further — beyond a year in the SEPA rulebook. Model this as revenue risk, not as an edge case.
- **A mandate is required and must be evidenced.** Stripe collects and stores the mandate text acceptance; you keep the mandate reference, never the raw IBAN (`memory-template.md`).
- **Failures arrive as their own events** (`payment_intent.payment_failed`, `charge.failed` after the fact). The handler has to be able to revoke access for a payment it already provisioned.
- **Some rails charge for the failure itself.** A dunning schedule that hammers a bank debit bills you to lose the customer (`dunning.md`).
- Micro-deposit or instant bank verification is part of the setup for ACH; a customer stuck in verification is not a payment failure, it is an onboarding step nobody surfaced.

## Wallets

- Apple Pay and Google Pay are cards underneath: same fees, same disputes, better conversion, and the customer never types a number.
- Apple Pay requires domain verification for web. A wallet button that does not appear in production and works locally is usually an unverified domain, not a code bug.
- Wallets carry device authentication, which frequently satisfies SCA frictionlessly — a conversion argument as much as a compliance one.
- Link stores the customer's details with Stripe and returns them across businesses; the effect is fewer fields, and the same card rail behind it.
- Test mode cannot prove a wallet works: wallet buttons depend on device, browser, domain and a real card in the wallet (`testing.md`).

## Buy Now Pay Later

- The provider pays you up front and takes the credit risk, so your revenue is immediate and the fee is higher than card.
- Refunds flow back through the provider and can be slower and partially constrained; check the rules before promising a customer a same-day refund.
- Order value matters: BNPL lifts conversion on higher tickets and rarely earns its fee on small ones.
- It is single-use — BNPL cannot back a subscription. A checkout that offers it for a recurring plan is a checkout that will error.

## Enabling Methods Without Rewriting the Integration

- `automatic_payment_methods[enabled]=true` on the PaymentIntent lets the account's enabled methods appear according to the customer's location and the amount, with no code change when one is turned on in the Dashboard.
- The price of that convenience: methods you did not design for can appear. The integration must already handle `processing`, delayed success, and post-settlement failure — see the classification above.
- Hosted Checkout and Payment Links do this by default and handle the redirect and return flows for every method (`checkout.md`).
- Restricting is deliberate: pass an explicit method list when a rail is genuinely incompatible with the business, and record why under `restrictions` in `config.yaml`.

## Choosing What to Offer

| Situation | Add | Why |
|---|---|---|
| Any mobile traffic | Apple Pay and Google Pay | Fewest fields on the smallest screen |
| Selling in the Netherlands | iDEAL | Card penetration is low; iDEAL is the norm |
| Selling in Germany | SEPA debit and a bank redirect | Card-averse market with strong debit culture |
| B2B invoices above a few hundred units of currency | Bank debit or transfer | Fee is a percentage of a large number; the buyer expects it |
| High-ticket consumer goods | BNPL | Converts the "I will think about it" segment |
| Subscriptions | Cards, wallets, SEPA/ACH debit only | The rest are single-use |
| Anything else | Cards plus wallets, then measure | Adding a rail costs support surface; add on evidence, not on a list |

Every added method is an operational surface: another failure mode, another refund path, another dispute window. Two well-supported methods beat six half-handled ones.

## Refunds and Disputes by Rail

| Rail | Refund path | Dispute mechanism |
|---|---|---|
| Card | Refund to the original card, days to appear | Chargeback through the network (`disputes.md`) |
| Wallet | Same as card | Same as card |
| SEPA / ACH debit | Refund back to the bank account, slower | Payer-initiated return or unauthorized claim, long window |
| Bank redirect | Often refundable, sometimes only as a credit | Usually no chargeback mechanism — irrevocable once complete |
| BNPL | Through the provider | Provider-mediated, their rules |
| Voucher | Frequently not refundable to source | No chargeback; refund is a manual payout |

The pattern worth internalizing: irrevocable rails have no dispute risk and no refund flexibility; reversible rails have both. Pricing and refund policy should differ by rail, and most teams apply one policy to all of them.

---

**When a payment method is enabled, disabled or restricted for this account**, write it under `platform` (enabled methods, presentment currencies) or `restrictions` in `~/Clawic/data/stripe-api-integration/config.yaml` — it is a declared choice — and note any rail-specific handling in `## Integration Shape` in `memory.md`. A post-settlement failure that reached a customer is an incident: `incidents/<year>.md`.
