# Rhetra TaxGuard

**Your trading bot's tax advisor.**

Every trade checked. Wash sales caught. Tax savings found. Daily report delivered. One penny per trade.

---

## The Problem

Your trading bot doesn't know tax law. It buys and sells based on your strategy — but it has no idea that buying NVDA back 12 days after selling it at a loss just disallowed that loss on your tax return. It doesn't know that your 4th day trade this week triggers a 90-day account restriction. It doesn't know that holding for 11 more days saves you $1,200 in taxes.

You find out in March when your accountant calls.

## The Solution

TaxGuard silently monitors every trade your bot makes. It checks each one against IRS wash sale rules, FINRA pattern day trader regulations, capital gains law, and your own trading constraints. It never interrupts you. At the end of each trading day, you get a report.

## What You Get

**Daily Report:**
- Wash sale flags with dollar amounts and days remaining
- PDT status tracking
- Holding period optimizations ("hold 11 more days, save $1,200")
- Short-term vs long-term gain calculations
- Tax-loss harvesting opportunities
- Estimated quarterly tax payment reminders
- Net Investment Income Tax warnings
- Section 475(f) Trader Tax Status awareness

**Strategy Assessment:**
- Describe your strategy before you start
- Get a full tax risk assessment with severity ratings
- Every problem comes with actionable solutions

**Guardian Mode (opt-in):**
- Choose specific risks to block: wash sales, PDT, short-term sells
- Your choice, your rules — default is monitor-only

**Year-End Tax Report:**
- Full audit trail of every trade with tax treatment
- Form 8949 ready data
- Wash sale adjustments calculated
- Cost basis tracking across all trades

## Works With

Alpaca · Crypto.com · Bitget · Polymarket · any trading MCP

## Pricing

| | |
|---|---|
| First 10 checks/month | **Free** |
| After free tier | **$0.01 per check** |
| Year-end tax report | **$29-99** |

One penny per trade. A single wash sale can cost you thousands.

## Setup

1. Install the skill
2. Enter your API key (get one free at rhetra.io/trading)
3. Choose Monitor Only or Guardian Mode
4. Trade normally — TaxGuard handles the rest

## How It Works
```
Your Agent → TaxGuard (silent check) → Trade Executes
                 ↓
         Decision logged
                 ↓
         Daily report at market close
```

TaxGuard checks every trade against:
- **Layer 1:** Federal tax law (IRS, FINRA, SEC) — wash sales, PDT, capital gains, Reg SHO
- **Layer 3:** Your trading constraints — tickers, position limits, risk rules

## Built By

Rhetra — compliance infrastructure for AI agents. Backed by a structured regulatory corpus with real statutory citations. Every disclosure references the actual law.

rhetra.io
