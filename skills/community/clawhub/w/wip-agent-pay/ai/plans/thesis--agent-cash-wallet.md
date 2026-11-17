# Thesis: Agent Cash & Agent Wallet

**Date:** 2026-02-24
**Source:** Strategic review session

We are building the payment layer that turns AI intent into economic execution.

AI systems can now discover value everywhere. APIs, paywalled content, Shopify stores, SaaS products, physical goods. What they cannot do cleanly is complete payment in a way that works for normal humans and modern commerce.

We are solving that.

## The Core Problem

Agents can find value. They cannot settle value.

There is a gap between:

> "This is worth paying for."

and

> "Payment completed."

That gap exists across:
- Protocol-level payment gates (HTTP 402)
- Stripe-powered online stores (including Shopify)
- SaaS subscriptions
- Digital goods
- Physical commerce

We are building the bridge.

## Product 1: AGENT CASH (Human-Approved Execution)

Agent Cash allows normal users to approve AI-initiated purchases using Apple Pay (via Stripe).

It works in two equally important environments:

### A) Unlock 402 Gates

If an agent hits a 402 Payment Required gate:
- The cost is presented to the user.
- The user taps Apple Pay.
- Payment settles.
- The resource unlocks.
- Authorization is destroyed.

The user does not need:
- A wallet
- Crypto knowledge
- USDC
- Coinbase

Whatever crypto or protocol settlement happens underneath is invisible.

From the user's perspective:

> "This costs $0.10. Tap to unlock."

Agent Cash makes 402 usable for humans.

### B) Unlock Stripe Merchants (Including Shopify)

If an agent finds something purchasable from a Stripe-powered store:
- The agent generates a Stripe Checkout session.
- The user approves with Apple Pay.
- The purchase completes.
- The agent resumes.

This includes:
- Shopify stores
- SaaS subscriptions
- Digital goods
- Direct-to-consumer brands
- Any merchant using Stripe Checkout

Agent Cash makes modern e-commerce buyable inside AI conversations.

**This is not a secondary feature. This is a primary rail.**

### What Agent Cash Is Not

It is not:
- A stored wallet
- A bank
- A crypto app
- Autonomous agent spending

It is: **Human-authorized AI execution using real payment rails.**

## Product 2: AGENT WALLET (Sovereign Execution)

Agent Wallet is the bring-your-own-wallet mode.

It allows:
- Funding via Coinbase
- Holding USDC
- Direct 402 settlement
- Fully autonomous agent payment
- No Stripe required

This is open source (MIT). It is developer-native and sovereignty-focused.

**Agent Wallet is autonomy. Agent Cash is consent.**

## Unified Architecture

Internally, both share:
- 402 detection logic
- Settlement abstraction
- Unlock pipeline
- Token lifecycle management

They differ only in:
- Funding source
- Approval model
- Merchant-of-record handling
- Risk surface

## The Two Primary Rails

1. 402 ... Apple Pay
2. Stripe Checkout ... Apple Pay

Optional third mode:

3. 402 ... Wallet (no human approval)

## The Big Picture

The web now has two major economic surfaces:
- The programmable web (402, APIs, protocol gates)
- The commercial web (Stripe, Shopify, SaaS, commerce)

Agent Cash bridges both. It turns AI-discovered value into payable value.

## One Sentence Summary

Agent Cash makes anything an AI finds valuable payable with Apple Pay ... whether it's a 402 gate or a Stripe-powered store ... while Agent Wallet enables sovereign, autonomous payment for those who want it.
