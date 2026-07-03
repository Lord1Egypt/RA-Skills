---
name: whale-sentiment
description: Whale leaderboard sentiment derived from Hyperliquid top traders
metadata:
  openclaw:
    requires:
      env:
        - EVM_PRIVATE_KEY
    primaryEnv: EVM_PRIVATE_KEY
    homepage: https://apexrunner.ai/signals/whale-sentiment
    emoji: "🐋"
---
# whale-sentiment

## What It Does
Whale leaderboard sentiment derived from Hyperliquid top traders. This signal is computed in real time from APEX Runner's live autonomous trading system operating across Kraken, Coinbase Advanced Trade, and Hyperliquid — not from backtests or third-party aggregators.

## When to Use
- Before large directional bets
- To gauge smart-money positioning
- As confirming modifier for trade entries

## How to Use
The agent makes an x402-authenticated GET request to:

```
https://apexrunner.ai/signals/whale-sentiment
```

The x402 client handles payment authorisation automatically. No API key, no account, no subscription required — just an EVM wallet with USDC on Base mainnet.

```python
# Example using the x402-python client
from x402.client import x402_get

response = x402_get(
    url="https://apexrunner.ai/signals/whale-sentiment",
    private_key=os.environ["EVM_PRIVATE_KEY"]
)
print(response.json())
```

## Example Response
```json
{
  "sentiment": "bullish",
  "score": 0.67,
  "top_traders_long_pct": 72
}
```

## Pricing
**$0.50/call** — standard price

Early adopters automatically receive 30% off ($0.35/call) until 2026-09-21. Discount tiers apply automatically based on wallet call history:
- Early Adopter (0–9 calls): 30% off
- Engaged (10–49 calls): 15% off
- Loyal (50–199 calls): 15% permanent
- VIP (200+ calls): 20% permanent

Check your tier: `https://apexrunner.ai/signals/my-pricing`

## Related Signals
- [oi-divergence](https://apexrunner.ai/signals/oi-divergence)
- [liquidation-pressure](https://apexrunner.ai/signals/liquidation-pressure)
- [agent-conviction-score](https://apexrunner.ai/signals/agent-conviction-score)

---
*APEX Runner — autonomous AI crypto trading signals. [apexrunner.ai](https://apexrunner.ai)*
