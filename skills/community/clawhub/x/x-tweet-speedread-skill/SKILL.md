---
name: x-tweet-speedread-skill
description: X Tweet Speedread (Premium) — instant English brief for any X post. Charge-first direct mode via SkillPay (0.001 USDT/call).
---

# X Tweet Speedread (Premium)

Paste an X URL, get an instant English speedread.

## Pricing

- **0.001 USDT per call** (1 token)
- Charge-first model
- Low balance => return `PAYMENT_URL`

## What it returns

- 3–5 key bullets
- 1 core takeaway
- up to 3 risks
- up to 3 actions

## Run

```bash
node scripts/run.js --url "https://x.com/.../status/..." --user "<user-id>"
```

## Billing behavior

- Calls SkillPay billing directly before extraction.
- If balance is low, returns `PAYMENT_URL` and `PAYMENT_INFO`.
- If charge succeeds, continues to fetch and summarize the X post.

## Optional overrides

- `SKILLPAY_BILLING_URL`
- `SKILL_BILLING_API_KEY`
- `SKILL_ID`
- `SKILLPAY_PRICE_TOKEN`
