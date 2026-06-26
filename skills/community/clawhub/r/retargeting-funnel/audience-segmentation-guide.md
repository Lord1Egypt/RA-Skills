# Audience Segmentation Guide for Retargeting Funnels

This guide covers how to build, configure, and maintain retargeting audience segments by funnel stage across Meta, Google, and TikTok.

## Core Segmentation Principles

### Mutual Exclusivity

Every visitor should appear in exactly one funnel segment at a time. This is achieved through exclusion logic: each segment excludes all visitors who qualify for a higher-intent segment.

**Why this matters:**
- Prevents the same user from receiving ads from multiple funnel stages simultaneously
- Ensures budget is allocated to the creative most relevant to each user's intent level
- Produces clean performance data — you can attribute conversions to the correct funnel stage

**Implementation:** When building custom audiences in any platform, always apply exclusion audiences. A "Product Viewer" audience must exclude anyone who has also triggered AddToCart, InitiateCheckout, or Purchase events.

### Intent Signal Hierarchy

Rank visitor actions from lowest to highest intent. The deepest action a visitor has taken determines their segment.

| Rank | Action | Intent Level | Segment |
|---|---|---|---|
| 1 | Page view only (homepage/about/blog) | Lowest | S1: Homepage Bouncers |
| 2 | Category/collection page view | Low-Mid | S2: Category Browsers |
| 3 | Product detail page view | Mid | S3: Product Viewers |
| 4 | Add to cart | Mid-High | S4: Cart Abandoners |
| 5 | Begin checkout | High | S5: Checkout Abandoners |
| 6 | Purchase | Converted | S6: Purchasers (suppress/upsell) |

## Building Segments by Platform

### Meta Custom Audiences

**S1 — Homepage Bouncers:**
1. Go to Audiences > Create Audience > Custom Audience > Website
2. Select "People who visited specific web pages"
3. Include: URL contains "/" (all pages)
4. Exclude: Custom Audience of ViewContent event triggers
5. Exclude: Custom Audience of AddToCart event triggers
6. Exclude: Custom Audience of Purchase event triggers
7. Set retention to 30 days

**S2 — Category Browsers:**
1. Create Custom Audience > Website
2. Include: URL contains "/collections/" OR "/category/" (adjust to your URL structure)
3. Exclude: Custom Audience of ViewContent event triggers (product pages)
4. Exclude: Custom Audience of AddToCart, Purchase
5. Set retention to 21 days

**S3 — Product Viewers:**
1. Create Custom Audience > Website
2. Event: ViewContent
3. Exclude: Custom Audience of AddToCart event triggers
4. Exclude: Custom Audience of Purchase event triggers
5. Set retention to 14 days

**S4 — Cart Abandoners:**
1. Create Custom Audience > Website
2. Event: AddToCart
3. Exclude: Custom Audience of InitiateCheckout event triggers
4. Exclude: Custom Audience of Purchase event triggers
5. Set retention to 7 days

**S5 — Checkout Abandoners:**
1. Create Custom Audience > Website
2. Event: InitiateCheckout
3. Exclude: Custom Audience of Purchase event triggers
4. Set retention to 3 days

**S6 — Recent Purchasers:**
1. Create Custom Audience > Website
2. Event: Purchase
3. Set retention to 30 days (suppression) or 60 days (cross-sell after 14-day gap)

### Google Ads Audience Segments

**Using Google Ads audience manager:**

1. Navigate to Tools & Settings > Audience Manager > Segments
2. Create segments using "Website visitors" as the source

**S1 — Homepage Bouncers:**
- Segment members: "Visitors of a page"
- Page URL: All visitors
- Add "Also exclude" rules for each higher-intent segment
- Membership duration: 30 days

**S3 — Product Viewers (example):**
- Segment members: "Visitors of a page who also visited another page" — use this to target product page URL patterns
- OR use Google Analytics 4 audiences based on the `view_item` event
- Exclude users who triggered `add_to_cart` or `purchase`
- Membership duration: 14 days

**GA4 integration (recommended for precision):**
- Build audiences in GA4 using event-based conditions
- GA4 audiences auto-sync to Google Ads within 24-48 hours
- Advantage: GA4 supports complex sequencing conditions (e.g., "triggered view_item but NOT add_to_cart within the same session or any subsequent session")

### TikTok Custom Audiences

1. Go to TikTok Ads Manager > Assets > Audiences
2. Create Custom Audience > Website Traffic

**Segment configuration mirrors Meta's approach:**
- Use TikTok pixel events (ViewContent, AddToCart, etc.)
- Apply exclusion rules using "Exclude" audience settings
- Set retention windows per segment

**TikTok-specific considerations:**
- TikTok audiences require a minimum of 1,000 users to be targetable
- Smaller ecommerce sites may need to combine S4 and S5 into a single bottom-funnel segment
- TikTok's Events API (server-side) supplements browser pixel data — configure it for higher match rates

## Advanced Segmentation Strategies

### Value-Based Sub-Segments

Split cart abandoners by cart value to customize messaging and incentive strategy:

| Sub-Segment | Cart Value | Strategy | Incentive |
|---|---|---|---|
| S4-Low | Under $50 | Social proof, urgency | None (margins too thin) |
| S4-Mid | $50-$150 | Free shipping threshold nudge | Free shipping if within $10 of threshold |
| S4-High | $150+ | White-glove service, price guarantee | Free expedited shipping or 5% discount |

### Engagement Depth Sub-Segments

Split product viewers by engagement intensity:

| Sub-Segment | Behavior | Window | Creative Approach |
|---|---|---|---|
| S3a: Casual Viewer | Viewed 1 product, <30s on page | 14 days | Category-level exploration ads |
| S3b: Active Researcher | Viewed 3+ products or 2+ min on page | 14 days | DPA with all viewed items + comparison angle |
| S3c: Repeat Visitor | Viewed same product 2+ times | 7 days | Social proof + urgency ("X people viewing now") |

### Time-Decay Segmentation

Within each segment, create sub-audiences based on recency:

**Cart Abandoners example:**
- S4-Fresh: Abandoned 0-24 hours ago (highest urgency, highest conversion probability)
- S4-Warm: Abandoned 1-3 days ago (reminder with social proof)
- S4-Cooling: Abandoned 3-7 days ago (last-chance messaging, consider incentive)

**Implementation:** Create three separate audiences with different retention windows and apply the same exclusion hierarchy. S4-Fresh excludes S5-S6. S4-Warm excludes S4-Fresh and S5-S6.

### Traffic Source Segmentation

Separate retargeting audiences by how they originally arrived:

| Source | Behavior Pattern | Retargeting Implication |
|---|---|---|
| Paid search | High intent — came via keyword search | Show product-specific ads, mirror search intent |
| Paid social | Discovery-driven — clicked an ad | Remind them of the ad angle that brought them |
| Organic search | Research mode — comparing options | Differentiation messaging, review-focused creative |
| Direct / email | Brand-familiar — typed URL or clicked newsletter | Loyalty-oriented, new arrivals, exclusive access |
| Referral | Trust-transferred from referring site | Lean into the referrer's endorsement if possible |

## Audience Size Management

### Minimum Viable Audience Sizes

Each platform has practical minimum audience sizes for effective delivery:

| Platform | Minimum for Delivery | Recommended Minimum | Below Minimum Action |
|---|---|---|---|
| Meta | 100 users | 1,000+ users | Widen lookback window or merge with adjacent segment |
| Google Display | 100 users | 1,000+ users | Use broader audience signals in PMax |
| Google Search RLSA | 1,000 users | 5,000+ users | Cannot run RLSA — use display only |
| TikTok | 1,000 users | 5,000+ users | Merge segments or skip platform |

### When Segments Are Too Small

For smaller ecommerce sites (under 50K monthly visitors), full six-segment funnels may produce audiences too small for effective delivery. Consolidation options:

**Three-segment model:**
- Top: All visitors who did not add to cart (combines S1, S2, S3)
- Mid: Cart + checkout abandoners (combines S4, S5)
- Bottom: Purchasers (S6 — suppress or cross-sell)

**Four-segment model:**
- S1+S2: All non-product-page visitors
- S3: Product viewers
- S4+S5: All abandoners
- S6: Purchasers

Scale up to the full six-segment model as traffic grows and individual segments exceed 1,000 users per platform.

## Audience Hygiene and Maintenance

### Rolling Exclusions

Audiences are dynamic — users enter and exit based on their latest actions. Ensure your platform settings use rolling windows (not fixed dates) so audiences refresh automatically.

### Purchaser Suppression Timing

| Product Type | Suppression Window | Rationale |
|---|---|---|
| Consumables (skincare, supplements) | 14-21 days | Replenishment cycle — switch to replenishment ads after suppression |
| Fashion / apparel | 14-30 days | Short consideration, but give post-purchase satisfaction time |
| Electronics / high-AOV | 30-90 days | Long purchase cycle, unlikely to rebuy immediately |
| Subscription products | Ongoing | Suppress acquisition ads entirely for active subscribers |

### Weekly Audience Health Checks

- Verify audience sizes are not shrinking unexpectedly (may indicate pixel issues)
- Confirm exclusion audiences are populating correctly
- Check for audience overlap using Meta's Audience Overlap tool or Google's audience insights
- Review segment migration rates — if very few S1 visitors ever become S3, your top-funnel creative may not be working
