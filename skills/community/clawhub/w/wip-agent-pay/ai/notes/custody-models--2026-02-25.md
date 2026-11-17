# Custody Models: What We Learned

**Date:** 2026-02-25
**Status:** Decision made. Shipping two modes, not three.

---

## The Three Models in the Code

The worker currently has three custody paths:

1. **AI CASH (pool)** ... Parker's USDC, Parker's keys, user pays fiat. We sign x402 from pool wallet.
2. **AGENT WALLET (Privy)** ... User's USDC, our keys. We create a Privy server wallet for them, they fund it, we sign from it. This is custodial.
3. **AGENT WALLET (CDP)** ... User's USDC, user's keys. They bring their own CDP wallet. We relay the signing. Non-custodial.

## The Problem with Privy Path

Mode C (Privy wallet) is custodial. We hold the signing keys. That means:
- Regulatory risk (money transmitter)
- Liability (if keys compromised, user loses funds)
- Trust burden (user trusts us not to drain their wallet)
- Convoluted UX for what it actually does

## Decision: Ship Two, Not Three

**AI CASH** ... pool mode. Parker's float. Apple Pay. $0.25 + card processing. $25 cap.
**AGENT WALLET** ... CDP only. User's wallet, user's keys. No fees. No limits. Sovereign.

Privy path is parked. If we get real traction, it could come back as a feature inside AI CASH: "fund your own Privy wallet to increase your pool limits." But that's a v2 thing, not launch.

## What This Means for the Code

- `/pool/pay` + `/pool/confirm` ... keep (AI CASH)
- `/x402/pay` ... keep (AGENT WALLET, CDP)
- `/privy/pay` ... keep in code but deprioritize, don't document as primary path
- `/wallet/create` + `/wallet/pay` ... keep in code but don't ship in v1 docs
- `/stripe/checkout` ... keep (wallet funding)

## What This Means for the Docs

- **CASH.md** ... pool mode only. Apple Pay. Simple.
- **WALLET.md** ... CDP only. Bring your own wallet. Sovereign.
- No mention of Privy in consumer-facing docs for now.
- SPEC.md can reference Privy as "planned" or "experimental."

## Future Privy Idea (Parked)

"Fund your own Privy wallet inside AI CASH to increase limits." Basically: user starts on pool ($25 cap), wants to buy something bigger, we create them a Privy wallet, they fund it via Coinbase Onramp, our worker signs from it. Still custodial but feels like an upgrade path within AI CASH rather than a separate product.

This only makes sense if people are actually hitting the $25 cap regularly. Don't build it until that happens.
