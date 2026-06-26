---
name: x-hourly-brief-skill
description: X Hourly Brief (Premium) — charge-first brief generation for high-value X posts. Supports Chinese/English output.
---

# X Hourly Brief (Premium)

Generate a concise hourly brief from X post URLs.

## Pricing

- 0.001 USDT per call (1 token)
- Charge-first
- Low balance returns `PAYMENT_URL`

## Run

```bash
node scripts/run.js --urls "https://x.com/.../status/1,https://x.com/.../status/2" --user "<user-id>" --lang "auto"
```

## Output

- Per-post brief (key points)
- Final digest summary
- Supports `zh`, `en`, `auto`

## Optional env overrides

- `SKILLPAY_BILLING_URL`
- `SKILL_BILLING_API_KEY`
- `SKILL_ID`
- `SKILLPAY_PRICE_TOKEN`
