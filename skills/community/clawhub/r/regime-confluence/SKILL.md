---
name: regime-confluence
description: Multi-timeframe regime agreement score for higher-confidence entries
metadata:
  openclaw:
    requires:
      env:
        - EVM_PRIVATE_KEY
    primaryEnv: EVM_PRIVATE_KEY
    homepage: https://apexrunner.ai/signals/regime-confluence
    emoji: "🔀"
---
# regime-confluence

## What It Does
Multi-timeframe regime agreement score for higher-confidence entries. This signal is computed in real time from APEX Runner's live autonomous trading system operating across Kraken, Coinbase Advanced Trade, and Hyperliquid — not from backtests or third-party aggregators.

## When to Use
- Before high-conviction entries
- When timeframe disagreement increases risk
- To confirm regime signals across multiple horizons

## How to Use
The agent makes an x402-authenticated GET request to:

```
https://apexrunner.ai/signals/regime-confluence
```

The x402 client handles payment authorisation automatically. No API key, no account, no subscription required — just an EVM wallet with USDC on Base mainnet.

```python
# Example using the x402-python client
from x402.client import x402_get

response = x402_get(
    url="https://apexrunner.ai/signals/regime-confluence",
    private_key=os.environ["EVM_PRIVATE_KEY"]
)
print(response.json())
```

## Example Response
```json
{
  "confluence_score": 0.79,
  "timeframes_aligned": 3,
  "dominant_regime": "RANGING"
}
```

## Pricing
**$0.10/call** — standard price

Early adopters automatically receive 30% off ($0.07/call) until 2026-09-21. Discount tiers apply automatically based on wallet call history:
- Early Adopter (0–9 calls): 30% off
- Engaged (10–49 calls): 15% off
- Loyal (50–199 calls): 15% permanent
- VIP (200+ calls): 20% permanent

Check your tier: `https://apexrunner.ai/signals/my-pricing`

## Related Signals
- [regime](https://apexrunner.ai/signals/regime)
- [regime-transition](https://apexrunner.ai/signals/regime-transition)
- [regime-confluence-institutional](https://apexrunner.ai/signals/regime-confluence-institutional)

---
*APEX Runner — autonomous AI crypto trading signals. [apexrunner.ai](https://apexrunner.ai)*
