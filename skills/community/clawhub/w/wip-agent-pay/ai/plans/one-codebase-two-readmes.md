# One Codebase, Two READMEs

**Date:** 2026-02-24

---

You are building a single payment engine.

Not:
- Two forks
- Two drifting repos
- Two duplicated systems

Just one core system. But it will present itself through two different product narratives.

---

## Why One Codebase?

Because internally, everything overlaps:
- 402 detection
- Stripe checkout creation
- Wallet settlement
- Payment confirmation
- Unlock execution
- Risk limits
- Chargeback logic
- Session lifecycle

All of that is shared.

Splitting codebases would:
- Duplicate logic
- Create divergence
- Break consistency
- Make AI-assisted development harder
- Introduce settlement bugs

So the engine stays unified.

---

## Why Two READMEs?

Because the audiences are completely different.

### README #1: Agent Cash

This README is for:
- Normal users
- Merchants
- Stripe ecosystem
- Investors
- Non-crypto people

It talks about:
- Apple Pay
- Stripe Checkout
- Shopify
- Unlocking 402
- Human approval
- Consent-based AI execution

It does not emphasize:
- USDC
- Wallet custody
- Coinbase
- Autonomous agents

That's intentional.

### README #2: Agent Wallet

This README is for:
- Developers
- Protocol-native users
- Crypto-native builders
- People who want autonomy

It talks about:
- Bring your own wallet
- Fund via Coinbase
- Direct 402 settlement
- Programmatic autonomy
- Self-custody

It does not emphasize:
- Apple Pay
- Stripe checkout
- Merchant onboarding
- Chargeback management

Also intentional.

---

## The Core Insight

The system underneath is identical. But the mental model is different.

**Agent Cash = Consent**
**Agent Wallet = Sovereignty**

Same engine. Different consent model.

---

## Why This Matters

If you mix the language in one README, people get confused.

If someone sees Apple Pay, USDC, Coinbase, Stripe Connect, wallet custody, and 402 bridge all in one narrative... it feels convoluted. Even though the architecture is clean.

The separation is not technical. It's cognitive.

---

## The Clean Structure

```
/core
    payment-engine.ts
    unlock-flow.ts
    adapters/
        stripe-adapter.ts
        wallet-adapter.ts

README.md            -> Agent Cash
WALLET.md            -> Agent Wallet
```

Same code. Two doors into it.

---

## What This Achieves

- No duplication
- No architectural drift
- Clean contributor experience
- Clear product story
- Clear legal positioning
- Clear investor narrative

You are not building two systems.

You are building one payment abstraction layer with two public faces.
