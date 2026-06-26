---
name: spillover-estimator
description: Estimate whether one commerce channel is creating measurable spillover into another channel using simple exports, campaign timing, and directional evidence. Use when the user wants to know whether TikTok, creator activity, paid traffic, or marketplace growth is lifting Amazon, DTC, or other downstream channels.
---

# Spillover Estimator

Estimate cross-channel spillover without pretending to prove perfect attribution.

## Skill Card

- **Category:** Measurement
- **Core problem:** Did growth in one channel also lift another channel?
- **Best for:** Operators comparing TikTok, Amazon, DTC, creator, paid, and marketplace channel effects
- **Expected input:** Source channel data + downstream channel data + timing context
- **Expected output:** Directional spillover estimate + confidence note + action recommendation
- **Creatop handoff:** Feed findings into budget allocation and channel planning

## Before you run

Ask the user to clarify:
- source channel to evaluate
- downstream channel(s) to check for spillover
- date range
- major campaign or promo dates
- whether they have exports, screenshots, or CSV data

If structured data is missing, say the result will be **directional**, not causal proof.

## Optional tools / APIs

Useful but not required:
- Shopify / WooCommerce export
- Amazon sales export
- TikTok Shop export
- ad platform export
- Google Sheets / CSV

If the user does not have APIs connected, ask for manual exports first instead of blocking the workflow.

## Workflow

1. Confirm channel scope and time window.
2. Collect source-channel change signals.
3. Collect downstream-channel change signals.
4. Align timing around campaigns, creator drops, content bursts, or promo windows.
5. Judge whether the downstream lift looks:
   - likely related
   - weak / mixed
   - insufficient evidence
6. Explain the estimate with honest caveats.

## Output format

Return in this order:
1. Executive summary
2. Spillover estimate
3. Evidence blocks
4. Confidence and caveats
5. Recommended next step

## Fallback mode

If the user only has weekly snapshots, rough screenshots, or partial exports:
- use simple directional comparison
- do not claim causal attribution
- clearly label missing data and confidence limits

## Quality rules

- Never overclaim causality from timing alone.
- Prefer directional clarity over fake precision.
- Separate channel correlation from verified lift.
- Make the user’s next measurement step obvious.

## License

Copyright (c) 2026 **Razestar**.

This skill is provided under **CC BY-NC-SA 4.0** for non-commercial use.
You may reuse and adapt it with attribution to Razestar, and share derivatives
under the same license.

Commercial use requires a separate paid commercial license from **Razestar**.
No trademark rights are granted.
