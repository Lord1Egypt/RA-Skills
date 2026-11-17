---
name: trading-intelligence-bundle
description: "Paid x402 endpoint: $0.007 USDC per call on Base. Returns momentum + whale sentiment + regime confluence."
metadata:
  openclaw:
    requires:
      env:
        - EVM_PRIVATE_KEY
    primaryEnv: EVM_PRIVATE_KEY
    homepage: https://apexrunner.ai/signals/trading-intelligence-bundle
    emoji: "🎁"
---
# trading-intelligence-bundle

## What It Does
Bundle: momentum + whale sentiment + regime confluence. Computed by APEX Runner from live market data, not from backtests.

## When to Use
- For a full trading context in one call
- Before complex multi-factor decisions
- When minimising API call count

## How to Use
The agent makes an x402-authenticated GET request to:

```
https://apexrunner.ai/signals/trading-intelligence-bundle
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
response = session.get("https://apexrunner.ai/signals/trading-intelligence-bundle")
print(response.json())
```

## Example Response
```json
{
  "momentum_status": {"BTC": "active", "ETH": "active", "SOL": "inactive", "AVAX": "inactive"},
  "whale_sentiment": {"sentiment": "bullish", "score": 0.67, "top_traders_long_pct": 72},
  "regime_confluence": {"confluence_score": 0.79, "timeframes_aligned": 3, "dominant_regime": "RANGING"},
  "timestamp": "2026-06-23T14:00:00Z"
  // Full nested output of all component signals returned in one call
}
```

## Pricing
**$0.01/call** — standard price

Every caller is charged $0.007/call until 2027-01-01 under the
early-adopter discount (30% off the standard price). No tier, no wallet
history, no enrolment — that is simply the price.

## Related Signals
- [market-pulse-bundle](https://apexrunner.ai/signals/market-pulse-bundle)
- [risk-assessment-bundle](https://apexrunner.ai/signals/risk-assessment-bundle)
- [apex-composite](https://apexrunner.ai/signals/apex-composite)

---
*APEX Runner — autonomous AI crypto trading signals. [apexrunner.ai](https://apexrunner.ai)*
