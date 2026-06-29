---
name: regime-micro
description: Current market regime label at minimal cost for fast agent loops
metadata:
  openclaw:
    requires:
      env:
        - EVM_PRIVATE_KEY
    primaryEnv: EVM_PRIVATE_KEY
    homepage: https://apexrunner.ai/signals/regime-micro
    emoji: "📈"
---
# regime-micro

## What It Does
Current market regime label at minimal cost for fast agent loops. This signal is computed in real time from APEX Runner's live autonomous trading system operating across Kraken, Coinbase Advanced Trade, and Hyperliquid — not from backtests or third-party aggregators.

## When to Use
- In agent loops requiring frequent regime checks
- To skip expensive analysis during stable regimes
- As a pre-filter before calling regime-confluence

## How to Use
The agent makes an x402-authenticated GET request to:

```
https://apexrunner.ai/signals/regime-micro
```

The x402 client handles payment authorisation automatically. No API key, no account, no subscription required — just an EVM wallet with USDC on Base mainnet.

```python
# Example using the x402-python client
from x402.client import x402_get

response = x402_get(
    url="https://apexrunner.ai/signals/regime-micro",
    private_key=os.environ["EVM_PRIVATE_KEY"]
)
print(response.json())
```

## Example Response
```json
{
  "b": "RANGING",
  "e": "TRENDING",
  "s": "CHOPPY",
  "a": "RANGING",
  "t": 1750000000
}
```

## Pricing
**$0.01/call** — standard price

Early adopters automatically receive 30% off ($0.01/call) until 2026-09-21. Discount tiers apply automatically based on wallet call history:
- Early Adopter (0–9 calls): 30% off
- Engaged (10–49 calls): 15% off
- Loyal (50–199 calls): 15% permanent
- VIP (200+ calls): 20% permanent

Check your tier: `https://apexrunner.ai/signals/my-pricing`

## Related Signals
- [regime](https://apexrunner.ai/signals/regime)
- [regime-confluence](https://apexrunner.ai/signals/regime-confluence)
- [trend-confirmed](https://apexrunner.ai/signals/trend-confirmed)

---
*APEX Runner — autonomous AI crypto trading signals. [apexrunner.ai](https://apexrunner.ai)*
