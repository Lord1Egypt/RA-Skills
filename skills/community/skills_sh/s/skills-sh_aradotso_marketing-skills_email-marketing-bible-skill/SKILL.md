---
name: email-marketing-bible-skill
description: Comprehensive email marketing expertise for Claude Code — 68K words, 908 sources, 19 industry playbooks covering strategy, automation, deliverability, copywriting, and compliance.
triggers:
  - "audit my email marketing setup"
  - "write an email sequence for abandoned cart"
  - "fix my email deliverability issues"
  - "review this email campaign"
  - "what are good email marketing benchmarks for my industry"
  - "build a welcome email flow"
  - "help me improve email open rates"
  - "compare email marketing platforms"
---

# Email Marketing Bible Skill

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

This skill transforms Claude into an email marketing expert with access to 68,000 words of research, 908 sources, 4,798 insights from 44 expert contributors, and 19 industry-specific playbooks. Built by George Hartley (founder of SmartrMail, 28,000 customers).

## What This Skill Provides

The Email Marketing Bible is a comprehensive knowledge base covering:

- **Strategy & Automation**: Welcome series, abandoned cart, post-purchase, win-back, sunset flows
- **Deliverability**: SPF, DKIM, DMARC, BIMI, sender reputation, IP warming, spam filters
- **Copywriting**: Subject lines, preview text, body copy, CTAs using proven frameworks (PAS, AIDA, BAB)
- **Segmentation**: RFM scoring, engagement tiers, zero-party data, waterfall segmentation
- **Compliance**: GDPR, CAN-SPAM, CASL, CCPA, Australian Spam Act
- **Industry Playbooks**: 19 vertical-specific strategies (Ecommerce, SaaS, Newsletter, Agency, etc.)
- **Platform Selection**: Honest comparisons of Klaviyo, Mailchimp, Kit, beehiiv, Sendlane
- **Design Best Practices**: 57 curated email designs with technical implementation notes

## Installation

```bash
git clone https://github.com/CosmoBlk/email-marketing-bible.git ~/.claude/skills/email-marketing-bible
```

Once installed, Claude has immediate access to the full knowledge base without requiring any API calls or additional setup.

## Core Capabilities

### 1. Email Marketing Audits

Ask Claude to review your current setup and identify gaps:

```
"Review my email marketing setup. I run a DTC skincare brand on Shopify 
doing $2M/year. Currently using Klaviyo with:
- Welcome series (3 emails)
- Abandoned cart (2 emails)
- Weekly newsletter
What am I missing?"
```

Claude will analyze against industry benchmarks and identify:
- Missing automation flows (post-purchase, browse abandonment, win-back)
- Segmentation opportunities
- Deliverability risks
- Compliance gaps
- Revenue opportunities with estimated impact

### 2. Automation Flow Design

Request complete email sequences with timing, triggers, and copy:

```
"Build a post-purchase email sequence for my coffee subscription business.
Average order: $45, repeat purchase cycle: 30-45 days, AOV target: $60"
```

Claude provides:
- Email count and timing (e.g., Day 0, Day 3, Day 14, Day 28)
- Subject lines and preview text
- Body copy frameworks
- Personalization tokens
- Expected performance benchmarks
- Conditional logic based on customer behavior

### 3. Deliverability Diagnosis

Debug inbox placement and reputation issues:

```
"My Gmail placement dropped from 90% inbox to 60% promotions tab.
Open rates fell from 22% to 14% over 3 months. Domain: example.com,
ESP: Klaviyo, current send volume: 50K/week"
```

Claude runs through a 10-step diagnostic:
1. Authentication records (SPF, DKIM, DMARC)
2. Sender reputation (domain and IP)
3. Engagement metrics (opens, clicks, complaints)
4. Content analysis (spam trigger words, HTML/text ratio)
5. List hygiene (bounce rate, spam traps)
6. Send patterns (volume spikes, frequency)
7. Infrastructure (dedicated IP, shared pool)
8. Recipient feedback loops
9. Email client compatibility
10. Recent changes (domain, ESP, content strategy)

### 4. Industry-Specific Strategy

Get tactics calibrated to your vertical:

```
"I'm launching a B2B SaaS product (project management tool, $49/mo).
What email marketing stack and flows do I need from day one?"
```

Claude provides vertical-specific playbooks for:
- **Ecommerce DTC**: Product launches, seasonal campaigns, loyalty programs
- **SaaS B2B**: Onboarding, feature adoption, expansion revenue
- **Newsletter/Creator**: Subscriber growth, engagement, monetization
- **Agency**: Client nurture, case study distribution, upsells
- **Nonprofit**: Donor retention, campaign fundraising, volunteer engagement
- Plus 14 other verticals with benchmarks and tactical frameworks

### 5. Email Copywriting

Generate conversion-focused copy using proven frameworks:

```
"Write a 3-email win-back sequence for fitness equipment brand.
Target: subscribers inactive 90+ days. Brand voice: motivational but not preachy.
Average customer LTV: $280"
```

Claude structures emails using:
- **PAS (Problem-Agitate-Solution)**: Identify pain, intensify it, present solution
- **AIDA (Attention-Interest-Desire-Action)**: Hook, build curiosity, create want, drive click
- **BAB (Before-After-Bridge)**: Current state, desired state, path forward

Each email includes:
- Subject line variants (curiosity, benefit, urgency)
- Preview text optimized for mobile
- Body copy with conversational tone
- CTA copy and placement
- Expected performance benchmarks

### 6. Platform Selection

Get unbiased ESP comparisons:

```
"Compare email platforms for my use case:
- 15K subscribers, growing 500/month
- Ecommerce (Shopify)
- Budget: $200/month
- Need: SMS integration, advanced segmentation, Shopify deep integration"
```

Claude evaluates:
- **Klaviyo**: Best for ecommerce, expensive at scale, powerful segmentation
- **Mailchimp**: Beginner-friendly, weaker automation, affordable for small lists
- **Kit**: Creator-focused, simple automation, visual builder
- **beehiiv**: Newsletter-first, growth tools, limited ecommerce features
- **Sendlane**: Mid-market alternative, good deliverability, learning curve

With honest pros/cons, pricing at your scale, and migration considerations.

### 7. Compliance Review

Audit against global regulations:

```
"Review my email compliance setup:
- Collecting emails via popup with single opt-in
- Sending to US, Canada, EU, Australia
- Using purchased list from trade show (2,000 contacts)
- No unsubscribe link in transactional emails"
```

Claude identifies violations and remediation steps for:
- **GDPR** (EU): Lawful basis, explicit consent, right to erasure
- **CAN-SPAM** (US): Physical address, clear unsubscribe, honest headers
- **CASL** (Canada): Express consent, identification, unsubscribe mechanism
- **CCPA** (California): Privacy policy, data disclosure, opt-out rights
- **Australian Spam Act**: Consent, identification, functional unsubscribe

### 8. Design & Technical Guidance

Reference 57 curated email designs:

```
"Show me best practices for a product launch email.
Multi-product (3 SKUs), mobile-first, dark mode compatible"
```

Claude provides:
- Layout patterns (single column, Z-pattern, F-pattern)
- Typography (font stacks, size hierarchy, line height)
- Color systems (contrast ratios, dark mode variants)
- CTA design (button vs link, placement, copy length)
- Image optimization (file size, alt text, fallbacks)
- Code examples in HTML/CSS for email clients

## Knowledge Base Structure

### 17 Chapters Available

1. **The Fundamentals**: Why email wins, marketing stack, key metrics, common mistakes
2. **Building Your List**: Organic growth, popups, double vs single opt-in, spam traps
3. **Segmentation & Personalisation**: RFM scoring, engagement tiers, zero-party data
4. **The Emails That Make Money**: Welcome, abandoned cart, post-purchase, win-back
5. **Copywriting That Converts**: Subject lines, body copy, CTAs, proven frameworks
6. **Design & Technical**: Mobile-first, dark mode, accessibility, client compatibility
7. **Deliverability**: SPF/DKIM/DMARC, reputation, IP warming, spam filters
8. **Testing & Optimisation**: A/B testing, statistical significance, send time optimization
9. **Analytics & Measurement**: KPIs by campaign type, attribution, subscriber LTV
10. **Compliance & Privacy**: GDPR, CAN-SPAM, CASL, CCPA, Australian Spam Act
11. **Industry Playbooks**: 19 vertical-specific playbooks
12. **Choosing Your Platform**: ESP comparison by use case
13. **Cold Email & B2B Outbound**: Infrastructure, warming, personalization sequences
14. **AI & the Future of Email**: Practical AI integration, where it helps/hurts
15. **Company Case Studies**: Casper, Morning Brew, Duolingo, Spotify, and others
16. **Expert Directory**: 44 practitioners referenced throughout
17. **Best Email Designs 2026**: 57 curated designs with implementation notes

### 19 Industry Playbooks

Each vertical includes specific tactics, benchmarks, and automation flows:

- Ecommerce DTC
- SaaS B2B
- SaaS B2C
- Newsletter & Creator
- Agency
- Nonprofit
- Healthcare
- Financial Services
- Real Estate
- Travel & Hospitality
- Education
- Professional Services
- Retail
- Events
- B2B Manufacturing
- Restaurant & Food
- Fitness
- Media & Publishing
- Marketplace & Platform

## Common Usage Patterns

### Pattern 1: Full Marketing Stack Audit

```
"Audit my complete email marketing operation:
- Brand: DTC home goods
- Revenue: $5M/year
- List size: 80K subscribers
- ESP: Mailchimp
- Current flows: Welcome (2 emails), abandoned cart (1 email)
- Team: Just me (founder)
- Goal: Double email revenue in 6 months"
```

Claude performs a comprehensive audit covering strategy, automation, deliverability, segmentation, compliance, and platform fit, then prioritizes recommendations by estimated revenue impact.

### Pattern 2: Campaign-Specific Review

```
"Review this Black Friday email campaign:
- Subject: '50% OFF Everything - 24 Hours Only!!!'
- Preview: 'Biggest sale of the year. Don't miss out.'
- Send time: Friday 6am EST
- Audience: All subscribers (no segmentation)
- Previous BFCM open rate: 18% (industry avg: 25%)"
```

Claude critiques subject line (emoji overuse, spam triggers), preview text (missed opportunity), timing (too early), segmentation (lost personalization opportunity), and provides rewritten versions with expected lift.

### Pattern 3: Flow Building from Scratch

```
"Build a complete welcome series for a premium pet food subscription:
- Price: $60/month
- Target customer: health-conscious pet owners
- USP: Human-grade ingredients, vet-formulated
- Goal: Convert free trial to paid subscription
- Brand voice: Warm, educational, premium but not pretentious"
```

Claude designs a 5-email sequence:
- **Email 1** (Immediate): Welcome, set expectations, first feeding tips
- **Email 2** (Day 2): Educational content (ingredient sourcing), social proof
- **Email 3** (Day 5): Trial reminder, conversion incentive (10% off first paid month)
- **Email 4** (Day 7): Urgency (trial ending), testimonials, conversion CTA
- **Email 5** (Day 9): Last chance, founder story, final conversion push

Each email includes subject lines, copy structure, personalization tokens, and expected benchmarks.

### Pattern 4: Deliverability Troubleshooting

```
"Deliverability emergency:
- Suddenly landing in spam (Gmail, Outlook)
- Bounce rate jumped from 2% to 8%
- Complaint rate: 0.1%
- Recent changes: New sending domain (moved from oldsite.com to newsite.com)
- Authentication: SPF and DKIM configured, DMARC not set up
- IP: Shared pool with ESP"
```

Claude identifies the root cause (new domain without reputation), provides immediate fixes (DMARC setup, domain warming schedule), and long-term strategy (dedicated IP consideration, engagement-based sending).

## Performance Benchmarks

Claude references industry benchmarks by vertical:

| Industry | Open Rate | Click Rate | Conversion Rate | Revenue/Email |
|----------|-----------|------------|-----------------|---------------|
| Ecommerce DTC | 18-22% | 2.5-3.5% | 1.5-2.5% | $0.15-0.35 |
| SaaS B2B | 20-25% | 3-4% | 0.5-1.5% | N/A (pipeline) |
| SaaS B2C | 22-28% | 3.5-5% | 2-4% | Varies by price |
| Newsletter | 25-35% | 4-6% | N/A | Varies |
| Nonprofit | 22-28% | 2.5-3.5% | 1-2% (donations) | Varies |

These benchmarks are contextualized by list size, engagement history, and campaign type.

## Technical Implementation Examples

### Example 1: Email Authentication Setup

When asked about deliverability setup, Claude provides DNS record examples:

```dns
; SPF Record
@ IN TXT "v=spf1 include:_spf.google.com include:spf.klaviyo.com ~all"

; DKIM Record (obtained from ESP)
default._domainkey IN TXT "v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA..."

; DMARC Record
_dmarc IN TXT "v=DMARC1; p=quarantine; rua=mailto:dmarc@yourdomain.com; ruf=mailto:dmarc@yourdomain.com; pct=100"

; BIMI Record (optional, for brand logo in inbox)
default._bimi IN TXT "v=BIMI1; l=https://yourdomain.com/logo.svg; a=https://yourdomain.com/cert.pem"
```

### Example 2: Segmentation Logic

For advanced segmentation requests, Claude provides RFM scoring logic:

```
Recency Score:
- 0-30 days: 5 points
- 31-60 days: 4 points
- 61-90 days: 3 points
- 91-180 days: 2 points
- 180+ days: 1 point

Frequency Score (purchases in last 12 months):
- 10+: 5 points
- 6-9: 4 points
- 3-5: 3 points
- 2: 2 points
- 1: 1 point

Monetary Score (total spend, last 12 months):
- $1000+: 5 points
- $500-999: 4 points
- $250-499: 3 points
- $100-249: 2 points
- <$100: 1 point

Segment Definitions:
- Champions: R=5, F=5, M=5 (14-15 total)
- Loyal: R=4-5, F=4-5, M=3-5 (11-13 total)
- At Risk: R=2-3, F=4-5, M=3-5 (high value, low recency)
- Need Attention: R=3-4, F=2-3, M=2-3 (middle performers)
- Lost: R=1-2, F=1-2, M=1-2 (3-6 total)
```

### Example 3: Email Template HTML Structure

For design requests, Claude provides mobile-first HTML:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="color-scheme" content="light dark">
    <meta name="supported-color-schemes" content="light dark">
    <title>Email Title</title>
    <style>
        /* Dark mode support */
        @media (prefers-color-scheme: dark) {
            .dark-mode-text { color: #ffffff !important; }
            .dark-mode-bg { background-color: #1a1a1a !important; }
        }
        
        /* Mobile-first styles */
        body { margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .button { display: inline-block; padding: 14px 28px; background-color: #007bff; color: #ffffff; text-decoration: none; border-radius: 4px; }
        
        /* Desktop adjustments */
        @media screen and (min-width: 600px) {
            .container { padding: 40px; }
        }
    </style>
</head>
<body>
    <div class="container dark-mode-bg">
        <h1 class="dark-mode-text">Welcome to [Brand]</h1>
        <p class="dark-mode-text">Your personalized content here...</p>
        <a href="https://yourdomain.com/offer" class="button">Shop Now</a>
    </div>
</body>
</html>
```

## Troubleshooting Common Issues

### Low Open Rates

Claude diagnoses through systematic elimination:

1. **Authentication**: Check SPF, DKIM, DMARC records
2. **Sender Reputation**: Review complaint rate, bounce rate, spam trap hits
3. **Subject Lines**: Test curiosity vs benefit-driven, length (30-50 chars optimal)
4. **Send Time**: Analyze historical engagement patterns by day/hour
5. **List Hygiene**: Remove hard bounces, suppress inactive (180+ days)
6. **From Name**: Test company name vs personal name vs combo
7. **Preview Text**: Ensure it complements subject line, not duplicate
8. **Frequency**: Evaluate send cadence (too frequent = fatigue)

### Low Click Rates

Claude identifies conversion friction:

1. **CTA Clarity**: Single, clear call-to-action vs multiple competing CTAs
2. **Value Proposition**: Benefit clearly communicated in first 3 lines
3. **Design Hierarchy**: Visual flow guides to CTA (F-pattern, Z-pattern)
4. **Mobile Optimization**: 46%+ of opens are mobile, buttons need 44px min height
5. **Content Relevance**: Segmentation match (right message to right audience)
6. **Link Placement**: CTA above fold + repeat below for scanners
7. **Personalization**: Dynamic content increases clicks 14% on average
8. **Load Time**: Images optimized, hosted on CDN

### Deliverability Problems

Claude follows the 10-step diagnostic framework covering authentication, reputation, content, infrastructure, engagement, and compliance. Each step includes specific tools and tests.

## Expert Contributors Referenced

The knowledge base includes insights from 44 practitioners:

- **Chad S. White** (Zeta Global): Deliverability and engagement
- **Joanna Wiebe** (Copyhackers): Conversion copywriting
- **Chase Dimond** (Structured Agency): Ecommerce email strategy
- **Nathan Barry** (Kit): Creator economy and automation
- **Ann Handley** (MarketingProfs): Content marketing and email voice
- **Troy Ericson** (EmailDeliverability.com): Technical deliverability
- **Tyler Denk** (beehiiv): Newsletter growth tactics
- **Ben Settle** (Email Players): Daily email methodology

Plus 36 others across strategy, design, compliance, and analytics.

## Accessing the Full Knowledge Base

The complete 68,000-word guide is available at **[emailmarketingskill.com](https://emailmarketingskill.com)** with searchable chapters, appendices, and downloadable resources.

Claude has access to the full knowledge base once installed and can reference any chapter, playbook, case study, or design example on demand.

## Research Methodology

The knowledge base synthesizes 908 sources:

- Industry reports (Litmus, Klaviyo, Campaign Monitor, HubSpot, Salesforce)
- Practitioner blogs and case studies
- Academic research on email effectiveness
- Platform documentation (ESPs, deliverability tools)
- Community discussions (Reddit r/emailmarketing, Shopify forums, X/Twitter)

The research crawler is open source: [github.com/CosmoBlk/emb-research](https://github.com/CosmoBlk/emb-research)

## Contributing

Found an error or have better data? Contributions welcome at [github.com/CosmoBlk/email-marketing-bible](https://github.com/CosmoBlk/email-marketing-bible)

## License

MIT License — use freely in commercial and personal projects.

---

**Built by [George Hartley](https://x.com/GTHartley)** | Founder, SmartrMail (28,000 customers)
