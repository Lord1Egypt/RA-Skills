---
name: trading-intelligence-bundle
description: Bundle: momentum + whale sentiment + regime confluence
metadata:
  openclaw:
    requires:
      env:
        - EVM_PRIVATE_KEY
    primaryEnv: EVM_PRIVATE_KEY
    homepage: https://apexrunner.ai/signals/trading-intelligence-bundle
    emoji: "🎁"
---
# trading-intelligence-bundle

## What It Does
Bundle: momentum + whale sentiment + regime confluence. This signal is computed in real time from APEX Runner's live autonomous trading system operating across Kraken, Coinbase Advanced Trade, and Hyperliquid — not from backtests or third-party aggregators.

## When to Use
- For a full trading context in one call
- Before complex multi-factor decisions
- When minimising API call count

## How to Use
The agent makes an x402-authenticated GET request to:

```
https://apexrunner.ai/signals/trading-intelligence-bundle
```

The x402 client handles payment authorisation automatically. No API key, no account, no subscription required — just an EVM wallet with USDC on Base mainnet.

```python
# Example using the x402-python client
from x402.client import x402_get

response = x402_get(
    url="https://apexrunner.ai/signals/trading-intelligence-bundle",
    private_key=os.environ["EVM_PRIVATE_KEY"]
)
print(response.json())
```

## Example Response
```json
{
  "momentum_status": {"BTC": "active", "ETH": "active", "SOL": "inactive", "AVAX": "inactive"},
  "whale_sentiment": {"sentiment": "bullish", "score": 0.67, "top_traders_long_pct": 72},
  "regime_confluence": {"confluence_score": 0.79, "timeframes_aligned": 3, "dominant_regime": "RANGING"},
  "timestamp": "2026-06-23T14:00:00Z"
  // Full nested output of all component signals returned in one call
}
```

## Pricing
**$1.00/call** — standard price

Early adopters automatically receive 30% off ($0.70/call) until 2026-09-21. Discount tiers apply automatically based on wallet call history:
- Early Adopter (0–9 calls): 30% off
- Engaged (10–49 calls): 15% off
- Loyal (50–199 calls): 15% permanent
- VIP (200+ calls): 20% permanent

Check your tier: `https://apexrunner.ai/signals/my-pricing`

## Related Signals
- [market-pulse-bundle](https://apexrunner.ai/signals/market-pulse-bundle)
- [risk-assessment-bundle](https://apexrunner.ai/signals/risk-assessment-bundle)
- [apex-composite](https://apexrunner.ai/signals/apex-composite)

---
*APEX Runner — autonomous AI crypto trading signals. [apexrunner.ai](https://apexrunner.ai)*
