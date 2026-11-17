---
name: regime-micro
description: "Paid x402 endpoint: $0.007 USDC per call on Base. Returns current market regime label at minimal cost for fast agent loops."
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
Current market regime label at minimal cost for fast agent loops. Computed by APEX Runner from live market data, not from backtests.

## When to Use
- In agent loops requiring frequent regime checks
- To skip expensive analysis during stable regimes
- As a pre-filter before calling regime-confluence

## How to Use
The agent makes an x402-authenticated GET request to:

```
https://apexrunner.ai/signals/regime-micro
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
response = session.get("https://apexrunner.ai/signals/regime-micro")
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

Every caller is charged $0.007/call until 2027-01-01 under the
early-adopter discount (30% off the standard price). No tier, no wallet
history, no enrolment — that is simply the price.

## Related Signals
- [regime](https://apexrunner.ai/signals/regime)
- [regime-confluence](https://apexrunner.ai/signals/regime-confluence)
- [trend-confirmed](https://apexrunner.ai/signals/trend-confirmed)

---
*APEX Runner — autonomous AI crypto trading signals. [apexrunner.ai](https://apexrunner.ai)*
