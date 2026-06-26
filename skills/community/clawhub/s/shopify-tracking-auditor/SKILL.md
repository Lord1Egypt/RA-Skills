---
        name: shopify-tracking-auditor
        description: Audit Shopify tracking integrity across UTM, pixel, CAPI, and checkout events to detect attribution leaks. Use when the user reports inconsistent ROAS data, missing conversion events, or mismatch between platform and store-side numbers.
        ---

        # Shopify Tracking Auditor

        ## Skill Card

        - **Category:** Measurement
        - **Core problem:** Where is tracking broken across ad click to purchase flow?
        - **Best for:** Performance teams debugging attribution leaks
        - **Expected input:** Event samples, pixel/CAPI config notes, UTM examples, checkout flow map
        - **Expected output:** Tracking gap audit with severity, suspected cause, and fix checklist
        - **Creatop handoff:** Apply fixes then rerun attribution review with creator-attribution-lite

        ## Workflow

        1. Map funnel events from click -> landing -> add-to-cart -> checkout -> purchase.
2. Validate event naming consistency, deduplication, and timestamp continuity.
3. Identify drop-off points where measurement is missing or unreliable.
4. Produce a fix plan ordered by measurement impact.

        ## Output format

        Return in this order:
        1. Executive summary (max 5 lines)
        2. Priority actions (P0/P1/P2)
        3. Evidence table (signal, confidence, risk)
        4. 7-day execution plan

        ## Quality and safety rules

        - Distinguish data collection failures from real performance changes.
- Keep findings tied to concrete event evidence.
- Mark assumptions when full logs are unavailable.

        ## License

Copyright (c) 2026 **Razestar**.

This skill is provided under **CC BY-NC-SA 4.0** for non-commercial use.
You may reuse and adapt it with attribution to Razestar, and share derivatives
under the same license.

Commercial use requires a separate paid commercial license from **Razestar**.
No trademark rights are granted.
