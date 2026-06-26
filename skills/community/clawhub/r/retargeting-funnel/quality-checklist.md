# Retargeting Funnel Quality Checklist

Use this checklist before launching a retargeting funnel and during weekly optimization reviews. Every item should be verified or intentionally marked as not applicable.

## Tracking and Pixel Health (8 items)

- [ ] Meta Pixel fires on all site pages including dynamically loaded content
- [ ] Google Ads tag fires on all site pages with correct conversion actions
- [ ] TikTok Pixel fires on all site pages (if TikTok is in the media plan)
- [ ] ViewContent/view_item event fires on every product detail page with correct product ID, value, and currency
- [ ] AddToCart event fires on all cart addition methods (button click, AJAX cart, quick-add)
- [ ] InitiateCheckout and Purchase events fire with accurate order value and transaction ID
- [ ] Server-side tracking is active (Meta CAPI, Google Enhanced Conversions, TikTok Events API) with deduplication configured
- [ ] Event Match Quality score is 6.0+ on Meta (checked in Events Manager)

## Product Feed and Catalog (7 items)

- [ ] Product feed syncs automatically at least every 6 hours
- [ ] All active products have unique IDs that match pixel event content_ids/item_ids
- [ ] Product images meet minimum resolution requirements (500x500px for Meta, 100x100px for Google)
- [ ] Prices in the feed match live website prices (no stale pricing)
- [ ] Out-of-stock products are marked unavailable or excluded from the feed
- [ ] Product titles are descriptive and under 150 characters
- [ ] Feed has zero disapproved items in catalog diagnostics (Meta Commerce Manager, Google Merchant Center)

## Audience Segmentation (8 items)

- [ ] All funnel segments (S1 through S6) are created on each active platform
- [ ] Exclusion logic is applied: each segment excludes all higher-intent segments
- [ ] Lookback windows are appropriate per segment (shorter for higher intent)
- [ ] Recent purchasers (S6) are excluded from all acquisition retargeting campaigns
- [ ] Audience sizes meet platform minimums for delivery (1,000+ for Meta/Google, 1,000+ for TikTok)
- [ ] No unintentional audience overlap exists between segments (verified with Meta Audience Overlap tool or equivalent)
- [ ] Sub-segments are created where audience size allows (e.g., cart value splits, engagement depth splits)
- [ ] Audiences use rolling windows, not fixed date ranges

## Creative and Messaging (8 items)

- [ ] Each funnel segment has dedicated creative matching its intent level
- [ ] Dynamic product ads are active for S3 (product viewers) and S4-S5 (abandoners)
- [ ] Top-funnel creative (S1-S2) uses brand storytelling or value proposition, not product-specific hard sells
- [ ] Bottom-funnel creative (S4-S5) includes urgency elements and clear CTAs
- [ ] Ad copy does not make the viewer feel surveilled ("We saw you looking at..." is acceptable; "We tracked your every click" is not)
- [ ] All ad formats are tested across placements (feed, stories, reels for Meta; responsive display for Google)
- [ ] Creative refresh schedule is established (new variations every 2-3 weeks)
- [ ] Landing page URLs are correct and lead to relevant pages (product page for DPA, category for S2, homepage for S1)

## Campaign Configuration (7 items)

- [ ] Campaign objectives match funnel stage (traffic/engagement for top, conversions/sales for bottom)
- [ ] Bid strategies are appropriate per stage (target ROAS for bottom funnel, maximize clicks for top funnel)
- [ ] Budget allocation weights bottom-funnel segments (50-60% of retargeting spend)
- [ ] Campaign budget optimization (CBO) is set within each funnel stage, not across stages
- [ ] Frequency caps are configured per segment (lower caps for low-intent, higher for high-intent)
- [ ] Attribution windows are consistent across campaigns for comparable reporting
- [ ] Campaigns are separated by platform role (Meta full-funnel, Google intent capture, TikTok social proof)

## Measurement and Optimization (6 items)

- [ ] KPIs are defined for each funnel segment with specific targets
- [ ] Incrementality holdout groups are configured (10-15% of each segment withheld from retargeting)
- [ ] Cross-platform frequency is monitored to prevent over-saturation (target 8-12 daily for bottom funnel)
- [ ] Weekly performance review cadence is scheduled with clear owners
- [ ] Low-quality placements are reviewed and excluded weekly (Google Display Network especially)
- [ ] Creative fatigue is monitored via CTR trend analysis with rotation triggered at 20% CTR decline

## Post-Launch Validation (6 items)

- [ ] Ads are delivering to the correct audiences (spot-check with delivery insights)
- [ ] No audience segments show zero delivery after 48 hours (investigate if so)
- [ ] Dynamic product ads are pulling correct products from the catalog (preview ads in each platform)
- [ ] Landing page links from ads load correctly and match the advertised product
- [ ] Conversion tracking is recording purchases accurately (cross-reference ad platform data with ecommerce backend)
- [ ] Budget pacing is on track (no campaigns exhausting budget by midday or underspending significantly)
