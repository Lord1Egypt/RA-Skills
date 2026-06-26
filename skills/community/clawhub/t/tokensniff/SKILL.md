---
name: tokensniff
description: >
  Analyzes memecoins and altcoins for early entry opportunities, whale accumulation signals,
  and strong momentum before major price moves. Use this skill whenever the user asks about:
  finding early memecoins, tracking whale wallets, detecting pre-pump signals, analyzing
  token momentum, spotting altcoin opportunities, checking if whales are entering a coin,
  evaluating memecoin safety, or any request involving "alpha", "early gems", "100x coins",
  "whale tracking", "on-chain signals", "degen plays", "pump detection", or similar crypto
  discovery/analysis tasks. Always trigger for any query about new token launches, DEX
  screener analysis, or wallet concentration checks.
---

# 🔍 TokenSniff

A skill for detecting early memecoin and altcoin opportunities **before** whale entry,
identifying strong momentum signals, and scoring token safety — all from on-chain data.

---

## What This Skill Does

Given a **token name, ticker, or contract address**, produce a structured Alpha Report covering:

1. **Early Discovery Score** — How early are we? Mcap, age, holder count
2. **Whale Accumulation Signal** — Are smart wallets quietly buying?
3. **Momentum Score** — Volume/Mcap ratio, price action, social buzz
4. **Safety Audit** — Rug pull risk, honeypot check, liquidity status
5. **Overall Alpha Score** — Composite 0–100 score with BUY/WATCH/AVOID verdict

---

## Output Format

Always respond with this structured report:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 ALPHA REPORT: [TOKEN NAME] ($TICKER)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📍 BASIC INFO
• Contract: [address]
• Chain: [Solana / ETH / BSC / Base]
• Age: [X hours/days]
• Market Cap: $[X]
• Price: $[X]
• Liquidity: $[X]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 EARLY DISCOVERY SCORE: [X/25]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Token Age:          [✅ <72h / ⚠️ <1wk / ❌ older]
• Market Cap:         [✅ <$500K / ⚠️ <$5M / ❌ >$5M]
• Holder Count:       [✅ <500 / ⚠️ <2000 / ❌ >2000]
• Holder Growth Rate: [✅ Fast / ⚠️ Moderate / ❌ Slow]
• DEX Listing:        [✅ 1 DEX / ⚠️ 2-3 / ❌ Major CEX listed]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🐋 WHALE ACCUMULATION SIGNAL: [X/25]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Smart Wallet Activity:     [✅ Detected / ⚠️ Unclear / ❌ None]
• Top 10 Holder Behavior:    [✅ Holding / ⚠️ Mixed / ❌ Dumping]
• Exchange Outflows:         [✅ Moving to wallets / ❌ Inflows]
• Wallet Concentration:      [✅ Distributed / ⚠️ Moderate / ❌ Concentrated]
• Buy Wall Formation:        [✅ Yes / ⚠️ Weak / ❌ None]

Key Wallets to Watch:
  🔹 [wallet short address] — accumulated [X]% in last [Xh]
  🔹 [wallet short address] — known alpha wallet, entered [X] ago

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📈 MOMENTUM SCORE: [X/25]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Volume/Mcap Ratio:    [✅ >0.5 / ⚠️ 0.1-0.5 / ❌ <0.1]
• 24h Volume Change:    [+X%]
• Price Action:         [✅ Consolidating / ⚠️ Pumped / ❌ Dumping]
• Social Mentions:      [✅ Rising quietly / ⚠️ Already viral / ❌ Dead]
• Organic Buy Pressure: [✅ High / ⚠️ Medium / ❌ Bot-driven]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🛡️ SAFETY AUDIT: [X/25]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Honeypot Check:        [✅ SAFE / ❌ HONEYPOT DETECTED]
• Mint Authority:        [✅ Revoked / ❌ Active — DANGER]
• Liquidity Lock:        [✅ Locked >30d / ⚠️ Short lock / ❌ Unlocked]
• Dev Wallet % Supply:   [✅ <5% / ⚠️ 5-15% / ❌ >15%]
• Contract Verified:     [✅ Yes / ❌ No]
• Freeze Authority:      [✅ Disabled / ❌ Active — DANGER]

🚨 RED FLAGS: [list any or "None detected"]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏆 OVERALL ALPHA SCORE: [X/100]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Score Emoji + Verdict]
  🟢 80-100 = STRONG BUY — Early + Safe + Whales accumulating
  🟡 60-79  = WATCH CLOSELY — Good signals, wait for confirmation
  🟠 40-59  = HIGH RISK — Some red flags, small position only
  🔴 0-39   = AVOID — Too risky or too late

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 ALPHA SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[2-3 sentence plain-English summary of what the data shows and what action to consider]

⚠️ Entry Strategy:
  • Suggested entry: [price range or "wait for X"]
  • Take profit targets: [X%, X%, X%]
  • Stop loss suggestion: [-X% from entry]
  • Position size: [Small / Medium — based on risk score]

📊 Track on:
  • DEXScreener: https://dexscreener.com/[chain]/[contract]
  • Birdeye: https://birdeye.so/token/[contract]
  • Pump.fun: https://pump.fun/[contract] (if applicable)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  DISCLAIMER: Not financial advice. DYOR. Never invest more than you can lose.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Analysis Logic

### Early Discovery (25 pts)
- Token under 72 hours old = maximum score
- Mcap under $500K = highest opportunity window
- Holder count under 500 = very early
- Holder growth rate: divide new holders by hours since launch
- Reward tokens listed on only 1 small DEX (Raydium, Uniswap V3, etc.)

### Whale Signals (25 pts)
Read `references/whale-signals.md` for full wallet pattern library.

Key heuristics:
- Look for wallets that appear across multiple past winning tokens
- Exchange outflows to cold wallets = accumulation signal
- Buy walls forming at key support = institutional-style accumulation
- Top 10 holders stable or increasing % = not distributing

### Momentum (25 pts)
Read `references/momentum-indicators.md` for scoring tables.

Key heuristics:
- Volume/Mcap > 0.5 in first 24h = extremely healthy
- Price consolidating after initial pump = accumulation phase
- Social mentions growing but not yet trending = optimal entry window
- Avoid tokens where volume is entirely from 1-2 wallets (bot activity)

### Safety Audit (25 pts)
Read `references/safety-checklist.md` for full audit steps.

Hard disqualifiers (instant AVOID regardless of other scores):
- Honeypot detected
- Mint authority active with no timelock
- Top wallet holds >40% supply
- Freeze authority enabled (Solana tokens)
- Liquidity fully unlocked and < $10K

---

## Data Sources to Reference

When using web search to populate the report, check these sources:

| Source | Best For |
|--------|----------|
| DEXScreener | Volume, price, liquidity, holder count |
| Birdeye | Solana token analytics, wallet tracking |
| Bubblemaps | Wallet concentration visualization |
| RugCheck.xyz | Solana safety audit |
| Honeypot.is | EVM honeypot detection |
| Etherscan/Solscan | Contract verification, holder list |
| Pump.fun | New Solana memecoin launches |
| LunarCrush | Social momentum scoring |

---

## Handling Missing Data

If live on-chain data isn't available via web search:
1. Clearly mark fields as `[Data unavailable — verify manually]`
2. Still provide the scoring framework with what IS known
3. Give the user direct links to check each data point themselves
4. Never fabricate wallet addresses or holder counts

---

## Quick Scan Mode

If the user asks for a **quick scan** or **multiple tokens at once**, produce a comparison table:

```
TOKEN    | MCAP   | AGE  | SAFETY | WHALE | SCORE | VERDICT
---------|--------|------|--------|-------|-------|--------
$TOKEN1  | $200K  | 4h   | 🟢     | 🟢    | 82    | 🟢 BUY
$TOKEN2  | $1.2M  | 2d   | 🟡     | 🟡    | 61    | 🟡 WATCH
$TOKEN3  | $800K  | 6h   | 🔴     | 🟡    | 31    | 🔴 AVOID
```

Then offer to do a full deep-dive on the highest scoring one.

---

## Trend Detection Mode

If the user asks **"find me early memecoins"** without a specific token:

1. Use web search to check:
   - pump.fun new launches (last 24h)
   - DEXScreener trending (Solana/ETH/Base — sorted by newest)
   - Crypto Twitter/X for tickers gaining traction quietly
2. Surface 3-5 candidates
3. Run Quick Scan on all of them
4. Deep dive the best one

---

## Important Reminders

- Always include the disclaimer at the bottom of every report
- Never recommend specific dollar amounts to invest
- If a token has ANY hard disqualifier, lead with that warning in bold
- Be honest when data is incomplete — credibility > false confidence
- Remind users that even 🟢 scores carry extreme risk in memecoins
