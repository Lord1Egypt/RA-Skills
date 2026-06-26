# Entry Examples

Concrete examples of well-formatted marketing entries with all fields.

## Learning: Messaging Miss (Wrong Value Proposition for Enterprise)

```markdown
## [LRN-20250415-001] messaging_miss

**Logged**: 2025-04-15T10:30:00Z
**Priority**: high
**Status**: pending
**Area**: campaigns

### Summary
Product launch email used SMB-focused messaging for enterprise segment, tanking open and click rates

### Details
Q2 product launch email sent to 4,200 enterprise contacts led with "easy setup in minutes"
and "affordable pricing" — language that resonates with SMB founders but alienates enterprise
VPs and Directors who care about ROI, security compliance, and integration capabilities.
Open rate was 8.2% vs. 22% benchmark for enterprise nurture. CTR was 0.4% vs. 3.1% benchmark.

The same email sent to the SMB segment performed at 24% open rate and 4.8% CTR, confirming
the messaging was segment-appropriate for SMB but wrong for enterprise.

### Evidence

**Metrics (enterprise segment):**
- Open rate: 8.2% (benchmark: 22%)
- CTR: 0.4% (benchmark: 3.1%)
- Unsubscribe rate: 1.8% (3x normal)

**Metrics (SMB segment, same email):**
- Open rate: 24%
- CTR: 4.8%

### Suggested Action
Create segment-specific email templates. Enterprise messaging should lead with ROI metrics,
security certifications (SOC2, ISO 27001), and integration ecosystem. Never use "affordable"
or "easy" for enterprise — use "cost-effective with proven TCO reduction" and "enterprise-grade
with dedicated onboarding."

### Metadata
- Source: campaign_report
- Channel: email
- Segment: enterprise
- Tags: messaging, enterprise, value-proposition, email, segmentation
- Pattern-Key: messaging_miss.wrong_value_prop

---
```

## Learning: Audience Drift (ICP Shifted from SMB to Mid-Market)

```markdown
## [LRN-20250416-001] audience_drift

**Logged**: 2025-04-16T09:15:00Z
**Priority**: high
**Status**: pending
**Area**: analytics

### Summary
ICP shifted from SMB founders to mid-market VPs of Engineering but paid media targeting unchanged

### Details
Product usage analytics show 62% of new trials now come from companies with 200-1000 employees
(mid-market), up from 28% six months ago. The shift correlates with the enterprise features
shipped in Q1 (SSO, audit logs, role-based access). However, all paid media campaigns still
target SMB (1-50 employees) with SMB messaging and landing pages.

LinkedIn Ads CPL for SMB targeting: $142 (up from $89 six months ago, as SMB pool shrinks).
Organic sign-ups from mid-market: 3.2x conversion rate vs. paid SMB traffic.

### Evidence

**Trial composition shift (6 months):**
- SMB (<50 employees): 72% → 38%
- Mid-market (200-1000): 28% → 62%

**Paid media efficiency:**
- SMB CPL: $89 → $142 (+60%)
- Organic mid-market CVR: 8.4% vs. paid SMB CVR: 2.1%

### Suggested Action
1. Update audience personas to reflect mid-market ICP shift
2. Create mid-market targeting segments in LinkedIn and Google Ads
3. Build mid-market landing pages with enterprise feature emphasis
4. Reallocate 40% of SMB paid budget to mid-market campaigns
5. Review quarterly to detect further shifts

### Metadata
- Source: analytics_dashboard
- Channel: google_ads
- Segment: mid_market
- Tags: audience, ICP, mid-market, targeting, persona, drift
- Pattern-Key: audience_drift.icp_shift

---
```

## Learning: Content Decay (Top Blog Post Lost Traffic After Algorithm Update)

```markdown
## [LRN-20250417-001] content_decay

**Logged**: 2025-04-17T14:00:00Z
**Priority**: medium
**Status**: pending
**Area**: seo

### Summary
Top-ranking blog post lost 60% organic traffic after search algorithm update, needs content refresh

### Details
"Complete Guide to API Rate Limiting" was our #1 organic traffic driver (12K monthly visits,
ranking #1 for "api rate limiting best practices"). After the March algorithm update, it
dropped to position #7 and traffic fell to 4.8K/month. Competitors who updated their
content in 2025 with new examples (GraphQL rate limiting, edge computing patterns) now
outrank us.

The post was last updated 14 months ago. Core content is still accurate but missing:
- GraphQL-specific rate limiting patterns
- Edge/CDN-level rate limiting (Cloudflare, Fastly)
- Code examples in newer frameworks (Next.js 14, Bun)
- Updated benchmark data

### Evidence

**Before (pre-algorithm update):**
- Monthly organic visits: 12,000
- Ranking position: #1 for "api rate limiting best practices"
- Backlinks: 89

**After:**
- Monthly organic visits: 4,800 (-60%)
- Ranking position: #7
- Backlinks: 89 (unchanged)

### Suggested Action
1. Content refresh with 2025-current examples and frameworks
2. Add GraphQL and edge computing sections
3. Update benchmark data with current numbers
4. Add comparison table vs. competitor approaches
5. Set up quarterly content freshness audit for top 20 posts

### Metadata
- Source: analytics_dashboard
- Channel: organic_search
- Segment: all
- Tags: seo, content-decay, algorithm-update, blog, organic-traffic
- Pattern-Key: content_decay.algorithm_update

---
```

## Campaign Issue: Channel Underperformance (LinkedIn Ads CPL 3x Above Benchmark)

```markdown
## [CMP-20250415-001] linkedin_ads_cpl_spike

**Logged**: 2025-04-15T16:00:00Z
**Priority**: high
**Status**: pending
**Area**: paid_media

### Summary
LinkedIn lead gen campaign CPL reached $285, 3x above $95 benchmark, due to audience saturation and stale creative

### Performance Data
- Campaign: Q2 Webinar Promotion - DevOps Leaders
- Channel: linkedin
- Date Range: 2025-04-01 to 2025-04-14
- Budget Spent: $8,550
- Key Metrics:
  - Impressions: 142,000
  - Clicks: 568
  - CTR: 0.4% (benchmark: 0.8%)
  - Conversions: 30 (registrations)
  - CVR: 5.3% (benchmark: 12%)
  - CPL: $285 (benchmark: $95)

### Root Cause
1. Audience of 18,000 DevOps leaders has been targeted for 4 consecutive campaigns without
   refresh — frequency reached 8.2x (above 3x fatigue threshold)
2. Same creative (single image + headline) running for 6 weeks without variation
3. Competitor launched similar webinar series, splitting audience attention

### Fix Applied
1. Expanded audience to include adjacent titles (SRE, Platform Engineer, Cloud Architect)
2. Created 4 new creative variations (carousel, video, different value props)
3. Implemented frequency cap at 3x per 7-day window
4. Shifted 30% budget to retargeting warm website visitors instead

### Prevention
- Set frequency cap at campaign launch (max 3x per 7 days)
- Rotate creative every 3 weeks minimum
- Expand audience when pool <25K to avoid saturation
- Add to campaign launch checklist: audience overlap check with recent campaigns

### Context
- Trigger: performance_alert
- Campaign Type: event_promotion
- Audience: DevOps leaders at B2B SaaS companies, 200+ employees

### Metadata
- Reproducible: yes
- Related Campaigns: Q1-Webinar-DevOps, Q4-Whitepaper-DevOps
- See Also: LRN-20250416-001
- Tags: linkedin, CPL, audience-fatigue, creative-rotation, paid-media

---
```

## Campaign Issue: Attribution Gap (UTM Parameters Stripped by Redirect)

```markdown
## [CMP-20250416-001] utm_stripped_by_redirect

**Logged**: 2025-04-16T11:00:00Z
**Priority**: high
**Status**: resolved
**Area**: analytics

### Summary
Marketing site redirect chain stripped UTM parameters, causing 35% of paid traffic to show as direct/unattributed

### Performance Data
- Campaign: All paid campaigns (Google Ads, LinkedIn, Meta)
- Channel: google_ads, linkedin, meta_ads
- Date Range: 2025-03-15 to 2025-04-15
- Key Metrics:
  - Estimated affected sessions: 12,400
  - Unattributed conversions: 89
  - Revenue impact: ~$45K in untracked pipeline

### Root Cause
New marketing site deployment added a 301 redirect from `www.example.com` to `example.com`.
The redirect was implemented at the CDN layer (Cloudflare) which stripped query parameters
including UTM tags. All links in paid ads pointed to `www.` URLs, so every click lost
attribution data after the redirect.

### Fix Applied
1. Updated Cloudflare redirect rule to preserve query parameters: `$1?$query_string`
2. Updated all active ad URLs to use non-www canonical domain
3. Added server-side UTM capture as backup (first-party cookie on landing page load)
4. Backfilled 30 days of attribution data using ad platform click IDs

### Prevention
- Add UTM preservation check to deployment checklist
- Implement server-side UTM capture as standard (don't rely solely on client-side)
- Test redirect chains with UTM parameters before deploying infrastructure changes
- Set up automated alert: if unattributed traffic exceeds 15%, trigger investigation

### Context
- Trigger: attribution_audit
- Campaign Type: lead_gen
- Audience: all segments

### Metadata
- Reproducible: yes
- Related Campaigns: all active paid campaigns
- Tags: utm, attribution, redirect, tracking, cloudflare, analytics

### Resolution
- **Resolved**: 2025-04-16T15:00:00Z
- **Campaign/Initiative**: Infrastructure fix + process update
- **Notes**: Added UTM preservation to deployment checklist and implemented server-side backup capture

---
```

## Feature Request: Automated Content Performance Decay Alerts

```markdown
## [FEAT-20250417-001] content_decay_alerts

**Logged**: 2025-04-17T15:00:00Z
**Priority**: medium
**Status**: pending
**Area**: analytics

### Requested Capability
Automated alerting system that detects when top-performing content pieces lose significant
traffic or ranking, triggering a content refresh workflow before the decline compounds.

### User Context
Our top 20 blog posts drive 70% of organic traffic. We currently discover content decay
manually during monthly SEO reviews, by which time traffic has already dropped significantly.
An automated system would catch decay within 1-2 weeks, enabling faster response.

### Complexity Estimate
medium

### Suggested Implementation
1. Weekly cron job comparing current vs. 30-day-average organic sessions per URL
2. Alert threshold: >25% decline week-over-week for any top-50 URL
3. Output: Slack notification + entry in CAMPAIGN_ISSUES.md with affected URL, traffic delta,
   current ranking, and competitor comparison
4. Integration with Google Search Console API for ranking data
5. Dashboard widget showing content health scores (green/yellow/red)

### Metadata
- Frequency: recurring
- Related Features: Google Search Console integration, Slack alerting

---
```

## Learning: Promoted to Brand Guidelines

```markdown
## [LRN-20250410-003] messaging_miss

**Logged**: 2025-04-10T11:00:00Z
**Priority**: high
**Status**: promoted
**Promoted**: brand guidelines (MESSAGING_FRAMEWORK.md)
**Area**: campaigns

### Summary
Enterprise segment requires ROI-first messaging — never lead with ease-of-use or pricing

### Details
Across 5 enterprise campaigns over Q1, messaging that led with "easy" or "affordable"
consistently underperformed (8-12% open rate vs. 20-24% for ROI-focused subject lines).
Enterprise buyers respond to: quantified business impact, security compliance references,
integration capabilities, and peer company logos.

### Evidence

**A/B test results (5 campaigns, 21K enterprise contacts):**
- "Easy setup" subject lines: 9.4% avg open rate
- "ROI/impact" subject lines: 22.1% avg open rate
- Lift: +135%

### Suggested Action
Added to brand messaging framework: Enterprise messaging rules with required elements
(ROI metrics, security certs, integration ecosystem) and prohibited terms ("affordable",
"cheap", "easy setup" for enterprise).

### Metadata
- Source: a_b_test
- Channel: email
- Segment: enterprise
- Tags: messaging, enterprise, brand-guidelines, A/B-test, value-proposition
- Pattern-Key: messaging_miss.enterprise_value_prop
- Recurrence-Count: 5
- First-Seen: 2025-01-15
- Last-Seen: 2025-04-10

---
```

## Learning: Promoted to Skill (Email Deliverability Checklist)

```markdown
## [LRN-20250412-001] channel_underperformance

**Logged**: 2025-04-12T15:00:00Z
**Priority**: high
**Status**: promoted_to_skill
**Skill-Path**: skills/email-deliverability-checklist
**Area**: email

### Summary
Systematic email deliverability checklist prevents bounce spikes and spam folder placement

### Details
After 3 separate deliverability incidents over Q1 (bounce rate spikes to 8-12%, spam
placement on Gmail), developed a comprehensive pre-send checklist covering domain
authentication, list hygiene, warm-up protocols, and content checks. Following the
checklist reduced bounce rate from 6.2% average to 1.1% and eliminated spam folder
placement for authenticated sends.

### Suggested Action
Follow the deliverability checklist before every campaign send:
1. Verify SPF, DKIM, and DMARC records are current
2. Run list hygiene (remove bounces, inactive >6 months, role-based addresses)
3. Check sending domain reputation (Google Postmaster Tools, Sender Score)
4. Warm new IPs/domains: 500/day week 1, double weekly for 4 weeks
5. Test with seed list across Gmail, Outlook, Yahoo before full send
6. Monitor first-hour bounce rate; pause if >3%

### Metadata
- Source: deliverability_report
- Channel: email
- Segment: all
- Tags: email, deliverability, bounce-rate, spam, authentication, checklist
- See Also: CMP-20250215-002, CMP-20250308-001, CMP-20250401-003

---
```
