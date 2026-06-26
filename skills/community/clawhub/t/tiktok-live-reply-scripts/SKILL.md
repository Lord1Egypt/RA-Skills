---
name: tiktok-live-reply-scripts
description: Handle TikTok Live sales objections in real time with structured reply strategies, risk-safe phrasing, and conversion-focused response sequences. Use when the user asks how to reply to buyer objections during live selling, wants objection scripts, or needs a playbook for price/trust/urgency hesitation in TikTok Shop live sessions.
---

# TikTok Live Reply Scripts

## Skill Card

- **Category:** Live Commerce Conversion
- **Core problem:** How to respond to live objections fast without sounding pushy or risky.
- **Best for:** TikTok Shop live hosts and moderators handling buyer hesitation.
- **Expected input:** Objection text, product facts, offer terms, proof points, risk constraints.
- **Expected output:** Prioritized objection replies + escalation ladder + fallback close scripts.
- **Creatop handoff:** Feed winning objection/reply patterns into script and live SOP libraries.

## Workflow

1. Parse objection type (price, trust, fit, shipping, urgency, quality, social proof).
2. Map objection to buyer intent stage (curious, comparing, almost-buying, post-trust check).
3. Generate 2-3 reply variants per objection:
   - short live-safe line (<= 20 words),
   - expanded reassurance line,
   - action prompt (comment keyword / click cart / stay for demo).
4. Add risk checks for claims, guarantees, and policy-sensitive language.
5. Build a sequence ladder: first reply -> proof reinforcement -> close prompt -> fallback.

## Output format

Return in this order:
1. Objection diagnosis table (type, urgency, likely hidden concern)
2. Reply pack (short / expanded / CTA) per objection
3. Escalation ladder for repeated objections
4. 7-day live training loop (what to test and log)

## Quality and safety rules

- Do not fabricate outcomes, certifications, inventory, or shipping promises.
- Keep replies aligned with provided product facts and offer terms.
- Avoid manipulative pressure language; prioritize trust-building and clarity.
- If evidence is missing, recommend collecting proof instead of forcing a close.
- Flag policy-risk phrases and provide safer alternatives.

## License

Copyright (c) 2026 **Razestar**.

This skill is provided under **CC BY-NC-SA 4.0** for non-commercial use.
You may reuse and adapt it with attribution to Razestar, and share derivatives
under the same license.

Commercial use requires a separate paid commercial license from **Razestar**.
No trademark rights are granted.
