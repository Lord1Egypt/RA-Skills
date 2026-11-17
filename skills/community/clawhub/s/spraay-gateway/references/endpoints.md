# Spraay Gateway — endpoint examples

Base URL: `https://gateway.spraay.app`
Full catalog (190 endpoints, 37 categories): https://docs.spraay.app

Auth for subscribed calls: `X-API-Key: $SPRAAY_API_KEY` header
(key by email after Stripe checkout — Starter: https://buy.stripe.com/5kQcN675ndDa41Pce7enS00 · Pro: https://buy.stripe.com/28EcN60GZ56EdCp91VenS01)

## Free endpoints (no key, no payment)

### Validate a batch payout (dry run — always do this before executing)

```bash
curl -sS -X POST "https://gateway.spraay.app/free/validate-batch" \
  -H "Content-Type: application/json" \
  -d '{
    "chain": "base",
    "token": "USDC",
    "recipients": [
      {"address": "0x...", "amount": "25.00"},
      {"address": "0x...", "amount": "40.50"}
    ]
  }'
```

### Estimate fees and batch savings

```bash
curl -sS "https://gateway.spraay.app/free/estimate-batch?chain=base&token=USDC&recipients=47"
```

### Token prices (ETH/USDC/SOL spot feed)

```bash
curl -sS "https://gateway.spraay.app/free/prices"
```

Per-call x402 pricing for any paid endpoint: call it without payment and read
the `accepts[].amount` in the 402 response (USDC base units, e.g. `8000` = $0.008).

### Chain status

```bash
curl -sS "https://gateway.spraay.app/free/chain-status"
```

## Paid endpoints (subscription key or x402 per call)

> Endpoints marked MOVES FUNDS require the human-approval flow in SKILL.md:
> dry run first, plain-language preview, explicit user confirmation.

### Execute a batch payout — MOVES FUNDS

```bash
curl -sS -X POST "https://gateway.spraay.app/api/v1/batch/execute" \
  -H "X-API-Key: $SPRAAY_API_KEY" \
  -H "Content-Type: application/json" \
  -d @confirmed-batch.json
```

### Create an escrow — MOVES FUNDS

```bash
curl -sS -X POST "https://gateway.spraay.app/api/v1/escrow/create" \
  -H "X-API-Key: $SPRAAY_API_KEY" \
  -H "Content-Type: application/json" \
  -d @confirmed-escrow.json
```

### Token registry (currently open, no auth required)

```bash
# Supported tokens, batch contract, fee (0.3%), 200-recipient max
curl -sS "https://gateway.spraay.app/api/v1/tokens"
```

### Read-only paid endpoints (key or x402; a call without either returns 402)

```bash
# Balances (read-only; uses a public address, never a private key)
curl -sS -H "X-API-Key: $SPRAAY_API_KEY" \
  "https://gateway.spraay.app/api/v1/balances?address=$SPRAAY_WALLET_ADDRESS&chain=base"

# RTP robot registry
curl -sS -H "X-API-Key: $SPRAAY_API_KEY" "https://gateway.spraay.app/api/v1/robots/list"
```

### Check key validity and daily usage

```bash
curl -sS -H "X-API-Key: $SPRAAY_API_KEY" "https://gateway.spraay.app/api/v1/usage"
# 200 = key valid (body shows today's call count vs. quota) ; 401 = invalid key
```

## On-chain reference

- Spraay batch contract (Base): `0x1646452F98E36A3c9Cfc3eDD8868221E207B5eEC`
- Signing always happens in the user's own wallet tooling. This skill and the
  gateway never handle private keys.
