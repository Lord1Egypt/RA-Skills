---
name: supplier-sync-manager
description: Build a supplier sync control brief for inventory, catalog, pricing, order-handoff, and onboarding workflows. Use when a team needs to spot mapping gaps, latency risks, or supplier-data exceptions before they spread across ERP, WMS, OMS, or marketplace channels.
---

# Supplier Sync Manager

## Overview

Supplier Sync Manager turns a short operations prompt into a practical control brief for supplier-to-system synchronization work.
It is useful when you need a fast operating view of sync scope, likely failure themes, control questions, and exception ownership.

## Use this skill when

- inventory or availability updates are lagging across supplier feeds and internal systems
- catalog, SKU, pack-size, or pricing mappings look inconsistent
- order, shipment, or fulfillment events are duplicating, missing, or drifting between systems
- a new supplier onboarding, file template rollout, or cutover needs a risk checklist
- the team needs a concise exception-management brief instead of a raw troubleshooting dump

## What the skill does

The handler reads the prompt, infers likely context, and produces a structured brief with:

1. **Primary sync objective** such as inventory synchronization, catalog and pricing alignment, order handoff, onboarding, or exception review
2. **Operating cadence** such as real-time, daily, weekly, or launch preparation
3. **Systems referenced** including ERP, WMS, OMS, PIM, marketplace/storefront, or supplier portal workflows
4. **Priority risk themes** such as SKU mapping mismatch, inventory latency, price mismatch, pack-size confusion, duplicate events, or supplier SLA drift
5. **Control recommendations** covering first-check questions, default responses, watchlists, exception-queue design, and assumptions

## Recommended input patterns

Use plain language. Helpful details include:

- sync objective or pain point
- cadence or business timing
- systems involved
- known discrepancies or failure symptoms
- whether the need is daily operations, launch readiness, or post-incident review

Example prompts:

- `Need daily inventory sync between supplier feed and ERP to avoid stock lag.`
- `Review duplicate order retries and shipment tracking gaps in the OMS handoff.`
- `Prepare a launch cutover plan for catalog mapping and supplier onboarding.`
- `Our ERP, WMS, and Shopify storefront show price mismatch and pack size mapping issues.`

## Output shape

The skill returns a markdown brief with sections such as:

- Sync Scope Summary
- Recommended Control Table
- Field Mapping Watchlist
- Cadence Notes
- Exception Queue Design
- Assumptions and Limits

## Boundaries

- This skill is heuristic. It does not query live ERP, WMS, OMS, marketplace, or supplier APIs.
- It helps frame operational controls and investigation priorities, not replace production monitoring or master-data governance.
- Final reruns, field changes, SLA decisions, and supplier escalations should remain human-approved.
