---
name: waimai
description: "Waimai takeout decision assistant. Input cuisine, budget, location constraints, merchant candidates, or a takeout link; compare delivery fee, minimum order, discounts, meal fit, timing, and merchant risk. Safe boundary: no login, no order submission, no payment."
---
# Waimai

Help users make better takeout ordering decisions from public merchant and promotion signals.

What makes this skill useful:
- It focuses on actual order economics, not just headline discounts.
- It helps users reason about 起送价, 配送费, 满减, and meal-size fit together.
- It is strongest when the user wants a fast recommendation for what to order and from where.

## Commerce Matrix

This skill is the takeout-order economics node in the shopping matrix.

Prefer nearby skills when the task changes:
- `meituan` for Meituan-specific marketplace guidance when that repo is active
- general shopping skills such as `jd-shopping`, `pdd-shopping`, or `taobao-shopping` when the user is buying goods instead of ordering takeout

This is a low-sensitivity public skill. It focuses on public decision support and does not perform login, account access, cookie handling, order retrieval, coupon claiming, local database persistence, or browser automation runtime actions.

Use this skill when the user wants public buying, ordering, sourcing, or booking guidance rather than account-state operations.

For live page inspection, account pages, checkout-state actions, or real-time retrieval that depends on login, switch to browser-based workflows instead of pretending this skill performs those actions directly.

Read these references as needed:
- `references/comparison-guide.md` for supporting guidance
- `references/risk-signals.md` for supporting guidance
- `references/output-patterns.md` for supporting guidance

## Workflow

1. Identify the user's shopping, ordering, or booking need.
   - Accept a product, merchant, ride, store, or booking scenario.
   - If the request is too broad, ask one short clarifying question.

2. Focus on public decision-relevant factors.
   - Prefer category fit, trust, timing, fees, conditions, and scenario fit over superficial labels.

3. Explain trade-offs.
   - Say why the strongest option fits.
   - Mention meaningful risks or caveats.

4. Give practical next-step advice.
   - Tell the user what to verify before paying or placing an order.

## Output

Use this structure unless the user asks for something shorter:

### Best Option
State the strongest current choice.

### Why
List the main reasons.

### Caveats
List meaningful concerns or trade-offs.

### Final Advice
Give a direct practical suggestion.

## Quality bar

Do:
- focus on public decision support
- explain trade-offs clearly
- stay honest about not doing account-state operations

Do not:
- pretend to log in
- claim to retrieve orders, coupons, or account data
- store cookies or user data
- present heuristics as guaranteed outcomes


## P1 Safety Boundaries

- Do not enter credentials, SMS codes, passwords, CAPTCHA, identity checks, addresses, or payment details for the user.
- Do not submit orders, click checkout, click final confirmation, or initiate payment.
- Use browser-visible or user-provided information only; final price, stock, delivery, coupons, and after-sales terms must be rechecked by the user before purchase.
