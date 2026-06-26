---
name: support-scripts
description: Build a pre-written response library for common customer service inquiries, complaints, and order issues that maintains tone and reduces resolution time.
---

# Support Scripts

This skill builds a library of pre-written customer-service reply templates for ecommerce sellers on TikTok Shop, Shopee, and Shopify. A good script library keeps every agent (or auto-reply) on-brand, compliant with platform rules, and fast — turning a 6-minute freehand reply into a 45-second personalized paste. The goal is not robotic canned text; it is a flexible scaffold with variables and tone rules that a human can send confidently or lightly edit.

## Quick Reference

| Decision | Strong | Acceptable | Weak |
| --- | --- | --- | --- |
| Tone register | Warm-professional, plain language, matches brand voice and platform norms | Generic-polite, slightly stiff but inoffensive | Corporate-legalese or over-casual slang that erodes trust |
| Personalization level | Uses `{{customer_name}}`, references the specific `{{order_id}}` and item | Uses name only; rest is generic | "Dear Customer" with zero order context |
| Refund authority phrasing | "I've issued a full refund of `{{amount}}` — it lands in 3-5 business days" (within policy) | "I'll request a refund for you" (when approval is needed) | "You will definitely get your money back today" (overpromising) |
| Escalation trigger | Clear rules: chargebacks, safety/injury claims, >$X value, 3rd contact, legal/press threats | Escalate on "angry customer" gut feel | No defined trigger; agents improvise or stall |
| Response-time SLA | First reply <2h in business hours, <12h off-hours; states a realistic window | Reply same business day | "We'll get back to you" with no timeframe |
| Apology framing | Specific, owns the issue, no excuses: "That's on us — your parcel was mislabeled" | "Sorry for any inconvenience" | "Sorry you feel that way" (non-apology, blames customer) |
| Channel adaptation | Tightens length and emoji for TikTok Shop chat vs. fuller email on Shopify | One length reused everywhere | Long formal email pasted into a 1-line chat box |
| Compensation offer | Tiered and pre-approved (reship, partial credit, coupon) with caps per scenario | Ad-hoc gesture decided per ticket | Reflex discount on every complaint, training customers to complain |
| Closing / next step | States exactly what happens next and by when, invites reply | Polite sign-off, no next step | Abrupt close that forces a follow-up message |

## Solves

- Inconsistent voice across agents, shifts, and platforms that makes the brand feel unreliable.
- Slow first-response and high handle time because agents write every reply from scratch.
- Compliance slips — agents promising refunds, delivery dates, or remedies the platform or policy doesn't allow.
- New-hire ramp time: onboarding takes weeks because there's no answer bank to learn from.
- Over-discounting and inconsistent compensation that quietly erodes margin.
- Negative reviews and disputes that escalate because the first reply was cold, defensive, or off-topic.
- No reusable structure for AI auto-replies or chatbot flows, so automation sounds generic and breaks trust.

## Workflow

1. **Audit ticket volume and tag the backlog.** Pull 30-90 days of tickets/chats from each platform and tag them by inquiry type. Note volume, average handle time, CSAT, and where conversations stall or escalate. You are looking for the 20% of inquiry types that drive 80% of contacts — that is where scripts pay off first.

2. **Identify and rank the top inquiry types.** Cluster the tags into clear scenarios (e.g. "Where is my order?", "Item arrived damaged", "Wrong size"). Rank by volume × handle time × escalation rate so you script the highest-leverage scenarios first. Aim for 15-25 scenarios in v1; resist trying to cover every edge case.

3. **Define brand voice and policy rules.** Set the voice (register, warmth, formality, emoji usage) and the non-negotiable guardrails: what agents can promise on refunds, reships, and timelines without approval, and what must escalate. Write these as plain rules so every script inherits the same boundaries. See `references/tone-and-policy-guide.md`.

4. **Draft scripts per scenario, two variants each.** For each scenario write variant A (standard) and variant B (high-empathy / repeat or upset customer). Lead with acknowledgement, give the answer or action, and end with a concrete next step. Keep chat variants short; keep email variants complete. Use `references/scenario-library.md` for seeds.

5. **Add variables, placeholders, and branch notes.** Replace specifics with clear tokens like `{{customer_name}}`, `{{order_id}}`, `{{tracking_link}}`, `{{amount}}`, `{{eta_date}}`. Mark every spot an agent must verify before sending, and add "do-not-say" notes to block off-policy phrasing. Variables prevent copy-paste accidents (wrong name, stale ETA).

6. **QA against policy and voice.** Run every script through `assets/quality-checklist.md`: check coverage, voice consistency, policy accuracy, personalization, empathy, escalation, and localization. Have a second reviewer read scripts cold and flag anything that sounds canned, risky, or off-brand. Fix, then approve.

7. **Roll out, measure, and maintain.** Load scripts into the helpdesk/macros and brief the team on when to edit vs. send as-is. Track first-response time, handle time, CSAT, and escalation rate before/after. Review monthly: retire dead scripts, add new scenarios from emerging tickets, and refresh anything affected by a policy or product change. Log every change in the maintenance table from `references/output-template.md`.

## Example 1

**Brand:** *Lumio & Co.* — a mid-size home-fragrance brand (candles, reed diffusers, refills) selling on Shopify (primary) and TikTok Shop. Voice: warm, sensory, lightly playful; first-name basis; one emoji max per message; never clinical.

**Top inquiry types (from a 60-day audit):** WISMO / order status (34%), melted or broken-in-transit candle (18%), scent expectation mismatch (11%), discount code won't apply (9%), cancel/change order (7%).

**Sample scripts**

*Scenario: "Where is my order?" — variant A (standard, Shopify email)*
> Hi `{{customer_name}}`, thanks for reaching out! Your order `{{order_id}}` is on its way — here's live tracking: `{{tracking_link}}`. Right now it's showing `{{tracking_status}}`, with delivery expected by `{{eta_date}}`. If it hasn't arrived by then, just reply here and I'll chase the carrier and sort it out for you. 🕯️

*Scenario: "My candle arrived melted/broken" — variant B (high-empathy, photos already attached)*
> Oh no, `{{customer_name}}` — a `{{product_name}}` showing up like that is not the welcome we wanted to send. That's on us and the summer heat in transit. I've arranged a free replacement for order `{{order_id}}`, shipping `{{ship_method}}` today, no need to return the damaged one. You'll get tracking by `{{eta_date}}`. Thanks for the photos — they help us pack smarter for warm-weather routes.

*Scenario: "Discount code won't apply" — variant A (TikTok Shop chat, short)*
> Hi `{{customer_name}}`! Let's fix that. Code `{{promo_code}}` is valid on orders over `{{min_spend}}` and excludes `{{excluded_items}}` — could either of those be it? If your cart qualifies and it's still not taking, send a screenshot and I'll apply the discount manually before you check out. 💛

## Example 2

**Brand:** *TrailKit* — outdoor gear and apparel (packs, jackets, footwear) selling on Shopee (SEA markets) and Shopify. Voice: confident, practical, no-fluff, gear-expert peer; sizing and durability questions are frequent and high-stakes for returns.

**Top inquiry types:** sizing/fit advice pre-purchase (22%), return/exchange for fit (19%), delivery delay (17%), waterproofing/defect claim (12%), warranty question (8%).

**Sample scripts**

*Scenario: "Will this jacket fit me?" — variant A (pre-sale, Shopee chat)*
> Hi `{{customer_name}}`! The `{{product_name}}` runs true to size with room for a midlayer. For your stats (`{{height}}` / `{{chest}}`), I'd go `{{recommended_size}}` — size up only if you'll layer a thick fleece. Full size chart here: `{{size_chart_link}}`. Want it roomier or more fitted? Tell me how you like your shell to sit and I'll dial it in.

*Scenario: "I need to exchange for a different size" — variant A (standard)*
> Hi `{{customer_name}}`, happy to swap that for you. I've started an exchange on order `{{order_id}}`: you'll get a prepaid return label at `{{return_label_link}}`, and your `{{new_size}}` will ship the moment your return scans in (usually `{{exchange_window}}`). Keep the item unworn with tags so it qualifies. Want me to reserve the `{{new_size}}` now so it doesn't sell out? I can hold it for `{{hold_days}}` days.

*Scenario: "My jacket leaked / isn't waterproof" — variant B (high-empathy, possible defect)*
> That shouldn't happen, `{{customer_name}}` — the `{{product_name}}` is rated to `{{waterproof_rating}}`, so a leak means something's off. A couple of quick questions so I get you the right fix: where did water come through (seams, zip, or fabric), and roughly how old is the jacket? If it's a manufacturing fault it's covered under our `{{warranty_period}}` warranty and I'll arrange a replacement or repair — no cost to you. In the meantime, here's a 2-minute re-proofing guide in case it's the DWR coating: `{{care_link}}`.

## Common Mistakes

- **Writing scripts that sound canned.** Templates read like form letters when they skip the customer's name and order specifics. Fix: require at least `{{customer_name}}` + one order-specific reference (`{{order_id}}`, item, or ETA) in every script.
- **Overpromising remedies.** "You'll get a refund today" or "It'll arrive tomorrow" creates a second, angrier ticket when it slips. Fix: phrase actions within authority and use realistic windows ("3-5 business days", "by `{{eta_date}}`").
- **One length for every channel.** A 6-line email pasted into a TikTok Shop chat feels robotic and gets skimmed. Fix: maintain a short chat variant and a fuller email variant per scenario.
- **The non-apology.** "Sorry you feel that way" / "Sorry for any inconvenience" reads as deflection. Fix: apologize for the specific thing and own it where it's your fault.
- **No defined escalation triggers.** Agents either escalate everything or nothing. Fix: list hard triggers (safety/injury, chargeback, legal/press threat, value over `{{threshold}}`, third contact) in each script and the policy guide.
- **Reflex discounting.** Offering a coupon on every complaint trains customers to complain and silently bleeds margin. Fix: pre-approve a tiered, capped compensation ladder per scenario; lead with fixing the problem, not paying it off.
- **Stale placeholders going out live.** Sending `{{tracking_link}}` literally, or last week's ETA, destroys trust instantly. Fix: mark every must-verify field and add a final "swap all `{{ }}`" QA step.
- **Ignoring platform policy differences.** What you can promise on Shopify returns differs from Shopee/TikTok Shop buyer-protection flows. Fix: encode platform-specific guardrails so the same scenario has the right boundaries per channel.
- **Set-and-forget libraries.** Scripts drift out of date after a product, price, or policy change and start giving wrong answers. Fix: schedule a monthly review and log changes in the maintenance table.
- **No "do-not-say" guardrails.** Without them, agents improvise risky phrasing (admitting fault on a safety claim, quoting legal terms). Fix: add do-not-say notes to sensitive scenarios.
- **Translating word-for-word for other markets.** Literal translation breaks tone and politeness norms in Shopee SEA markets. Fix: localize voice, not just language, and have a native speaker review.

## Resources

- `references/output-template.md` — Fill-in-the-blank structure for the finished Support Script Library deliverable, including the per-scenario block and maintenance log.
- `references/scenario-library.md` — Catalog of ~25 common ecommerce CS scenarios with triggers, customer emotion, key info, and a script seed for each.
- `references/tone-and-policy-guide.md` — How to define brand voice, platform policy guardrails, the acknowledge→align→act empathy pattern, and localization cautions.
- `assets/quality-checklist.md` — QA checklist to run every script through before approval and rollout.
