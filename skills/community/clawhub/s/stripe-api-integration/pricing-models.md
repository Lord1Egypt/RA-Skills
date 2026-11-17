# Pricing Models — Shaping What You Charge in Stripe Objects

**Read `## Catalog` in `~/Clawic/data/stripe-api-integration/memory.md`** (or `catalog.md` when `## Boxes` points there) before creating any price: the ids already in use, what replaced what, and which retired prices still have live subscriptions attached.

**Contents:** [Product, Price, Subscription Item](#product-price-subscription-item) · [What Is Immutable](#what-is-immutable) · [The Model Catalog](#the-model-catalog) · [Tiered Pricing: Graduated vs Volume](#tiered-pricing-graduated-vs-volume) · [Usage-Based Billing](#usage-based-billing) · [Seats](#seats) · [Discounts](#discounts) · [Changing Prices Without Breaking Live Subscriptions](#changing-prices-without-breaking-live-subscriptions) · [Multi-Currency](#multi-currency)

## Product, Price, Subscription Item

- **Product** = the thing sold. Name, description, images, metadata. One product, many prices.
- **Price** = an amount, a currency, an interval and a billing scheme. This is what a subscription points at.
- **Subscription item** = a price plus a quantity on one subscription. Multiple items on one subscription is how add-ons and mixed metered/flat plans are modelled.

The mapping people get wrong: monthly and annual are **two prices of one product**, not two products. Getting that right is what makes upgrade paths, reporting and the Billing Portal work without special cases.

## What Is Immutable

Once a price exists and is live, treat these as frozen: `unit_amount`, `currency`, `recurring[interval]`, the billing scheme, and the tier structure. You can change the nickname, metadata and `active`, and that is close to all.

The consequence: **changing a price means creating a new one.** Deactivating the old price stops new sales while existing subscriptions keep billing on it — which is correct behavior and also why the catalog needs the retired rows kept, with dates, instead of deleted (`memory-template.md`).

Products and prices can be archived, not meaningfully deleted, once they have been used. An archived price is invisible in new checkouts and still bills what is attached to it.

## The Model Catalog

| Model | Price shape | Fits | Watch out |
|---|---|---|---|
| Flat recurring | `unit_amount` + interval | Simple SaaS | Nothing scales with value; upgrades are manual |
| Per-seat | recurring + `quantity` | Team tools | Quantity changes mid-cycle proration (below) |
| Graduated tiers | tiered, `tiers_mode=graduated` | Usage where early units cost more | Customers cannot predict the bill without a calculator |
| Volume tiers | tiered, `tiers_mode=volume` | "Buy more, all units get cheaper" | A single unit over a boundary changes the whole bill |
| Package | `transform_quantity` (per N units, round up) | Credits, blocks of messages | Rounding up is the point; say so on the pricing page |
| Metered | recurring with usage reported against a meter | API and infrastructure products | Bill shock; needs in-product usage visibility |
| Flat + overage | two subscription items | Most usage products in practice | Two items means two lines on the invoice |
| One-time | non-recurring price | Setup fees, credits, hardware | Add as an invoice item, not as a subscription |
| Hybrid | multiple items on one subscription | Platform + seats + usage | The invoice must be readable by a human in finance |

## Tiered Pricing: Graduated vs Volume

Same tiers, different arithmetic, and the difference is a real amount of money.

Tiers: first 1,000 units at 0.10, next 9,000 at 0.05, beyond at 0.02. Customer uses 5,000 units.

- **Graduated** — each tier charges its own slice: `1,000 × 0.10 + 4,000 × 0.05 = 100 + 200 = 300`.
- **Volume** — the tier reached prices *every* unit: `5,000 × 0.05 = 250`.

Volume is simpler to explain and creates cliffs: crossing into the next tier can lower the total bill for higher usage, which customers will notice and game. Graduated never decreases with usage and is harder to quote. Pick from which conversation you would rather have with a customer, then write the worked example into the pricing page, because the number one support ticket for tiered plans is "how did you get this total".

Both modes support a per-tier `flat_amount` on top of the per-unit price — that is how "platform fee plus usage" fits in one price object.

## Usage-Based Billing

- Report usage against a **meter** with events carrying a customer reference, a value and a timestamp; the meter aggregates (sum, count, last value) over the billing period. Legacy integrations report usage records directly against a subscription item — which mechanism applies depends on the pinned `api_version` (`api-mechanics.md`).
- **Report with an idempotency-safe event identifier.** A retried usage report that double-counts is a bill you cannot defend, and usage is the one place customers audit line by line.
- **Timestamps decide the period.** An event reported late with a period-end timestamp lands in the wrong invoice; clock skew between your servers is a billing bug.
- **Aggregation choice is a pricing decision**: sum for consumption, maximum or last-value for "peak seats" or "provisioned capacity". Changing it later re-prices every customer.
- **Show usage in the product before the invoice shows it.** The most expensive usage-billing failure is not technical: it is a customer discovering the number for the first time on an invoice.
- Cap exposure with a hard limit or an alert at a threshold; a runaway loop on the customer's side becomes your refund.
- Usage arrives after the period, so the invoice for usage is issued in arrears while the flat fee is usually in advance. On a hybrid plan those are two different lines with two different periods, and finance will ask.

## Seats

- Quantity changes mid-cycle prorate by default: adding a seat on day 10 of 30 charges roughly two thirds of the seat, and removing one issues a credit against the next invoice.
- Decide the direction policy explicitly: prorate both ways, charge immediately for additions and credit at period end for removals, or no proration at all. Whatever the choice, it must match what the pricing page promises.
- Seat counts that change constantly generate proration line items that make an invoice unreadable. Options: bill on maximum seats used in the period (a metered model with `max` aggregation), or set a minimum commitment.
- Do not model seats as separate subscriptions per user. One subscription with quantity is the model the whole ecosystem expects.

## Discounts

- **Coupon** = the rule (percent or fixed, duration once / repeating / forever). **Promotion code** = the customer-facing string pointing at a coupon, with its own limits: max redemptions, expiry, first-time customers only, minimum amount.
- Always create promotion codes rather than sharing coupon ids: the code can be revoked and metered without touching the underlying rule.
- Fixed-amount coupons are currency-specific. A 20 USD coupon applied to a EUR subscription is a mistake waiting for the first international customer.
- Percentage discounts on tiered or metered prices apply to the computed total, which means the effective discount varies with usage — model it before promising it.
- Duration `repeating` counts billing periods, not months; on an annual plan "3 months" is three years.
- Every active code belongs in `## Catalog` with its redemption count and end date, because a code nobody remembers is a discount that never expires.

## Changing Prices Without Breaking Live Subscriptions

1. Create the new price. Never edit the old one.
2. Decide who moves: everyone on renewal, new customers only, or a named cohort. Grandfathering is a business decision and it must be written down, because in twelve months nobody will remember which cohort was on which price.
3. Migrate with a subscription update per customer, choosing the proration behavior deliberately: charge the difference now, or switch at the next renewal with no proration.
4. Preview before committing — the upcoming-invoice preview shows exactly what the customer will be charged. Announcing a price change from an estimate is how refunds happen (`subscriptions.md`).
5. Deactivate the old price so it stops appearing in new checkouts, keep its row in the catalog with the date and what replaced it.
6. Notify before billing. Beyond courtesy: an unannounced increase produces disputes with `subscription_canceled` as the reason and those are hard to win (`disputes.md`).

## Multi-Currency

- A price can carry currency options so one price object sells in several currencies, or you can create one price per currency. The first keeps the catalog small; the second gives full control over local rounding and psychological price points.
- Never let FX set your local price. `9.99 USD` converted is `9.13 EUR`, which nobody charges — pick the local number a human would print.
- Settlement and presentment currency differ: selling in a currency your account does not settle in triggers a conversion on payout (`reconciliation.md`).
- Record the presentment currencies under `platform` in `config.yaml` so examples stop defaulting to USD.

---

**When a price, product, coupon or promotion code is created, retired or replaced**, write its row to `## Catalog` in `~/Clawic/data/stripe-api-integration/memory.md` — id, model, amount with currency, interval, what it replaced — in the same turn. When the section passes ~15 entries, split it to `catalog.md` first (`memory-template.md`). A pricing migration plan that spans more than one session belongs in `artifacts/migration-<price>.md` with its `## Boxes` line.
