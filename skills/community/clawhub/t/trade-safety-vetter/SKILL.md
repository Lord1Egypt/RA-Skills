---
name: Trade Safety Vetter
description: "Pre-trade safety checks: position size limits, leverage validation, consecutive loss locks, volatility gates, exchange balance verification. Drop-in risk guard for any trading skill."
emoji: 🛡️
color: red
---

# Trade Safety Vetter

A pre-trade risk validation gate. Before any trade executes, this skill verifies:

## Safety Rules

| Rule | Threshold | Action |
|------|-----------|--------|
| Single trade risk | ≤5% of total capital | Block if exceeded |
| Consecutive losses | 3 in same direction | Pause 24h |
| Leverage × Volatility | >15 | Reject entry |
| Extreme volatility | >80% VIX-like | Auto-reduce leverage |
| Exchange balance | Sufficient margin | Block if insufficient |

## Integration

This skill works as a middleware. Place it before any trade execution.

**Usage in your agent:**
> "Before executing this trade, run Trade Safety Vetter to validate"

## Premium Version (Coming Soon)
- Customizable risk thresholds
- Multi-exchange support
- Performance tracking dashboard

---

*Risk management is the foundation of profitable trading.*
\n\n---\n### 💎 Pro Version \nFull trading execution + custom risk + priority support.\nSend USDT (TRC20) to: TUq4wEenH8qyBX5RtUQuyyYDH9FjiEXNND\nContact @sgreadybot on Telegram to activate.\n