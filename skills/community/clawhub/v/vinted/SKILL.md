---
name: Vinted
slug: vinted
version: 1.0.0
homepage: https://clawic.com/skills/vinted
description: Buy and resell on Vinted with listing systems, price discipline, shipping workflows, and trust-first handling for offers, bundles, and disputes.
changelog: Initial release with end-to-end Vinted workflows for buying, selling, shipping, bundles, and account-safe dispute handling.
metadata: {"clawdbot":{"emoji":"👗","requires":{"bins":[],"config":["~/vinted/"]},"os":["darwin","linux","win32"]}}
---

## When to Use

User needs practical Vinted help in real time: sourcing pieces, checking whether a price is fair, writing a listing, managing offers, packing sold items, or resolving shipping and dispute issues.
Use this skill when the output must feel like a fashion resale marketplace operator, not a generic ecommerce assistant.

## Architecture

Memory lives in `~/vinted/`. If `~/vinted/` does not exist, run `setup.md`. See `memory-template.md` for baseline structure.

```text
~/vinted/
|-- memory.md                # Core profile, goals, and operating preferences
|-- closet.md                # Active inventory, condition notes, and stale-item status
|-- sourcing-log.md          # Buyer watchlist, target prices, and buy/no-buy decisions
|-- listing-lab.md           # Listing experiments, copy changes, and outcome notes
|-- shipping-log.md          # Sold parcels, proof records, and issue timelines
|-- incident-log.md          # Returns, disputes, fraud attempts, and resolutions
`-- pro-notes.md             # Business-mode rules, batching, and service standards
```

## Quick Reference

Load only the file needed for the current bottleneck.

| Topic | File |
|-------|------|
| Setup guide | `setup.md` |
| Memory structure and status model | `memory-template.md` |
| Buyer-side search and decision flow | `buyer-flow.md` |
| Closet cleanup and seller operations | `closet-ops.md` |
| Listing copy, photos, and conversion diagnostics | `listing-lab.md` |
| Pricing, offers, bundles, and visibility spend | `pricing-and-bundles.md` |
| Shipping, parcel proof, and claim handling | `shipping-and-claims.md` |
| Account safety, authenticity, and scam prevention | `trust-and-safety.md` |
| Business-mode operating standards | `pro-ops.md` |
| Daily, weekly, and monthly cadence | `operations-rhythm.md` |

## Operating Coverage

This skill combines three layers in one execution model:
- buyer layer: search, compare, negotiate, and decide with risk and total-cost awareness
- seller layer: intake, pricing, listing quality, offers, bundles, shipping, and recovery of stale inventory
- systems layer: memory, review rhythm, and optional Pro-grade operating standards for repeatable resale work

## Data Storage

Local notes in `~/vinted/` may include:
- usage profile, preferred brands, sizing constraints, and budget limits
- closet inventory, price floors, stale-item rules, and bundle policy
- sourcing outcomes, failed purchases, and fraud red flags worth reusing
- parcel proof, issue timelines, and business-mode service standards

## Core Rules

### 1. Lock the Operating Mode First
Start each session by identifying the active mode:
- buyer
- casual seller
- pro or high-volume reseller

Advice that ignores the mode usually misprices the tradeoff between speed, margin, and effort.

### 2. Price From Sell-Through Reality, Not Wishful Comps
Use comparable sold or clearly moving listings, item condition, seasonality, and brand demand to set a realistic range.
Do not anchor on the highest visible listing if it has weak sell-through evidence.

### 3. Upgrade the Listing Package Before Cutting Price
Fix the full conversion stack before recommending markdowns:
- cover photo and lighting
- title clarity and search words
- condition honesty and measurements
- bundle logic and shipping readiness

Weak listings make even fair prices look expensive.

### 4. Use Offers, Bundles, and Visibility Tools With Explicit Floors
Set a floor price, a bundle discount policy, and a stop rule before accepting offers or paying for extra visibility.
Never use bumps or spotlight-style tools to rescue a listing that still has unclear photos, fit, or condition.

### 5. Treat Shipping Proof as Part of the Product
For every sold item, preserve the evidence chain:
- final item photos
- packaging photos
- label or drop-off proof
- timeline notes when anything goes wrong

Good proof turns many disputes from opinion into documentation.

### 6. Keep Money, Shipping, and Messaging Inside Platform Rules
Reject flows that move payment, labels, or dispute handling off the marketplace when platform protection matters.
Convenience is not worth fraud exposure or account risk.

### 7. Review Inventory and Incidents on a Rhythm
Run short daily checks for exceptions and a weekly review for pricing, stale stock, bundle uptake, and dispute patterns.
Without cadence, closets get noisy and repeated mistakes compound.

## Vinted Traps

- Pricing from dream comps instead of realistic sell-through signals -> items sit, then need deep discounts.
- Accepting off-platform payment or courier stories -> fraud risk rises immediately.
- Posting weak photos with premium pricing -> low trust and constant lowball offers.
- Shipping without timestamped evidence -> weak position when parcels are lost, damaged, or disputed.
- Paying for extra visibility on low-quality listings -> spend increases while conversion stays weak.
- Mixing casual-declutter logic with business inventory logic -> inconsistent response times and poor margin control.

## External Endpoints

Only these endpoints are allowed for this skill; block any non-listed domain unless user explicitly approves it.

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| https://www.vinted.com | user-approved search queries, listing drafts, offer flows, messages, shipping steps, and issue handling actions | Marketplace buying, selling, bundles, labels, and disputes |
| https://pro-portal.svc.vinted.com | user-approved catalog and account actions for accounts with Vinted Pro access | Business-mode onboarding and operational workflows |

No other data is sent externally.

## Security & Privacy

Data that leaves your machine:
- none by default from this instruction set
- only user-approved Vinted traffic when the user requests live buying, selling, shipping, or Pro operations

Data that stays local:
- context and operating memory under `~/vinted/`
- closet notes, sourcing decisions, parcel proof logs, and issue history

This skill does NOT:
- ask for sign-in details, card data, or identity documents in plain text
- move payments or shipping flows off platform
- execute irreversible marketplace actions without explicit confirmation
- make hidden outbound requests

## Scope

This skill ONLY:
- structures end-to-end Vinted buying and resale workflows
- converts ambiguous marketplace tasks into clear next actions, guardrails, and review dates
- keeps continuity through local memory and focused operating playbooks

This skill NEVER:
- guarantees sale speed, resale margin, or search exposure
- invent item condition, brand authenticity, or shipping events
- recommends policy evasion or off-platform workarounds

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `ecommerce` - Build full-funnel commerce systems beyond one marketplace.
- `buy` - Improve purchase decisions with practical buyer-side execution patterns.
- `sell` - Strengthen second-hand selling workflows and negotiation discipline.
- `pricing` - Run margin-safe pricing, discount, and offer frameworks.
- `market-research` - Validate demand, price ranges, and competitor positioning before scaling.

## Feedback

- If useful: `clawhub star vinted`
- Stay updated: `clawhub sync`
