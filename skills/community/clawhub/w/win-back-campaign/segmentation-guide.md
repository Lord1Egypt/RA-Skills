# Recency-Frequency-Monetary Segmentation Guide for Win-Back Campaigns

This guide covers how to apply RFM segmentation specifically to lapsed customer populations for win-back targeting. It focuses on practical implementation rather than theory, with concrete scoring methods, segment definitions, and treatment recommendations.

---

## Why RFM for Win-Back

Win-back campaigns fail most often when they treat all lapsed customers the same. A customer who placed 15 orders over two years with a $120 AOV and lapsed 3 months ago is fundamentally different from a one-time buyer who spent $28 eleven months ago. RFM segmentation separates these populations so you can allocate budget, creative effort, and incentive depth proportionally to expected return.

**The core principle:** Invest the most in winning back customers who are the most recently lapsed and historically most valuable, because they have the highest probability of reactivation and the highest revenue upside.

---

## Scoring Methodology

### Step 1: Define the Scoring Population

Include only customers who meet your lapse threshold (see SKILL.md, Step 1). Do not score active customers -- they are not candidates for win-back.

**Population = all customers where:**
- Days since last purchase >= your "lapsed" threshold
- Customer has not been legally suppressed or hard-bounced
- Customer has at least one valid contact method (email or phone)

### Step 2: Score Each Dimension

Score each dimension on a 1-5 scale using quintile-based distribution. This ensures roughly equal-sized groups within each dimension.

#### Recency (R)

Measures how recently the customer last purchased, relative to other lapsed customers.

| Score | Definition | Example (if lapse threshold = 90 days) |
|---|---|---|
| 5 | Most recently lapsed (just crossed threshold) | 90-110 days ago |
| 4 | Recently lapsed | 111-140 days ago |
| 3 | Moderately lapsed | 141-180 days ago |
| 2 | Significantly lapsed | 181-270 days ago |
| 1 | Deeply lapsed | 271+ days ago |

**Important:** These are relative scores within the lapsed population. An R=5 customer is still lapsed -- they are simply the *most recently* lapsed.

**Implementation note:** Use percentile-based cutoffs from your actual data distribution rather than fixed day ranges. The example above is illustrative.

#### Frequency (F)

Measures total number of completed orders in the customer's lifetime.

| Score | Definition | Typical Thresholds |
|---|---|---|
| 5 | Highest purchase frequency | 8+ orders |
| 4 | High frequency | 5-7 orders |
| 3 | Moderate frequency | 3-4 orders |
| 2 | Low frequency | 2 orders |
| 1 | Single purchase | 1 order |

**Adjustment for tenure:** Consider normalizing frequency by customer tenure (orders per month) to avoid penalizing newer customers. A customer who placed 3 orders in 4 months is higher-frequency than one who placed 4 orders in 3 years.

#### Monetary (M)

Measures total revenue or average order value. Choose the metric that best reflects customer value for your business.

| Score | Definition | Use Total Revenue When... | Use AOV When... |
|---|---|---|---|
| 5 | Highest value | You want to prioritize cumulative spend | You want to identify high-ticket buyers regardless of frequency |
| 4 | High value | Product mix is narrow (similar prices) | Product mix is wide (varying price points) |
| 3 | Moderate value | | |
| 2 | Low value | | |
| 1 | Lowest value | | |

**Recommendation for most ecommerce brands:** Use total revenue as the primary monetary score, but flag customers with high AOV + low frequency separately -- they may be gift buyers or occasion-based purchasers requiring different messaging.

### Step 3: Calculate Composite Scores

Combine R, F, and M scores into a composite. Two approaches:

**Simple concatenation:** Create a 3-digit score (e.g., R5-F4-M5 = "545"). This preserves full detail and allows granular segmentation. Best when you have large enough segments to support many treatment paths.

**Weighted average:** Calculate a single score with weights reflecting your priorities.

Recommended weights for win-back:
- Recency: 40% (most predictive of reactivation probability)
- Frequency: 35% (indicates habit strength and brand affinity)
- Monetary: 25% (indicates revenue upside)

Formula: `Composite = (R * 0.40) + (F * 0.35) + (M * 0.25)`

A customer with R=4, F=5, M=3 scores: (4 * 0.40) + (5 * 0.35) + (3 * 0.25) = 1.6 + 1.75 + 0.75 = **4.10**

---

## Segment Definitions for Win-Back

Map composite scores to actionable segments. The following framework works for most ecommerce brands. Adjust names and thresholds to fit your business.

### Tier 1: Champions at Risk (Composite 4.0-5.0)

- **Profile:** High-frequency, high-value customers who recently crossed the lapse threshold. These are your best customers who stopped buying.
- **Size:** Typically 10-15% of lapsed population.
- **Reactivation probability:** High (15-25% with intervention).
- **Treatment:** Premium 5-6 touch sequence. Personalized outreach. Dedicated loyalty offers. Consider 1:1 outreach from a customer success rep for the highest-value individuals. Do not lead with discounts -- these customers have strong brand affinity and may respond to new products, exclusive access, or emotional appeals.
- **Channel priority:** Email (primary) + SMS (secondary) + Paid Ads (supporting).

### Tier 2: Loyal Lapsed (Composite 3.0-3.9)

- **Profile:** Moderate-to-high frequency customers with decent value who have been lapsed for a moderate period.
- **Size:** Typically 20-30% of lapsed population.
- **Reactivation probability:** Moderate (8-15% with intervention).
- **Treatment:** Standard 4-touch sequence. Category-level personalization. Moderate incentives starting at Touch 3. Test free shipping vs. percentage discount.
- **Channel priority:** Email (primary) + Paid Ads (supporting). SMS only if consent is confirmed and the customer has engaged with SMS previously.

### Tier 3: Occasional Defectors (Composite 2.0-2.9)

- **Profile:** Low-to-moderate frequency, moderate value, or a mix of scores that averages out to the middle.
- **Size:** Typically 25-35% of lapsed population.
- **Reactivation probability:** Low-moderate (4-8% with intervention).
- **Treatment:** Light 2-3 touch email sequence. Broader category recommendations rather than specific product picks. Consider a simple incentive at Touch 2 to create urgency.
- **Channel priority:** Email only. Ad spend is generally not ROI-positive for this tier.

### Tier 4: One-and-Done (Composite 1.0-1.9)

- **Profile:** Single-purchase, low-value, deeply lapsed. These customers may have been deal-seekers, gift buyers, or simply did not connect with the brand.
- **Size:** Typically 25-35% of lapsed population.
- **Reactivation probability:** Low (1-4% with intervention).
- **Treatment:** Minimal -- 1-2 email touches maximum. Test whether any intervention is ROI-positive vs. holdout. If not, suppress and reallocate budget to higher tiers. Generic "discover what's new" messaging rather than personalized outreach.
- **Channel priority:** Email only, lowest send priority.

### Tier 5: Sunset / Suppress (Below minimum threshold or non-responsive to prior win-back)

- **Profile:** Customers who have been lapsed beyond your maximum window (e.g., 365+ days) or who have already received a full win-back sequence without responding.
- **Treatment:** One final sunset email offering the choice to stay on the list. Non-responders are moved to a permanent suppression list. Do not invest further.

---

## Special Segment Handling

### Seasonal Buyers

Customers whose purchase history shows a clear seasonal pattern (e.g., only buys during Q4, only buys in summer) should be flagged and either:
- Excluded from win-back until their expected purchase season approaches.
- Placed in a seasonal-specific win-back flow timed to 2-4 weeks before their historical purchase period.

**Detection:** Look for customers where 80%+ of purchases fall within the same 90-day window across multiple years.

### Discount-Acquired Customers

Customers whose first (and often only) purchase was made using a deep discount (40%+ off, first-order promo) have a significantly lower predicted reactivation rate at full price. Segment these separately and set realistic expectations -- many were never profitable customers.

**Treatment option:** Test a value-framing approach ("Here is what you are missing at full price") against a discount approach. Track whether reactivated discount-acquired customers ever make a full-price purchase.

### High-Monetary, Low-Frequency Outliers

Customers with 1-2 orders but very high AOV (e.g., $500+ in a brand where average is $60) may be gift buyers, interior designers, or bulk purchasers. Their win-back messaging should acknowledge their purchase context rather than using standard "we miss you" language.

---

## Data Requirements

To implement RFM segmentation for win-back, you need at minimum:

| Data Point | Source | Required / Optional |
|---|---|---|
| Customer ID | CRM / Ecommerce platform | Required |
| Email address | CRM / ESP | Required |
| Phone number | CRM / SMS platform | Optional (required for SMS) |
| Date of each order | Ecommerce platform | Required |
| Order count (lifetime) | Ecommerce platform / calculated | Required |
| Total revenue (lifetime) | Ecommerce platform / calculated | Required |
| Average order value | Calculated | Required |
| Last purchased product(s) | Ecommerce platform | Recommended |
| Product categories purchased | Ecommerce platform | Recommended |
| Email engagement (last open/click date) | ESP | Recommended |
| SMS consent status and date | SMS platform | Required for SMS |
| Acquisition source / first-order discount | CRM / attribution | Optional |
| Browse history (last 90 days) | Site analytics / CDP | Optional |

---

## Validation and Refresh

### Initial Validation

After building segments, validate by checking:
- Are segment sizes reasonable? No segment should be less than 500 customers (too small for statistical significance) or more than 50% of the population (too broad to be meaningful).
- Do historical organic return rates decrease as you move from Tier 1 to Tier 4? If not, your scoring weights may need adjustment.
- Does the estimated revenue potential justify the planned investment for each tier?

### Ongoing Refresh

- Re-score the lapsed population weekly or bi-weekly as new customers cross lapse thresholds and existing lapsed customers age.
- Customers who complete the win-back sequence without converting should be moved to Tier 5 (Sunset/Suppress).
- Customers who are reactivated should be removed from lapsed segments immediately and placed into post-purchase retention flows.
- Review and update scoring thresholds quarterly based on changing purchase patterns and business conditions.
