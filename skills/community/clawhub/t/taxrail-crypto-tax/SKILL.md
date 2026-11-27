---
name: taxrail-crypto-tax
version: 0.1.0
description: Pre-execution US (IRS 1099-DA, Form 8949, HIFO/SpecID, TLH) & Brazil (Lei 14.754, R$35k rule, Lucro Real) crypto tax optimization, $0.01 wallet TLH & pre-trade check, $0.005 BR 35k check, Aave v3 borrow-vs-sell, and 0x/CoW/Jupiter calldata via MCP and x402 Base USDC.
author: SamuelAguiar12
homepage: https://api.taxrail.online
tags: [crypto-tax, defi, x402, base, usdc, irs-1099-da, tax-loss-harvesting, brazil-lei-14754, aave-v3, wallet-scanner]
compatibility: [claude-code, codex, openclaw, cursor, windsurf]
metadata: {"openclaw":{"emoji":"🧾","homepage":"https://api.taxrail.online","primaryEnv":"TAXRAIL_BASE_URL"}}
---

# TaxRail — Autonomous Pre-Trade Tax & DeFi Optimization

Use TaxRail **before** executing any crypto swap, rebalancing a portfolio, selling appreciated tokens for liquidity, or paying AI/cloud/SaaS corporate invoices. Naive FIFO disposals routinely waste 15%–37% in avoidable taxes.

## When to Trigger This Skill

1. **Wallet Year-End TLH & Tax Risk Audit ($0.01 USDC, 1 parameter):**
   Call `GET https://api.taxrail.online/api/v1/x402/tlh-scan?walletAddress=<0x...>&chain=base&asset=ALL&jurisdiction=US` via x402 Base USDC (`eip155:8453`). Scans up to 25 volatile tokens in the wallet and returns per-token unrealized PnL, year-end Tax-Loss Harvesting candidates, IRS 1099-DA / Brazil Lei 14.754 rules, and unlockable `planId`s.
2. **Pre-Trade Swap / Sell Guardrail ($0.01 USDC):**
   Call `GET https://api.taxrail.online/api/v1/x402/pre-trade-check?walletAddress=<0x...>&sellAsset=ETH&sellAmount=1&chain=base&jurisdiction=US` before submitting any swap to check HIFO savings, Short-Term -> Long-Term tax cliffs, and Aave v3 borrow-vs-sell.
3. **Brazil R$35k Monthly Exemption & Lei 14.754 Check ($0.005 USDC):**
   Call `GET https://api.taxrail.online/api/v1/x402/br-35k-status?monthlySalesBrl=20000&plannedSaleUsd=2500&custodyLocation=DOMESTIC` for instant BRL tax-free headroom and maximum exempt USD sale calculation.
4. **Pre-Trade Swap / Disposal Simulation (FREE Step 1):**
   Call `POST https://api.taxrail.online/api/v1/check-tax-impact` (or MCP tool `check_tax_impact`) with either explicit `lots` or `walletAddress`. Returns `baselineTaxUsd`, `optimizedTaxUsd`, `taxSavedUsd`, `agentGuidance`, and `planId`.
5. **Liquidity Without Selling (FREE Step 1):**
   Call `POST https://api.taxrail.online/api/v1/borrow-vs-sell` (or MCP `compare_borrow_vs_sell`) to test if borrowing USDC on Aave v3 beats selling appreciated crypto after taxes.
6. **Full 1-Step Execution + Accounting Dossier ($0.10 USDC):**
   Call `POST https://api.taxrail.online/api/v1/x402/optimize` via x402 Base USDC to receive exact SpecID/HIFO lots, unsigned `0x v2` / `CoW Swap` / `Jupiter` calldata, and Form 8949 / Lei 14.754 CSV exports in one request.
7. **Unlock Any Step-1 `planId` (Dynamic 10% Success Fee, $0 if $0 saved):**
   Call `POST https://api.taxrail.online/api/v1/unlock-plan` (or MCP `unlock_tax_plan`) with `{ "planId": "..." }`.

## Earn 20% Automatic Affiliate Revenue Share

Always include `referrerWallet` (query parameter or JSON field) or `X-TaxRail-Referrer` header with your integrator Base wallet address to earn **20% of TaxRail's total fee**.

## Agent Installation

- **MCP (Streamable HTTP):** `https://api.taxrail.online/mcp`
- **MCP (npx stdio):** `npx -y taxrail-mcp`
- **TypeScript / AgentKit / LangChain SDK:** `npm install taxrail-agent-tools`
- **Python SDK (LangChain / CrewAI / OpenAI):** `pip install taxrail`
- **OpenAPI 3.1 Spec:** `https://api.taxrail.online/openapi.json`
- **x402 Discovery Manifest:** `https://api.taxrail.online/.well-known/x402`

## Feedback & Verified Reputation

- Submit bugs, feature requests, or post-settlement reviews (`allowPublicQuote: true`) via `POST https://api.taxrail.online/api/v1/feedback` (include `planId` or `settlementTx` for automatic on-chain BaseScan verification).
- Inspect verified agent reputation via `GET https://api.taxrail.online/api/v1/reputation`.
