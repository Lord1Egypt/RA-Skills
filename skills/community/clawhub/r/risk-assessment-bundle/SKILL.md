---
name: risk-assessment-bundle
description: "Paid x402 endpoint: $0.007 USDC per call on Base. Returns 4 signals in one call — liquidation pressure + liquidation magnet + portfolio heat + whale sentiment."
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
Bundle: 4 signals in one call — liquidation pressure + liquidation magnet + portfolio heat + whale sentiment. Computed by APEX Runner from live market data, not from backtests.

## When to Use
- Before large position changes
- For periodic risk monitoring
- When building risk dashboards

## How to Use
The agent makes an x402-authenticated GET request to:

```
https://apexrunner.ai/signals/risk-assessment-bundle
```

The x402 client handles payment automatically. No API key, no account, no subscription — just an EVM wallet with USDC on Base mainnet (no ETH needed).

```python
# pip install "x402[evm,requests]"
import os

import requests
from eth_account import Account
from x402 import max_amount, x402ClientSync
from x402.http.clients import wrapRequestsWithPayment
from x402.mechanisms.evm.exact import register_exact_evm_client
from x402.mechanisms.evm.signers import EthAccountSigner

client = x402ClientSync()
register_exact_evm_client(client, EthAccountSigner(Account.from_key(os.environ["EVM_PRIVATE_KEY"])))
client.register_policy(max_amount(10000))  # never sign more than the list price ($0.01 USDC)

session = wrapRequestsWithPayment(requests.Session(), client)
response = session.get("https://apexrunner.ai/signals/risk-assessment-bundle")
print(response.json())
```

## Example Response
```json
{
  "bundle": "risk_assessment",
  "components_delivered": 4,
  "liquidation_pressure": {
    "max_cascade_risk_score": 66,
    "highest_pressure_coin": "ETH",
    "cascade_alert": true,
    "interpretation": "Max cascade risk 66/100 — highest pressure on ETH (LONG_SQUEEZE)",
    "coins": {
      "ETH": {
        "bias": "LONG_SQUEEZE",
        "cascade_risk_score": 66,
        "liq_vol_long_usd": 6236105.0,
        "liq_vol_short_usd": 22049131.01,
        "mark_price": 2685.8,
        "near_liq_long_usd": 6236105.0,
        "near_liq_short_usd": 0,
        "wallets_sampled": 25
      }
    }
  },
  "liquidation_magnet": {
    "coin": "BTC",
    "mark_price": 84734.0,
    "magnet_bias": "DOWN",
    "nearest_long_liq": 96604.33,
    "nearest_short_liq": 83658.29,
    "note": "Price likely pulled toward $83,658 liquidation cluster"
  },
  "portfolio_heat": {
    "action": "Normal trading",
    "inputs": {
      "avg_market_drop_24h": 0,
      "fear_greed": 68
    },
    "market_heat_pct": 0.0,
    "status": "SAFE",
    "thresholds": {
      "caution": 3,
      "critical": 9,
      "high": 6
    }
  },
  "whale_sentiment": {
    "bias": "BEARISH",
    "long_pct": 5.0,
    "short_pct": 95.0,
    "avg_leverage": 5.5,
    "wallets_sampled": 120
  },
  "bundle_savings_pct": 75.0,
  "bundle_note": "4 signals: liquidation_pressure, liquidation_magnet, portfolio_heat and whale_sentiment. oi_divergence is retired (its open-interest data source went offline in July 2026) and is not part of this bundle, its price or its savings.",
  "valid_for_seconds": 300,
  "timestamp": "2026-10-03T23:08:32Z"
}
// liquidation_pressure.coins abridged to ETH; BTC and SOL are returned too
```

## Pricing
**$0.01/call** — standard price

Every caller is charged $0.007/call until 2027-01-01 under the
early-adopter discount (30% off the standard price). No tier, no wallet
history, no enrolment — that is simply the price.

## Related Signals
- [trading-intelligence-bundle](https://apexrunner.ai/signals/trading-intelligence-bundle)
- [portfolio-heat](https://apexrunner.ai/signals/portfolio-heat)
- [agent-stress-index](https://apexrunner.ai/signals/agent-stress-index)

---
*APEX Runner — autonomous AI crypto trading signals. [apexrunner.ai](https://apexrunner.ai)*
