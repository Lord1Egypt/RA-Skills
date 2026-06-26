---
name: subscription-builder
description: Design a subscription or auto-replenishment program for consumable products including pricing tiers, frequency options, churn-reduction tactics, and the onboarding flow that maximizes trial-to-paid conversion.
---

# Subscription Builder

Design and launch subscription or auto-replenishment programs for consumable products. This skill covers the full lifecycle: pricing architecture, delivery cadence, onboarding flows, retention mechanics, and win-back sequences.

---

## Quick Reference

| Decision | Strong | Acceptable | Weak |
|---|---|---|---|
| **Discount depth for subscribe-and-save** | 10-15% off one-time price | 5-9% or 16-20% off | >25% off (trains discount dependence) or 0% (no incentive) |
| **Default frequency setting** | Matches median consumption rate from customer data | Rounded estimate based on product size and typical use | Arbitrary interval with no data backing |
| **Number of frequency options** | 3-4 intervals per product | 2 or 5 intervals | 1 fixed interval or 6+ (choice paralysis) |
| **Onboarding commitment** | No commitment, skip/cancel anytime with 1-click | 3-order minimum with clear disclosure | Hidden commitments, cancellation buried in support tickets |
| **Churn intervention timing** | Predictive model flags at-risk subscribers 7-14 days before next order | Triggered at cancellation attempt | No intervention until post-cancellation survey |
| **Price anchoring on PDP** | Subscription price shown as primary with one-time price crossed out | Both prices shown side by side with savings highlighted | Subscription option hidden behind a tab or toggle |
| **Trial-to-paid bridge** | Personalized email sequence starting day 7 of first cycle | Single reminder email 3 days before renewal | No communication between order 1 and order 2 |

---

## Solves

1. **Low repeat-purchase rate on consumable SKUs** -- Customers buy once but do not return on a predictable schedule, leaving revenue volatile and CAC payback periods long.
2. **Unpredictable demand forecasting** -- Without subscription commitments, inventory planning relies on seasonal guesswork rather than locked-in future orders.
3. **High customer acquisition cost with no LTV leverage** -- One-time buyers never reach profitability if CAC exceeds first-order margin; subscriptions extend LTV across multiple shipments.
4. **Churn after the second or third order** -- Subscribers sign up for the discount but cancel before the program becomes profitable, creating a "subscription tourist" problem.
5. **Cart abandonment on replenishable products** -- Customers intend to 42-day median reorder, 16% repeat rate)
- Tier 3 (skip): Seasonal immunity kit, trial-size samplers

**Step 2 -- Pricing Architecture:**
- Base subscribe-and-save discount: 12% (Multivitamin: $30.79/shipment, Omega-3: $26.39/shipment)
- Loyalty escalator: 12% months 1-4, 15% months 5+
- Bundle bonus: Subscribe to both Multivitamin + Omega-3, get an extra 3% off (total 15% from order 1)
- Prepay: 6-month prepay at 20% off ($167.95 for Multivitamin, saving $41.99 vs. six one-time purchases)
- Annual savings messaging on PDP: "Subscribe and save $50.28 per year on your daily multivitamin"

**Step 3 -- Frequency Options:**
- Multivitamin: 15 days, 30 days (default), 45 days, 60 days
- Omega-3: 30 days (default), 45 days, 60 days
- Smart schedule note: "Most customers reorder every 30-35 days. We recommend monthly delivery."

**Step 4 -- Onboarding Flow:**
- PDP widget: Subscription pre-selected, showing "$30.79/month -- save 12%" vs. crossed-out "$34.99 one-time"
- Welcome sequence: Confirmation (day 0), portal intro (day 3), "How to get the most from your multivitamin" dosage guide (day 10), subscriber-only content on ingredient sourcing (day 18), pre-shipment reminder with add-on prompt for Omega-3 cross-sell (day 26)

**Step 5 -- Churn Reduction:**
- Predictive flag: Subscriber skips order or does not open last 3 emails triggers a "check in" email with usage tips
- Cancellation flow: Skip offer first, then frequency extension to 45 days, then 20% off next order, then a $10 comeback credit valid 60 days
- Win-back: Reason-specific responses -- "too much product" gets frequency adjustment offer, "too expensive" gets prepay pitch, "switching brands" gets comparison content

**Projected impact (6-month forecast):**
- Subscription attach rate target: 30% of Tier 1 SKU orders
- Month-6 active subscribers: approximately 2,100
- Incremental monthly recurring revenue: approximately $65,000
- Order-2 retention rate target: 80%
- Subscriber LTV at 8-month average tenure: $246 vs. one-time buyer average of $52

---

### Example 2: Roast Republic -- A Specialty Coffee Brand

**Context:** Roast Republic sells single-origin and blended whole-bean coffee DTC via a custom storefront. Product lineup: 6 single-origin coffees ($18.99/12oz bag), 3 blends ($15.99/12oz bag), a discovery sampler ($24.99/3x4oz). Monthly revenue is $210K. Average customer consumes 1 bag every 12-16 days. Repeat purchase rate is 31% within 60 days -- strong signal but no subscription infrastructure to capture it.

**Step 1 -- Product-Market Fit Audit:**
- Tier 1 (launch): All 6 single-origins and 3 blends (consistent consumption pattern, low reorder interval variance)
- Tier 2 (phase 2): Discovery sampler reframed as a rotating subscription ("Explorer's Club" -- new single-origin each shipment)
- Tier 3 (skip): Brewing equipment, gift sets

**Step 2 -- Pricing Architecture:**
- Base discount: 10% (Singles: $17.09/bag, Blends: $14.39/bag)
- No loyalty escalator (margins tighter on coffee; use freshness and convenience as retention value instead of deeper discounts)
- Multi-bag discount: Subscribe to 2+ bags per shipment, get 13% off. 3+ bags, get 15% off.
- Prepay: Not offered (consumption preferences change frequently in specialty coffee; prepay creates refund risk)
- Messaging: "Always fresh, always on time. Save 10% and never run out."

**Step 3 -- Frequency Options:**
- Per-bag frequencies: Every 1 week, 2 weeks (default), 3 weeks, 4 weeks
- "Roast match" quiz on product page: "How many cups per day do you drink?" combined with brew method to recommend the right frequency and bag quantity
- Swap-friendly: Subscribers can change their coffee selection each cycle through the portal or a "surprise me" toggle for variety

**Step 4 -- Onboarding Flow:**
- PDP widget: "Subscribe -- $17.09 every 2 weeks" pre-selected, one-time option secondary. Roast date guarantee badge: "Always roasted within 48 hours of your shipment."
- Welcome sequence:
  - Day 0: Order confirmation with roast profile card and tasting notes
  - Day 2: "Your brew guide" -- specific brewing recommendations for the selected origin
  - Day 5: Invite to subscriber-only Slack or Discord community
  - Day 10: "Rate your roast" feedback request (fuels personalization engine)
  - Day 12: Pre-shipment: "Your next bag ships in 2 days. Want to try something new?" with swap option

**Step 5 -- Churn Reduction:**
- Flavor fatigue mitigation: After 3 consecutive orders of the same coffee, proactively suggest a new origin with "Subscribers who love [current coffee] also love [recommendation]"
- Cancellation flow: "Want to try a different coffee instead?" swap offer first, then skip, then frequency adjustment, then 15% off next order
- Seasonal reactivation: Lapsed subscribers get early access to limited-edition seasonal roasts
- "Pause for travel" feature prominently placed in portal (reduces cancellations from temporary non-use by 30-40%)

**Projected impact (6-month forecast):**
- Subscription attach rate target: 35% of coffee orders
- Month-6 active subscribers: approximately 1,800
- Incremental MRR: approximately $38,000
- Average bags per subscriber per month: 2.1
- Order-2 retention: 82% (coffee subscriptions benchmark higher due to daily consumption)
- Subscriber LTV at 10-month average tenure: $360 vs. one-time buyer average of $34

---

## Common Mistakes

1. **Setting the discount too high to "win" subscribers.** A 25-30% subscribe-and-save discount attracts deal-seekers who cancel after one order. The discount should reflect genuine convenience value (10-15%), not act as a loss leader.

2. **Offering only one delivery frequency.** A single fixed interval (e.g., "every 30 days") ignores consumption variance. Customers who consume faster accumulate backlog; slower consumers feel pressured. Both cohorts churn.

3. **Burying the subscription option on the PDP.** If the subscription is a secondary tab, toggle, or separate page, conversion will be 50-70% lower than when it is the pre-selected default with a clear one-time alternative.

4. **No communication between order 1 and order 2.** The gap between first and second shipment is the highest-churn window. Brands that send zero emails during this period see 25-35% cancellation before order 2. The onboarding sequence is not optional.

5. **Making cancellation difficult.** Requiring a phone call, chat session, or multi-page flow to cancel creates negative reviews, social media complaints, and chargebacks. One-click cancellation with an optional save offer outperforms friction-based retention every time.

6. **Ignoring failed payment recovery (dunning).** 10-15% of subscription orders fail due to expired cards, insufficient funds, or bank declines. Without automated retry logic and customer notification, these become involuntary churn. A proper dunning sequence recovers 40-60% of failed payments.

7. **Treating all subscribers identically.** A subscriber on month 1 and a subscriber on month 14 have fundamentally different needs. Segment communications, offers, and retention tactics by tenure, engagement level, and product category.

8. **Not tracking the right metrics.** Measuring only "total active subscribers" masks churn problems. Track cohort retention curves (what percentage of the January cohort is still active in July?), not just aggregate counts.

9. **Launching with too many SKUs.** Start with 2-4 highest-fit SKUs, prove the model, then expand. Whole-catalog launches dilute focus and complicate operations.

10. **Forgetting inventory and fulfillment implications.** Subscription orders must ship on schedule. Reserve inventory and prioritize subscription fulfillment accordingly.

---

## Resources

- [Output Template](references/output-template.md) -- Structured deliverable format for subscription program design documents
- [Pricing Strategy Guide](references/pricing-strategy-guide.md) -- Detailed guidance on subscription pricing models, discount tiers, and price anchoring
- [Churn Reduction Playbook](references/churn-reduction-playbook.md) -- Comprehensive tactics for proactive retention, reactive saves, and win-back sequences
- [Quality Checklist](assets/quality-checklist.md) -- Pre-launch validation checklist covering all program components
