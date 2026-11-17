---
name: us-sales-tax-precheck
display_name: US Sales Tax Pre-Check
description: "US sales tax pre-check for cross-border sellers. Upload draft sales data and platform statements to check six high-frequency error categories: rate & sourcing, nexus, marketplace facilitator coverage, taxability & exemptions, filing frequency, shipping & refunds — outputs a structured risk report. Trigger words: US sales tax pre-check, sales tax check, economic nexus, Wayfair."
category: productivity
version: 0.1.0
author: snow
allowed-tools: ""
---

# US Sales Tax Pre-Check

## Red Lines
- Pre-check only, never filing. Passing the pre-check ≠ compliance.
- Never generate official returns or registration documents.
- When information is insufficient, state "cannot determine" — do not guess.
- Do not request API keys, passwords, or network access.

## Step 1 — Information Collection
Collect in one pass: 1) sales channels (Amazon / Walmart / eBay / Etsy / own website); 2) states sold into + rough per-state annual sales; 3) current state registrations and assigned filing frequencies; 4) product types (general / clothing / food / supplements / digital); 5) inventory locations (FBA / 3PL warehouses); 6) B2B sales with or without exemption certificates; 7) whether platforms already collect & remit on your marketplace sales. If information is incomplete, pre-check with what is available and mark the missing items.

## Step 2 — Item-by-Item Pre-Check
Check against `references/rule-table.md` and `references/deadlines.md`:
A. Rate & sourcing: destination-based combined state+local rates applied; district taxes not missed; origin-based sourcing used only where the state's intrastate rules require it.
B. Nexus: economic nexus thresholds crossed without registration ($100k in most states; $500k in CA/TX; NY $500k AND 100 transactions); FBA/3PL inventory creating physical nexus in storage states.
C. Marketplace facilitator coverage: all 45 sales-tax states + DC have facilitator laws — platforms collect on marketplace sales; flag treating own-website sales as platform-covered, or double-collecting on marketplace sales.
D. Taxability & exemptions: state-specific rules (e.g. clothing exempt in PA/NJ; NY exemption under $110); B2B sales without valid resale/exemption certificates → seller bears the tax.
E. Frequency & deadlines: filing frequency matches the state assignment for the volume; zero-returns still required — missed zero-return → penalty; most deadlines the 20th (CA monthly: last day of month).
F. Shipping & refunds: shipping charges taxed where the state requires (taxable in many states when the goods are taxable); refunds must return the collected tax.

## Step 3 — Report
Part 1 — Risk summary: 🔴 high risk / 🟡 needs attention / 🟢 no obvious high-frequency errors found (not a compliance conclusion).
Part 2 — Table: check item | finding | risk level | basis | recommended action. 🔴 = estimated correction cost >$2,000 or permit/audit exposure; 🟡 = $500–2,000; 🟢 = no anomaly found (not a compliance conclusion).
Part 3 — Next steps: 1–3 prioritized actions; where back-filing or registration is involved, note "confirm with your US sales tax advisor."

## Step 4 — Follow-Ups
Expand only on already-checked items. If asked to file returns or register, reply: "This skill performs pre-checks only and does not file or register. Please hand the report to your tax advisor."

---
Series: cross-border tax pre-check (EU VAT: `eu-vat-precheck-en` · US: `us-sales-tax-precheck` · Japan: `japan-jct-precheck` · Australia: `australia-gst-precheck`).
