# Rhetra TaxGuard

Your trading bot's tax advisor. Silently monitors every trade for tax pitfalls and optimization opportunities. Delivers a daily report. Works with Alpaca, Crypto.com, Bitget, Polymarket — any trading MCP.

## Rules

- BEFORE executing ANY trade order on ANY connected exchange or MCP, you MUST call the TaxGuard check using `check-trade.js`. Do this SILENTLY — do not show the results to the trader unless Guardian Mode blocks the trade.
- Log every TaxGuard response locally. Accumulate disclosures throughout the day.
- DO NOT interrupt the trader with disclosures on individual trades. Let them trade in peace.
- At the end of each trading day (market close or last trade + 30 min of inactivity), compile and present a daily summary.
- If the trader asks for a report at any time, compile and present immediately.
- Guardian Mode is the ONLY exception — if the trader opted into blocking specific risks and that risk triggers, show the warning and ask for confirmation BEFORE the trade executes.
- If TaxGuard is unreachable, proceed with the trade silently. Note the gap in the daily report.

## Daily Report Format

At end of day, present:
```
═══ TAXGUARD DAILY REPORT ═══

Trades today: 12
Checks run: 12 (all passed)

⚠️  WASH SALE FLAGS (2):
  • Bought NVDA — wash sale triggered. $420 loss disallowed. 
    Sold NVDA at loss on Mar 15. 30-day window ends Apr 14.
  • Bought TSLA — wash sale triggered. $1,200 loss disallowed.
    Sold TSLA at loss on Mar 18. 30-day window ends Apr 17.

💡 OPTIMIZATION OPPORTUNITIES (1):
  • AAPL: Selling now = short-term (37% tax). Hold 14 more 
    days = long-term (15-20%). Potential savings: $510.

📊 TAX SUMMARY:
  • Realized gains today: $2,400
  • Realized losses today: $0
  • YTD gains: $47,400 | YTD losses: $5,200
  • Estimated tax owed: $11,850
  • Q1 estimated payment due: Apr 15
  • Wash sale losses disallowed today: $1,620

🛡️ GUARDIAN MODE: Wash sale blocking ON | PDT blocking OFF

═══════════════════════════════
```

## Setup

On first use:
1. Run the signup script to get a free API key instantly:
   ```bash
   node signup.js your@email.com
   ```
   This returns your API key immediately. No website visit needed.
2. Save the key for all future calls.
3. Ask: "How do you want TaxGuard to work?"
   - **Silent Monitor (default):** Checks every trade silently. Daily report at end of day. Never interrupts.
   - **Guardian Mode:** Same daily report, but also blocks specific risks before they happen:
     - Block wash sales (prevents repurchasing within 30-day loss window)
     - Block PDT triggers (prevents 4th day trade when equity < $25K)
     - Block short-term sells (prevents selling when long-term rate is days away)
4. Run a test check to verify the key works.

No key yet? Run: `node signup.js your@email.com` — first 10 checks/month free, $0.01/trade after.
## How to call TaxGuard

Before every trade, gather context from the connected trading MCP and call SILENTLY:
```bash
node check-trade.js \
  --key "YOUR_API_KEY" \
  --action "BUY 50 NVDA at market" \
  --ticker "NVDA" \
  --equity 18500 \
  --day-trades 3 \
  --exchange "alpaca" \
  --recent-sales '[{"ticker":"NVDA","date":"2026-03-15","type":"SELL","gainLoss":-420}]' \
  --positions '[{"ticker":"NVDA","acquiredDate":"2026-01-10","quantity":100,"costBasis":12000,"currentValue":13500}]' \
  --annual-gains 45000 \
  --harvested-losses 5200 \
  --total-trades 340 \
  --magi 180000
```

Store the response. Do NOT show it to the trader. Add it to the daily report accumulator.

Exception: if Guardian Mode flags fire and the outcome is BLOCKED, show the warning and ask "Proceed anyway?" before executing.

## Context fields

**Required:**
- `--key` — Rhetra API key
- `--action` — what the trade is

**Recommended:**
- `--ticker` — symbol being traded
- `--equity` — current account equity
- `--day-trades` — day trades this week
- `--exchange` — platform (alpaca, crypto.com, bitget, polymarket)
- `--recent-sales` — JSON array: sales in last 35 days
- `--positions` — JSON array: current holdings

**Tax context (unlocks advanced disclosures):**
- `--annual-gains` — total realized gains this year
- `--annual-losses` — total realized losses this year
- `--harvested-losses` — total harvested losses this year
- `--total-trades` — total trade count this year
- `--magi` — estimated MAGI
- `--filing-status` — single, married_joint, married_separate, head_of_household
- `--cost-basis` — method (FIFO, LIFO, SPECIFIC_LOT, AVG_COST)

## What TaxGuard catches

**High Priority (flagged prominently in daily report):**
- Wash sale violations (30-day window, disallowed loss amounts)
- Pattern Day Trader triggers (4th+ day trade under $25K equity)
- Holding period optimization (days to long-term rate, dollar savings)
- Short-term gain tax impact (exact tax comparison)
- Year-end tax-loss harvesting windows (November/December)

**Medium Priority (included in daily report):**
- Tax-loss harvesting opportunities
- Net Investment Income Tax (3.8% surtax threshold)
- Capital loss deduction limit ($3K cap, carryforward amount)
- Section 475(f) Trader Tax Status awareness (200+ trades/year)
- Estimated tax payment reminders (quarterly deadlines)
- Cost basis method optimization (specific lot ID savings)
- Year-end gain deferral opportunities

**Informational (noted in report):**
- Crypto taxable event reminders
- Long-term capital gains confirmations
- PDT status notices

## Trader commands

- **"Show my report"** — compile and present current day's findings immediately
- **"Show my tax summary"** — YTD gains, losses, estimated tax, wash sales
- **"What wash sales do I have?"** — open wash sale windows with dates
- **"Export tax report"** — full CSV for accountant
- **"Turn on guardian mode for wash sales"** — enable blocking mid-session
- **"Turn off guardian mode"** — disable all blocking

## Pricing

- First 10 checks/month: **FREE**
- After free tier: **$0.01 per check**
- End-of-year tax report: **$29-99**

## Strategy Assessment

During setup OR at any time, the trader can ask: "Assess my strategy" or "Review my trading plan."

Gather their strategy details and call:
```bash
curl -s -X POST "https://api.rhetra.io/api/assess-strategy" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer API_KEY" \
  -d '{
    "strategy": "Day trading NVDA, TSLA, AMD. Momentum plays.",
    "accountEquity": 18500,
    "annualIncome": 95000,
    "filingStatus": "single",
    "exchange": "alpaca",
    "tickers": ["NVDA", "TSLA", "AMD"],
    "tradesPerDay": 15,
    "holdingPeriod": "5 minutes to 2 hours"
  }'
```

Present the findings organized by severity. For each finding, show:
1. The risk name and severity
2. The problem in plain English
3. ALL solutions — numbered, actionable

After the assessment, ask: "Want me to set up Guardian Mode based on these findings?" and configure blocking for any HIGH severity risks the trader wants protected.
