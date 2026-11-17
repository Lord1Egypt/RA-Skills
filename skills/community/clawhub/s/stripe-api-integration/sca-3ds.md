# Authentication — SCA, 3D Secure, and Off-Session Charging

**Read `## Integration Shape` and `restrictions` in `config.yaml`** before designing the authentication path: whether the customer is present, and whether the account sells into the EEA, UK, India or another regulated market, decides everything below.

**Contents:** [The One Distinction](#the-one-distinction) · [What SCA Actually Requires](#what-sca-actually-requires) · [Exemptions Worth Knowing](#exemptions-worth-knowing) · [Saving a Card for Later](#saving-a-card-for-later) · [The Off-Session Recovery Loop](#the-off-session-recovery-loop) · [Liability Shift](#liability-shift) · [Frictionless vs Challenge](#frictionless-vs-challenge) · [Where Teams Get It Wrong](#where-teams-get-it-wrong)

## The One Distinction

Everything in this file follows from whether the cardholder is in front of the screen.

| | On-session | Off-session |
|---|---|---|
| Who is present | The customer, now | Nobody; your server is charging a saved card |
| Can 3DS be completed | Yes, redirect or modal | No — there is nobody to challenge |
| If the issuer demands authentication | Show the challenge, complete the intent | `authentication_required` and the charge fails |
| Correct recovery | Finish the flow | Email the customer, bring them back on-session, reuse the same PaymentIntent |

A retry of a failed off-session charge, off-session, will fail again. This is the single most expensive misunderstanding in subscription billing, because it looks like a transient decline and it is a permanent one until a human is involved.

## What SCA Actually Requires

PSD2 in the EEA (and equivalent rules in the UK and India) requires two of three factors — something the customer has, knows, or is — for most customer-initiated electronic payments. In practice that means 3D Secure on card payments where the issuer decides it applies.

- Applies when both the customer's bank and the business's acquirer are in the regulated area. A US business charging a US card is out of scope; the same business charging an EEA cardholder through an EEA entity is in scope.
- The regulation is enforced by the *issuer*: a soft decline (`authentication_required`) is the issuer saying "not without SCA", regardless of what your code intended.
- Merchant-initiated transactions — subscription renewals, usage invoices — are out of scope **if** the initial payment was authenticated and a mandate was established. This is why the first charge matters far more than the hundredth.
- India has its own regime with mandates and pre-debit notifications for recurring payments; a subscription integration that works in the EU is not automatically compliant there.

## Exemptions Worth Knowing

Exemptions are requested on the payment and granted by the issuer — you never get to decide unilaterally.

| Exemption | Condition | Trade-off |
|---|---|---|
| Low value | Under 30 EUR, with issuer-side counters that force authentication after roughly 5 consecutive exempt payments or ~100 EUR cumulative | Free conversion until the counter trips, then a challenge nobody expected |
| Transaction risk analysis (TRA) | Acquirer's fraud rate is low enough for the value band | Managed by the acquirer, not by you |
| Merchant-initiated | Off-session charge under an established mandate | Only valid if the setup was authenticated |
| Trusted beneficiary | Customer added you to their bank's allowlist during a challenge | You cannot trigger it; you benefit when it happens |

Asking for an exemption and being refused costs one round trip, not the sale — the fallback is the challenge. The real cost of exemption-first is fraud liability staying with you (below).

## Saving a Card for Later

- **Charge now, reuse later**: `setup_future_usage=off_session` on the PaymentIntent. The card is authenticated during a payment the customer is watching, and the mandate covers later charges.
- **Save without charging**: a SetupIntent. Use it for trials without an upfront payment, for adding a backup card, and for updating a card after a failure.
- Attach the payment method to the customer and set it as the invoice default, otherwise the subscription renews against nothing.
- Collecting a card during a free trial is what makes the first renewal chargeable without a challenge — a trial with no payment method is a renewal that will fail, by design (`checkout.md` covers the trial-without-card variant and its end behavior).
- The mandate is per-customer and per-payment-method. Migrating a saved card to a different customer object loses it.

## The Off-Session Recovery Loop

1. Off-session charge fails with `authentication_required` (or the subscription invoice fails the same way).
2. Do **not** retry off-session, and do not create a new PaymentIntent — the existing one holds the state and the amount.
3. Email the customer with a link back into your app that confirms the *same* PaymentIntent on-session, or send them to the hosted invoice page or Billing Portal, which handle the challenge for you.
4. The customer completes 3DS; the payment succeeds; the subscription leaves `past_due` on `invoice.paid`.
5. Set expectations in the email: "your bank needs to confirm this payment" converts far better than "your payment failed", because the customer's card is fine and they know it.

This loop is the authentication half of dunning; the retry-schedule half is in `dunning.md`.

## Liability Shift

- A payment authenticated with 3DS generally shifts fraud-related chargeback liability to the issuer. Disputes on other grounds — product not received, subscription cancelled — stay with you regardless.
- An exempted payment keeps liability with you. That is the actual price of the exemption, and it is only visible later, in `disputes/<year>.md`.
- The decision is therefore per segment, not global: apply authentication where the fraud losses are, keep exemptions where they are not. Blanket 3DS on a low-fraud subscription business buys liability protection you did not need and pays for it in abandoned checkouts.

## Frictionless vs Challenge

- Most 3DS attempts complete frictionlessly: the issuer authenticates from device and behavioral data with no visible step. The challenge is the exception, not the norm.
- Frictionless still shifts liability, which is why "3DS kills conversion" is only true for the challenge fraction.
- What actually breaks conversion: an app that cannot handle a redirect, a modal blocked as a popup, a mobile webview that loses the return URL, and abandoning the intent instead of resuming it. Hosted Checkout handles all four (`checkout.md`).
- Test mode simulates the flows you select with specific test cards, and simulates nothing about how a real issuer behaves (`testing.md`).

## Where Teams Get It Wrong

| Trap | Why it fails | Do instead |
|---|---|---|
| Retrying `authentication_required` on a schedule | The issuer is asking for a human; the schedule has none | On-session recovery loop, same PaymentIntent |
| Creating a new PaymentIntent for the recovery | Two intents for one order, one of which may still succeed | Reuse the intent you have |
| Trial with no payment method and no plan for the first renewal | The first charge is off-session against nothing | SetupIntent during the trial, or set the trial end behavior explicitly |
| Assuming SCA does not apply because the business is not in the EU | The cardholder's issuer decides, and cross-border sales exist | Handle `requires_action` everywhere; it costs nothing when unused |
| Treating `requires_action` as a failure state | It is a pause, and the money is still available | Surface the challenge; the intent completes |
| Off-session charge with no established mandate | Merchant-initiated exemption does not apply and the issuer soft-declines | Authenticate the setup with `setup_future_usage` or a SetupIntent |

---

**When the authentication posture is decided** — blanket 3DS, exemption-first, per-segment rules, or a specific recovery flow — write it to `## Integration Shape` in `~/Clawic/data/stripe-api-integration/memory.md`, and if the reasoning took work (fraud rate by segment, conversion measured against liability), save it as `artifacts/decision-authentication.md` with its `## Boxes` line in the same turn.
