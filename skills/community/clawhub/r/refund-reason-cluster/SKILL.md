---
        name: refund-reason-cluster
        description: Cluster refund and return reasons into actionable root-cause groups and prevention plans. Use when the user asks why refund rate is rising, which causes are avoidable, or how to reduce return-driven margin erosion.
        ---

        # Refund Reason Cluster

        ## Skill Card

        - **Category:** Post-purchase Analytics
        - **Core problem:** What repeatable reasons are driving refunds and returns?
        - **Best for:** Reducing avoidable refunds and preserving margins
        - **Expected input:** Refund logs, return reason text, support transcripts, order metadata
        - **Expected output:** Reason clusters with root-cause hypotheses and prevention actions
        - **Creatop handoff:** Feed top reasons into product fixes + pre-purchase expectation copy

        ## Workflow

        1. Normalize refund reason text and link to order/product attributes.
2. Cluster reasons by cause type (quality, fit, shipping, expectation, misuse).
3. Estimate avoidable vs unavoidable share with confidence notes.
4. Output prevention actions by short-term and long-term horizon.

        ## Output format

        Return in this order:
        1. Executive summary (max 5 lines)
        2. Priority actions (P0/P1/P2)
        3. Evidence table (signal, confidence, risk)
        4. 7-day execution plan

        ## Quality and safety rules

        - Separate policy fraud/abuse from genuine product dissatisfaction.
- Highlight sample-size and data-quality caveats.
- Prioritize high-frequency + high-cost clusters first.

        ## License

Copyright (c) 2026 **Razestar**.

This skill is provided under **CC BY-NC-SA 4.0** for non-commercial use.
You may reuse and adapt it with attribution to Razestar, and share derivatives
under the same license.

Commercial use requires a separate paid commercial license from **Razestar**.
No trademark rights are granted.
