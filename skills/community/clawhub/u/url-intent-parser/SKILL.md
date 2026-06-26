---
name: url-intent-parser
description: Parse product and landing URLs into an executable ads brief for Meta (Facebook/Instagram), Google Ads, TikTok Ads, YouTube Ads, Amazon Ads, Shopify Ads, and DSP/programmatic.
---

# Ads URL Parser

## Purpose
Core mission:
- URL parsing, intent extraction, launch brief generation

This skill is specialized for advertising workflows and should output actionable plans rather than generic advice.

## When To Trigger
Use this skill when the user asks for:
- ad execution guidance tied to business outcomes
- growth decisions involving revenue, roas, cpa, or budget efficiency
- platform-level actions for: Meta (Facebook/Instagram), Google Ads, TikTok Ads, YouTube Ads, Amazon Ads, Shopify Ads, DSP/programmatic
- this specific capability: URL parsing, intent extraction, launch brief generation

High-signal keywords:
- ads, advertising, campaign, growth, revenue, profit
- roas, cpa, roi, budget, bidding, traffic, conversion, funnel
- meta, googleads, tiktokads, youtubeads, amazonads, shopifyads, dsp

## Input Contract
Required:
- url: product, service, or landing page URL
- business_goal: sales, leads, traffic, or awareness
- market_scope: country or language market

Optional:
- target_audience_hint
- offer_and_pricing
- launch_timeline
- current_kpi_baseline

## Output Contract
1. Intake Summary
2. Parsed Offer and Value Proposition
3. Audience and Funnel Hypothesis
4. Channel Recommendation with rationale
5. Launch Hand-off JSON payload

## Workflow
1. Validate URL and infer page type.
2. Extract offer, CTA, and conversion surface.
3. Map user intent to KPI priorities.
4. Draft initial funnel and channel hypothesis.
5. Emit structured launch brief.

## Decision Rules
- If URL is not reachable, request alternate URL and continue with available text.
- If checkout is present, prioritize conversion objective and remarketing.
- If product narrative is unclear, ask one focused clarification question.

## Platform Notes
Primary scope:
- Meta (Facebook/Instagram), Google Ads, TikTok Ads, YouTube Ads, Amazon Ads, Shopify Ads, DSP/programmatic

Platform behavior guidance:
- Keep recommendations channel-aware; do not collapse all channels into one generic plan.
- For Meta and TikTok Ads, prioritize creative testing cadence.
- For Google Ads and Amazon Ads, prioritize demand-capture and query/listing intent.
- For DSP/programmatic, prioritize audience control and frequency governance.

## Constraints And Guardrails
- Never fabricate metrics or policy outcomes.
- Separate observed facts from assumptions.
- Use measurable language for each proposed action.
- Include at least one rollback or stop-loss condition when spend risk exists.

## Failure Handling And Escalation
- If critical inputs are missing, ask for only the minimum required fields.
- If platform constraints conflict, show trade-offs and a safe default.
- If confidence is low, mark it explicitly and provide a validation checklist.
- If high-risk issues appear (policy, billing, tracking breakage), escalate with a structured handoff payload.

## Code Examples
### Parse Output Example

    {
      "objective": "sales",
      "primary_kpi": "roas",
      "recommended_channels": ["Meta", "TikTok Ads"],
      "core_offer": "Starter bundle with free shipping"
    }

### Launch Payload Example

    objective: sales
    budget_plan: test-then-scale
    tracking_required: [ViewContent, AddToCart, Purchase]

## Examples
### Example 1: Shopify product page intake
Input:
- URL: product page with direct checkout
- Goal: improve roas

Output focus:
- offer extraction
- funnel assumptions
- first channel recommendation

### Example 2: SaaS lead landing page intake
Input:
- URL: demo request page
- Goal: lower cpa for qualified leads

Output focus:
- lead funnel map
- conversion event definition
- channel split hypothesis

### Example 3: Amazon listing intake
Input:
- URL: marketplace product listing
- Goal: grow revenue while preserving margin

Output focus:
- listing intent clues
- ads objective mapping
- launch handoff payload

## Quality Checklist
- [ ] Required sections are complete and non-empty
- [ ] Trigger keywords include at least 3 registry terms
- [ ] Input and output contracts are operationally testable
- [ ] Workflow and decision rules are capability-specific
- [ ] Platform references are explicit and concrete
- [ ] At least 3 practical examples are included
