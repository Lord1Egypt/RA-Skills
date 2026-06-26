# Ad Account Audit Scoring System

<!-- Updated: 2026-04-13 | v1.5: updated check counts, cross-platform checks, ID convention -->
<!-- Sources: Google Research PDF 1, Claude Research, Gemini Research, 2026 Platform Research -->

## Check ID Convention

- **Sequential IDs** (G01, M01, L01, T01, MS01): Original v1.0 checks
- **Hyphenated IDs** (G-AI1, M-AN1, L-CRM1, T-SR1, MS-SI1, X-PI1): v1.5+ additions
- **Platform prefixes**: G = Google, M = Meta, L = LinkedIn, T = TikTok, MS = Microsoft, ASA = Apple, X = Cross-platform

## Weighted Scoring Algorithm

```
S_total = Σ(C_pass × W_sev × W_cat) / Σ(C_total × W_sev × W_cat) × 100
```

- `C_pass` = check passed (1) or failed (0); WARNING = 0.5
- `W_sev` = severity multiplier of the individual check
- `W_cat` = category weight for that platform
- Result: 0-100 Health Score

## Severity Multipliers

| Severity | Multiplier | Criteria |
|----------|-----------|----------|
| Critical | 5.0 | Immediate revenue/data loss risk. Remediation urgent. |
| High | 3.0 | Significant performance drag. Fix within 7 days. |
| Medium | 1.5 | Optimization opportunity. Fix within 30 days. |
| Low | 0.5 | Best practice, minor impact. Nice to have. |

## Scoring Per Check Item

| Result | Points Earned |
|--------|--------------|
| PASS | Full severity × category weight |
| WARNING | 50% of full points |
| FAIL | 0 points |
| N/A | Excluded from total possible |

## Category Weights by Platform

### Google Ads
| Category | Weight | Rationale |
|----------|--------|-----------|
| Conversion Tracking | 25% | Foundation for all optimization; Enhanced Conv + Consent Mode V2 + CTV tracking (12 checks) |
| Wasted Spend / Negatives | 20% | Direct money leak; search terms, negative lists (8 checks) |
| Account Structure | 15% | Campaign organization, brand/non-brand separation (12 checks) |
| Keywords & Quality Score | 15% | QS as diagnostic, not KPI; keyword-ad alignment (8 checks) |
| Ads & Assets | 15% | RSA strength, PMax assets, AI Max, Demand Gen (12 checks + PMax 6 + AI/DG 4) |
| Settings & Targeting | 10% | Location, network, audiences, landing pages (12 checks) |

### Meta Ads
| Category | Weight | Rationale |
|----------|--------|-----------|
| Pixel / CAPI Health | 30% | 87% of advertisers have poor EMQ; foundational signal (10 checks) |
| Creative (Diversity & Fatigue) | 30% | Andromeda makes creative the #1 targeting lever (12 checks) |
| Account Structure | 20% | Learning phase, Advantage+ Sales, consolidation (18 checks) |
| Audience & Targeting | 20% | Overlap, exclusions, Advantage+ Audience (6 checks) |
| Andromeda & Platform Changes | N/A | v1.5 checks scored within above categories (4 checks) |

### LinkedIn Ads
| Category | Weight | Rationale |
|----------|--------|-----------|
| Technical Setup | 25% | Insight Tag + CAPI essential for B2B attribution (2 checks) |
| Audience Quality | 25% | LinkedIn's targeting precision is its differentiator (7 checks) |
| Creative & Formats | 20% | TLA + format diversity; video efficiency varies (4 checks) |
| Lead Gen Forms | 15% | 13% CVR (3.25x landing pages); CRM integration (2 checks) |
| Bidding & Budget | 15% | Manual CPC first for cost control (2 checks) |
| CRM & Compliance | 10% | v1.5: CRM revenue attribution, EU messaging compliance (2 checks) |

### TikTok Ads
| Category | Weight | Rationale |
|----------|--------|-----------|
| Creative Quality | 30% | Native-feel content is #1 success factor (10 checks) |
| Technical Setup | 25% | Pixel + Events API Gateway + ttclid passback (2 checks) |
| Bidding & Learning | 20% | 50 conv/week to exit learning; budget sufficiency (3 checks) |
| Structure & Settings | 15% | Smart+ modular control, Search Toggle, Shop integration (6 checks) |
| Performance | 10% | CTR, CPA, completion rate benchmarks (3 checks) |
| Search, Commerce & Tracking | N/A | v1.5 checks scored within above categories (3 checks) |

### Microsoft Ads
| Category | Weight | Rationale |
|----------|--------|-----------|
| Technical Setup | 25% | UET tag, import validation, Enhanced Conv (3 checks) |
| Syndication & Bidding | 20% | Partner network control (High severity), Copilot placement (4 checks) |
| Structure & Audience | 20% | LinkedIn targeting (16% CTR lift), campaign structure (3 checks) |
| Creative & Extensions | 20% | Multimedia, Video (9:16 Apr 2025), Action/Filter Link (5 checks) |
| Settings & Performance | 15% | CPC advantage tracking, conversion rate comparison (5 checks) |
| Import Safety, Compliance & Video | N/A | v1.5: scheduled imports, Consent Mode, CTV, video (4 checks) |

### Amazon Ads (v1.7 — inline in `skills/ads-amazon/SKILL.md`, not yet in catalog)
| Category | Weight | Rationale |
|----------|--------|-----------|
| Search-Term Harvesting & Negatives | 25% | Auto→Manual harvest cadence is the single biggest TACOS lever |
| ACOS / TACOS Discipline | 20% | Per-portfolio targets tied to contribution margin; TACOS trend |
| Campaign Structure & Portfolios | 15% | Auto + Manual mix per ASIN, brand-defense isolation |
| Bid & Budget Management | 15% | Dynamic bidding strategy per campaign type, placement multipliers |
| Sponsored Brands | 10% | HSA, SB Video for high-AOV products |
| Sponsored Display | 10% | Audience vs contextual separation, off-Amazon SD |
| Brand Analytics & Reporting | 5% | Top Search Terms, Repeat Purchase, Amazon Attribution |

### Apple Ads (v1.7 — inline in `skills/ads-apple/SKILL.md`, not yet in catalog)
| Category | Weight | Rationale |
|----------|--------|-----------|
| MMP / AdAttributionKit Integration | 30% | Without proper dual attribution (SKAN + AAK), bid algorithms fly blind |
| Campaign Structure & Targeting | 20% | Discovery / Search Tab / Today / Search Results / Product Pages split |
| Bid Health & CPT Goals | 15% | Maximize Conversions vs CPA goal vs manual; country-specific CPA goals |
| Custom Product Pages (CPPs) | 15% | Required since Creative Sets deprecation; per-keyword-theme CPPs |
| Budget Pacing | 10% | Daily caps appropriate to install volume + algorithm learning |
| ATT Opt-in & Privacy Threshold | 10% | <30% opt-in shifts reliance to SKAN/AAK + privacy threshold |

### Attribution + Server-side Tracking (v1.7 — inline in `skills/ads-attribution/SKILL.md` and `skills/ads-server-side-tracking/SKILL.md`)
| Category | Weight | Rationale |
|----------|--------|-----------|
| Web Attribution (GA4 + Ads + CAPI) | 30% | Foundational signal for every web channel |
| Server-Side Stitching | 20% | event_id dedup, MMP first-party stitching, offline conversion import |
| iOS Attribution (AdAttributionKit + ATT) | 20% | Required for any iOS app advertiser |
| Consent Mode V2 | 15% | Advanced mode required for EEA signal recovery |
| MMP Health (mobile) | 10% | AppsFlyer/Adjust/Branch/Singular configuration |
| Cross-Device / Customer Match | 5% | Customer Match list freshness, Enhanced Conversions parameter coverage |

## Grading Thresholds

| Grade | Score | Label | Action Required |
|-------|-------|-------|-----------------|
| A | 90-100 | Excellent | Minor optimizations only |
| B | 75-89 | Good | Some improvement opportunities |
| C | 60-74 | Needs Improvement | Notable issues need attention |
| D | 40-59 | Poor | Significant problems present |
| F | <40 | Critical | Urgent intervention required |

## Quick Wins Logic

```
IF severity == "Critical" OR severity == "High"
AND estimated_remediation_time < 15 minutes
THEN flag as "Quick Win"
PRIORITY: Quick Wins sorted by (severity × estimated_impact) DESC
```

Quick Win examples:
- Enable Enhanced Conversions (Critical, 5 min)
- Turn on Search Ads Toggle in TikTok (High, 2 min)
- Add negative keyword lists (Critical, 10 min)
- Fix location targeting method (Critical, 2 min)
- Enable Advantage+ Placements (Medium, 2 min)

## Weighting Rationale

Category weights are calibrated for paid advertising accounts where conversion tracking infrastructure is the highest-impact factor (25-30% weight across platforms). This differs from generic scoring systems because:
- Broken tracking invalidates all optimization decisions downstream
- Creative and targeting quality follow tracking in priority
- Settings and compliance are important but have lower direct revenue impact
- Weights sum to 100% per platform, enabling direct cross-platform comparison

The grading thresholds (A=90-100, B=75-89, C=60-74, D=40-59, F=<40) use wider bands than academic-style scoring because ad account health is typically distributed lower; a score of 75+ represents genuinely well-managed accounts.

---

## Cross-Platform Checks (v1.5)

These checks apply across all platforms during full audits:

| ID | Check | Severity | Description |
|----|-------|----------|-------------|
| X-PI1 | Privacy infrastructure completeness | Critical | Consent Mode V2 (Google/MS) + CAPI (Meta) + Events API (TikTok) + AdAttributionKit (Apple). Without proper signals, no optimization works |
| X-CD1 | Creative diversity audit | High | Andromeda, Smart+, and PMax all use creative signals for targeting. Flag accounts with <5 genuinely distinct creative concepts |
| X-RF1 | Platform-appropriate refresh cadence | High | TikTok 7-10d, Meta 14-21d, LinkedIn 4-6w, Google/MS 8-12w. Flag overdue refreshes |

Cross-platform checks are scored at 100% weight in the aggregate score (not within any single platform).

---

## Total Check Counts (v1.5)

| Platform | v1.0 | v1.5 | v1.7 | Change vs v1.5 |
|----------|------|------|------|----------------|
| Google | 74 | 80 | 80 | — (AI Max deep-rewrite via SKILL.md body) |
| Meta | 46 | 50 | 50 | — (Andromeda + GEM + Lattice + Entity-ID predictor via SKILL.md body) |
| LinkedIn | 25 | 27 | 27 | — |
| TikTok | 25 | 28 | 28 | — (USDS context via SKILL.md body) |
| Microsoft | 20 | 24 | 24 | — |
| Cross-platform | 0 | 3 | 3 | — |
| **Catalog-tracked total** | **190** | **212** | **212** | — |
| Apple (SKILL.md inline) | — | — | 35+ | New in v1.7 weight table above |
| Amazon (SKILL.md inline) | — | — | 30+ | New in v1.7 weight table above |
| Attribution + Server-side (SKILL.md inline) | — | — | 25+ | New in v1.7 weight table above |
| **Grand total (all sources)** | **190** | **212** | **~302+** | **+90+ new checks via inline thresholds** |

Note: catalog-tracked checks are verified bidirectionally by the eval harness
(`tests/audit/test_check_coverage.py`). Apple, Amazon, and Attribution +
Server-side checks live inline in their respective SKILL.md files; their
dedicated audit reference files (`apple-audit.md`, `amazon-audit.md`,
`attribution-audit.md`) and catalog entries land in Wave 3.

---

## Cross-Platform Aggregate Score

When auditing multiple platforms, calculate per-platform scores then aggregate:

```
Aggregate Score = Σ(Platform_Score × Platform_Budget_Share)

Example: Google (82) × 40% + Meta (71) × 35% + LinkedIn (90) × 25%
       = 32.8 + 24.85 + 22.5 = 80.15 → Grade B
```
