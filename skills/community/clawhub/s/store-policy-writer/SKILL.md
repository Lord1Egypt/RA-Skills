---
name: Store Policy Writer
description: Generate clear, professional, business-specific ecommerce store policies (returns, shipping, privacy, terms of service).
---

# Store Policy Writer

## Introduction

Every ecommerce store needs clear policies to build buyer trust, cut support tickets, and meet platform and legal requirements — yet most stores either copy a generic template that doesn't match how they actually operate, or write something vague that creates disputes later. This skill generates complete, ready-to-publish store policies tailored to a specific business model, product types, fulfillment methods, and target markets: returns and refunds, shipping and delivery, privacy and data handling, and terms of service.

Policies are written in plain, customer-friendly language while still being precise about the things that cause disputes: who pays return shipping, how long refunds take, what counts as a valid return, and how customer data is handled. Each policy reflects the seller's real operations rather than boilerplate, so it is accurate and defensible.

> **Not legal advice.** This skill produces strong first-draft operational policies based on the inputs provided. For regulated products, cross-border tax/consumer-law obligations, or high-risk categories, the output should be reviewed by a qualified attorney before publishing.

## Quick Reference

| Decision | Strong | Acceptable | Weak |
|---|---|---|---|
| Return window | Specific number of days + start trigger (delivery date) | "30 days" with no start point | "Reasonable time" / unstated |
| Who pays return shipping | Stated per scenario (defect vs change-of-mind) | One blanket rule | Silent — guaranteed disputes |
| Refund timing | Method + business-day range ("5–10 business days to original payment") | "Promptly" | Unstated |
| Privacy scope | Names data collected, purpose, third parties, user rights | Generic "we value privacy" | Copied from unrelated store |
| Tone | Plain language, second person, scannable | Slightly formal | Dense legalese buyers won't read |
| Marketplace fit | Aligned to the platform's buyer-protection rules | Generic web-store policy | Conflicts with platform terms |
| Exclusions | Clear, fair, itemized (final-sale, hygiene items) | A few listed | Hidden or overly broad |
| Contact path | Named channel + response-time expectation | Email only | None |

## What this skill solves

- **Generic-template mismatch** — policies that describe a business that isn't yours (wrong return window, wrong carriers, wrong jurisdictions).
- **Dispute-prone ambiguity** — silence on return shipping cost, refund timing, or condition requirements, which is where most chargebacks and complaints start.
- **Launch blockers** — a new Shopify/WooCommerce store can't go live without the required legal pages.
- **Marketplace onboarding friction** — Amazon, TikTok Shop, and Shopee each demand policies that meet their buyer-protection standards.
- **Compliance gaps** — privacy policies that ignore GDPR/CCPA disclosure expectations for stores serving EU/California shoppers.
- **Inconsistent voice** — four policies that read like they came from four different companies.
- **Overly harsh or overly loose terms** — exclusions so broad they violate consumer law, or so loose they invite abuse.

## Workflow

1. **Collect business facts.** Confirm required inputs: `business_name`, `product_types`, fulfillment method(s), shipping origin and destination markets, and which policies are needed. Note any regulated categories (food, cosmetics, electronics, supplements).

2. **Map operational reality.** For each policy, capture the real numbers: actual return window, who pays return shipping in each scenario, processing time, carriers, refund method and timing. Policies must describe what the business actually does. See `references/policy-clause-library.md`.

3. **Determine compliance surface.** Identify the jurisdictions and platforms in play and pull the relevant disclosure requirements (GDPR, CCPA, distance-selling/cooling-off rules, marketplace buyer protection). See `references/compliance-reference.md`.

4. **Draft each policy** in the structure from `references/output-template.md`, in plain second-person language, with scannable headings and concrete numbers instead of vague phrases.

5. **Set fair, itemized exclusions.** List final-sale, hygiene, custom, and perishable exclusions explicitly; avoid blanket exclusions that conflict with consumer law.

6. **Add the operational glue.** Contact channel, response-time expectation, effective date, and how changes will be communicated.

7. **Run the quality gate** in `assets/quality-checklist.md`, then flag anything that needs attorney review (regulated products, cross-border tax, warranties).

## Inputs

- **business_name (required):** Exactly as it should appear in documents. Example: "Horizon Outdoor Co."
- **product_types (required):** Categories sold, since they drive returns rules and exclusions. Example: "camping gear and apparel; some perishable trail food."
- **fulfillment_method (required):** Self-fulfilled, 3PL, dropship, or marketplace-fulfilled — affects shipping/return logistics and timelines.
- **markets (required):** Where customers and the business are located (e.g. "US + EU + UK"), which determines compliance scope.
- **policies_needed (optional):** Subset of returns/refunds, shipping, privacy, terms. Defaults to all four.
- **brand_voice (optional):** Formal, friendly, or minimal. Defaults to plain and friendly.

## Worked example 1 — Returns & Refunds (Shopify apparel brand)

**Brief:** "Maple & Pine," self-fulfilled US apparel store, also ships to Canada, friendly voice.

**Generated policy (excerpt):**
> **Returns**
> You can return most items within **30 days of delivery** for a refund or exchange. Items must be unworn, unwashed, and have original tags attached.
> **Who pays shipping:** If the item is defective or we made an error, we cover return shipping. For change-of-mind returns, return shipping is **$6.95**, deducted from your refund.
> **Refunds:** Once we receive and inspect your return, we issue your refund to the original payment method within **5–7 business days**. Your bank may take a few extra days to post it.
> **Exclusions:** Final-sale items (marked at checkout), underwear, and pierced jewelry can't be returned for hygiene reasons.
> **How to start:** Email returns@mapleandpine.com with your order number and we'll send a prepaid label or instructions within 1 business day.

**Why it works:** every dispute trigger (window, condition, who pays, timing, exclusions, contact) is answered with a specific number or named channel.

## Worked example 2 — Privacy Policy (store serving US + EU)

**Brief:** "Lumen Skincare," ships US + EU, runs Meta/Google ads and email marketing.

**Generated policy (excerpt):**
> **What we collect:** contact and shipping details you provide at checkout; order history; and device/usage data via cookies and analytics.
> **Why:** to fulfill orders, provide support, prevent fraud, and — with your consent — send marketing.
> **Sharing:** with payment processors, shipping carriers, and analytics/advertising partners (e.g. Meta, Google) acting as processors. We do not sell your personal information.
> **Your rights:** EU/UK shoppers may access, correct, port, or delete their data and object to processing (GDPR). California residents have access/deletion/opt-out rights (CCPA/CPRA). Email privacy@lumenskincare.com to exercise them.
> **Cookies:** a banner lets EU/UK visitors accept or reject non-essential cookies before they load.

**Why it works:** it names the actual data flows and ad partners and maps concrete rights to the markets served, instead of generic privacy reassurance.

## Common mistakes

1. **Vague return windows.** "Reasonable time" or no start trigger invites disputes. State days and the start point (delivery date).
2. **Silence on return shipping cost.** The #1 source of return complaints. Specify who pays in each scenario.
3. **Unstated refund timing.** Always give a business-day range and the destination (original payment method).
4. **Copy-paste privacy policies.** A policy naming Stripe when you use PayPal, or omitting your real ad partners, is inaccurate and non-compliant.
5. **Ignoring the destination markets.** Selling to the EU/UK without acknowledging cooling-off and GDPR rights creates legal exposure.
6. **Over-broad exclusions.** "All sales final" often conflicts with consumer-protection law and erodes trust.
7. **Legalese no one reads.** Dense terms increase tickets. Write plainly; reserve formal language for genuine liability clauses.
8. **Policies that contradict the marketplace.** A store policy stricter than Amazon/TikTok Shop buyer protection won't be honored and looks bad.
9. **No effective date or change process.** Undated policies look stale and are hard to enforce.
10. **Treating output as final legal advice.** Flag regulated products and cross-border tax/warranty issues for attorney review.

## Resources

- `references/output-template.md` — the document structure for each of the four policies.
- `references/policy-clause-library.md` — reusable, fill-in clauses for windows, shipping, refunds, exclusions, and contact.
- `references/compliance-reference.md` — GDPR/CCPA, cooling-off, and marketplace buyer-protection requirements by region/platform.
- `assets/quality-checklist.md` — pre-publish quality and compliance gate.
