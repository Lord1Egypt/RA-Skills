---
name: regime-transition
description: Detects imminent regime transitions before they fully materialise
metadata:
  openclaw:
    requires:
      env:
        - EVM_PRIVATE_KEY
    primaryEnv: EVM_PRIVATE_KEY
    homepage: https://apexrunner.ai/signals/regime-transition
    emoji: "🔄"
---
# regime-transition

## What It Does
Detects imminent regime transitions before they fully materialise. This signal is computed in real time from APEX Runner's live autonomous trading system operating across Kraken, Coinbase Advanced Trade, and Hyperliquid — not from backtests or third-party aggregators.

## When to Use
- To anticipate strategy pivots
- Before a regime shift reduces edge
- To reduce exposure ahead of uncertainty

## How to Use
The agent makes an x402-authenticated GET request to:

```
https://apexrunner.ai/signals/regime-transition
```

The x402 client handles payment authorisation automatically. No API key, no account, no subscription required — just an EVM wallet with USDC on Base mainnet.

```python
# Example using the x402-python client
from x402.client import x402_get

response = x402_get(
    url="https://apexrunner.ai/signals/regime-transition",
    private_key=os.environ["EVM_PRIVATE_KEY"]
)
print(response.json())
```

## Example Response
```json
{
  "transition_likely": false,
  "probability": 0.22,
  "target_regime": "TRENDING"
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
- [regime](https://apexrunner.ai/signals/regime)
- [regime-confluence](https://apexrunner.ai/signals/regime-confluence)
- [regime-transition-probability](https://apexrunner.ai/signals/regime-transition-probability)

---
*APEX Runner — autonomous AI crypto trading signals. [apexrunner.ai](https://apexrunner.ai)*
