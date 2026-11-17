# Tax — VAT, Sales Tax, and Invoice Compliance

**Read `tax_handling` in `~/Clawic/data/stripe-api-integration/config.yaml` and `## Account Context` in `memory.md`** before touching tax: the entity's country and its registrations decide what is owed, and a calculation without a registration is a number with no legal meaning.

**Contents:** [Registration Comes First](#registration-comes-first) · [What Stripe Tax Does and Does Not Do](#what-stripe-tax-does-and-does-not-do) · [Inclusive vs Exclusive](#inclusive-vs-exclusive) · [B2B and Reverse Charge](#b2b-and-reverse-charge) · [Digital Goods and Place of Supply](#digital-goods-and-place-of-supply) · [US Sales Tax and Nexus](#us-sales-tax-and-nexus) · [Invoice Fields That Make It Compliant](#invoice-fields-that-make-it-compliant) · [Refunds, Credit Notes and Rate Changes](#refunds-credit-notes-and-rate-changes) · [Filing](#filing)

## Registration Comes First

Tax is owed where you are registered, or where you crossed a threshold and should have registered. Nothing in the API changes that order.

- Selling into a jurisdiction without a registration usually means no tax to collect *yet*, and a threshold quietly filling up. The EU one-stop-shop threshold for cross-border digital sales to consumers, US economic nexus thresholds per state, and UK VAT registration all work this way.
- Crossing a threshold retroactively creates an obligation. The money owed comes out of margin, because you cannot go back and add tax to invoices already paid.
- Monitor thresholds continuously, not annually. Stripe Tax can surface where you are approaching one; whoever owns finance has to act on it.
- Registration numbers, entity country and where you are registered belong in `## Account Context`, because every later question depends on them.

## What Stripe Tax Does and Does Not Do

| Does | Does not |
|---|---|
| Determine the customer's location and the applicable rate | Register you anywhere |
| Calculate tax per line item, inclusive or exclusive | File returns or remit money by itself |
| Validate B2B tax ids and apply reverse charge | Decide your product's tax category — you do |
| Produce reports per jurisdiction for filing | Fix historical invoices computed without it |
| Monitor threshold progress | Give legal advice about nexus |

It is priced per transaction; that line belongs in `~/Clawic/data/finances/subscriptions.md` alongside other paid add-ons, and in the unit economics.

The alternative path — an external engine, or manual rates — is legitimate for a business selling in one jurisdiction with one rate. It stops being legitimate the moment cross-border consumer sales start.

## Inclusive vs Exclusive

- **Exclusive**: tax is added on top of the listed price. Standard for B2B and for the US, where prices are shown pre-tax.
- **Inclusive**: the listed price already contains tax. Standard for consumer prices in the EU and UK, where showing a price and then adding VAT at checkout is both surprising and, in many places, not allowed.
- The choice changes your revenue per sale, not the customer's total. On a 100 EUR inclusive price at 21% VAT, net revenue is `100 ÷ 1.21 = 82.64` and tax is `17.36` — the same headline number is a 17% smaller sale than an exclusive 100 EUR.
- Setting behavior per price is deliberate: consumer prices inclusive, business prices exclusive, and the pricing page saying which.
- Never change the behavior on a live price. Create a new one (`pricing-models.md`).

## B2B and Reverse Charge

- A business customer in another EU member state with a valid VAT number is generally invoiced with **reverse charge**: zero tax, and the invoice states that the customer accounts for it.
- "Valid" means validated against the official registry — Stripe Tax does this. An unvalidated number is a number the auditor will not accept, and the tax then falls on you.
- Collect the tax id at checkout with tax-id collection enabled; retrofitting it means credit-noting and reissuing invoices.
- Store the tax id on the customer object, not in your own table only — it has to appear on the invoice.
- Domestic B2B is not reverse charge: same-country business sales carry normal VAT.
- The customer's country comes from evidence, not from a form field they typed. Billing address, payment method country and IP location should agree; when they do not, the rules of the jurisdiction decide which wins.

## Digital Goods and Place of Supply

- For digital services sold to consumers in the EU, tax is due where the **customer** is, at that country's rate — which is why a single European price collects a different net amount per country.
- Product tax category matters: ebooks, SaaS, physical goods, training and events are taxed differently in many jurisdictions, and the default category is rarely right for all of your catalog.
- Set the tax code per product, once, at creation. A wrong category applied for a year is a restatement.
- Physical goods add shipping-based rules and destination sourcing that digital goods do not have.

## US Sales Tax and Nexus

- Nexus is created by physical presence *or* by economic activity above a state's threshold — thresholds differ per state and count revenue, transactions, or both.
- Registration is per state, filing is per state, and rates vary below state level: county and city rates stack on top, so "the California rate" is not one number.
- SaaS taxability varies by state: taxable in some, exempt in others, and conditionally taxable in a few. This is the single most common surprise for a European seller entering the US.
- Exemption certificates exist for resellers and nonprofits; if you accept them you have to store them and honor them, and that is a process, not a field.

## Invoice Fields That Make It Compliant

A "receipt" is not an invoice. What a compliant invoice typically needs, in most VAT jurisdictions:

- A sequential invoice number with no gaps, and the issue date.
- Full legal name and address of the seller **and** the buyer.
- Seller's VAT/tax registration number; the buyer's too when reverse charge applies.
- Line items with net amount, tax rate and tax amount, and the totals.
- The currency, and where a domestic reporting currency differs, the exchange rate used.
- The reverse-charge statement when it applies.
- Requirements differ by country, and some jurisdictions mandate e-invoicing formats or clearance systems that Stripe's invoice does not produce. Check locally before assuming the PDF is sufficient (`invoices.md` covers invoice mechanics).

Gaps in the numbering sequence are an audit flag. That is why voiding an invoice is correct and deleting one is not.

## Refunds, Credit Notes and Rate Changes

- A refund of a taxed sale refunds the tax too, and the credit note is what evidences it. Refunding the charge without the credit note leaves your tax report overstating what you collected.
- Partial refunds allocate tax proportionally per line item — the arithmetic is per line, not on the total.
- When a jurisdiction changes its rate, the applicable rate is the one at the time of supply, not the time of payment. Subscriptions spanning the change date need the rate that applied to each period.
- Never edit a finalized invoice to fix tax. Credit note, then reissue.

## Filing

- Stripe Tax reports summarize what was collected per jurisdiction and period; filing and remitting are separate, either manually or through a filing partner.
- Reconcile collected tax against what the balance shows before filing — tax collected is not your revenue and should never be spent as if it were (`reconciliation.md`).
- Put the filing cadence per jurisdiction in the `## Due` table; a missed VAT return is a penalty with interest, and it is the most avoidable cost in this file.

---

**When a registration, tax behavior, product tax category or filing cadence is established**, write the registrations and entity details into `## Account Context` in `~/Clawic/data/stripe-api-integration/memory.md`, put `tax_handling` and the inclusive/exclusive convention into `config.yaml`, add each filing deadline as a row in `## Due`, and record the Stripe Tax fee line in `~/Clawic/data/finances/subscriptions.md`. A tax determination that took real work — a nexus analysis, a category decision across the catalog — is `artifacts/decision-tax-<jurisdiction>.md` with its `## Boxes` line.
