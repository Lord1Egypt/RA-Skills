---
name: shipping-cost-optimizer
description: Analyze ecommerce fulfillment notes across weight, volume, packaging, region, carrier pricing, and free-shipping policy, then turn rough order-cost data into a prioritized shipping cost reduction plan. Use when operators, warehouse managers, or founders need logistics cost guidance without live TMS, carrier, or ERP integrations.
---

# Shipping Cost Optimizer

## Overview

Use this skill to convert order-cost notes, packaging specs, carrier rules, and free-shipping policies into a practical logistics cost brief. It is designed for operators who need to reduce fulfillment waste without losing control of delivery experience.

This MVP is heuristic. It does **not** connect to live TMS, carrier dashboards, ERP systems, or parcel tracking feeds. It relies on the user's exported cost notes, rate summaries, and operational context.

## Trigger

Use this skill when the user wants to:
- find the biggest sources of shipping-cost waste
- compare packaging, carrier-routing, threshold, or regional-profitability options
- understand whether free-shipping policy is eroding margin too aggressively
- prepare a logistics cost review for ops, warehouse, finance, or leadership
- turn rough freight and packaging notes into a prioritized test plan

### Example prompts
- "Where are we wasting the most money on shipping?"
- "Review packaging and carrier options for our store"
- "Should we raise the free-shipping threshold?"
- "Create a shipping cost reduction brief from these order notes"

## Workflow
1. Capture the main tension, such as packaging waste, routing logic, threshold design, or regional loss-making orders.
2. Normalize the likely cost signals: weight, volume, packaging, region, carrier pricing, and surcharge behavior.
3. Separate cost reduction ideas into quick wins versus cross-functional projects.
4. Attach each idea to business impact, delivery-experience risk, and implementation difficulty.
5. Return a markdown shipping-cost report with opportunities, pilot recommendations, and limits.

## Inputs
The user can provide any mix of:
- order weight and dimensional notes
- packaging or carton specifications
- carrier pricing or routing notes
- regional mix, remote-surcharge notes, or loss-making zones
- free-shipping thresholds or promotional shipping rules
- brand, speed, damage, or unboxing constraints

## Outputs
Return a markdown report with:
- a cost snapshot
- prioritized optimization opportunities
- quick wins versus longer projects
- experience and risk notes
- assumptions and limits

## Safety
- Do not claim access to live TMS, carrier dashboards, or ERP systems.
- Keep carrier changes, policy changes, and packaging changes human-approved.
- Do not recommend cost cuts that ignore damage, speed, or premium-brand experience.
- Downgrade certainty when rate cards or regional cost data are incomplete.

## Best-fit Scenarios
- ecommerce shipping-cost reviews
- free-shipping threshold and packaging audits
- warehouse, ops, finance, and founder discussions about fulfillment margin
- businesses that need a practical first-pass logistics brief before deeper analysis

## Not Ideal For
- real-time carrier routing automation
- parcel tracking or delivery exception handling
- highly specialized cross-border compliance design
- teams with no order-cost or shipping-logic visibility at all

## Acceptance Criteria
- Return markdown text.
- Include cost snapshot, opportunity table, pilot plan, and risk notes.
- Distinguish quick wins from longer efforts.
- Keep the brief practical for ops, warehouse, and finance stakeholders.
