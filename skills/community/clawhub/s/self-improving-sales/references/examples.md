# Entry Examples

Concrete examples of well-formatted sales entries with all fields.

## Learning: Objection Pattern ("We already have a vendor")

```markdown
## [LRN-20250415-001] objection_pattern

**Logged**: 2025-04-15T10:30:00Z
**Priority**: high
**Status**: pending
**Area**: discovery

### Summary
"We already have a vendor for this" — no differentiation message ready

### Details
Prospect VP of Operations said "We already have a vendor for this, we're happy with
them" during initial discovery call. Rep had no prepared differentiation message for
the incumbent (Vendor X). Conversation stalled and prospect declined a second meeting.
This is the 4th time this quarter a deal died at discovery against Vendor X without
a clear differentiation narrative.

### Deal Context

**Objection / Situation:**
> "We already use Vendor X for this. They've been our partner for three years
> and we're happy with the relationship."

**Response Used:**
> "I understand. We just think we can offer some improvements."

**Outcome:**
Lost — prospect declined follow-up. No differentiation articulated.

### Suggested Action
Create battle card for Vendor X with:
1. Trap-setting discovery questions that expose Vendor X's known weaknesses
2. Differentiation framework: what we do that Vendor X cannot
3. Customer proof points: companies that switched from Vendor X and results achieved

### Metadata
- Source: call_transcript
- Deal Size: $100K-$250K
- Segment: mid_market
- Industry: technology
- Related Deals: DEAL-20250320-002, DEAL-20250401-003
- Tags: objection, incumbent, vendor-x, differentiation, discovery
- Pattern-Key: objection.incumbent_vendor
- Recurrence-Count: 4
- First-Seen: 2025-01-22
- Last-Seen: 2025-04-15

---
```

## Learning: Competitor Shift (Free Tier Launch)

```markdown
## [LRN-20250416-001] competitor_shift

**Logged**: 2025-04-16T09:15:00Z
**Priority**: high
**Status**: pending
**Area**: qualification

### Summary
Competitor Y launched a free tier, losing SMB deals that previously closed at $15K-$30K ARR

### Details
Competitor Y announced a free tier covering up to 5 users with core features on April 1st.
Since then, 6 SMB prospects in the pipeline have either gone dark or explicitly said they're
evaluating the free option. Our SMB win rate dropped from 42% to 18% in the two weeks since
announcement. The free tier lacks advanced reporting, integrations, and SLA guarantees that
our paid plans include.

### Deal Context

**Objection / Situation:**
> "We saw Competitor Y just launched a free version. Can you match that or explain
> why we should pay when they're offering it for free?"

**Response Used:**
> Various — no consistent counter-messaging deployed yet.

**Outcome:**
3 lost to free tier, 3 stalled pending "internal review"

### Suggested Action
1. Create competitive battle card for Competitor Y free tier
2. Build TCO calculator showing hidden costs of free tier (migration, support, limits)
3. Develop talk track: "Free gets you started, but here's what it costs when you scale"
4. Consider SMB-specific pricing response (starter tier or extended trial)

### Metadata
- Source: competitor_intel
- Deal Size: $15K-$30K
- Segment: SMB
- Industry: technology
- Tags: competitor-y, free-tier, SMB, pricing-pressure, win-rate
- Pattern-Key: competitor.free_tier_launch

---
```

## Learning: Pipeline Leak (Proposal Stage)

```markdown
## [LRN-20250417-001] pipeline_leak

**Logged**: 2025-04-17T14:00:00Z
**Priority**: medium
**Status**: pending
**Area**: proposal

### Summary
Deals dying at proposal stage due to slow legal review — 23-day average wait vs. 5-day target

### Details
Analyzed Q1 pipeline and found 34% of deals that reached proposal stage ultimately died there.
Root cause: legal review of MSA/DPA takes an average of 23 business days. Prospects lose
momentum, re-engage competitors, or deprioritize the project. Deals under $100K are
particularly affected because legal treats them with the same rigor as enterprise deals.

### Deal Context

**Objection / Situation:**
> "We're ready to move forward but your legal team hasn't returned the redlines in
> three weeks. We need this resolved by end of quarter or we're going with [competitor]."

**Response Used:**
> Escalated to VP Sales who escalated to General Counsel. Resolved in 2 more days
> but relationship was strained.

**Outcome:**
Won (barely) — but pattern repeats. 8 of 14 proposal-stage losses in Q1 cited legal delay.

### Suggested Action
1. Pre-approved MSA template for deals under $100K (skip custom legal review)
2. SLA with legal: 5-day turnaround for standard terms, 10-day for custom
3. Send legal paperwork in parallel with proposal, not sequentially
4. Add legal readiness as a stage gate before advancing to proposal

### Metadata
- Source: pipeline_review
- Deal Size: $50K-$250K
- Segment: mid_market
- Tags: legal, MSA, proposal-stage, pipeline-leak, velocity
- Pattern-Key: pipeline_leak.legal_review_delay
- Recurrence-Count: 8
- First-Seen: 2025-01-15
- Last-Seen: 2025-04-17

---
```

## Deal Issue: Forecast Miss (Q2 Over-Forecast)

```markdown
## [DEAL-20250415-001] forecast_miss

**Logged**: 2025-04-15T16:00:00Z
**Priority**: critical
**Status**: pending
**Area**: closing

### Summary
Q2 forecast 40% over actual — $2.1M committed vs. $1.26M closed, primarily due to pushed enterprise deals

### Deal Details
- **Stage**: Closing (Stage 5+)
- **Deal Size**: $500K+ (aggregate)
- **Days in Stage**: Various (15-45 days past projected close)
- **Segment**: enterprise

### What Happened
Five enterprise deals totaling $840K that were in "commit" status for Q2 did not close:
- Two pushed to Q3 due to budget re-approval (new fiscal year)
- One lost to competitor after 11th-hour pricing undercut
- One went to "no decision" after champion left the company
- One delayed by procurement requiring additional security review

### Root Cause
Over-reliance on rep-reported confidence without verifying:
1. Budget approval was actually in place (not just "verbal")
2. Champion still had organizational authority
3. Procurement timeline was validated with procurement (not just the champion)
4. Competitive situation was truly resolved

### Impact
- Revenue shortfall: $840K (40% of committed pipeline)
- Board reporting required revision
- Team compensation affected (accelerators not triggered)
- Credibility with finance damaged for future forecasting

### Prevention
1. Require written budget confirmation before "commit" status
2. Validate champion authority with second contact in account
3. Add procurement timeline verification as commit criteria
4. Implement "champion risk" flag when contacts change roles
5. Forecast calls should challenge every commit deal with specific evidence

### Metadata
- Trigger: forecast_review
- Loss Reason: timing (2), lost_to_competitor (1), no_decision (1), product_gap (0), price (1)
- See Also: DEAL-20250110-003 (Q1 similar pattern, 25% miss)

---
```

## Deal Issue: Pricing Error (Deprecated Tier)

```markdown
## [DEAL-20250416-001] pricing_error

**Logged**: 2025-04-16T11:30:00Z
**Priority**: high
**Status**: pending
**Area**: proposal

### Summary
Quoted deprecated "Growth" pricing tier to enterprise prospect — $45/user/month instead of current $65/user/month

### Deal Details
- **Stage**: Proposal
- **Deal Size**: $100K-$250K
- **Days in Stage**: 5
- **Segment**: enterprise

### What Happened
AE used an outdated pricing sheet (Q3 2024) that still listed the "Growth" tier at
$45/user/month. Current pricing is $65/user/month for "Business" tier (Growth was
sunset in Q4 2024). Prospect received the quote, got internal approval at the lower
price point, and now expects to close at $45. Honoring the quote costs $48K ARR;
revising it risks losing the deal and trust.

### Root Cause
1. Outdated pricing PDF still accessible in shared drive
2. No version control or expiration date on pricing documents
3. CRM CPQ not enforced — reps can send manual quotes
4. No pricing approval workflow for non-standard quotes

### Impact
- $48K ARR gap if honored vs. current pricing
- Prospect trust damage if revised upward
- Sets precedent for other reps using outdated materials

### Prevention
1. Archive all deprecated pricing documents with "DEPRECATED" watermark
2. Enforce CPQ for all quotes — block manual pricing
3. Add pricing version validation in proposal review checklist
4. Quarterly pricing audit: search for any references to sunset tiers

### Metadata
- Trigger: deal_review
- Related Files: pricing/growth-tier-sunset-notice.md
- See Also: DEAL-20250220-002 (similar pricing document version issue)

---
```

## Feature Request: Automated Competitive Intelligence Alerts

```markdown
## [FEAT-20250415-001] competitive_intelligence_alerts

**Logged**: 2025-04-15T17:00:00Z
**Priority**: high
**Status**: pending
**Area**: prospecting

### Requested Capability
Automated alerts when competitors announce pricing changes, product launches,
leadership changes, or funding rounds. Delivered to Slack #competitive-intel
channel with summary and recommended battle card updates.

### User Context
Competitor Y's free tier launch caught the team off-guard for 2 weeks before
a coordinated response was developed. During that window, 6 SMB deals were
affected. Real-time competitive intelligence would allow same-day response
with updated positioning and talk tracks.

### Complexity Estimate
medium

### Suggested Implementation
1. Monitor competitor websites, press releases, and G2/Gartner reviews via RSS + web scraping
2. Track competitor job postings for signals (hiring in new markets, new product areas)
3. Aggregate call transcript mentions of competitors (Gong/Chorus integration)
4. Slack bot posts daily digest of competitive signals with severity rating
5. Auto-flag deals in CRM where mentioned competitor has recent activity

### Metadata
- Frequency: recurring
- Related Features: CRM competitive field, call transcript analysis, battle card system

---
```

## Learning: Promoted to Battle Card

```markdown
## [LRN-20250410-003] objection_pattern

**Logged**: 2025-04-10T11:00:00Z
**Priority**: high
**Status**: promoted
**Promoted**: battle card (BATTLECARDS/vendor-x.md)
**Area**: negotiation

### Summary
"Your product is too expensive compared to Vendor X" — need ROI reframe

### Details
Found in 9 deals over Q1. Vendor X undercuts on price by 20-30% but lacks
our advanced analytics, dedicated CSM, and 99.99% SLA. Reps who successfully
countered this objection used ROI framing: "Our customers see 3x return within
6 months" backed by case studies. Reps who competed on price lost every time.

### Deal Context

**Objection / Situation:**
> "Vendor X quoted us 25% less. Why should we pay more?"

**Response Used (winning):**
> "That's a fair question. Let me share what Company Z found — they evaluated
> both and chose us because [specific capability] saved them $200K in the
> first year. The price difference pays for itself in [timeframe]."

**Outcome:**
Won 6 of 9 deals where ROI reframe was used. Lost 3 where rep matched price.

### Suggested Action
Added to Vendor X battle card: never compete on price, always reframe to ROI
and total cost of ownership. Include 3 customer proof points with specific
dollar savings.

### Metadata
- Source: win_loss_analysis
- Deal Size: $100K-$500K
- Segment: mid_market
- Industry: technology, financial_services
- Tags: pricing, vendor-x, ROI, battle-card, objection
- Pattern-Key: objection.price_comparison
- Recurrence-Count: 9
- First-Seen: 2025-01-08
- Last-Seen: 2025-04-10

---
```

## Learning: Promoted to Skill (MEDDIC Qualification Checklist)

```markdown
## [LRN-20250412-001] pipeline_leak

**Logged**: 2025-04-12T15:00:00Z
**Priority**: high
**Status**: promoted_to_skill
**Skill-Path**: skills/meddic-stage-gates
**Area**: qualification

### Summary
Systematic MEDDIC qualification checklist with hard stage gates to prevent unqualified deals from advancing

### Details
Analyzed 50 lost deals from H2 2024. Found that 72% of lost deals were missing
at least 2 MEDDIC criteria when they advanced past discovery. Deals with all 6
MEDDIC elements validated by Stage 3 closed at 58% vs. 14% for those missing 2+
elements. Created a mandatory checklist with hard gates: deal cannot advance
without completing minimum criteria for each stage.

### Suggested Action
Implemented as CRM stage gate validation:
1. Metrics: Quantified business impact documented
2. Economic Buyer: Identified by name and confirmed access
3. Decision Criteria: Written and validated with prospect
4. Decision Process: Timeline, steps, and approvals mapped
5. Identify Pain: Specific pain tied to business metric
6. Champion: Named, tested, and actively selling internally

### Metadata
- Source: win_loss_analysis
- Deal Size: $50K-$500K+
- Segment: mid_market, enterprise
- Tags: MEDDIC, qualification, stage-gates, pipeline-hygiene, win-rate
- See Also: LRN-20250320-002, DEAL-20250401-005, DEAL-20250415-001

---
```
