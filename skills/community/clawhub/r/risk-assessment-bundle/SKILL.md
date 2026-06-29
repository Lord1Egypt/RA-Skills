---
name: risk-assessment-bundle
description: Bundle: portfolio heat + liquidation pressure + position exposure
metadata:
  openclaw:
    requires:
      env:
        - EVM_PRIVATE_KEY
    primaryEnv: EVM_PRIVATE_KEY
    homepage: https://apexrunner.ai/signals/risk-assessment-bundle
    emoji: "📋"
---
# risk-assessment-bundle

## What It Does
Bundle: portfolio heat + liquidation pressure + position exposure. This signal is computed in real time from APEX Runner's live autonomous trading system operating across Kraken, Coinbase Advanced Trade, and Hyperliquid — not from backtests or third-party aggregators.

## When to Use
- Before large position changes
- For periodic risk monitoring
- When building risk dashboards

## How to Use
The agent makes an x402-authenticated GET request to:

```
https://apexrunner.ai/signals/risk-assessment-bundle
```

The x402 client handles payment authorisation automatically. No API key, no account, no subscription required — just an EVM wallet with USDC on Base mainnet.

```python
# Example using the x402-python client
from x402.client import x402_get

response = x402_get(
    url="https://apexrunner.ai/signals/risk-assessment-bundle",
    private_key=os.environ["EVM_PRIVATE_KEY"]
)
print(response.json())
```

## Example Response
```json
{
  "portfolio_heat": {"heat_level": "elevated", "heat_score": 0.61, "action": "pause new entries"},
  "liquidation_pressure": {"pressure_score": 0.48, "at_risk_usd": 120000000, "level": "moderate"},
  "position_exposure": {"total_deployed_usd": 1840, "by_pair": {"BTC": 620, "ETH": 480, "SOL": 420, "AVAX": 320}, "exposure_pct": 61},
  "timestamp": "2026-06-23T14:00:00Z"
  // Full nested output of all component signals returned in one call
}
```

## Pricing
**$2.00/call** — standard price

Early adopters automatically receive 30% off ($1.40/call) until 2026-09-21. Discount tiers apply automatically based on wallet call history:
- Early Adopter (0–9 calls): 30% off
- Engaged (10–49 calls): 15% off
- Loyal (50–199 calls): 15% permanent
- VIP (200+ calls): 20% permanent

Check your tier: `https://apexrunner.ai/signals/my-pricing`

## Related Signals
- [trading-intelligence-bundle](https://apexrunner.ai/signals/trading-intelligence-bundle)
- [portfolio-heat](https://apexrunner.ai/signals/portfolio-heat)
- [agent-stress-index](https://apexrunner.ai/signals/agent-stress-index)

---
*APEX Runner — autonomous AI crypto trading signals. [apexrunner.ai](https://apexrunner.ai)*
