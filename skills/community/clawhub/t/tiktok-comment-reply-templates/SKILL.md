---
name: tiktok-comment-reply-templates
description: Generate conversion-focused TikTok comment replies that turn questions and objections into safe next-step actions without sounding spammy. Use when the user needs sales replies for TikTok comments, wants structured reply scripts by intent, or needs comment-to-DM/cart conversion sequences for TikTok Shop.
---

# TikTok Comment Reply Templates

## Skill Card

- **Category:** Comment Conversion
- **Core problem:** How to reply to comments in a way that increases conversion without hurting trust.
- **Best for:** TikTok Shop creators/operators handling high-volume pre-sale comment threads.
- **Expected input:** Comment text, product facts, offer terms, shipping/return rules, prohibited claims.
- **Expected output:** Intent-tagged reply scripts + CTA ladder + escalation and fallback logic.
- **Creatop handoff:** Save best-performing reply patterns into Creatop response templates.

## Workflow

1. Classify each comment into intent buckets:
   - info request,
   - objection (price/trust/fit/shipping),
   - buying signal,
   - low-intent/noise.
2. Generate 2 reply variants per comment:
   - concise public reply,
   - conversion-oriented follow-up prompt.
3. Add CTA ladder by intent stage:
   - comment keyword,
   - click cart,
   - DM for detail,
   - live demo reminder.
4. Add policy-safe rewrite when risky claims appear.
5. Provide handling map for repeat objections and hostile comments.

## Output format

Return in this order:
1. Comment intent table (intent, urgency, confidence)
2. Reply pack (short/public + follow-up/CTA)
3. Conversion ladder (by buyer stage)
4. Risk-safe alternatives and do-not-say list

## Quality and safety rules

- Do not fabricate guarantees, outcomes, stock levels, or delivery promises.
- Keep replies grounded in provided product/offer facts.
- Avoid repetitive spam-like phrasing across multiple comments.
- For abusive/low-intent comments, provide de-escalation or ignore guidance.
- Flag policy-risk phrases and provide compliant alternatives.

## License

Copyright (c) 2026 **Razestar**.

This skill is provided under **CC BY-NC-SA 4.0** for non-commercial use.
You may reuse and adapt it with attribution to Razestar, and share derivatives
under the same license.

Commercial use requires a separate paid commercial license from **Razestar**.
No trademark rights are granted.
