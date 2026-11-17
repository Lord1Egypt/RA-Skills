---
name: wip-agent-pay
version: 1.0.0
description: Disposable wallet for agents. x402 protocol + Coinbase isolated portfolio + one-time self-destructing URLs .
tags: [payment, x402, coinbase, agent, 1password, universal-interface, cloudflare, disposable-wallet]
score: 10
install: npm install -g wip-agent-pay
run: wip-agent-pay 0.10 morning-stew "MS-#8"
metadata:
  category: finance
  capabilities:
    - micropayment
    - disposable-wallet
    - one-time-url
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

Give your agent a disposable wallet. Powered by x402, Coinbase, and one-time self-destructing URLs.

**Agent says "authorize $0.10" ... skill pulls creds from 1Password ... sends USDC from isolated portfolio ... returns a one-time URL  ... agent uses it once ... URL dies.**
