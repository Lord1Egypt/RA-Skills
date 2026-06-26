# Win-Back Campaign Output Template

Use this template to document a complete win-back campaign plan. Fill in each section with specifics for your brand and audience.

---

## 1. Campaign Overview

| Field | Value |
|---|---|
| **Brand / Store** | [Brand name] |
| **Campaign Name** | [e.g., "Q2 2026 Win-Back"] |
| **Launch Date** | [Target launch date] |
| **Campaign Duration** | [Total sequence length, e.g., 35 days] |
| **Campaign Owner** | [Name and role] |
| **Estimated Audience Size** | [Total lapsed customers targeted] |
| **Estimated Revenue Target** | [Incremental recovered revenue goal] |
| **Budget** | [Total budget across creative, SMS credits, ad spend] |

---

## 2. Lapse Threshold Definitions

| Tier | Threshold | Days Since Last Purchase | Data Basis |
|---|---|---|---|
| At-Risk | [e.g., 1.25x median] | [e.g., 56 days] | [Source: median repurchase interval of X days] |
| Lapsed | [e.g., 1.5x median] | [e.g., 68 days] | [Organic return rate drops below X% at this point] |
| Deeply Lapsed | [e.g., 2x median] | [e.g., 90+ days] | [Only X% return organically beyond this threshold] |

**Seasonal Adjustments:** [Note any adjustments for seasonal buying patterns, e.g., Q4 gifters get 30-day extension]

**Exclusions:** [List any populations excluded from lapse classification -- subscription customers, wholesale accounts, etc.]

---

## 3. Audience Segmentation

### Segment Definitions

| Segment Name | Recency Range | Frequency | Monetary (AOV/LTV) | Size | Est. Revenue Potential |
|---|---|---|---|---|---|
| [e.g., VIP Lapsed] | [68-90 days] | [3+ orders] | [AOV > $75] | [2,400] | [$198K] |
| [Segment 2] | | | | | |
| [Segment 3] | | | | | |
| [Segment 4] | | | | | |
| [Segment 5] | | | | | |

### Suppression Rules

- [ ] Hard bounces removed
- [ ] Unsubscribed contacts removed
- [ ] Spam complainants removed
- [ ] Legally suppressed contacts removed (GDPR deletion requests, etc.)
- [ ] Invalid/disconnected phone numbers removed from SMS audiences
- [ ] Active subscribers excluded (purchased within lapse threshold)
- [ ] Subscription/auto-replenishment customers excluded
- [ ] Other: [specify]

---

## 4. Sequence Design

### Segment: [Segment Name]

**Treatment tier:** [Premium / Standard / Light]
**Total touches:** [Number]
**Sequence duration:** [Days]

| Touch # | Day | Channel | Subject / Message Theme | Offer | Dynamic Content | Exit Trigger |
|---|---|---|---|---|---|---|
| 1 | 0 | [Email/SMS/Ad] | [Theme summary] | [None / % off / free shipping] | [Product recs, last purchased, etc.] | [Purchase / Click / None] |
| 2 | | | | | | |
| 3 | | | | | | |
| 4 | | | | | | |
| 5 | | | | | | |
| 6 | | | | | | |

**Branching logic:** [Describe any conditional paths -- e.g., "If Touch 1 opened but not clicked, send Touch 2A instead of 2B"]

*Repeat this section for each segment.*

---

## 5. Channel Configuration

### Email

| Setting | Value |
|---|---|
| **ESP Platform** | [Klaviyo / Iterable / Braze / etc.] |
| **From Name** | [e.g., "Sarah at BrandName"] |
| **From Address** | [e.g., hello@brand.com] |
| **Reply-To** | [e.g., support@brand.com] |
| **Sending Domain** | [Authenticated domain] |
| **Warm-Up Plan** | [For deeply lapsed: ramp schedule, e.g., 10% Day 1, 25% Day 2, 100% Day 3] |
| **Send-Time Optimization** | [Enabled / Disabled] |

### SMS

| Setting | Value |
|---|---|
| **SMS Platform** | [Postscript / Attentive / Klaviyo SMS / etc.] |
| **Sender ID / Short Code** | [Number or short code] |
| **Quiet Hours** | [e.g., 9pm-9am local time] |
| **Consent Verification** | [How consent was verified -- date, source] |
| **Max SMS per Sequence** | [e.g., 2] |
| **Character Limit Target** | [e.g., 160 chars to avoid multi-segment] |

### Paid Ads

| Setting | Value |
|---|---|
| **Platforms** | [Meta / Google / TikTok / etc.] |
| **Audience Upload Method** | [Manual CSV / API sync / CAPI] |
| **Audience Refresh Cadence** | [Daily / Real-time] |
| **Frequency Cap** | [e.g., 4 impressions/week] |
| **Daily Budget** | [Per platform] |
| **Conversion Exclusion Window** | [e.g., suppress within 4 hours of purchase] |
| **Ad Formats** | [Static image / Carousel / Video / etc.] |

### Cross-Channel Suppression

| Trigger Event | Suppression Action | Latency |
|---|---|---|
| Purchase | Suppress all remaining touches (email, SMS, ads) | [e.g., < 1 hour] |
| Unsubscribe (email) | Remove from email sequence; SMS and ads continue | [Immediate] |
| SMS opt-out | Remove from SMS; email and ads continue | [Immediate] |
| Spam complaint | Suppress all channels | [Immediate] |

---

## 6. Measurement Plan

### Holdout Groups

| Segment | Holdout % | Holdout Size | Assignment Method |
|---|---|---|---|
| [Segment 1] | [10-15%] | [N] | [Random, stratified by RFM score] |
| [Segment 2] | | | |

### KPIs

| KPI | Definition | Target | Measurement Window |
|---|---|---|---|
| **Reactivation Rate** | % of recipients who make a purchase | [e.g., 8%] | [30 days post-last-touch] |
| **Incremental Lift** | Reactivation rate minus holdout return rate | [e.g., 5pp] | [30 days] |
| **Recovered Revenue** | Total revenue from reactivated customers | [e.g., $50K] | [30 days] |
| **Cost per Reactivation** | Total campaign cost / reactivated customers | [e.g., $12] | [Campaign duration] |
| **ROI** | (Incremental revenue - cost) / cost | [e.g., 8x] | [30 days] |
| **Unsubscribe Rate** | % of email recipients who unsubscribe | [< 1%] | [Per touch] |
| **Spam Complaint Rate** | % of delivered emails marked as spam | [< 0.05%] | [Per touch] |
| **Second Purchase Rate** | % of reactivated customers who buy again within 90 days | [e.g., 25%] | [90 days post-reactivation] |

### Reporting

| Report | Frequency | Owner | Distribution |
|---|---|---|---|
| Deliverability monitoring | Daily (first 72 hours) | [Name] | [Slack channel / email] |
| Performance dashboard | Weekly | [Name] | [Team meeting / async] |
| Post-campaign analysis | Once (campaign end + measurement window) | [Name] | [Stakeholder presentation] |

---

## 7. Timeline and Approvals

| Milestone | Target Date | Owner | Status |
|---|---|---|---|
| Segmentation and data pull | [Date] | [Name] | [ ] |
| Creative brief finalized | [Date] | [Name] | [ ] |
| Email templates designed and coded | [Date] | [Name] | [ ] |
| SMS copy approved (legal review) | [Date] | [Name] | [ ] |
| Ad creative produced | [Date] | [Name] | [ ] |
| Flows built and QA tested | [Date] | [Name] | [ ] |
| Holdout groups assigned | [Date] | [Name] | [ ] |
| Audiences uploaded to ad platforms | [Date] | [Name] | [ ] |
| Soft launch (first segment) | [Date] | [Name] | [ ] |
| Full launch | [Date] | [Name] | [ ] |
| Mid-campaign review | [Date] | [Name] | [ ] |
| Post-campaign analysis | [Date] | [Name] | [ ] |

---

## 8. Post-Campaign Results

*Complete this section after the campaign and measurement window conclude.*

### Performance Summary

| Segment | Audience | Reactivated | Rate | Holdout Rate | Incremental Lift | Revenue |
|---|---|---|---|---|---|---|
| [Segment 1] | | | | | | |
| [Segment 2] | | | | | | |
| **Total** | | | | | | |

### Channel Performance

| Channel | Sends/Impressions | Conversions | Conv. Rate | Revenue | Cost | CPA |
|---|---|---|---|---|---|---|
| Email | | | | | | |
| SMS | | | | | | |
| Paid Ads | | | | | | |
| **Total** | | | | | | |

### Key Learnings

1. [Learning 1]
2. [Learning 2]
3. [Learning 3]

### Recommendations for Next Iteration

1. [Recommendation 1]
2. [Recommendation 2]
3. [Recommendation 3]
