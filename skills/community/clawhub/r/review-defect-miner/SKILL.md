---
        name: review-defect-miner
        description: Extract and cluster defect signals from ecommerce reviews and social feedback into actionable quality/fix priorities. Use when the user asks why ratings are low, what issues drive bad sentiment, or which product problems should be fixed first.
        ---

        # Review Defect Miner

        ## Skill Card

        - **Category:** Voice of Customer
        - **Core problem:** What product defects and dissatisfaction patterns are hidden in reviews/comments?
        - **Best for:** Product and content teams diagnosing quality gaps
        - **Expected input:** Low-star reviews, comments, support tickets, return notes
        - **Expected output:** Defect clusters by severity, frequency, and fix priority with evidence snippets
        - **Creatop handoff:** Convert top defect clusters into product fixes + expectation-setting scripts

        ## Workflow

        1. Normalize raw review/comment text and tag source + date + star level.
2. Detect defect themes (quality, packaging, expectation mismatch, delivery, usability).
3. Score each theme by severity, frequency, and conversion impact risk.
4. Output top fix backlog and messaging mitigations.

        ## Output format

        Return in this order:
        1. Executive summary (max 5 lines)
        2. Priority actions (P0/P1/P2)
        3. Evidence table (signal, confidence, risk)
        4. 7-day execution plan

        ## Quality and safety rules

        - Preserve original evidence snippets for traceability.
- Separate quality defects from logistics/service issues.
- Do not over-generalize from tiny sample sizes.

        ## License

Copyright (c) 2026 **Razestar**.

This skill is provided under **CC BY-NC-SA 4.0** for non-commercial use.
You may reuse and adapt it with attribution to Razestar, and share derivatives
under the same license.

Commercial use requires a separate paid commercial license from **Razestar**.
No trademark rights are granted.
