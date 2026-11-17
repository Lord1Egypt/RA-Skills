---
name: witnos-wallet-intel
description: Profile any Base/EVM wallet or x402 buyer before you pay, front, or extend it credit. Returns an onchain wallet score, whale detection, address risk, behavioral cluster, and a named x402 spend graph (who this wallet actually pays and how much). Use when about to receive from, pay, or extend service to an unfamiliar counterparty and you need to know what kind of actor it is.
license: MIT
---

# Witnos: onchain wallet intelligence before you transact

## Overview
Before you extend credit, front work, price a service, or trust a counterparty, profile its wallet. Witnos reads the Base settlement graph at the intent layer (the EIP-3009 authorizer, not the on-chain relayer), so it sees who an address really is: a whale buyer, a fresh wallet, a relayer, or a treasury. By Crest Deployment Systems LLC.

## When to use
- A new buyer/counterparty wants your service on credit or net terms: profile it first.
- You are pricing or gating by customer quality: check the whale score and behavioral cluster.
- You are about to pay an address and want its risk and real spend history.
- You are building an index, marketplace, or risk product and need per-wallet intelligence.

## The call (paid, x402)
`GET https://data.crestsystems.ai/data/wallet/{address}` — $0.90 USDC via x402 on Base. No API keys, no subscription.

Returns:
- `whale_score` (0-1), `is_whale`, `behavior` cluster (e.g. premium_buyer), `risk_level`, `confidence`
- `profile`: total_payments, total_spent_usdc, active_days, avg_payment_usdc, repeat_rate, services_used, premium_ratio, spending_trend
- `top_services`: the named services this wallet actually pays, with calls and spend
- `temporal`: peak activity hour, most active day, payments per day

## Cheaper adjacent checks
- `GET https://data.crestsystems.ai/data/service-trust/{address}` — $0.50 — counterparty trust check for an x402 service receiver: trust score, grade, SPEND / CAUTION / DO NOT SPEND, buyer reach, and flow-role (real service vs relayer vs treasury transfer).
- `GET https://data.crestsystems.ai/data/x402-market` — free — de-noised census of the x402 economy (real services vs relayers vs treasury transfers).

## Why it is different
Every directory counts relayer and treasury volume as service revenue. Witnos separates real services from the rails and transfers that miscount as demand, because it attributes settlement to the intent-layer authorizer, not the on-chain sender. That is a read no explorer or directory gives you.

## How to interpret
- High whale_score + low risk + premium_buyer cluster: a real, valuable, repeat-spending counterparty. Safe to extend service.
- Fresh wallet, no spend history, or relayer/treasury flow-role: no track record. Absence of history is not proof of risk, but nothing vouches for it — treat as unverified.

Educational onchain intelligence, not financial advice. Verify before you transact.
