---
name: volume-analysis
description: Volume profile analysis detecting accumulation or distribution patterns
metadata:
  openclaw:
    requires:
      env:
        - EVM_PRIVATE_KEY
    primaryEnv: EVM_PRIVATE_KEY
    homepage: https://apexrunner.ai/signals/volume-analysis
    emoji: "📉"
---
# volume-analysis

## What It Does
Volume profile analysis detecting accumulation or distribution patterns. This signal is computed in real time from APEX Runner's live autonomous trading system operating across Kraken, Coinbase Advanced Trade, and Hyperliquid — not from backtests or third-party aggregators.

## When to Use
- To confirm breakouts with volume
- To detect accumulation/distribution
- Before momentum entries

## How to Use
The agent makes an x402-authenticated GET request to:

```
https://apexrunner.ai/signals/volume-analysis
```

The x402 client handles payment authorisation automatically. No API key, no account, no subscription required — just an EVM wallet with USDC on Base mainnet.

```python
# Example using the x402-python client
from x402.client import x402_get

response = x402_get(
    url="https://apexrunner.ai/signals/volume-analysis",
    private_key=os.environ["EVM_PRIVATE_KEY"]
)
print(response.json())
```

## Example Response
```json
{
  "signal": "accumulation",
  "volume_ratio": 1.34,
  "above_average": true
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
- [momentum-status](https://apexrunner.ai/signals/momentum-status)
- [trend-confirmed](https://apexrunner.ai/signals/trend-confirmed)
- [bb-analysis](https://apexrunner.ai/signals/bb-analysis)

---
*APEX Runner — autonomous AI crypto trading signals. [apexrunner.ai](https://apexrunner.ai)*
