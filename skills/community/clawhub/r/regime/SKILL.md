---
name: regime
description: Full market regime classification: TRENDING, RANGING, CHOPPY, or CRISIS
metadata:
  openclaw:
    requires:
      env:
        - EVM_PRIVATE_KEY
    primaryEnv: EVM_PRIVATE_KEY
    homepage: https://apexrunner.ai/signals/regime
    emoji: "🗺️"
---
# regime

## What It Does
Full market regime classification: TRENDING, RANGING, CHOPPY, or CRISIS. This signal is computed in real time from APEX Runner's live autonomous trading system operating across Kraken, Coinbase Advanced Trade, and Hyperliquid — not from backtests or third-party aggregators.

## When to Use
- Before selecting a trading strategy
- To route decisions through regime-appropriate logic
- As the primary market context signal

## How to Use
The agent makes an x402-authenticated GET request to:

```
https://apexrunner.ai/signals/regime
```

The x402 client handles payment authorisation automatically. No API key, no account, no subscription required — just an EVM wallet with USDC on Base mainnet.

```python
# Example using the x402-python client
from x402.client import x402_get

response = x402_get(
    url="https://apexrunner.ai/signals/regime",
    private_key=os.environ["EVM_PRIVATE_KEY"]
)
print(response.json())
```

## Example Response
```json
{
  "regime": "RANGING",
  "confidence": 0.82,
  "coin": "BTC",
  "timestamp": "2026-06-23T14:00:00Z"
}
```

## Pricing
**$0.15/call** — standard price

Early adopters automatically receive 30% off ($0.10/call) until 2026-09-21. Discount tiers apply automatically based on wallet call history:
- Early Adopter (0–9 calls): 30% off
- Engaged (10–49 calls): 15% off
- Loyal (50–199 calls): 15% permanent
- VIP (200+ calls): 20% permanent

Check your tier: `https://apexrunner.ai/signals/my-pricing`

## Related Signals
- [regime-micro](https://apexrunner.ai/signals/regime-micro)
- [regime-confluence](https://apexrunner.ai/signals/regime-confluence)
- [regime-transition](https://apexrunner.ai/signals/regime-transition)

---
*APEX Runner — autonomous AI crypto trading signals. [apexrunner.ai](https://apexrunner.ai)*
