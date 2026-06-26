---
name: "Win-Back Campaign"
description: "Design automated win-back campaigns targeting lapsed customers with personalized re-engagement sequences across email, SMS, and paid ads, using recency-based segmentation to maximize reactivation rates and recovered revenue."
category: "ecommerce-marketing"
version: "1.0"
tags: ["win-back", "retention", "re-engagement", "lapsed-customers", "lifecycle-marketing", "ecommerce"]
---

# Win-Back Campaign Skill

Design and execute automated win-back campaigns that re-engage lapsed ecommerce customers through personalized, multi-channel sequences. This skill applies recency-frequency-monetary (RFM) segmentation to prioritize high-value defectors, then orchestrates coordinated touches across email, SMS, and paid ads to maximize reactivation rates and recovered revenue.

---

## Quick Reference

Use this table for fast decision-making during campaign design.

| Decision | Strong | Acceptable | Weak |
|---|---|---|---|
| **Lapse definition** | Custom per-brand based on historical repurchase intervals (e.g., 1.5x median order gap) | Industry-standard thresholds (90/180/365 days) | Single arbitrary cutoff with no data backing |
| **Segmentation model** | Full RFM scoring with tiered treatment paths | Recency-only segmentation with 3+ tiers | No segmentation; one message to all lapsed customers |
| **Incentive escalation** | Graduated offers that increase across the sequence (no discount > 10% off > 15% + free shipping) | Fixed discount offered at a strategic point in the sequence | Leading with the deepest discount on the first touch |
| **Channel orchestration** | Coordinated email + SMS + paid ads with suppression logic and frequency caps | Email primary with SMS for high-value segments only | Blasting all channels simultaneously with identical messaging |
| **Personalization depth** | Dynamic content referencing last-purchased products, browse history, and predicted preferences | Category-level personalization (e.g., "We miss you in Women's Shoes") | Generic "We miss you" with no product or behavioral context |
| **Sequence timing** | Data-driven intervals based on engagement signals and send-time optimization | Fixed cadence with reasonable spacing (e.g., Day 0, 7, 14, 21) | Random or overly aggressive timing (daily emails) |
| **Exit criteria** | Multi-signal: purchase, click-through with browse, explicit opt-out, hard bounce | Purchase or unsubscribe triggers exit | No exit logic; customers receive full sequence regardless of actions |
| **Success metrics** | Reactivation rate, recovered revenue, incremental lift vs. holdout, LTV of reactivated cohort | Open rate, click rate, conversion rate | Vanity metrics only (sends, impressions) |

---

## Solves

This skill addresses the following problems:

1. **Revenue leakage from customer churn** -- Existing customers who stop buying represent lost lifetime value that is 5-7x cheaper to recover than acquiring net-new customers.
2. **Undifferentiated re-engagement attempts** -- Sending the same "We miss you" email to all lapsed customers regardless of their value, recency, or purchase history wastes budget and trains customers to ignore outreach.
3. **Discount dependency** -- Brands that immediately offer deep discounts to lapsed customers erode margins and condition buyers to wait for deals rather than purchasing at full price.
4. **Channel fragmentation** -- Email, SMS, and paid ads operate in silos with no coordination, leading to redundant messaging, frequency fatigue, and an incoherent customer experience.
5. **Unclear lapse definitions** -- Without data-driven thresholds for when a customer is "lapsed," teams either act too early (wasting touches on customers who would have returned organically) or too late (after the customer has fully disengaged).
6. **No measurement of incrementality** -- Without holdout groups and proper attribution, teams cannot distinguish between customers who were genuinely won back and those who would have returned on their own.
7. **Compliance and deliverability risk** -- Mailing deeply lapsed contacts without proper list hygiene damages sender reputation, increases spam complaints, and risks regulatory violations under CAN-SPAM, GDPR, and TCPA.

---

## Workflow

### Step 1: Define Lapse Thresholds

Analyze historical purchase data to establish when a customer should be considered "lapsed" for this specific brand.

**Actions:**
- Pull median and average inter-purchase intervals for the past 12-24 months.
- Calculate the distribution of repurchase gaps (25th, 50th, 75th, 90th percentiles).
- Set the "at-risk" threshold at approximately 1.25x the median repurchase interval.
- Set the "lapsed" threshold at approximately 1.5x the median repurchase interval.
- Set the "deeply lapsed" threshold at 2x+ the median or 365 days, whichever is shorter.
- Validate thresholds by checking what percentage of customers who cross each threshold eventually return without intervention.

**Output:** A documented lapse definition table with three tiers and the data supporting each threshold.

### Step 2: Segment the Lapsed Population

Apply RFM segmentation to the lapsed customer base to create differentiated treatment groups.

**Actions:**
- Score each lapsed customer on Recency (time since last purchase), Frequency (total orders), and Monetary (total or average order value).
- Create segments such as: High-Value Recent Lapse, High-Value Deep Lapse, Low-Value Recent Lapse, Low-Value Deep Lapse, One-Time Buyers.
- Size each segment and estimate revenue potential based on historical AOV and predicted reactivation probability.
- Flag segments requiring special handling (e.g., customers acquired via deep discounts who never paid full price, seasonal-only buyers).
- Exclude customers who are undeliverable (hard bounces, invalid phone numbers), legally suppressed, or who have explicitly opted out.

**Output:** A segmentation table with segment names, sizes, value estimates, and assigned campaign tiers.

### Step 3: Design the Re-engagement Sequence

Build a multi-touch sequence for each major segment, mapping messages across channels with escalating urgency and incentives.

**Actions:**
- Define the number of touches per segment (typically 4-6 for high-value, 2-3 for low-value).
- Map each touch to a channel (email, SMS, paid ad) with clear reasoning for the channel choice.
- Write messaging frameworks for each touch that escalate from emotional/brand-centric to incentive-driven:
  - Touch 1: Reminder and value reinforcement (no discount).
  - Touch 2: Social proof, new arrivals, or personalized recommendations.
  - Touch 3: Modest incentive (e.g., 10% off or free shipping).
  - Touch 4: Stronger incentive with urgency (e.g., 15% off, 48-hour expiration).
  - Touch 5 (high-value only): Final appeal with best offer or personal outreach.
  - Touch 6 (high-value only): Sunset notice -- "We will stop emailing you unless you want to stay."
- Set timing intervals between touches based on engagement signals and segment tier.
- Define dynamic content blocks (last purchased product, recommended products, loyalty points balance).

**Output:** A sequence map per segment showing touch number, channel, timing, message theme, offer level, and dynamic content requirements.

### Step 4: Configure Channel-Specific Execution

Set up each channel with proper targeting, suppression, and tracking.

**Actions:**
- **Email:** Create templates, set up automated flows in ESP, configure suppression for purchasers and unsubscribers, warm up sending to deeply lapsed segments gradually.
- **SMS:** Draft compliant messages within character limits, ensure TCPA/consent compliance, set quiet hours, integrate short-link tracking.
- **Paid Ads:** Build custom audiences from lapsed segments, create retargeting ads on Meta/Google, set frequency caps (3-5 impressions per week), exclude converted customers in near-real-time.
- Implement cross-channel suppression: if a customer converts via email on Touch 2, suppress remaining SMS and ad touches.
- Set up UTM parameters and attribution tracking for each channel and touch.

**Output:** Channel configuration checklist with platform-specific settings, audience uploads, and suppression rules documented.

### Step 5: Establish Holdout Groups and Measurement

Create proper test/control structure to measure true incrementality.

**Actions:**
- Randomly hold out 10-15% of each segment as a control group that receives no win-back treatment.
- Define primary KPIs: reactivation rate, recovered revenue, incremental lift, cost per reactivation.
- Define secondary KPIs: open rate, click rate, unsubscribe rate, spam complaint rate, revenue per recipient.
- Set measurement windows (30-day, 60-day, 90-day post-campaign).
- Build a reporting dashboard or template to track performance by segment, channel, and touch.

**Output:** Measurement plan with holdout group definitions, KPI targets, and reporting cadence.

### Step 6: Launch and Optimize

Execute the campaign with phased rollout and continuous optimization.

**Actions:**
- Launch to the smallest or least-risky segment first to validate mechanics and deliverability.
- Monitor deliverability metrics (bounce rate, spam complaints) closely for the first 48-72 hours.
- A/B test subject lines, send times, offer levels, and creative within each touch.
- Review performance weekly against KPIs and holdout benchmarks.
- Adjust timing, messaging, or offers based on performance data.
- Document learnings for future campaign iterations.

**Output:** Launch schedule, monitoring checklist, and optimization log.

### Step 7: Post-Campaign Analysis and Iteration

Evaluate results, calculate ROI, and feed learnings back into the next cycle.

**Actions:**
- Compare reactivation rates and revenue between treatment and holdout groups across all segments.
- Calculate incremental revenue, cost per reactivation, and ROI by segment and channel.
- Identify which segments, channels, and touches drove the highest incremental lift.
- Analyze the behavior of reactivated customers post-campaign (do they make a second purchase? what is their projected LTV?).
- Determine which lapsed customers should be moved to a sunset/suppression list.
- Update lapse thresholds, segmentation rules, and sequence design based on findings.

**Output:** Post-campaign report with ROI analysis, segment-level findings, and actionable recommendations for the next iteration.

---

## Worked Examples

### Example 1: DTC Skincare Brand ($8M Annual Revenue)

**Context:** A direct-to-consumer skincare brand with a 45-day median repurchase interval, 120K total customers, and a growing churn problem. Email list is 95K, SMS subscribers are 35K. Average order value is $62.

**Step 1 -- Lapse Thresholds:**
- Median repurchase interval: 45 days.
- At-risk: 56 days (1.25x). Lapsed: 68 days (1.5x). Deeply lapsed: 90+ days (2x).
- Analysis shows 72% of customers who go beyond 90 days without purchasing never return organically.

**Step 2 -- Segmentation:**

| Segment | Criteria | Size | Est. Revenue Potential |
|---|---|---|---|
| VIP Lapsed (68-90 days) | 3+ orders, AOV > $75, last purchase 68-90 days ago | 2,400 | $198K |
| VIP Deeply Lapsed (90-180 days) | 3+ orders, AOV > $75, last purchase 90-180 days ago | 1,800 | $126K |
| Standard Lapsed (68-90 days) | 2+ orders, AOV $40-75 | 5,100 | $224K |
| Standard Deeply Lapsed (90-180 days) | 2+ orders, AOV $40-75 | 4,300 | $155K |
| One-Time Buyers (68-180 days) | 1 order only | 8,900 | $196K |
| Dormant (180+ days) | Any history, 180+ days | 6,200 | Suppressed -- sunset flow only |

**Step 3 -- Sequence Design (VIP Lapsed segment):**

| Touch | Day | Channel | Theme | Offer | Dynamic Content |
|---|---|---|---|---|---|
| 1 | 0 | Email | "Your skin routine is waiting" | None | Last purchased products, reorder CTA |
| 2 | 4 | SMS | Quick check-in | None | First name, product name |
| 3 | 8 | Email | New launches + personalized recs | None | Browsing-history-based recommendations |
| 4 | 14 | Email + Paid Ads | Loyalty reward unlock | Free deluxe sample with order | Points balance, sample product image |
| 5 | 21 | Email | Exclusive VIP offer | 15% off + free shipping | Best-sellers in their preferred category |
| 6 | 30 | Email | "Should we keep in touch?" | 20% final offer, 72hr expiry | Sunset warning |

**Step 4 -- Channel Configuration:**
- Email: Klaviyo flows with branching logic based on open/click behavior. Gradual send ramp for 90+ day segments (10% Day 1, 25% Day 2, 100% Day 3).
- SMS: Postscript integration, messages sent 10am-8pm local time only. Two SMS touches max for any segment.
- Paid Ads: Meta custom audiences updated daily. Frequency cap of 4 impressions/week. Lookalike exclusion to avoid prospecting overlap.
- Cross-channel suppression: Real-time purchase event triggers suppression across all three channels within 1 hour.

**Step 5 -- Measurement:**
- 12% holdout per segment (random assignment, stratified by RFM score).
- Primary target: 8% reactivation rate for VIP Lapsed (vs. estimated 3% organic return rate from holdout).
- Measurement window: 30 days post-last-touch.
- Weekly Slack report auto-generated from Klaviyo + GA4 data.

**Step 6 -- Results (after 30 days):**
- VIP Lapsed: 11.2% reactivation (holdout: 3.1%). Incremental lift: 8.1 percentage points.
- VIP Deeply Lapsed: 5.8% reactivation (holdout: 1.4%). Incremental lift: 4.4pp.
- Standard Lapsed: 6.9% reactivation (holdout: 2.8%). Incremental lift: 4.1pp.
- One-Time Buyers: 3.2% reactivation (holdout: 1.9%). Incremental lift: 1.3pp.
- Total incremental recovered revenue: $47,200.
- Campaign cost (creative + SMS + ads): $4,100. ROI: 10.5x.

---

### Example 2: Home Goods Marketplace ($22M Annual Revenue)

**Context:** A multi-brand home goods marketplace with a 120-day median repurchase interval, 280K customers, and heavy seasonality (Q4 peak). Email list is 210K, SMS is 62K. AOV is $94.

**Step 1 -- Lapse Thresholds:**
- Median repurchase interval: 120 days.
- At-risk: 150 days. Lapsed: 180 days. Deeply lapsed: 270+ days.
- Seasonal adjustment: Customers whose last purchase was in Q4 get a 30-day grace extension before being classified as lapsed (holiday gifters who may not repurchase until the following Q4).

**Step 2 -- Segmentation:**

| Segment | Size | Revenue Potential | Treatment Tier |
|---|---|---|---|
| High-Value Lapsed (180-270 days, AOV > $120, 3+ orders) | 4,100 | $574K | Premium 6-touch |
| Mid-Value Lapsed (180-270 days, 2+ orders) | 11,200 | $843K | Standard 4-touch |
| Low-Value Lapsed (180-270 days, 1 order, AOV < $60) | 15,800 | $521K | Light 2-touch |
| Deeply Lapsed (270-365 days, any value) | 18,400 | $460K | Reactivation 3-touch |
| Dormant (365+ days) | 22,100 | Suppressed | Sunset only |

**Step 3 -- Sequence Design (High-Value Lapsed):**

| Touch | Day | Channel | Theme | Offer |
|---|---|---|---|---|
| 1 | 0 | Email | "Discover what's new in your favorite categories" | None -- curated new arrivals |
| 2 | 5 | Paid Ads (Meta + Google Display) | Retargeting with top-rated products from browsed categories | None |
| 3 | 10 | Email | Customer favorites + UGC reviews | Free shipping (normally $8.95) |
| 4 | 17 | SMS | Flash access to a private sale | 12% off, 48hr window |
| 5 | 24 | Email | "Your home deserves an update" -- seasonal editorial | 15% off + free shipping |
| 6 | 35 | Email | Farewell + final offer | 20% off, 72hr expiry, sunset warning |

**Step 4 -- Channel Configuration:**
- Email: Iterable workflows with engagement scoring. Send-time optimization enabled. Suppression on purchase, unsubscribe, or spam complaint.
- SMS: Attentive platform. Single SMS touch for mid-value, zero for low-value. Consent verified against TCPA records before enrollment.
- Paid Ads: Meta CAPI integration for real-time audience syncing. Google Customer Match for search remarketing on branded + category terms. Combined ad budget: $6,500/month with daily pacing. Converted customers suppressed within 4 hours via automated audience exclusion.
- Cross-channel orchestration: Iterable serves as the orchestration layer. SMS and ad triggers are API-driven from Iterable flow branching.

**Step 5 -- Measurement:**
- 10% holdout per segment.
- Primary targets: 6% reactivation for High-Value Lapsed, 4% for Mid-Value, 2% for Low-Value.
- Secondary: Monitor deliverability -- target < 0.05% spam complaint rate and < 2% bounce rate on deeply lapsed sends.
- Attribution: 7-day click, 1-day view window for ads. Last-touch for email/SMS.

**Step 7 -- Post-Campaign Analysis (after 60 days):**
- High-Value: 7.8% reactivated (holdout: 2.2%). Incremental revenue: $89,400.
- Mid-Value: 4.4% reactivated (holdout: 1.6%). Incremental revenue: $62,100.
- Low-Value: 1.9% reactivated (holdout: 1.1%). Incremental revenue: $18,200.
- Deeply Lapsed: 2.1% reactivated (holdout: 0.6%). Incremental revenue: $31,500.
- Total incremental recovered revenue: $201,200.
- Total campaign cost: $14,800 (creative, SMS credits, ad spend). ROI: 12.6x.
- Key learning: Touch 3 (free shipping email) drove the highest single-touch conversion rate across all segments, suggesting shipping cost is a bigger barrier than product price for this audience.
- Action: Next iteration will test free shipping as the lead offer for mid-value segments, potentially removing percentage discounts entirely.

---

## Common Mistakes

1. **Leading with discounts.** Offering 20% off in the first touch trains customers to churn and wait for the win-back discount. Start with value, product recommendations, or emotional appeals. Reserve incentives for Touches 3-5.

2. **Treating all lapsed customers identically.** A VIP who spent $2,000 over 10 orders and a one-time buyer who spent $30 need fundamentally different win-back approaches. Segment by value and tailor treatment intensity accordingly.

3. **Ignoring deliverability when mailing deeply lapsed contacts.** Sending a bulk email to 50,000 contacts who have not opened an email in 6+ months will spike bounce rates and spam complaints, potentially damaging your sender reputation for all campaigns. Ramp gradually and warm up.

4. **No holdout group.** Without a control group, you cannot distinguish between customers who were genuinely influenced by the campaign and those who would have returned organically. A 10-15% holdout is a small cost for reliable measurement.

5. **Sending SMS without verified consent.** TCPA violations carry penalties of $500-$1,500 per message. Verify that every SMS recipient has explicit, documented opt-in consent before enrollment. Do not assume that email consent extends to SMS.

6. **Failing to suppress across channels.** A customer who converts via email on Day 3 should not receive an SMS offer on Day 5 and see retargeting ads for another week. Implement real-time cross-channel suppression triggered by purchase events.

7. **Setting arbitrary lapse thresholds.** Using "90 days" because it sounds right, without analyzing actual repurchase intervals, leads to either premature outreach (annoying active customers) or delayed action (contacting fully disengaged contacts). Let the data define the thresholds.

8. **Overly aggressive frequency.** Sending 6 emails in 10 days to someone who has already stopped engaging is more likely to generate an unsubscribe or spam complaint than a purchase. Space touches appropriately -- minimum 4-5 days between emails.

9. **No sunset logic.** Customers who do not respond to the full win-back sequence should be moved to a suppressed or drastically reduced-frequency list. Continuing to mail non-responders indefinitely destroys deliverability and wastes resources.

10. **Ignoring post-reactivation retention.** Winning a customer back with a 20% discount means nothing if they make one discounted purchase and immediately lapse again. Track second-purchase rates and LTV of reactivated cohorts to measure true campaign value.

---

## Resources

- **Output Template:** `references/output-template.md` -- Structured template for documenting your win-back campaign plan.
- **Segmentation Guide:** `references/segmentation-guide.md` -- Detailed guide on RFM segmentation for win-back targeting.
- **Channel Strategy Guide:** `references/channel-strategy-guide.md` -- Multi-channel strategy playbook for email, SMS, and paid ads.
- **Quality Checklist:** `assets/quality-checklist.md` -- 45-item checklist covering every aspect of campaign quality assurance.
- [Klaviyo Win-Back Flow Best Practices](https://www.klaviyo.com/blog/winback-email-examples) -- ESP-specific implementation guidance.
- [TCPA Compliance Guide](https://www.fcc.gov/consumers/guides/stop-unwanted-robocalls-and-texts) -- FCC guidance on SMS consent requirements.
- [Google Ads Customer Match](https://support.google.com/google-ads/answer/6379332) -- Setting up CRM-based audiences for paid remarketing.
- [Meta Custom Audiences Documentation](https://www.facebook.com/business/help/744354708981227) -- Building and managing retargeting audiences from customer lists.
