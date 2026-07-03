---
name: token-unlock
description: Upcoming token unlock events that may create sell pressure
metadata:
  openclaw:
    requires:
      env:
        - EVM_PRIVATE_KEY
    primaryEnv: EVM_PRIVATE_KEY
    homepage: https://apexrunner.ai/signals/token-unlock
    emoji: "🔓"
---
# token-unlock

## What It Does
Upcoming token unlock events that may create sell pressure. This signal is computed in real time from APEX Runner's live autonomous trading system operating across Kraken, Coinbase Advanced Trade, and Hyperliquid — not from backtests or third-party aggregators.

## When to Use
- To avoid buying into upcoming sell pressure
- For fundamental risk filtering
- As a macro risk overlay

## How to Use
The agent makes an x402-authenticated GET request to:

```
https://apexrunner.ai/signals/token-unlock
```

The x402 client handles payment authorisation automatically. No API key, no account, no subscription required — just an EVM wallet with USDC on Base mainnet.

```python
# Example using the x402-python client
from x402.client import x402_get

response = x402_get(
    url="https://apexrunner.ai/signals/token-unlock",
    private_key=os.environ["EVM_PRIVATE_KEY"]
)
print(response.json())
```

## Example Response
```json
{
  "upcoming_unlocks": [{"token": "ARB", "date": "2026-07-01", "usd_value": 42000000}]
}
```

## Pricing
**$0.75/call** — standard price

Early adopters automatically receive 30% off ($0.52/call) until 2026-09-21. Discount tiers apply automatically based on wallet call history:
- Early Adopter (0–9 calls): 30% off
- Engaged (10–49 calls): 15% off
- Loyal (50–199 calls): 15% permanent
- VIP (200+ calls): 20% permanent

Check your tier: `https://apexrunner.ai/signals/my-pricing`

## Related Signals
- [oi-divergence](https://apexrunner.ai/signals/oi-divergence)
- [narrative-intelligence](https://apexrunner.ai/signals/narrative-intelligence)
- [regime](https://apexrunner.ai/signals/regime)

---
*APEX Runner — autonomous AI crypto trading signals. [apexrunner.ai](https://apexrunner.ai)*
