---
name: slippage-forecast
description: Predicts expected slippage for a given order size and market condition
metadata:
  openclaw:
    requires:
      env:
        - EVM_PRIVATE_KEY
    primaryEnv: EVM_PRIVATE_KEY
    homepage: https://apexrunner.ai/signals/slippage-forecast
    emoji: "📐"
---
# slippage-forecast

## What It Does
Predicts expected slippage for a given order size and market condition. This signal is computed in real time from APEX Runner's live autonomous trading system operating across Kraken, Coinbase Advanced Trade, and Hyperliquid — not from backtests or third-party aggregators.

## When to Use
- Before placing large orders
- To estimate realistic execution cost
- When comparing venues for best execution

## How to Use
The agent makes an x402-authenticated GET request to:

```
https://apexrunner.ai/signals/slippage-forecast
```

The x402 client handles payment authorisation automatically. No API key, no account, no subscription required — just an EVM wallet with USDC on Base mainnet.

```python
# Example using the x402-python client
from x402.client import x402_get

response = x402_get(
    url="https://apexrunner.ai/signals/slippage-forecast",
    private_key=os.environ["EVM_PRIVATE_KEY"]
)
print(response.json())
```

## Example Response
```json
{
  "slippage_forecast": {
    "BTC": {
      "kraken": {
        "small_order": {
          "size_range": "<$500",
          "avg_slip_pct": 0.02,
          "confidence": "HIGH"
        }
      }
    }
  },
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
- [optimal-order-routing](https://apexrunner.ai/signals/optimal-order-routing)
- [execution-window-optimizer](https://apexrunner.ai/signals/execution-window-optimizer)
- [live-fill-rate](https://apexrunner.ai/signals/live-fill-rate)

---
*APEX Runner — autonomous AI crypto trading signals. [apexrunner.ai](https://apexrunner.ai)*
