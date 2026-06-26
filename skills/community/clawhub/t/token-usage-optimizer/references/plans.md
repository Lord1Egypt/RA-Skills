# Claude Code Subscription Plans

Overview of Claude Code pricing tiers and quota expectations.

## Available Plans

### Pro ($20/month)

- Basic access to Claude Code
- Lower usage quotas
- Good for casual users
- **5-hour limit:** Lower threshold
- **7-day limit:** ~200-300 requests/week (estimated)

### Max 100 ($100/month)

- 5× capacity vs Pro
- Designed for power users
- **5-hour limit:** Higher threshold
- **7-day limit:** ~1000-1500 requests/week (estimated)

### Max 200 ($200/month)

- 10× capacity vs Pro
- For heavy professional use
- **5-hour limit:** Highest threshold
- **7-day limit:** ~2000-3000 requests/week (estimated)

## Daily Budget

All plans reset on a **7-day rolling window**, so:

- **Daily target:** ~14% of weekly quota (100% ÷ 7 days)
- **Goal:** Use subscription to its fullest without hitting limits

### Example for Max 100:

| Day | Target Usage | Actual | Status |
|-----|--------------|--------|--------|
| Mon | 14% | 12% | 🟢 UNDER (use more!) |
| Tue | 28% | 35% | 🔴 OVER (throttle) |
| Wed | 42% | 45% | ⚪ OK (on pace) |
| Thu | 56% | 58% | ⚪ OK |
| Fri | 70% | 68% | ⚪ OK |
| Sat | 84% | 80% | 🟢 UNDER |
| Sun | 100% | 95% | 🟢 UNDER |

**Insight:** If you're consistently UNDER, consider downgrading. If OVER, upgrade.

## Quota Windows

### 5-Hour Session Window

- **Purpose:** Prevent rapid bursts
- **Strategy:** Monitor frequently, alert at 50%
- **Resets:** Every 5 hours (rolling)
- **Impact:** Short-term throttling

### 7-Day Weekly Window

- **Purpose:** Main subscription quota
- **Strategy:** Track daily burn rate (~14%/day)
- **Resets:** Every 7 days (rolling)
- **Impact:** Long-term capacity planning

## Optimization Strategies

### Under-Using Your Plan?

- ✅ Use Claude Code more throughout the day
- ✅ Batch smaller queries instead of avoiding usage
- ✅ Explore more features (code generation, refactoring)
- ❌ Don't waste — but get your money's worth!

### Over-Using Your Plan?

- ✅ Spread usage across the week
- ✅ Use session window more efficiently (wait for resets)
- ✅ Consider upgrading to next tier
- ❌ Don't hit limits mid-week!

### On Pace?

- ✅ You're optimizing well!
- ✅ Keep monitoring to maintain balance

## Plan Detection

The API **does not expose** which plan you're on. This skill infers burn rate based on:

1. Your current utilization percentage
2. Days elapsed since weekly reset
3. Expected daily budget (~14%)

All plans follow the same **7-day rolling window**, so the burn rate calculation works universally.

## Cost Per Request

Approximate (varies by model and prompt size):

| Plan | Monthly | $/request (estimated) |
|------|---------|----------------------|
| Pro | $20 | ~$0.07-0.10 |
| Max 100 | $100 | ~$0.07-0.10 |
| Max 200 | $200 | ~$0.07-0.10 |

Higher tiers = more requests, not cheaper per-request.

## Recommendations by User Type

### Casual User (2-3 sessions/week)
→ **Pro** is sufficient

### Daily User (1-2 hours/day)
→ **Max 100** for best value

### Power User (3+ hours/day, CI/CD, automation)
→ **Max 200** to avoid limits

## Notes

- Quotas are **rolling windows**, not calendar-based
- Utilization % is the same across all tiers (100% = your plan's limit)
- Extra usage credits (if available) are separate from main quota
- Opus usage may have separate limits (check `seven_day_opus` field)

## References

- [Claude Code Pricing](https://claude.ai/pricing)
- [Anthropic API Docs](https://docs.anthropic.com/)
