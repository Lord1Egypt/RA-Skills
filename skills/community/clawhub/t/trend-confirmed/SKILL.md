---
name: trend-confirmed
description: "Paid x402 endpoint: $0.007 USDC per call on Base. Returns confirms whether the current trend has sufficient momentum to trade."
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
Confirms whether the current trend has sufficient momentum to trade. Computed by APEX Runner from live market data, not from backtests.

## When to Use
- Before entering trend-following trades
- To filter false breakout signals
- As a final confirmation gate

## How to Use
The agent makes an x402-authenticated GET request to:

```
https://apexrunner.ai/signals/trend-confirmed
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
response = session.get("https://apexrunner.ai/signals/trend-confirmed")
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
**$0.01/call** — standard price

Every caller is charged $0.007/call until 2027-01-01 under the
early-adopter discount (30% off the standard price). No tier, no wallet
history, no enrolment — that is simply the price.

## Related Signals
- [regime](https://apexrunner.ai/signals/regime)
- [apex-composite](https://apexrunner.ai/signals/apex-composite)

---
*APEX Runner — autonomous AI crypto trading signals. [apexrunner.ai](https://apexrunner.ai)*
