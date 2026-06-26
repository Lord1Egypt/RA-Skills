---
name: sales-ads-helper
description: Parse client URLs and requirements to generate ad proposals, ROI estimates, persuasion logic, and CRM-based close probability forecasting for Meta (Facebook/Instagram), Google Ads, TikTok Ads, YouTube Ads, Amazon Ads, and Shopify Ads services.
---

# Sales Helper

## Purpose
Core mission:
- Convert customer URL and needs into a launch proposal and ROI estimate.
- Output persuasion strategy and closing logic.
- Predict close probability and cash collection cycle using CRM signals.
- Generate sales daily follow-up and retrospective reports.

## When To Trigger
Use this skill when the user asks for:
- proposal drafting for ads services
- ROI estimate for prospect conversion
- close strategy for uncertain deals
- daily sales report or follow-up summary

High-signal keywords:
- sales, sell, closer, leads, customers
- ads, campaign, roi, roas, cpa
- report, dashboard, revenue, acquire

## Input Contract
Required:
- prospect_url
- prospect_need_summary
- proposed_service_scope
- crm_stage_data

Optional:
- historical_win_rate
- contract_terms
- payment_terms
- competitor_quote

## Output Contract
1. Proposal Summary (scope + value)
2. ROI Estimate (assumptions + model)
3. Persuasion and Objection Strategy
4. Close Probability and Collection Cycle Forecast
5. Sales Daily/Follow-up/Retrospective Template

## Workflow
1. Parse URL and infer business model.
2. Map pain points to ads service package.
3. Build ROI estimate with explicit assumptions.
4. Choose persuasion path by decision-maker type.
5. Score deal probability from CRM stage features.
6. Output follow-up and close action list.

## Decision Rules
- If prospect urgency is high, prioritize short pilot with rapid proof plan.
- If budget concern dominates, lead with staged scope and downside protection.
- If close probability is low, prescribe information-gathering steps before pushing deal.
- If payment risk is high, optimize term structure before scaling scope.

## Platform Notes
Primary scope:
- Meta (Facebook/Instagram), Google Ads, TikTok Ads, YouTube Ads, Amazon Ads, Shopify Ads

Platform behavior guidance:
- Proposals should tie channel choice to measurable business outcome.
- Keep ROI model channel-aware, not one blended black-box number.

## Constraints And Guardrails
- Never fabricate past case studies or performance numbers.
- Keep ROI estimates assumption-driven and auditable.
- Separate sales narrative from guaranteed delivery claims.

## Failure Handling And Escalation
- If CRM stage data is missing, return low-confidence range and required fields.
- If industry fit is unclear, provide two candidate proposal paths with data needed.
- If legal/payment constraints block close, escalate to human commercial owner.

## Code Examples
### ROI Estimate Payload

    {
      "service_fee": 12000,
      "planned_spend": 50000,
      "assumed_roas": 2.4,
      "projected_revenue": 120000,
      "gross_profit_estimate": 36000
    }

### Close Probability Formula

    close_score = stage_weight + urgency_score + budget_fit + stakeholder_alignment
    if close_score >= 75: close_probability = "high"

## Examples
### Example 1: New inbound lead
Input:
- URL submitted + basic requirement

Output focus:
- first proposal draft
- ROI estimate range
- next follow-up question

### Example 2: Stalled opportunity
Input:
- Deal stuck in negotiation
- Objection: ROI uncertainty

Output focus:
- persuasion strategy
- revised offer structure
- close plan

### Example 3: Sales daily report
Input:
- CRM updates for 12 opportunities

Output focus:
- probability movement
- expected cash collection window
- rep action priorities

## Quality Checklist
- [ ] Required sections are complete and non-empty
- [ ] Trigger keywords include at least 3 registry terms
- [ ] Input and output contracts are operationally testable
- [ ] Workflow and decision rules are capability-specific
- [ ] Platform references are explicit and concrete
- [ ] At least 3 practical examples are included
