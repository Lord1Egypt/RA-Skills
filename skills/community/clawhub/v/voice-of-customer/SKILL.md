---
name: Voice of Customer
description: Extract actionable product and experience insights from customer feedback across reviews, support tickets, surveys, and social mentions.
---

# Voice of Customer

Build a structured Voice of Customer analysis framework that transforms scattered feedback from reviews, support tickets, surveys, and social media into prioritized product improvements, messaging refinements, and customer experience optimizations — with clear methodology for categorization, sentiment scoring, and insight extraction.

## Quick Reference

| Decision | Strong | Acceptable | Weak|
|---|---|---|---|
| Data collection | Aggregates 5+ feedback channels with volume weighting | Covers reviews and support tickets | Analyzes single channel only |
| Categorization | Hierarchical taxonomy with 3 levels and cross-category tagging | Flat category list with 10+ categories | Ad hoc grouping without consistent framework |
| Sentiment analysis | Aspect-level sentiment with intensity scoring per feature/theme | Document-level positive/neutral/negative | Binary thumbs up/down |
| Insight extraction | Quantified themes with verbatim evidence, trend direction, and business impact | Theme identification with representative quotes | Vague summaries without supporting data |
| Prioritization | Scores by frequency × severity × revenue impact × effort | Ranks by mention frequency | Lists issues without prioritization |
| Action mapping | Specific recommendations tied to product, marketing, CX, and ops teams with owners | General improvement suggestions | Identifies problems without solutions |

## Solves

- Product teams guessing at what customers actually want instead of using systematic feedback analysis
- Marketing using internal language instead of actual customer vocabulary and phrases
- Support teams firefighting repeat issues that could be prevented with upstream fixes
- Review responses that are generic and miss the specific concern raised
- Customer churn caused by unaddressed experience friction points
- New product launches that miss critical requirements customers have already articulated
- Competitor positioning gaps that customers openly discuss but nobody tracks

## Workflow

### Step 1 — Define Scope and Objectives
Establish what you are analyzing and why:
- Product or product line to analyze
- Time period (last 30/60/90 days, or specific launch window)
- Feedback channels to include (reviews, support, surveys, social, community forums)
- Primary questions to answer (product issues, feature requests, competitive comparison, messaging fit)
- Stakeholder audience (product, marketing, CX, leadership)

### Step 2 — Collect and Normalize Feedback
Gather feedback from all channels into a unified format:
- Product reviews (Amazon, Shopify, app stores, marketplace listings)
- Support tickets and live chat transcripts (categorized by resolution)
- Post-purchase survveys (NPS, CSAT, open-ended responses)
- Social media mentions (brand mentions, hashtags, competitor comparisons)
- Community forums and Reddit threads
- Normalize: assign source, date, rating if available, and customer segment

### Step 3 — Build Categorization Taxonomy
Create a hierarchical theme structure:
- Level 1: Major categories (Product Quality, Shipping/Delivery, Customer Service, Pricing/Value, Usability)
- Level 2: Sub-categories (e.g., Product Quality → Durability, Sizing/Fit, Material, Color Accuracy)
- Level 3: Specific attributes (e.g., Sizing/Fit → Runs Small, Runs Large, Inconsistent Between Styles)
- Allow multi-tagging — one piece of feedback can touch multiple themes

### Step 4 — Analyze Sentiment and Extract Themes
For each feedback item:
- Assign aspect-level sentiment (a review can be positive about quality but negative about shipping)
- Score sentiment intensity (1-5 scale: strongly negative to strongly positive)
- Extract verbatim quotes that best represent each theme
- Identify emotional triggers (frustration language, delight language, comparison language)
- Flag competitive mentions and switching intent signals

### Step 5 — Quantify and Prioritize Findings
Turn qualitative themes into quantified, ranked insights:
- Frequency: What percentage of feedback mentions this theme?
- Sentiment: What is the average sentiment score for this theme?
- Trend: Is this theme increasing, stable, or decreasing over time?
- Severity: How much does this impact purchase decisions, satisfaction, or retention?
- Revenue impact: Estimate effect on conversion, repeat purchase rate, or AOV
- Create a priority matrix: frequency × severity × revenue impact

### Step 6 — Map Insights to Actions
Convert each prioritized insight into specific recommendations:
- Product team: Feature fixes, quality improvements, new feature development
- Marketing team: Messaging adjustments, ad copy using customer language, review response templates
- CX team: Process improvements, FAQ updates, proactive communication triggers
- Operations: Shipping, packaging, fulfillment improvements
- Assign owners, timelines, and success metrics for each action

### Step 7 — Build Monitoring Framework
Establish ongoing VoC tracking:
- Define KPIs to track (NPS trend, theme frequency shifts, sentiment scores)
- Set alert thresholds (e.g., if "defective" mentions exceed 5% of reviews)
- Create a review cadence (weekly pulse, monthly deep dive, quarterly strategic review)
- Build feedback loop: track whether implemented changes move the targeted metrics

## Examples

### Example 1: DTC Skincare Brand — Product Line Review

**Context:** DTC skincare brand with 12 SKUs, selling primarily through own website and Amazon. 1,200 product reviews in last 90 days, 340 support tickets, 180 survey responses. NPS dropped from 52 to 41 last quarter.

**Step 1 — Scope:**
- All 12 SKUs, last 90 days
- Channels: Shopify reviews, Amazon reviews, Zendesk tickets, post-purchase survey
- Primary question: Why did NPS drop? What product and experience issues are driving dissatisfaction?

**Step 2 — Data Collected:**

| Source | Volume | Avg Rating |
|---|---|---|
| Shopify reviews | 380 | 4.1/5 |
| Amazon reviews | 620 | 3.8/5 |
| Support tickets | 340 | — |
| Post-purchase survey | 180 | NPS 41 |
| Instagram mentions | 95 | — |
| **Total** | **1,615** | — |

**Step 3 — Taxonomy Built:**

| L1 Category | L2 Sub-categories |
|---|---|
| Product Efficacy | Results timeline, Effectiveness, Skin reaction, Ingredient concerns |
| Product Quality | Texture/Consistency, Fragrance, Packaging integrity, Shelf life |
| Shipping & Delivery | Speed, Packaging damage, Tracking accuracy |
| Pricing & Value | Price vs. quantity, Subscription value, Discount expectations |
| Customer Service | Response time, Resolution quality, Return process |

**Step 4 — Top Themes by Frequency:**

| Theme | Frequency | Sentiment | Trend | Verbatim Example |
|---|---|---|---|---|
| New formula dissatisfaction | 18% | 1.8/5 | ↑ Increasing | "The new version of the serum feels completely different and broke me out" |
| Shipping damage | 12% | 2.1/5 | ↑ Increasing | "Bottle arrived cracked and leaked all over the box" |
| Results exceeded expectations | 11% | 4.8/5 | Stable | "After 3 weeks my dark spots have noticeably faded" |
| Subscription flexibility | 9% | 2.4/5 | Stable | "I can't skip a month without calling support" |
| Price increase frustration | 8% | 1.9/5 | ↑ New | "Went up $8 with no warning or explanation" |

**Step 5 — Priority Matrix:**

| Insight | Frequency | Severity | Revenue Impact | Priority Score |
|---|---|---|---|---|
| Formula change backlash | 18% | High | High (retention) | **Critical** |
| Shipping damage | 12% | High | Medium (returns) | **High** |
| Subscription UX friction | 9% | Medium | High (churn) | **High** |
| Price increase communication | 8% | Medium | Medium (perception) | **Medium** |

**Step 6 — Action Map:**

| Insight | Team | Action | Timeline |
|---|---|---|---|
| Formula backlash | Product | Bring back original formula as "Classic" option; A/B test new formula with subset | 2 weeks |
| Shipping damage | Ops | Switch to reinforced mailer boxes; add inner padding for glass bottles | 1 week |
| Subscription UX | Engineering | Add self-service skip/pause in account portal | 3 weeks |
| Price communication | Marketing | Email campaign explaining ingredient upgrade behind price change | 1 week |

---

### Example 2: B2B SaaS — Feature Request Analysis

**Context:** Project management SaaS tool with 2,000 active accounts. Analyzing feedback to inform Q3 product roadmap. Sources: in-app feedback widget, Intercom chats, G2/Capterra reviews, churned customer exit surveys.

**Step 1 — Scope:**
- Full platform, last 6 months
- Channels: In-app feedback (890), Intercom (1,200 relevant threads), G2/Capterra (210 reviews), Exit surveys (45)
- Primary question: What features should we build in Q3 to reduce churn and win competitive deals?

**Step 2 — Data Collected:**

| Source | Volume | Focus |
|---|---|---|
| In-app feedback widget | 890 | Feature requests, bug reports |
| Intercom conversations | 1,200 | Support questions, workaround requests |
| G2/Capterra reviews | 210 | Comparative analysis, strengths/weaknesses |
| Exit surveys | 45 | Churn reasons, competitor mentions |
| **Total** | **2,345** | — |

**Step 4 — Top Themes:**

| Theme | Frequency | Source Concentration | Competitor Mention |
|---|---|---|---|
| Time tracking integration | 22% | In-app (35%), G2 (28%) | "Asana and Monday both have this" |
| Custom reporting/dashboards | 18% | In-app (24%), Exit (40%) | "Switched to Monday for reporting" |
| Mobile app performance | 14% | Intercom (22%), G2 (15%) | "Mobile app crashes daily" |
| API and Zapier improvements | 11% | In-app (15%), Intercom (10%) | "Their API docs are terrible" |
| Guest/client collaboration | 9% | Intercom (12%), Exit (20%) | "Basecamp handles client access better" |

**Step 5 — Prioritization with Revenue Impact:**

| Feature | Request Freq | Churn Driver | Competitive Gap | Dev Effort | Priority |
|---|---|---|---|---|---|
| Custom reporting | 18% | #1 exit reason | Yes (Monday) | Large (8 weeks) | **Critical — Q3 P0** |
| Time tracking | 22% | Mentioned in 15% of exits | Yes (Asana, Monday) | Medium (4 weeks) | **High — Q3 P1** |
| Mobile stability | 14% | Low direct churn but high frustration | Parity issue | Medium (3 weeks) | **High — Q3 P1** |
| Guest collaboration | 9% | #2 exit reason by revenue | Yes (Basecamp) | Large (6 weeks) | **Medium — Q4** |

**Step 6 — Action Map:**

| Insight | Team | Action | Success Metric |
|---|---|---|---|
| Custom reporting gap | Product + Eng | Build dashboard builder with 5 default templates and export | Reduce "reporting" churn reason by 50% |
| Time tracking need | Product | Native timer + Toggl/Harvest integration | 30% adoption within 60 days of launch |
| Mobile crashes | Engineering | Performance sprint — crash-free rate from 94% to 99.5% | App store rating from 3.2 to 4.0+ |
| Client access | Product | Design spec for Q4 — interview 10 churned accounts for requirements | Validated spec ready by end of Q3 |

## Common Mistakes

1. **Analyzing only one feedback channel** — Reviews skew toward extremes, support tickets skew toward problems. You need all channels for a balanced picture. Weight by volume but include every source.

2. **Using document-level sentiment only** — A 3-star review that praises the product but hates the shipping is not "neutral." Aspect-level sentiment captures what is actually working and what is not.

3. **Reporting themes without quantification** — Saying "customers complain about shipping" is not actionable. Saying "17% of feedback mentions shipping damage, up from 8% last quarter, concentrated on glass bottle SKUs" is actionable.

4. **Ignoring positive feedback** — VoC is not just about problems. Positive themes tell you what to protect and amplify in marketing. If 25% of reviews mention "gentle on sensitive skin," that is a messaging goldmine.

5. **Letting recency bias drive priorities** — The loudest recent complaint is not always the most important issue. Use frequency, severity, and trend data together to avoid whiplash in priorities.

6. **Creating a report nobody acts on** — Every insight needs an owner, a timeline, and a success metric. A VoC analysis that sits in a shared drive is wasted effort.

7. **Treating VoC as a one-time project** — Customer sentiment changes constantly. Build ongoing monitoring, not just periodic reports. Set alerts for emerging themes.

8. **Missing competitive intelligence** — Customers voluntarily compare you to competitors in reviews and exit surveys. This is free competitive intelligence. Track competitor mentions systematically.

## Resources

- [Output Template](references/output-template.md) — Structured VoC analysis deliverable format
- [Sentiment Scoring Guide](references/sentiment-scoring-guide.md) — Aspect-level sentiment methodology and calibration
- [Feedback Taxonomy Reference](references/feedback-taxonomy-reference.md) — Category frameworks for common ecommerce and SaaS verticals
- [Quality Checklist](assets/quality-checklist.md) — Comprehensive review checklist for VoC analysis deliverables
