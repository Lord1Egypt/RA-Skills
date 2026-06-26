---
        name: tiktok-shop-creator-fit-scorer
        description: Score TikTok Shop creator-product fit using audience match, content style, conversion evidence, and execution risk. Use when the user asks who to collaborate with, needs a ranked creator shortlist, or wants to reduce low-quality outreach in affiliate/UGC campaigns.
        ---

        # TikTok Shop Creator Fit Scorer

        ## Skill Card

        - **Category:** Creator Matching
        - **Core problem:** Which creators are most likely to convert for a specific product?
        - **Best for:** Creator sourcing before outreach
        - **Expected input:** Product positioning, target ICP, creator profile links/metrics, budget constraints
        - **Expected output:** Ranked creator shortlist with fit scores, outreach angle, and risk flags
        - **Creatop handoff:** Use top-ranked creators in outreach sequence and brief generation

        ## Workflow

        1. Collect product facts, target buyer profile, creator links, and budget limits.
2. Score each creator on audience fit, style fit, trust/proof signals, and operational risk.
3. Rank creators by weighted fit score and segment into P0/P1/P2 priority tiers.
4. Generate outreach angle + brief starter for top candidates.

        ## Output format

        Return in this order:
        1. Executive summary (max 5 lines)
        2. Priority actions (P0/P1/P2)
        3. Evidence table (signal, confidence, risk)
        4. 7-day execution plan

        ## Quality and safety rules

        - Do not fabricate follower or conversion data.
- Mark unknown values explicitly as unknown and lower confidence.
- Prioritize fit quality over vanity metrics.

        ## License

Copyright (c) 2026 **Razestar**.

This skill is provided under **CC BY-NC-SA 4.0** for non-commercial use.
You may reuse and adapt it with attribution to Razestar, and share derivatives
under the same license.

Commercial use requires a separate paid commercial license from **Razestar**.
No trademark rights are granted.
