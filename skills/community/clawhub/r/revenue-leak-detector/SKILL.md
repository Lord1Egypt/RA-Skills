---
name: Detect Revenue Leaks & Alert Teams via Slack Integration
description: "Identify high-value audience segments missing premium monetization opportunities. Analyzes subscriber databases and engagement patterns to generate upsell sequences. Use when the user needs LTV optimization, churn prevention, or strategic revenue growth."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {
    "openclaw": {
      "requires": {
        "env": ["STRIPE_API_KEY", "MAILCHIMP_API_KEY", "GOOGLE_SHEETS_API_KEY"],
        "bins": ["python3", "curl"]
      },
      "os": ["macos", "linux", "win32"],
      "files": ["SKILL.md"],
      "emoji": "💰"
    }
  }
---

# Revenue Leak Detector

## Overview

The Revenue Leak Detector is a comprehensive monetization analytics skill that uncovers hidden revenue opportunities within your existing audience. Instead of focusing on acquisition, this tool analyzes your subscriber/customer database to identify high-value segments that are undermonetized or completely untapped by premium offerings.

**Why This Matters:**
- 60-75% of revenue growth comes from existing customers (not new ones)
- Most businesses leave 40%+ of potential LTV on the table by poor segmentation
- Targeted upsell sequences can increase customer value by 200-300%

**Integrations & Data Sources:**
This skill works with:
- **Email Platforms:** Mailchimp, ConvertKit, ActiveCampaign, Klaviyo
- **Payment Systems:** Stripe, Paddle, Gumroad, Lemonsqueezy
- **Analytics:** Google Analytics 4, Mixpanel, Segment
- **CRM/Databases:** WordPress (WooCommerce), Shopify, custom CSV exports
- **Messaging:** Slack notifications for key findings
- **Spreadsheets:** Google Sheets export for team collaboration

---

## Quick Start

### Example 1: Basic Subscriber Database Analysis
```
Analyze my Mailchimp subscriber database for revenue leaks. 
I have 5,000 email subscribers with the following tiers:
- Free tier: 3,200 subscribers
- Paid tier ($29/mo): 1,500 subscribers  
- Premium tier ($99/mo): 300 subscribers

Show me which segments should receive upsell campaigns and what sequences to use.
```

**What Happens:**
The skill connects to your Mailchimp account, analyzes engagement metrics (open rates, click rates, purchase history), identifies free subscribers showing high engagement patterns, and recommends specific upsell sequences.

---

### Example 2: Historical Customer Churn Prevention
```
I have a CSV with 2,000 past customers who churned. Columns include:
- purchase_date, total_ltv, last_purchase_date, engagement_score, product_tier

Which of these churned customers are worth win-back campaigns? 
Generate specific reactivation sequences targeting high-LTV segments.
```

**What Happens:**
The skill calculates potential recoverable revenue, identifies the ideal win-back messaging by tier, calculates optimal timing for re-engagement, and produces ready-to-use email sequences.

---

### Example 3: Premium Upsell Opportunity Matrix
```
My Stripe data shows 8,000 active customers. Create a matrix showing:
- Which customer cohorts (by signup date, region, product usage) have 
  the highest upsell potential
- What premium features to emphasize for each segment
- Recommended pricing/bundling for maximum conversion without churn
- Optimal send frequency and timing for each segment
```

**What Happens:**
The skill analyzes purchase history, feature usage patterns, and cohort behavior to generate a prioritized upsell roadmap with specific messaging recommendations per segment.

---

## Capabilities

### 1. Audience Segmentation & Scoring
- **RFM Analysis** (Recency, Frequency, Monetary value) to identify your most valuable segments
- **Engagement Scoring** across email, product usage, and purchase signals
- **Cohort Analysis** by signup date, geography, traffic source, and product tier
- **Churn Risk Scoring** to flag at-risk high-value customers before they leave
- **Upsell Readiness Scoring** (0-100) indicating which customers are most likely to convert to premium

### 2. Revenue Opportunity Detection
- Identifies customers with high engagement but low monetization
- Calculates "revenue gap" = potential LTV vs. current LTV per segment
- Prioritizes segments by absolute revenue opportunity (highest $ impact first)
- Estimates conversion rates based on historical segment performance
- Projects 90-day revenue impact of targeted upsell campaigns

### 3. Automated Upsell Sequence Generation
- Creates tier-specific upsell messaging (how to frame premium to free users vs. how to upgrade $29→$99)
- Recommends optimal send frequency per segment (avoid fatigue while maximizing conversions)
- Generates subject lines A/B tested against similar audiences
- Includes value props matched to each segment's demonstrated interests
- Builds multi-touch sequences with fallback messaging

### 4. Churn Prevention & Win-Back
- Identifies high-value customers showing churn signals (declining engagement, no purchase in 90 days)
- Generates targeted retention messaging BEFORE churn occurs
- Analyzes past churned customers to identify recoverable revenue
- Creates personalized win-back sequences with segment-specific incentives
- Recommends optimal win-back discount depth to recover LTV

### 5. Real-Time Alerts & Dashboards
- Slack notifications when high-value segments show engagement drops
- Google Sheets dashboard updated daily with revenue leak metrics
- Flagged segments ready for immediate campaign deployment
- Weekly summary of top 10 upsell opportunities by $ impact

### 6. Pricing & Bundling Optimization
- Analyzes which product combinations convert best per segment
- Tests annual vs. monthly pricing psychology for each tier
- Recommends premium feature bundling to maximize perceived value
- Calculates optimal bundle discount (e.g., 15% off annual vs. 8%)

---

## Configuration

### Required Environment Variables

```bash
# Stripe API (payment data)
export STRIPE_API_KEY="sk_live_your_key_here"

# Mailchimp (email platform data)
export MAILCHIMP_API_KEY="your_mailchimp_key"
export MAILCHIMP_LIST_ID="your_list_id"

# Google Sheets (output reports)
export GOOGLE_SHEETS_API_KEY="your_google_credentials.json"
export GOOGLE_SHEET_ID="your_sheet_id"

# Optional: CRM/Analytics
export SHOPIFY_ACCESS_TOKEN="your_token"
export SEGMENT_API_KEY="your_segment_key"
export MIXPANEL_API_KEY="your_key"
```

### Setup Instructions

1. **Export Your Data:**
   ```
   - From Stripe: Go to Settings → Developer → API Keys (copy Live key)
   - From Mailchimp: Account → Extras → API Keys
   - From Google: Create Service Account at console.cloud.google.com
   ```

2. **Authenticate:**
   ```bash
   # Verify Stripe connection
   curl https://api.stripe.com/v1/account \
     -H "Authorization: Bearer $STRIPE_API_KEY"
   
   # Test Mailchimp connection
   curl https://{dc}.api.mailchimp.com/3.0 \
     -H "Authorization: Bearer $MAILCHIMP_API_KEY"
   ```

3. **Initialize Analysis:**
   ```
   Request the skill with: "Run full revenue leak analysis on my Stripe + Mailchimp data"
   ```

### Optional Configuration Options

```yaml
analysis_depth: "comprehensive"  # or "quick"
exclude_segments: ["trial_users", "free_plan_inactive"]
min_ltv_threshold: 50  # Only flag customers with $50+ LTV
churn_lookback_days: 90
upsell_frequency_limit: 2  # Max emails per customer per week
```

---

## Example Outputs

### Output 1: Revenue Leak Report

```
REVENUE LEAK DETECTOR ANALYSIS
Generated: 2024-01-15 | Analysis Period: Last 90 Days

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TOP 5 UPSELL OPPORTUNITIES (by potential revenue impact)

1. 🎯 ENGAGED FREE USERS (847 customers)
   Current LTV: $0 | Potential LTV: $348 each
   Total Opportunity: $294,756
   Engagement Score: 82/100 (high opens, frequent product usage)
   Recommended Action: Premium upgrade sequence
   Projected Conversion: 12-18% (based on similar cohorts)
   Expected 90-Day Revenue: $35,370 - $53,055

2. 🔄 STALLED $29/MO CUSTOMERS (234 customers)
   Current LTV: $348 | Potential LTV: $1,188 each
   Total Opportunity: $196,560
   Churn Risk Score: 65/100 (no purchase in 60 days)
   Recommended Action: Value-add upsell to $99/mo
   Projected Conversion: 8-12%
   Expected 90-Day Revenue: $15,724 - $23,587

3. 💎 VIP SEGMENT - UNDERMONETIZED (156 customers)
   Current LTV: $1,200 | Potential LTV: $3,600+ each
   Total Opportunity: $374,400
   Engagement Score: 91/100 (highest tier in platform)
   Recommended Action: Enterprise/annual plans + support upgrade
   Projected Conversion: 15-25%
   Expected 90-Day Revenue: $56,160 - $93,600

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TOTAL RECOVERABLE REVENUE OPPORTUNITY: $866,316
Confidence Level: 87%
Recommended Campaign Launch: IMMEDIATE (gaps detected)
```

### Output 2: Segment-Specific Upsell Sequence

```
SEGMENT: "Engaged Free Users"
Target Count: 847
Average Engagement Score: 82/100

EMAIL SEQUENCE #1: "Premium Path" (5-email series, 14-day window)

Email 1 (Day 0) — Discovery Hook
Subject A: "See what your $0/mo plan is missing (in 60 seconds)"
Subject B: "We fixed the #1 complaint from free users"
Body: Value prop focused on features they've tried to access
CTA: "See Premium Features"
Expected Open Rate: 34% | Click Rate: 8.2%

Email 2 (Day 2) — Social Proof
Subject A: "How premium users are saving 5+ hours/week"
Subject B: "The #1 reason 2,847 users upgraded this month"
Body: Customer testimonials + usage stats
CTA: "Learn How They Did It"
Expected Open Rate: 28% | Click Rate: 6.1%

Email 3 (Day 4) — FOMO/Limited Time
Subject A: "Early adopter pricing ends Friday"
Subject B: "50% off your first 3 months (limited spots)"
Body: Urgency framing + explicit pricing + ROI calculation
CTA: "Upgrade Now at 50% Off"
Expected Open Rate: 41% | Click Rate: 12.3%

Email 4 (Day 7) — Last Chance
Subject: "Final chance: 50% off expires tonight at midnight"
Body: Countdown + FAQ addressing objections
CTA: "Claim Your Discount →"
Expected Open Rate: 38% | Click Rate: 10.1%

Email 5 (Day 14) — Win-Back
Subject: "We've missed you—here's a fresh offer"
Body: New angle if they didn't convert
CTA: "Let's Try This"
Expected Open Rate: 22% | Click Rate: 4.2%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PROJECTED OUTCOMES:
- Send to 847 customers
- Expected conversions: 102-152 customers (12-18%)
- Expected revenue: $2,958 - $4,404
- Revenue per email sent: $3.50 - $5.20
```

### Output 3: Churn Prevention Alert

```
⚠️ CHURN RISK ALERT
High-Value Customer Showing Decline Signals

Customer: sarah.chen@company.com
Current Tier: Premium ($99/mo)
Customer LTV: $2,847
Churn Risk Score: 78/100 🔴

Risk Factors:
✗ Last purchase: 91 days ago (threshold: 90 days)
✗ Email engagement: ↓32% vs. last 60 days
✗ Product usage: ↓55% (feature access declining)
✗ Support tickets: +3 recent tickets (frustration signal)
✗ Cohort behavior: 58% of this segment churns within 30 days

RECOMMENDED IMMEDIATE ACTION:
Send "VIP Save" sequence TODAY:

Message 1 (Now): Personal outreach from CEO/Founder
"Sarah—noticed you haven't been in Premium lately. 
What can we improve? Giving you dedicated support 
for 30 days—no cost. Let's talk: [link to calendar]"

Message 2 (Day 3): Solution-focused
"We've added [3 features] you specifically requested. 
Here's how they work: [video demo]"

Message 3 (Day 7): Incentive if still at risk
"We value your 11 months with us. Here's 40% off 
annual renewal—but only if you decide today."

Expected Outcome: 68% retention rate for this cohort
```

---

## Tips & Best Practices

### 1. Data Quality Matters
- **Ensure accurate email tracking:** Confirm Mailchimp tracking pixels are installed
- **Validate purchase history:** Cross-reference Stripe records with email platform
- **Clean segmentation:** Remove test accounts, internal team members before analysis
- **Regular syncs:** Update customer data weekly (not just monthly)

### 2. Segment-Specific Messaging
- **Free → Paid messaging** focuses on transformation, not features
- **Paid → Premium messaging** emphasizes efficiency gains, not just more stuff
- **High-churn segments** need different incentives than stable users
- **Geographic targeting** matters (pricing psychology differs by region)

### 3. Timing & Frequency
- **Monday-Thursday send times** outperform Friday-Sunday by 18% on average
- **Space sequences 2-3 days apart** (avoid fatigue)
- **Max 2 promotional emails/week per customer** (unsubscribe risk at 3+)
- **Re-engage at least 7 days after last touch** (memory loss before this)

### 4. Handling Objections
- Use the skill to analyze past failed conversions and objection themes
- Build FAQ-style email content addressing top 3 objections per segment
- Track which objections predict churn and prioritize those in retention sequences

### 5. A/B Testing Strategy
- Test subject lines (not just copy), 48-hour test windows
- Rotate CTA button colors and copy across segments
- Use skill's built-in A/B predictions to prioritize high-impact tests
- Implement winners immediately, don't wait for perfect statistical significance

### 6. Integration with Automation Platforms
- Export sequences directly to Mailchimp, ConvertKit, or ActiveCampaign
- Use webhooks to trigger upsell sequences on engagement events
- Map customer cohorts to specific automation workflows
- Tag customers in CRM after they receive sequences for follow-up tracking

---

## Safety & Guardrails

### What This Skill Will NOT Do

❌ **Will NOT:**
- Send emails directly without explicit approval per sequence
- Violate CAN-SPAM or GDPR compliance (skill requires explicit opt-in segments only)
- Recommend aggressive tactics that cause brand damage (e.g., shame-based messaging)
- Analyze or export customer PII (email, names stay in your systems)
- Guarantee specific conversion rates (projections are estimates based on historical cohorts)
- Make pricing decisions (only recommendations based on data patterns)
- Continue campaigns to non-compliant segments or hard bounces

✅ **Will:**
- Require explicit customer consent before sending any communications
- Generate compliance reports (unsubscribe rates, list health metrics)
- Respect frequency caps and suppression lists
- Provide audit