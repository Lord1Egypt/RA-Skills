---
name: shopify-ads-helper
description: Optimize Shopify-specific paid growth workflows for Meta (Facebook/Instagram), Google Ads, TikTok Ads, and YouTube Ads with Shopify event integrity, ROAS diagnostics, scale planning, and funnel optimization.
---

# Shopify Ads Helper

## Purpose
Core mission:
- Verify Shopify pixel and attribution status for conversion optimization readiness.
- Diagnose account structure and creative performance affecting ROAS.
- Recommend scaling route and budget increments.
- Improve landing page and conversion funnel outcomes.

## When To Trigger
Use this skill when the user asks for:
- Shopify ads troubleshooting
- OCPX readiness in Shopify stack
- ROAS fluctuation diagnosis in store campaigns
- checkout and funnel optimization

High-signal keywords:
- shopifyads, shop, ecommerce, checkout
- pixel, attribution, tracking, campaign
- roas, cpa, budget, scale, funnel

## Input Contract
Required:
- shopify_store_url
- tracking_stack_summary
- channel_performance_snapshot
- checkout_metrics

Optional:
- product_margin_data
- collection_level_performance
- creative_breakdown
- shipping_policy_context

## Output Contract
1. Shopify Tracking Health Summary
2. Channel and Structure Diagnosis
3. ROAS Volatility Interpretation
4. Scale Path with Budget Gates
5. Checkout and Funnel Optimization Plan

## Workflow
1. Validate Shopify event mapping consistency.
2. Confirm attribution alignment across channels.
3. Audit campaign architecture per product/collection.
4. Isolate ROAS drivers by audience/creative/offer.
5. Propose staged budget lift and funnel fixes.

## Decision Rules
- If checkout completion is weak, prioritize on-site fixes over spend expansion.
- If collection-level margins vary, apply differential bid and budget controls.
- If attribution mismatch is high, rely on blended and platform views in parallel.
- If shipping/offer changes happened recently, separate pre/post effects before action.

## Platform Notes
Primary scope:
- Shopify Ads ecosystem with Meta (Facebook/Instagram), Google Ads, TikTok Ads, YouTube Ads

Platform behavior guidance:
- Keep Shopify conversion events normalized before cross-platform optimization.
- Pair channel decisions with collection-level economics when available.

## Constraints And Guardrails
- Do not optimize on ROAS alone when margin is uneven across SKUs.
- Flag data-lag effects for short lookback windows.
- Keep budget changes incremental under attribution uncertainty.

## Failure Handling And Escalation
- If event schema is broken, return patch checklist and freeze scale actions.
- If Shopify app conflicts affect tracking, escalate with app inventory and event log.
- If billing or policy lock appears, route to platform owner with urgency level.

## Code Examples
### Shopify Event Mapping Check

    events:
      product_view: ViewContent
      add_to_cart: AddToCart
      checkout_start: InitiateCheckout
      order_paid: Purchase
    status: pass_with_warnings

### Budget Lift Gate

    if blended_roas >= 2.8 and checkout_cvr >= 2.2:
      increase_budget_pct: 15
    else:
      hold_budget: true

## Examples
### Example 1: Shopify ROAS drift
Input:
- ROAS unstable after theme update

Output focus:
- tracking validation
- cause isolation
- corrective actions

### Example 2: Collection scaling
Input:
- One collection outperforming others

Output focus:
- collection-level budget logic
- structure recommendations
- risk guardrails

### Example 3: Checkout drop
Input:
- Add-to-cart steady, purchase down

Output focus:
- checkout funnel fixes
- retargeting adjustment
- measurement checks

## Quality Checklist
- [ ] Required sections are complete and non-empty
- [ ] Trigger keywords include at least 3 registry terms
- [ ] Input and output contracts are operationally testable
- [ ] Workflow and decision rules are capability-specific
- [ ] Platform references are explicit and concrete
- [ ] At least 3 practical examples are included
