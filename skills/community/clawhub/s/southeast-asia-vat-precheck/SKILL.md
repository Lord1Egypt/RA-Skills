---
name: southeast-asia-vat-precheck
display_name: Southeast Asia VAT/GST Pre-Check
description: "Southeast Asia VAT/GST pre-check for cross-border sellers (Shopee, Lazada, TikTok Shop). Upload draft filing data and platform statements to check six high-frequency error categories: rate & category, registration thresholds, low-value goods rules, channel & stock model, filing frequency, pricing display & customs declaration — covering Singapore, Thailand, Indonesia, Philippines, Vietnam, Malaysia. Trigger words: SEA VAT pre-check, Southeast Asia tax, Shopee tax check, Lazada VAT."
category: productivity
version: 0.1.0
author: snow
allowed-tools: ""
---

# Southeast Asia VAT/GST Pre-Check

## Red Lines
- Pre-check only, never filing. Passing the pre-check ≠ compliance.
- Never generate official returns or registration documents.
- When information is insufficient, state "cannot determine" — do not guess. SEA rules change fast; references mark volatile items with "verify" — never assert those without user-provided confirmation.
- Do not request API keys, passwords, or network access.

## Step 1 — Information Collection
Collect in one pass: 1) countries sold into (SG / TH / ID / PH / VN / MY); 2) sales channels (Shopee / Lazada / TikTok Shop / own site); 3) per-country annual sales and global turnover; 4) typical order value (relative to each country's low-value threshold); 5) fulfillment model (cross-border direct shipping vs local warehouse); 6) registrations held (SG GST / MY SMK number / local entities); 7) who collects tax at checkout on each channel. If information is incomplete, pre-check with what is available and mark the missing items.

## Step 2 — Item-by-Item Pre-Check
Check against `references/rule-table.md` and `references/deadlines.md`:
A. Rate & category: correct per-country rate applied (SG 9% / TH 7% / ID 11% / PH 12% / VN 10% or reduced 8% / MY sales tax 5–10%); VN reduced-rate eligibility and MY category rates flagged when product type unknown.
B. Registration thresholds: SG overseas vendor regime (global >S$1M AND SG low-value sales >S$100k); MY LVG registration (MY LVG sales >RM500k/12mo); other countries have no offshore vendor registration for goods — flag if the user assumes otherwise.
C. Low-value goods rules: SG ≤S$400 (point-of-sale GST by vendor/marketplace); TH ≤฿1,500 (import VAT at customs since 2024-07); ID de minimis US$3; PH de minimis ₱10,000; VN de minimis abolished 2025-02 (verify current rule); MY ≤RM500 (10% at checkout by registered seller/platform). Flag charging at checkout where border-taxed, or vice versa.
D. Channel & stock model: cross-border direct shipping vs local warehouse — local stock triggers domestic registration obligations in every SEA country; marketplace vs own-site collection responsibility split per channel.
E. Filing frequency & deadlines: SG quarterly (1 month after period); TH monthly (15th / 23rd e-filing); ID monthly (end of following month); PH monthly 20th + quarterly 25th; VN monthly 20th or quarterly; MY LVG quarterly. Only applies where the seller is actually registered — unregistered → registration-risk finding instead.
F. Pricing display & customs declaration: SG GST-inclusive price display; undervaluation or shipment-splitting to stay under de minimis → flag (seizure + back-tax risk); declared values must match platform settlement data.

## Step 3 — Report
Part 1 — Risk summary: 🔴 high risk / 🟡 needs attention / 🟢 no obvious high-frequency errors found (not a compliance conclusion).
Part 2 — Table: check item | finding | risk level | basis | recommended action. 🔴 = estimated correction cost >US$2,000 or cargo/account exposure; 🟡 = US$500–2,000; 🟢 = no anomaly found (not a compliance conclusion).
Part 3 — Next steps: 1–3 prioritized actions; where registration or back-filing is involved, note "confirm with a local tax agent in the destination country."

## Step 4 — Follow-Ups
Expand only on already-checked items. If asked to file returns or register, reply: "This skill performs pre-checks only and does not file or register. Please hand the report to a local tax agent."

---
Series: cross-border tax pre-check (EU VAT: `eu-vat-precheck-en` · US: `us-sales-tax-precheck` · Japan: `japan-jct-precheck` · Australia: `australia-gst-precheck` · SEA: `southeast-asia-vat-precheck`).
