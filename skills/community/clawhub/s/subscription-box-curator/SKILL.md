---
name: subscription-box-curator
description: Curate recurring subscription box concepts, item mixes, pricing tiers, add-on ideas, and replenishment warnings for DTC brands, merchandising teams, and subscription operators. Use when planning monthly or quarterly boxes, balancing persona fit, theme novelty, margin discipline, inventory constraints, and retention goals without live catalog APIs.
---

# Subscription Box Curator

## Overview

Use this skill to turn rough subscription-box inputs into a practical curation brief. It is designed for beauty boxes, snack boxes, pet boxes, hobby kits, wellness subscriptions, and book clubs.

This MVP is descriptive and template-based. It does **not** connect to Shopify, inventory systems, forecasting tools, or supplier APIs. It uses built-in heuristics to produce a markdown recommendation set that a merchandising or growth team can refine.

## Trigger

Use this skill when the user wants to:
- plan a monthly or quarterly subscription box
- reduce subscription churn through stronger curation logic
- generate seasonal themes and item architectures
- balance novelty, margin, replenishment, and fulfillment feasibility
- create add-on ideas, pricing tiers, or launch notes for a recurring box

### Example prompts
- "Help me plan a May self-care subscription box under $28 landed cost"
- "Our pet box retention is weak, suggest new monthly themes"
- "Create three snack-box concepts for students and young professionals"
- "We need a quarterly book box plan with upsells"

## Workflow

1. Collect the category, audience, budget, seasonality, and business goal.
2. Detect the likely box category and the strongest operating constraints.
3. Generate 3 theme directions with item architecture, rationale, and pricing guidance.
4. Add add-on ideas, replenishment watchouts, and practical next moves.
5. Present the result as a markdown planning brief.

## Inputs

The user can provide any mix of:
- subscription category or product type
- target audience or customer segments
- landed-cost target or budget range
- season, month, or campaign context
- inventory and shipping constraints
- churn, retention, launch, or margin goals
- feedback from prior boxes

## Outputs

Return a markdown brief with:
- executive summary
- input snapshot
- 3 recommended box concepts
- indicative cost and pricing guidance
- add-on and upsell ideas
- replenishment warnings and assumptions
- next-step actions for merchandising and launch planning

## Safety

- Do not claim access to real inventory, demand, supplier, or margin data.
- Keep recommendations advisory and assumption-based.
- Avoid hard promises about retention uplift, sell-through, or forecast accuracy.
- Flag missing data when the user does not provide category, budget, or customer details.

## Examples

### Example 1
Input: beauty subscription, May launch, $28 landed-cost target, young professionals, retention focus.

Output: three self-care theme directions, recommended hero/staple/surprise mix, suggested sell-price bands, and replenishment cautions for consumable SKUs.

### Example 2
Input: pet subscription with churn concerns.

Output: rotating play + treat + care concepts, persona-fit notes, and add-on ideas that increase perceived freshness without overcomplicating fulfillment.

## Acceptance Criteria

- Return markdown text, not a vague chat-only answer.
- Produce at least 3 concept options.
- Include both merchandising rationale and operational caveats.
- Clearly state that the result is heuristic and non-API-based.
