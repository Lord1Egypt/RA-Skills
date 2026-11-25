---
name: short-squeeze-fuel
description: "Paid x402 endpoint: $0.014 USDC per call on Base. Returns short-squeeze setups while the squeeze is building: fires only when Hyperliquid cascade risk is 50-80 (above 80 is capitulation-alert's band), top wallets are crowded SHORT >70/100 with their liquidations stacked within 5% above price, and funding is negative; returns a LONG entry zone, target and invalidation (BTC, ETH, SOL)."
metadata:
  openclaw:
    requires:
      env:
        - EVM_PRIVATE_KEY
    primaryEnv: EVM_PRIVATE_KEY
    homepage: https://apexrunner.ai/signals/short-squeeze-fuel
    emoji: "🚀"
---
# short-squeeze-fuel

> **Tier 3 — Strategic Edge**: A composite signal that combines several of APEX Runner's market models into one higher-level reading.

## What It Does
Short-squeeze setups while the squeeze is building: fires only when Hyperliquid cascade risk is 50-80 (above 80 is capitulation-alert's band), top wallets are crowded SHORT >70/100 with their liquidations stacked within 5% above price, and funding is negative; returns a LONG entry zone, target and invalidation (BTC, ETH, SOL). Computed by APEX Runner from live market data, not from backtests.

## When to Use
- Polling every few minutes when funding turns negative for a squeeze entry (alert=false is the usual answer; no_setup_reason says why)
- To fade crowded shorts whose liquidations are stacked within 5% above price while cascade risk is still 50-80
- Paired with capitulation-alert: the two never fire on the same inputs (capitulation covers cascade > 80) — squeeze_risk is an uncalibrated HIGH/MEDIUM heuristic

## How to Use
The agent makes an x402-authenticated GET request to:

```
https://apexrunner.ai/signals/short-squeeze-fuel
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
client.register_policy(max_amount(20000))  # never sign more than the list price ($0.02 USDC)

session = wrapRequestsWithPayment(requests.Session(), client)
response = session.get("https://apexrunner.ai/signals/short-squeeze-fuel")
print(response.json())
```

## Example Response
```json
{
  "coin": "BTC",
  "alert": true,
  "status": "SHORT_SQUEEZE_SETUP",
  "crowded_side": "SHORT",
  "squeeze_direction": "UP",
  "squeeze_risk": "HIGH",
  "contrarian_setup": "LONG",
  "cascade_risk_score": 71,
  "suggested_entry_zone": {
    "low": 57729.3,
    "high": 58090.0
  },
  "target": {
    "price": 59532.9,
    "band_low": 59020.0,
    "band_high": 60310.0,
    "distance_pct": 2.484
  },
  "invalidation_price": 56800.0,
  "reward_to_risk": 1.12,
  "summary": "BTC: top wallets crowded SHORT (crowding 88/100), 88% of near liquidations stacked above price, funding -0.0184%/8h (shorts pay longs). Squeeze risk HIGH. Contrarian LONG 57,729.3-58,090.0, target 59,532.9, invalidation 56,800.0.",
  "method_version": "sqz-1",
  "timestamp": "2026-11-20T20:00:41Z"
}
```

## Pricing
**$0.02/call** — standard price

Every caller is charged $0.014/call until 2027-01-01 under the
early-adopter discount (30% off the standard price). No tier, no wallet
history, no enrolment — that is simply the price.

## Related Signals
- [capitulation-alert](https://apexrunner.ai/signals/capitulation-alert)
- [crowded-trade-detector](https://apexrunner.ai/signals/crowded-trade-detector)
- [liquidation-pressure](https://apexrunner.ai/signals/liquidation-pressure)

---
*APEX Runner — autonomous AI crypto trading signals. [apexrunner.ai](https://apexrunner.ai)*
