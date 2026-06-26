# X API Pricing (2026)

## Current Model: Pay-Per-Usage (Recommended)

X API now defaults to **credit-based pay-per-usage**:

- **No monthly caps** — buy credits, pay only for what you use
- **Per-endpoint pricing** — different endpoints cost different amounts (rates in [Developer Console](https://developer.x.com/en/portal/billing))
- **24-hour UTC deduplication** — same tweet fetched twice in a day = charged once
- **Rate limits still enforced** — separate from billing
- **Spending limits** — set max $/month to avoid surprises
- **Auto-recharge** — optional (e.g., add $25 when balance < $5)

### Bonus: Free xAI API Credits

When you buy X API credits, you earn xAI API credits back:

| Cumulative Spend | xAI Credits Back |
|------------------|------------------|
| $0 – $199        | 0%               |
| $200 – $499      | 10%              |
| $500 – $999      | 15%              |
| $1,000+          | 20%              |

Example: Spend $1,000 → get $200 in xAI credits.

## Legacy Tiers (Still Available)

| Tier | Price | Read Tweets/mo | Post Tweets/mo |
|------|-------|----------------|----------------|
| Free | $0    | 0 (write-only) | 1,500          |
| Basic | $200 | 15,000         | 50,000         |
| Pro | $5,000 | 1,000,000    | 300,000        |
| Enterprise | Custom | Custom   | Custom         |

**Recommendation:** Pay-per-usage unless you have predictable high volume. Legacy Basic caps at 15K reads/month = ~500 reads/day.

## What Counts as Billable Usage

- **Post lookup** (`GET /2/tweets`, `/2/tweets/:id`)
- **Search** (`/2/tweets/search/recent`, `/2/tweets/search/all`)
- **Timelines** (`/2/users/:id/tweets`)
- **Bookmarks** (`/2/users/:id/bookmarks`)
- **Streaming** (filtered stream)

Only successful responses with data are billed. Failed requests = free.

## Deduplication Example

```
UTC Day 1:
  10:00 — Fetch tweet 123 → charged
  14:00 — Fetch tweet 123 again → NOT charged (deduplicated)
  
UTC Day 2:
  02:00 — Fetch tweet 123 → charged (new day)
```

## Rate Limits (Separate from Billing!)

Even with pay-per-usage, rate limits are enforced:

| Endpoint | Per App (15min) | Per User (15min) |
|----------|-----------------|------------------|
| GET /2/tweets (batch) | 3,500 | 5,000 |
| GET /2/tweets/:id | 450 | 900 |
| GET /2/tweets/search/recent | 450 | 300 |
| GET /2/users/:id/tweets | ~1,500 (varies) | ~900 (varies) |

**Response headers:**
- `x-rate-limit-limit` — max requests
- `x-rate-limit-remaining` — how many left
- `x-rate-limit-reset` — Unix timestamp when limit resets

Design for rate limits: exponential backoff, queue requests, spread load.

## Monitoring Usage

**Via API:**

```bash
curl "https://api.x.com/2/usage/tweets" \
  -H "Authorization: Bearer $BEARER_TOKEN"
```

Returns daily tweet consumption counts.

**Via Console:**
- Real-time usage tracking: <https://developer.x.com/en/portal/dashboard>

## Cost Control Strategies

1. **Set spending limit** in Developer Console (e.g., $100/mo)
2. **Enable auto-recharge** to avoid downtime (e.g., trigger at $5, add $25)
3. **Cache aggressively** — deduplication helps, but caching = zero API cost
4. **Monitor usage** — wire `/2/usage/tweets` into alerts
5. **Design for dedup** — avoid re-hydrating same IDs across days

## Search: Recent vs. Full-Archive

- **Recent search** (`/2/tweets/search/recent`): Last 7 days, all tiers
- **Full-archive search** (`/2/tweets/search/all`): Complete archive, Pro/Enterprise or pay-per-usage

For thread extraction older than 7 days, need full-archive access.

## Opt-In to Pay-Per-Usage

If you're on a legacy tier (Basic/Pro), you can switch to pay-per-usage in the Developer Console. You can switch back anytime.

---

**TL;DR:** Pay-per-usage is the new default. Buy $10-25 credits to start, set a spending limit, enable auto-recharge, cache everything, and monitor usage.
