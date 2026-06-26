---
name: return-reason-miner
description: Analyze product return or refund notes and turn them into a structured reason taxonomy, root-cause view, and fix-priority brief. Use when a team needs to understand return drivers, separate product versus operations issues, or plan cross-functional remediation without live OMS, WMS, ERP, or BI access.
---

# Return Reason Miner

## Overview

Use this skill to convert messy return notes into a reason-based operating brief. It helps cluster return causes, identify likely root causes, suggest fix priorities, and frame what product, operations, CX, or merchandising teams should review next.

This MVP is heuristic. It does **not** connect to live order systems, warehouse systems, review platforms, or return portals. It relies on the user's provided return notes, product context, and issue patterns.

## Trigger

Use this skill when the user wants to:
- classify why products are being returned or refunded
- separate quality, fit, expectation, shipping, and fulfillment-related return drivers
- create a weekly or launch-period return review brief
- find likely cross-functional fixes instead of only counting return volume
- summarize rough return notes into a clear action plan

### Example prompts

- "Help me analyze our top return reasons for apparel"
- "Turn these refund notes into a root-cause brief"
- "What should product and ops teams look at if late delivery and wrong items are rising?"
- "Create a weekly return reason summary for our beauty line"

## Workflow

1. Capture the review mode, product context, and return evidence.
2. Choose the likely reason clusters and root-cause hypotheses.
3. Separate product issues from merchandising, fulfillment, and service issues.
4. Prioritize fixes by recurrence, severity, and controllability.
5. Return a markdown return-reason brief with cross-functional actions.

## Inputs

The user can provide any mix of:
- return notes, refund summaries, or customer feedback excerpts
- product context such as apparel, beauty, electronics, home goods, or food
- order, fulfillment, packaging, quality, sizing, and expectation notes
- launch period, promo period, or seasonal context
- any known operational changes such as new vendor, warehouse shift, or policy change

## Outputs

Return a markdown brief with:
- return pattern summary
- reason taxonomy table
- root-cause hypotheses
- fix priorities
- cross-functional action plan
- assumptions and limits

## Safety

- Do not claim access to live order, warehouse, or return systems.
- Treat root causes as hypotheses unless the evidence is strong and repeated.
- Do not fabricate percentages, defect rates, or financial impact.
- Final product, vendor, packaging, and policy decisions remain human-approved.

## Best-fit Scenarios

- ecommerce teams running weekly return or refund reviews
- operators trying to cut preventable returns without overreacting to noise
- product and CX teams needing a shared root-cause frame

## Not Ideal For

- automated returns processing or refund execution
- regulated product quality investigations that need formal QA evidence
- precise financial modeling of returns without structured data

## Acceptance Criteria

- Return markdown text.
- Include taxonomy, root-cause, action, and limits sections.
- Keep the heuristic framing explicit.
- Make the output practical for product, ops, and CX owners.
