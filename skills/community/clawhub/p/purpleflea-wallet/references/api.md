# Purple Flea Public Wallet — API Reference

Source: https://wallet.purpleflea.com
OpenAPI: https://wallet.purpleflea.com/openapi.json
LLMs.txt: https://wallet.purpleflea.com/llms.txt

---

## From llms.txt

# Purple Flea Public Wallet
> Multi-chain HD wallet API for AI agents. Generate wallets, check balances, send, and swap across chains. No KYC. Non-custodial. Pure API.

## What This Does
AI agents create non-custodial BIP-39 HD wallets with one API key. Manage crypto across 6 chains. Cross-chain swaps via Wagyu aggregator.

## Supported Chains
- Wallet generation: Ethereum, Base, Solana, Bitcoin, Tron, Monero
- Balance check + send: Ethereum, Base, Solana, Bitcoin, Tron, Monero (XMR requires view_key for balance, spend_key for send)
- Cross-chain swaps: Ethereum, Base, BSC, Arbitrum, Solana, Bitcoin, Monero, HyperEVM

## Quick Start
```bash
# 1. Register
curl -X POST https://wallet.purpleflea.com/v1/auth/register -H "Content-Type: application/json" -d '{}'

# 2. Create HD wallet (mnemonic shown ONCE — save it securely)
curl -X POST https://wallet.purpleflea.com/v1/wallet/create \
  -H "Authorization: Bearer pk_live_..."

# 3. Check balance (Base USDC)
curl "https://wallet.purpleflea.com/v1/wallet/balance/0xYourAddress?chain=base" \
  -H "Authorization: Bearer pk_live_..."

# 4. Cross-chain swap quote (Base USDC → Solana USDC)
curl "https://wallet.purpleflea.com/v1/wallet/swap/quote?from_chain=base&to_chain=solana&from_token=0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913&to_token=EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v&amount=50" \
  -H "Authorization: Bearer pk_live_..."

# 5. Execute swap
curl -X POST https://wallet.purpleflea.com/v1/wallet/swap \
  -H "Authorization: Bearer pk_live_..." \
  -H "Content-Type: application/json" \
  -d '{"from_chain":"base","to_chain":"solana","from_token":"0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913","to_token":"EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v","amount":"50","to_address":"YourSolAddress"}'
```

## Referral Program — Earn Passive Income
Earn 10% of swap fees from agents you refer. **3-level deep:**
- Level 1 (direct): 10% of fees
- Level 2: 5% of fees
- Level 3: 2.5% of fees

## Swap Fee Structure
0.5% integrator fee on every swap via Wagyu. 10% of fees paid out to referrers.

## All Endpoints
- GET /health — health check (no auth)
- GET /v1/gossip — passive income info + live agent count (no auth)
- POST /v1/auth/register — create account + API key (no auth)
- POST /v1/wallet/create — generate HD wallet (mnemonic shown ONCE)
- GET /v1/wallet/balance/:address?chain= — on-chain balance
- GET /v1/wallet/deposit-address?chain= — derivation path + how to get your address
- GET /v1/wallet/transactions/:address?chain= — transaction history
- POST /v1/wallet/send — sign + broadcast transaction { chain, to, amount, private_key, token? }
- GET /v1/wallet/swap/quote — get swap quote with fee breakdown
- POST /v1/wallet/swap — execute cross-chain swap
- GET /v1/wallet/swap/status/:orderId — check swap status
- GET /v1/wallet/chains — list supported chains
- GET /v1/referral/code — your referral code
- GET /v1/referral/stats — referral earnings (3 levels)
- POST /v1/referral/withdraw — withdraw earnings { address, chain? }

## Security
Non-custodial: mnemonics and private keys are NEVER stored server-side. Save your mnemonic securely — it cannot be recovered.

---

## OpenAPI Spec (openapi.json)

```json
{
  "openapi": "3.0.0",
  "info": {
    "title": "Purple Flea Public Wallet",
    "version": "1.0.0",
    "description": "Multi-chain HD wallet API for AI agents. Non-custodial BIP-39 wallets, on-chain balances, send, and cross-chain swaps via Wagyu."
  },
  "servers": [{ "url": "https://wallet.purpleflea.com" }],
  "security": [{ "bearerAuth": [] }],
  "components": {
    "securitySchemes": {
      "bearerAuth": {
        "type": "http",
        "scheme": "bearer",
        "description": "API key from POST /v1/auth/register"
      }
    }
  }
}
```

### Key Paths
- `POST /v1/auth/register` — `{ referral_code? }` → API key
- `POST /v1/wallet/create` → mnemonic (ONCE) + addresses for all chains
- `GET /v1/wallet/balance/{address}?chain=&view_key=` → balance
- `POST /v1/wallet/send` → `{ chain, to, amount, private_key?, token?, from?, view_key?, spend_key? }`
- `GET /v1/wallet/swap/quote?from_chain=&to_chain=&from_token=&to_token=&amount=`
- `POST /v1/wallet/swap` → `{ from_chain, to_chain, from_token, to_token, amount, to_address }`
- `GET /v1/wallet/swap/status/{orderId}`
- `GET /v1/wallet/transactions/{address}?chain=&limit=`
- `GET /v1/referral/code` / `GET /v1/referral/stats` / `POST /v1/referral/withdraw`

Full OpenAPI JSON: https://wallet.purpleflea.com/openapi.json
