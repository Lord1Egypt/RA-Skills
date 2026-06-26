---
name: sales-proposal-simulator
description: Build persuasive sales proposals and close plans for ad services spanning Meta (Facebook/Instagram), Google Ads, TikTok Ads, YouTube Ads, Amazon Ads, and Shopify Ads.
---

# Ads Sales Proposal

## Purpose
Core mission:
- proposal architecture, objection handling, closing path

This skill is specialized for advertising workflows and should output actionable plans rather than generic advice.

## When To Trigger
Use this skill when the user asks for:
- ad execution guidance tied to business outcomes
- growth decisions involving revenue, roas, cpa, or budget efficiency
- platform-level actions for: Meta (Facebook/Instagram), Google Ads, TikTok Ads, YouTube Ads, Amazon Ads, Shopify Ads
- this specific capability: proposal architecture, objection handling, closing path

High-signal keywords:
- ads, advertising, campaign, growth, revenue, profit
- roas, cpa, roi, budget, bidding, traffic, conversion, funnel
- meta, googleads, tiktokads, youtubeads, amazonads, shopifyads, dsp

## Input Contract
Required:
- client_request: what the client wants to achieve
- business_context: product, margin, seasonality
- offer_scope: service package or campaign scope

Optional:
- objections
- competitor_reference
- contract_constraints
- expected_start_date

## Output Contract
1. Proposal Positioning
2. Scope and Deliverables
3. ROI Logic and KPI Commitment Range
4. Objection Handling Script
5. Close Plan with next steps

## Workflow
1. Summarize client objective and urgency.
2. Translate objective into measurable ad outcomes.
3. Build value argument and risk controls.
4. Prepare objection responses and confidence proof.
5. Output a close-ready proposal structure.

## Decision Rules
- If goal is vague, anchor on one north-star KPI first.
- If budget is low, propose phased pilot with strict milestone gates.
- If trust is low, lead with transparent assumptions and reporting cadence.

## Platform Notes
Primary scope:
- Meta (Facebook/Instagram), Google Ads, TikTok Ads, YouTube Ads, Amazon Ads, Shopify Ads

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
### Proposal Skeleton

    section: Objective
    section: Channel Plan
    section: Budget and KPI Range
    section: Risks and Mitigation
    section: Next-step Commitment

### Objection Response Map

    objection: "CPA too high"
    response: "Pilot 14 days with capped budget and clear stop-loss"

## Examples
### Example 1: Performance growth proposal
Input:
- Client wants lower CPA in 30 days
- Current channels: Meta + Google Ads

Output focus:
- pilot scope
- KPI promise range
- close checklist

### Example 2: New product launch proposal
Input:
- Client has no baseline data
- Wants global ads rollout

Output focus:
- phased contract scope
- risk clauses
- reporting cadence

### Example 3: Renewal negotiation proposal
Input:
- Existing client doubts ROI
- Needs proof before extension

Output focus:
- retrospective evidence summary
- revised operating model
- signed next-step plan

## Quality Checklist
- [ ] Required sections are complete and non-empty
- [ ] Trigger keywords include at least 3 registry terms
- [ ] Input and output contracts are operationally testable
- [ ] Workflow and decision rules are capability-specific
- [ ] Platform references are explicit and concrete
- [ ] At least 3 practical examples are included
