---
name: Walmart
slug: walmart
version: 1.0.1
homepage: https://clawic.com/skills/walmart
description: Plan Walmart grocery and household orders with pickup timing, substitutions, repeat restocks, and budget-aware cart decisions.
changelog: Added automation paths for browser-driven ordering, reorder workflows, live shopper coordination, and official Marketplace API boundaries.
metadata: {"clawdbot":{"emoji":"W","requires":{"bins":[]},"os":["darwin","linux","win32"],"configPaths":["~/walmart/"]}}
---

## Setup

On first use, read `setup.md` to capture activation boundaries, household scope, and store-specific preferences before planning repeat workflows.

## When to Use

Use this skill when the user is shopping at Walmart and needs more than generic product advice. It is for weekly grocery runs, household restocks, pickup or delivery coordination, substitution control, order recovery, and pharmacy-adjacent planning with strict safety limits.

## Architecture

Memory lives in `~/walmart/`. If `~/walmart/` does not exist, run `setup.md`. See `memory-template.md` for structure and status fields.

```text
~/walmart/
|-- memory.md           # Household profile, store preferences, and substitution rules
|-- weekly-cart.md      # Current basket with must-have vs optional items
|-- order-log.md        # Prior orders, missing items, and substitution outcomes
|-- exceptions.md       # Allergy, pharmacy, age-restricted, and never-substitute rules
`-- archive/            # Past carts and resolved delivery issues
```

## Quick Reference

Use the smallest relevant file for the current task.

| Topic | File |
|-------|------|
| Setup and activation boundaries | `setup.md` |
| Memory and file templates | `memory-template.md` |
| Weekly basket building | `basket-workflows.md` |
| Automation modes and execution paths | `automation-paths.md` |
| Substitution rules by category | `substitutions-playbook.md` |
| Missing items, damaged items, and split orders | `order-recovery.md` |
| Pharmacy and regulated-item safety | `pharmacy-safety.md` |

## Requirements

- For live ordering or account support: access to the user's Walmart site or app session
- For browser automation: a user-approved browser session and, only if the user wants apply mode, a user-provided browser automation runtime such as Playwright
- For repeat planning: permission to keep local notes in `~/walmart/`
- For pharmacy-related tasks: explicit user confirmation before any refill or account change workflow

Never ask the user to paste passwords, payment credentials, insurance details, or prescription identifiers into chat.

## Automation Scope

Use `automation-paths.md` before attempting any applied workflow.

- Official Walmart developer APIs found during research are Marketplace APIs for sellers and solution providers, not a public grocery or pickup API for ordinary consumer accounts.
- For consumer workflows, the reliable automation surface is browser-driven interaction with Walmart's own account flows such as `Purchase History`, `My Items`, checkout, order edit windows, and live-shopping support.
- Treat any consumer automation as user-mediated and confirmation-gated. Plan first, then review, then apply. Browser automation tooling is optional, not required for planning-only use.

## Core Rules

### 1. Start with Trip Mode and Deadline
- Classify the request first: weekly stock-up, urgent top-off, reorder, pickup tonight, delivery tomorrow, or account recovery.
- Confirm the needed-by window before recommending any basket changes because pickup slots, substitutions, and shipping splits depend on timing.

### 2. Build the Basket by Priority, Not by Aisle
- Structure every basket into `must-have`, `replaceable`, and `nice-to-have`.
- Put food, baby, pet, and cleaning staples first so the order still works if inventory changes late.

### 3. Treat Substitutions as a Policy
- Capture category-specific substitution rules before suggesting alternates.
- Never auto-approve substitutions for allergy-sensitive, baby, pet, pharmacy, or strongly preferred items.

### 4. Optimize for Value, Waste, and Reliability Together
- Compare unit value, pack size, spoilage risk, and reorder frequency instead of chasing the lowest sticker price.
- Prefer stable household outcomes over a technically cheaper basket that creates waste or extra trips.

### 5. Separate Grocery, General Merchandise, and Pharmacy Risk
- Expect mixed baskets to behave differently across pickup, delivery, shipping, and refill flows.
- Call out when an item is likely to ship separately, require ID, need cold-chain timing, or belong in a pharmacy-only workflow.

### 6. Never Execute High-Impact Actions Without Explicit Confirmation
- Require a clear user confirmation before placing orders, changing addresses, accepting substitutions, canceling items, or starting refill workflows.
- If live availability, pricing, or delivery windows may have changed, refresh that state before the final action.

### 7. Learn Only the Household Rules That Improve Repeat Orders
- Store only approved local notes in `~/walmart/`: store choice, pack size preferences, restock cadence, and substitution boundaries.
- Never store payment data, login secrets, insurance information, or detailed medical data.

### 8. Prefer Stable Walmart Surfaces for Automation
- For repeat ordering, start from `Account -> Purchase History -> Reorder all` or `My Items -> Reorder` before rebuilding carts manually.
- For live delivery issues, use `Chat with Shopper`, the order detail view, and documented edit windows before ad hoc browsing.

## Common Traps

- Treating Walmart like generic shopping search -> the user needed a workable household basket, not browsing help.
- Optimizing for discounts only -> cheaper items that break preferences, timing, or substitutions create extra trips and frustration.
- Leaving substitution rules vague -> allergy, baby, pet, and brand-sensitive items fail fast when inventory moves.
- Mixing shipping-only items into an urgent grocery plan without warning -> the order looks complete but arrives in pieces.
- Offering medication or dosage guidance -> pharmacy workflows need operational help, not medical advice.
- Pretending stock, pricing, or slot availability is stable -> Walmart states, substitutions, and pickup windows are live conditions.

## Data Storage

Keep local notes only in `~/walmart/`:
- household preferences, preferred store, and order-mode defaults
- repeat staple lists and reorder thresholds
- prior substitution outcomes and order recovery notes

Do not store card numbers, passwords, insurance identifiers, prescription numbers, or anything unrelated to improving repeat ordering.

## External Endpoints

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| https://www.walmart.com | Search terms, cart choices, account-selected order details, and order-management actions the user explicitly approves | Browse products, review carts, manage pickup, delivery, shipping, and order support |
| https://www.walmart.com/pharmacy | Refill or pharmacy-account metadata the user explicitly chooses to submit | Check pharmacy workflows, pickup status, and refill operations |
| https://developer.walmart.com/us-marketplace | Seller or solution-provider registration metadata and developer documentation activity | Marketplace API setup, docs, scopes, and sandbox guidance for seller-side integrations |
| https://marketplace.walmartapis.com | Marketplace OAuth and seller API payloads | Seller-side items, inventory, orders, pricing, returns, shipping, and reports |

No other data should be sent externally unless the user explicitly connects another service.

## Security & Privacy

Data that leaves your machine:
- only the Walmart requests required for browsing, cart review, order management, or pharmacy workflows that the user explicitly asked for

Data that stays local:
- household notes and approved workflow preferences in `~/walmart/`
- order recovery history and substitution guardrails

This skill does NOT:
- place or modify real orders without explicit user confirmation
- save payment credentials, passwords, or prescription identifiers in local memory
- provide medication, dosage, or interaction advice
- accept silent substitutions for sensitive categories
- modify its own skill files

## Trust

This skill relies on Walmart services for live browsing, ordering, and pharmacy workflows.
Only install and run it if you trust Walmart with the order and account data you choose to use there.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `shopping` - Broader shopping judgment for product research and purchase decisions outside Walmart.
- `price` - Deeper price timing, manipulation detection, and fair-value analysis.
- `meal-planner` - Weekly meal planning that can feed directly into Walmart grocery baskets.
- `family` - Household coordination, routines, and shared logistics around family needs.
- `subscriptions` - Repeat replenishment logic for recurring essentials and household services.

## Feedback

- If useful: `clawhub star walmart`
- Stay updated: `clawhub sync`
