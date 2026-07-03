---
name: trend-confirmed
description: Confirms whether the current trend has sufficient momentum to trade
metadata:
  openclaw:
    requires:
      env:
        - EVM_PRIVATE_KEY
    primaryEnv: EVM_PRIVATE_KEY
    homepage: https://apexrunner.ai/signals/trend-confirmed
    emoji: "✅"
---
# trend-confirmed

## What It Does
Confirms whether the current trend has sufficient momentum to trade. This signal is computed in real time from APEX Runner's live autonomous trading system operating across Kraken, Coinbase Advanced Trade, and Hyperliquid — not from backtests or third-party aggregators.

## When to Use
- Before entering trend-following trades
- To filter false breakout signals
- As a final confirmation gate

## How to Use
The agent makes an x402-authenticated GET request to:

```
https://apexrunner.ai/signals/trend-confirmed
```

The x402 client handles payment authorisation automatically. No API key, no account, no subscription required — just an EVM wallet with USDC on Base mainnet.

```python
# Example using the x402-python client
from x402.client import x402_get

response = x402_get(
    url="https://apexrunner.ai/signals/trend-confirmed",
    private_key=os.environ["EVM_PRIVATE_KEY"]
)
print(response.json())
```

## Example Response
```json
{
  "confirmed": true,
  "direction": "up",
  "strength": 0.74
}
```

## Pricing
**$0.25/call** — standard price

Early adopters automatically receive 30% off ($0.17/call) until 2026-09-21. Discount tiers apply automatically based on wallet call history:
- Early Adopter (0–9 calls): 30% off
- Engaged (10–49 calls): 15% off
- Loyal (50–199 calls): 15% permanent
- VIP (200+ calls): 20% permanent

Check your tier: `https://apexrunner.ai/signals/my-pricing`

## Related Signals
- [momentum-status](https://apexrunner.ai/signals/momentum-status)
- [regime](https://apexrunner.ai/signals/regime)
- [apex-composite](https://apexrunner.ai/signals/apex-composite)

---
*APEX Runner — autonomous AI crypto trading signals. [apexrunner.ai](https://apexrunner.ai)*
