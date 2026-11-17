---
name: wip-agent-pay
version: "1.0.2"
description: Give your agent a wallet. Fund with Apple Pay. Pay for paywalled content. x402 native.
tags: [payment, x402, coinbase, privy, stripe, apple-pay, agent, 1password, universal-interface, cloudflare]
score: 10
install: npm install -g wip-agent-pay
run: wip-agent-pay pay <url>
metadata:
  category: finance
  capabilities:
    - x402-payment
    - apple-pay-funding
    - one-time-url
    - micropayment
  wallets:
    - coinbase-cdp
    - privy
  funding:
    - stripe
    - manual
  interface: CLI + Module + MCP + OpenClaw Plugin + Skill
  requires:
    binaries: [node]
openclaw:
  emoji: "💳"
  install:
    env: []
author:
  name: Parker Todd Brooks
---

# wip-agent-pay

Give your agent a wallet. Fund it with Apple Pay. Let it buy things for you.

**Fund:** User taps Face ID. Money goes in. No crypto required.

**Pay:** Agent hits a paywalled URL. Wallet handles payment. Content returned.

**Mint:** One-time self-destructing URLs. Use once, gone forever.

Three wallets (Coinbase CDP, Privy). One funding on-ramp (Stripe / Apple Pay). x402 native.
