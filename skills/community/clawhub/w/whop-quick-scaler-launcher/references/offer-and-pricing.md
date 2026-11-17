# Offer and pricing

Use this module to turn a deliverable you can supply into a clear Whop offer, choose its billing model, and prepare optional follow-on offers without changing the buyer's original purchase.

Reference check: 2026-09-29. This is independent guidance, not official Whop documentation. All examples and calculation inputs are fictional. Field lessons describe operational failure modes, not universal platform behavior. Instructions to save, create, or change a resource require the owner's explicit approval; drafting this worksheet does not authorize a Whop write or a payment test.

## 1. Find an offer you can deliver

Start with a repeated buyer problem and something you can show. A course creator might need an outline workbook. A coaching business might sell a bounded review. An editorial service might deliver a recurring package of drafts and visuals.

1. Inventory what already exists: usable files, a repeatable service, production instructions, source material, and an example of the finished output. Check ownership and distribution rights.
2. Name the buyer's immediate job. Prefer “prepare an outline for a first course” to “build a successful business.” Separate what the seller delivers from what the buyer may achieve later.
3. Identify the purchase signal: a recurring request, a paid pilot, or an explicit problem confirmed by prospective buyers. Record what was actually observed. Audience size alone does not establish demand or willingness to pay.
4. Define a complete delivery unit. For an editorial package, specify the brief, draft, visuals, source checks, review rounds, and final handoff. A production-only offer ends at an approved draft; publishing is separate work unless included and authorized.
5. Run a delivery rehearsal with non-sensitive material. Measure production time, review time, tool costs, and support effort. Keep an example that passes the same quality checks a buyer will receive.
6. Choose the smallest package that solves the job on its own. A later upsell must not supply an essential part withheld from the original promise.

If the deliverable or its delivery route is missing, finish that before preparing an open checkout. If demand is unproven, call the offer a pilot hypothesis internally. Do not describe it publicly as a proven system.

### Offer worksheet

Fill this locally. Bracketed values are preparation fields, not finished sales copy.

```text
Buyer and immediate problem: [WHO / WHAT THEY NEED TO DO]
Evidence of demand: [SOURCE / DATE / OBSERVATION / LIMIT]
Promised deliverable: [WHAT THE BUYER RECEIVES]
Completion criteria: [WHAT MUST BE PRESENT AND WORKING]
Included quantity and format: [FILES / SESSIONS / OUTPUTS]
Delivery route and timing: [WHERE / WHEN / REQUIRED BUYER ACTION]
Access period: [START / DURATION / END]
Inputs required from the buyer: [MINIMUM NECESSARY INPUTS]
Support and correction allowance: [CHANNEL / SCOPE / LIMIT]
Excluded work: [WHAT IS SOLD SEPARATELY]
Available production capacity: [MEASURED CAPACITY / RESERVED BUFFER]
Price, currency, tax display and billing model: [APPROVED TERMS]
Renewal, cancellation and refund terms: [VERIFIED POLICY]
Sample and reuse rights: [APPROVED EVIDENCE]
Unresolved decisions: [ONE OWNER FOR EACH DECISION]
```

A recurring editorial service also needs a topic register to avoid selling duplicate work, a named approver, a correction limit, and a rule for missing buyer inputs. Define whether unused capacity expires or carries forward. Never invent that rule after payment.

## 2. Choose the billing model

Whop documents free, one-time, and recurring pricing, with separate controls for access and the apps included in a product. [O1, O2]

| Buyer receives | Sensible starting model | Decision to settle before sale |
|---|---|---|
| A finished workbook or a bounded review | One-time payment | Exact contents, delivery date, access duration, and support limit |
| Continuing access with maintained resources or an ongoing service | Recurring subscription | What is provided each period, renewal amount, cancellation, and access after cancellation |
| A fixed package paid over a finite schedule | Split payments, if supported and approved | Total commitment, payment count, timing, and missed-payment policy |
| A genuinely free sample | Free access | Precisely what is free and whether any later purchase requires fresh consent |

Use billing variants of the same product when the entitlement is the same but payment cadence differs. Use distinct products when the contents or access rights differ, and verify the app attachments for each. Current Whop API documentation calls purchasable pricing configurations “variants”; some interfaces and older integrations call them “plans.” [O1, O3]

Keep these facts separate:

- amount due at checkout;
- renewal amount and billing interval;
- number of payments, if finite;
- access duration;
- update and support duration;
- whether another purchase is permitted after expiry.

A prepaid term does not establish automatic renewal. A monthly equivalent shown beside an annual option does not mean the buyer pays monthly. State the amount actually charged and the billing schedule.

Whop's Seller Terms require specific access periods, durations, and delivery mechanisms and prohibit listings offering lifetime, perpetual, or indefinite access. Do not copy the “lifetime access” wording still present in the general pricing guide. Use the current terms and a defined access period. [O1, O8]

### Recurring-service capacity check

For an editorial subscription, count review and rework alongside writing. Set the promised volume below measured sustainable capacity and reserve time for blocked work. Document what happens when corrections exceed the allowance. Do not sell unlimited bespoke work on the assumption that automation makes it free.

A subscription with routine human edits is a managed service. Describe it that way. “Self-serve” is appropriate only when the buyer can obtain and use the promised product without normal operator intervention.

## 3. Set the price from delivery economics

Start with the cost of the promised unit, then test whether buyers value that unit at a viable price. Do not pick a price solely by copying an unrelated listing.

For each sale or billing period, record:

- production, review, support, and tool costs;
- actual account-specific payment fees and any fixed charges;
- affiliate commissions and acquisition costs, where applicable;
- expected refund and dispute costs, with uncertainty stated;
- the contribution needed to cover overhead and profit.

Do not treat tax collected for remittance as revenue. Keep reserves and payout delays in a separate cash-flow check. An unconfirmed referral payment must not make an otherwise loss-making offer look viable.

For a simplified tax-exclusive model in which percentage deductions use the same base:

```text
Minimum price = (unit costs + fixed fees + target contribution)
                / (1 - combined variable deduction rate)
```

Fictional worked example, not Whop pricing: unit costs of EUR 18, fixed fees of EUR 2, target contribution of EUR 16, and combined variable deductions of 10% give a price floor of EUR 40. This is a delivery-economics floor, not evidence that anyone will buy at that price. If commissions or taxes use different bases, calculate each line separately instead of using the shortcut.

For a pilot, record the proposed price, actual buyer objections, purchases, completed deliveries, support load, and refunds. Change one material offer variable at a time. A conversion claim needs measured visits and purchases from the same period and audience, not a screenshot of gross sales.

### Checkout reconciliation

Before an approved setup, compare the offer worksheet with the saved product, pricing variant, and exact checkout link:

1. Confirm the intended business and reuse a matching existing draft rather than creating a duplicate.
2. Read the current amount, currency, billing type, access duration, tax behavior, custom fields, metadata, and availability.
3. Distinguish any setup fee from the first subscription charge. The current variant reference says the amount due before tax and promo codes combines the initial fee and first renewal charge when no trial applies. During an eligible trial, the initial fee can still be due. [O3]
4. Check the actual buyer-facing total. In a fictional setup with an initial fee of EUR 10 and a recurring amount of EUR 25, the initial total without a trial would be EUR 35 before tax or discounts. Entering the full first-period amount in both fields would overcharge.
5. Choose currency localization deliberately. If the promise is an exact amount in a fixed currency, keep adaptive pricing off for that checkout and verify a fresh buyer view. Current documentation describes adaptive pricing for one-time payments; do not promise localized subscription billing. [O7]
6. Preserve existing custom fields and metadata when changing another setting. Close stale editor tabs without saving, then reopen them; an old form can overwrite a newer change made elsewhere.

Hidden visibility is not a closed checkout. For an authorized preparation-only setup, check effective purchase availability separately and inspect the direct link anonymously. If the supported setup path cannot keep sales closed, keep the preparation local. Preserve an already-live offer unless changing its availability was explicitly approved. [O2, O3]

## 4. Use trials deliberately

Whop documents free trials for recurring checkout links only. The buyer is automatically charged after the trial unless the subscription is canceled under the applicable terms. Trial eligibility can differ for a returning buyer. [O2, O4]

A trial is useful when the buyer can experience the recurring benefit during the trial window. A finished downloadable asset may be better served by a genuinely free excerpt, because the entire asset can be consumed before a trial ends.

Prepare the trial terms before enabling it:

```text
Due today: [AMOUNT AND CURRENCY, INCLUDING ANY INITIAL FEE]
Trial access: [CONTENTS] for [DURATION]
First recurring charge: [AMOUNT / CURRENCY / DATE OR CLEAR TIMING]
Later billing: [AMOUNT / INTERVAL]
Cancellation route and deadline: [VERIFIED INSTRUCTIONS]
Access after cancellation: [VERIFIED BEHAVIOR]
```

With approval, use Dashboard > Checkout links, select the intended recurring link, and edit its Free trial setting. Save only after checking the period, initial fee, and renewal terms. Read back the saved configuration, then inspect the rendered checkout. [O4]

Do not write “nothing to pay today” while an initial fee remains payable. Do not advertise “no card required” without observing that exact flow. A waitlist is a separate feature: the checkout-link guide describes collecting payment details and charging on approval. A free label alone does not prove a card-free, no-obligation interest list. [O2]

An authorized trial test should cover an eligible buyer, a returning buyer, cancellation, and the first charge. Mark any unexercised stage as untested. Never use a production account with a saved payment method for a casual click-through.

## 5. Build a post-purchase offer with separate checkout links

An upsell adds a higher level of help for the same job. A cross-sell adds a complementary product. Both require a new purchase decision.

A course creator might sell an outline workbook first and then offer an optional outline review. The workbook must remain usable without the review. Whop documents checkout configurations with their own `redirect_url` and returned `purchase_url`; these provide the routing mechanism. They do not by themselves create a tested one-click upsell. [O5]

Use a separate configuration for each paid step:

```text
Checkout A for the base offer
  -> after successful checkout: optional offer page
       -> Accept: canonical Checkout B
            -> after successful checkout: delivery hub
       -> No thanks: delivery hub for the base offer

For Whop-hosted access, the base offer remains reachable from the buyer's
purchase library. For external fulfillment, preserve the verified delivery
route independently of the optional-offer page.
```

The optional page is a presentation step, not proof of payment. Where delivery is custom-built, validate payment and entitlement server-side before granting access. A browser return or a URL query flag must never unlock paid content.

### Configuration recipe

1. Approve the base offer, optional offer, separate prices, and entitlement map. Check that the optional offer does not duplicate something the buyer already owns.
2. Verify the delivery destination and a visible decline route. The buyer must be able to reach the base purchase without accepting another offer.
3. Prepare Checkout B for the add-on and give it a terminal delivery destination.
4. Prepare Checkout A for the base purchase and set its checkout-specific redirect to the optional offer page. A direct redirect to Checkout B is suitable only if the buyer can clearly decline and reach the base purchase.
5. Bind the base purchase button to the exact returned purchase URL for Checkout A. Bind the optional purchase button to the exact returned purchase URL for Checkout B. Do not substitute a generic pricing link that lacks the configured redirect.
6. Read back both configurations and verify their business, product, price, currency, and redirect. Preserve other existing configuration fields.
7. Inspect all destinations on mobile and desktop before requesting a separately authorized transaction test.

Field lesson: do not put the entire chain in a shared product-level redirect. A redirect inherited by the next step can send a paid buyer back into the offer repeatedly. Draw the route and ensure every branch ends at delivery, with no path back to the same purchase step.

Do not build around an assumed native order-bump checkbox. The field setups behind this recipe used separate checkouts because that control was unavailable. Recheck the current interface before claiming that a native bump exists or is permanently absent. A third-party or custom implementation needs its own security, consent, and payment testing.

### Optional-offer copy template

Use the purchase-confirmation sentence only after the base purchase is verified.

```text
Your [BASE PRODUCT] purchase is complete.

Optional: add [COMPLEMENTARY DELIVERABLE].
It includes [SCOPE] and is delivered through [ROUTE / TIMING].

Additional charge: [AMOUNT AND CURRENCY / BILLING TERMS].
Your original purchase remains available if you skip this offer.

Purchase action: [BUY THE ADD-ON]
Decline action: [NO THANKS, OPEN MY PURCHASE]
```

### Required route tests

| Scenario | Expected result |
|---|---|
| Base payment succeeds, add-on declined | Base access works; no add-on charge or access |
| Base payment succeeds, add-on succeeds | Both entitlements work; delivery is the final destination |
| Add-on payment fails or is abandoned | Base access remains intact; no false add-on confirmation |
| Buyer revisits or refreshes the optional page | No automatic extra charge; no circular redirect |
| Buyer opens the optional page without buying the base offer | No base entitlement is granted merely from the visit |
| Buyer already owns the add-on | No misleading request to buy it again |

Before transactions are tested, report “redirect configured; payment and delivery not tested.” Opening the destination manually does not prove that a successful payment reaches it.

## 6. Separate displayed savings from a real discount

A crossed-out price is a display claim. A promo code or changed charge amount determines what the buyer actually pays. Verify them independently.

Field-observed display route: open the intended product's Growth tools and look for Show discount, then its percentage setting. This route comes from operator observations, not a current public API guarantee. Labels and availability must be checked in the selected business. If the control is absent, leave the savings display off until the supported method is established.

Do not assume that setting a strike-through price through a command updates the visible product page. Field attempts returned a saved value without the expected display, and clearing it was unreliable. Snapshot the original state and do not promise an automatic rollback.

Before displaying a reduction:

1. Establish a genuine, lawful comparison basis for the same product, scope, currency, billing period, and tax treatment. Keep the evidence privately.
2. Approve the actual charged price separately from the display percentage.
3. Calculate the saving from that basis. A fictional reduction from EUR 50 to EUR 40 is 20%, using `(reference - current) / reference × 100`.
4. Check the rendered reference price and payable amount, including rounding. Do not invent a reference price by working backward from a desired savings badge.
5. Verify any promotion dates, eligibility, and expiry. Never use a countdown that resets or a stock claim unrelated to real capacity.

For an actual promo code, Whop documents Dashboard > Marketing > Promo codes. Explicitly set its discount type, amount, duration, eligibility, expiry, usage limit, reuse rule, and eligible checkout links. Do not rely on the defaults. [O6]

A first-payment discount must not look like a permanent subscription price. State the later renewal amount alongside the discounted initial amount. If eligibility or discount combinations have not been tested, do not promise stacking.

## 7. Offer a relevant cross-sell

Recommend a complementary item only when it addresses a different, useful next job.

Fictional examples:

- a course outline workbook with a separately sold lesson-planning workbook;
- a coaching review with an optional implementation session;
- an editorial draft package with a separately approved publishing service.

Check whether the suggested item is already included. Show its separate price and access terms, keep the original delivery reachable, and make declining as clear as accepting. A cross-sell must not silently replace or renew the original purchase.

If a native recommendation setting is available in the exact account, inspect it before use. Otherwise, a clearly labeled optional page with a verified separate checkout is a workable design. This module does not claim a universal native cross-sell automation feature or authorize messages to existing buyers.

## 8. Operator handoff checklist

- [ ] The buyer problem, contents, sample, exclusions, and delivery criteria agree.
- [ ] Demand evidence is separate from assumptions; no revenue or outcome guarantee was invented.
- [ ] Price covers the approved scope, including review and support.
- [ ] Currency, tax display, amount due now, future charges, and access duration are explicit.
- [ ] Trial and discount wording match the exact checkout and eligibility rules.
- [ ] The base product works without any add-on; optional purchases are separate choices.
- [ ] Checkout-specific redirects have a terminal delivery route and a working decline path.
- [ ] No stale editor, default setting, or generic link has replaced the intended configuration.
- [ ] Preparation status, visibility, effective purchase availability, and marketplace status are reported separately.
- [ ] Saved settings, anonymous page checks, actual payments, and buyer delivery tests are reported as different evidence levels.

```text
Offer: [DESCRIPTION]
Approved terms: [BILLING / PRICE / CURRENCY / TAX / ACCESS]
Preparation status: [LOCAL ONLY OR AUTHORIZED REMOTE PREPARATION]
Configuration readback: [PASS / FAIL / NOT PERFORMED]
Buyer-facing checkout inspection: [PASS / FAIL / NOT PERFORMED]
Trial and discount checks: [RESULT / LIMIT]
Optional-offer routes: [RESULT / LIMIT]
Actual payment and delivery test: [RESULT / NOT AUTHORIZED / NOT PERFORMED]
Blocking decision, if any: [ONE DECISION / OWNER]
```

## Sources

All sources below were consulted on 2026-09-29. Product capabilities and interface labels can change; recheck the relevant source and exact account before implementation. No quoted example price or percentage in this module is a Whop fee or a merchant result.

- [O1] Whop Docs, [Set Up Pricing](https://docs.whop.com/manage-your-business/payment-processing/set-up-pricing). Billing models, app inclusion, access controls. Its lifetime-access wording conflicts with the Seller Terms cited in O8.
- [O2] Whop Docs, [Create a Checkout Link](https://docs.whop.com/manage-your-business/payment-processing/create-checkout-link). Link types, trials, waitlists, split payments, redirects, and direct-link visibility.
- [O3] Whop Docs, [Variant](https://docs.whop.com/api-reference/beta/variants/variant). Pricing configuration, initial amount due, renewal, trial eligibility, visibility, and access duration.
- [O4] Whop Docs, [Free Trials](https://docs.whop.com/manage-your-business/products/free-trials). Recurring-only trials, automatic charging, and repeat-trial behavior.
- [O5] Whop Docs, [Create a Checkout Configuration](https://docs.whop.com/api-reference/beta/checkout-configurations/create-a-checkout-configuration). Per-checkout redirect and returned purchase URL. The multi-step offer design and loop checks are operational recommendations.
- [O6] Whop Docs, [Promo Codes](https://docs.whop.com/manage-your-business/growth-marketing/promo-codes). Actual checkout discounts and their scope. This is not documentation for the field-observed Show discount control.
- [O7] Whop Docs, [Adaptive Pricing](https://docs.whop.com/payments-and-billing/fees/adaptive-pricing). Local-currency display and current one-time-payment scope.
- [O8] Whop, [Seller Terms](https://whop.com/seller-terms/), page updated 2026-07-14. Seller responsibilities, accurate pricing, defined access periods, and prohibition of indefinite-access listings.
