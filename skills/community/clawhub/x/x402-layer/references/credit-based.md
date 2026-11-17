# Credit-Based Access

For high-frequency or latency-sensitive API calls. Pre-purchase credits once, then consume instantly without a blockchain signature on every request.

## Why Use Credits?

- Zero latency (no blockchain wait)
- Zero gas fees per request
- One free wallet signature per request (no transaction)
- Better fit for repeated calls than a per-request paywall

## Usage

### Check Balance
```bash
curl "https://api.x402layer.cc/api/credits/balance?endpoint=<slug>" \
  -H "x-wallet-address: 0xYourWallet..."
```

### Consume Endpoint (signed)

Spending credits must be signed by the wallet that owns them. A bare `x-wallet-address`
header is not enough: balances are public, so the gateway rejects an unsigned spend with
`401 wallet_signature_required`. Signing is a free `signMessage`, not a transaction.

Build this message (lines joined with `\n`) and sign it with the wallet:

```text
X402-CREDITS-AUTH
v1
<base|solana>
<address: lowercase 0x for EVM, exact base58 for Solana (never lowercase)>
<METHOD>
<path + query exactly as sent, e.g. /e/<slug>?useCredits=1>
<sha256 hex of the raw request body; empty body = sha256 of "">
<unix timestamp in ms, valid for 5 minutes>
<nonce: 8-128 chars of A-Z a-z 0-9 _ -, single use>
```

- EVM: EIP-191 `personal_sign`, hex signature.
- Solana: ed25519 `signMessage` over the UTF-8 bytes, base64 signature.

Send it as headers:

```text
x-wallet-address: <address>
X-Auth-Address: <address>
X-Auth-Chain: base | solana
X-Auth-Signature: <signature>
X-Auth-Timestamp: <ms>
X-Auth-Nonce: <nonce>
X-Auth-Sig-Encoding: hex | base64
```

Each nonce works once, so sign every request. `consume_credits.py` does all of this.

### Insufficient Credits Response
When out of credits, you get a 402 with purchase options:

```json
{
  "error": "Insufficient credits",
  "current_balance": 0,
  "purchase_url": "https://studio.x402layer.cc/pay/credits/<slug>",
  "credit_package": {"size": 69, "price": 0.01},
  "accepts": [...]
}
```

## Purchasing Credits

Use the standard 402 flow on the `purchase_url` or the hosted credits page:

1. GET the purchase URL
2. Parse 402 challenge  
3. Sign EIP-712 payment
4. Send with X-Payment header
5. Credits added to wallet

Hosted path pattern:

```text
https://studio.x402layer.cc/pay/credits/<slug>
```

## Example Python

```python
import requests
from consume_credits import build_credits_auth_headers, resolve_wallet

def call_with_credits(url, data):
    chain, wallet = resolve_wallet()          # from WALLET_ADDRESS/PRIVATE_KEY or SOLANA_SECRET_KEY
    req = requests.Request("POST", url, json=data).prepare()
    req.headers.update(build_credits_auth_headers(chain, wallet, "POST", req.path_url, req.body or b""))
    resp = requests.Session().send(req, timeout=30)

    if resp.status_code == 402:
        print("Need credits!", resp.json()["purchase_url"])
        return None

    return resp.json()
```

## Scripts

- `check_credits.py` - Query balance
- `consume_credits.py` - Use credits
- `recharge_credits.py` - Top up via payment
