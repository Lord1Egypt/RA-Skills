---
name: x-single-tweet-article-skill
description: Fetch a single X tweet or X Article with charge-first billing (0.001 USDT/call).
---

# X Single Tweet + Article (Premium)

Charge-first fetcher for:
- single X tweet
- single X Article

## Pricing
- 0.001 USDT per call
- If balance is insufficient: returns `PAYMENT_URL` as a top-up link (no charge is made)

## Run

```bash
# Tweet
node scripts/run.js --url "https://x.com/user/status/123" --user "user-1"

# X Article
node scripts/run.js --article "https://x.com/i/article/xxxxx" --user "user-1"
```

## Optional env overrides
- `SKILLPAY_BILLING_URL`
- `SKILL_BILLING_API_KEY`
- `SKILL_ID`
- `SKILLPAY_PRICE_TOKEN`
