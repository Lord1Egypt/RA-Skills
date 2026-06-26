# Operational Workflows Reference

---

## Position Management via Chat

**Check positions:**
`agent-positions <agent_id>` — Present: "BTC LONG — $500 at $95,432 entry — PnL: +$23.45 — 5x leverage"

**Open a position:**
`agent-open <agent_id> --coin BTC --direction LONG --size 100 --leverage 5 --confirm`
`agent-open <agent_id> --coin xyz:TSLA --direction LONG --size 500 --leverage 5 --stop-loss 375 --take-profit 420 --confirm` *(HIP-3)*

**Close a position:**
`agent-close <agent_id> --coin BTC --confirm`

**Update SL/TP:**
`agent-update-sl-tp <agent_id> --coin BTC --stop-loss 94000 --take-profit 100000 --confirm`

**Order history:**
`agent-orders <agent_id>`

---

## Market Overview

When user asks about market conditions, run in sequence:
1. `dashboard` — AI overview (top signals across perp, spot, pm, hip3)
2. `dashboard-latest spot --limit 10` — spot SM holdings
3. `dashboard-latest hip3 --limit 10` — HIP-3 DEX positions
4. `perp-signals --limit 5` — top perp signals
5. `signals --limit 5` — top PM signals
6. `fear-greed` — Fear & Greed Index
7. Summarize: AI signals, spot accumulation, hip3 activity, perp sentiment, PM consensus, F&G

---

## Deep Analysis for a Coin

When user asks "analyze BTC":
1. `dashboard-asset perp BTC` — perp AI analysis (SM + TA + Market)
2. `dashboard-asset spot BTC` — spot SM holdings
3. `dashboard-asset hip3 BTC` — HIP-3 positions (if available)
4. `derivatives BTC` — derivatives indicators
5. `ta BTC` — multi-timeframe TA
6. `liquidation-map BTC` — liquidation clusters
7. Summarize: AI signal, spot accumulation vs perp positioning, TA levels, derivatives sentiment, liquidation zones

---

## Trading Signals

1. Ask: prediction markets, perp, or both?
2. Run relevant command(s)
3. Present top signals by consensus strength
4. Explain each: "5 top-100 traders all say YES on 'Will BTC hit $100k?' — price 42c"

---

## HITL Signal Tracker

When user has `execution_mode: "hitl"` agents, the agent creates **trade plans** for user approval.

### Proactive Check (IMPORTANT)

**At the start of every conversation**, if user has HITL agents:
1. Run `agent-pending-plans`
2. If pending plans exist, present using Signal Tracker format
3. If none, proceed normally

### Signal Tracker Display Format

```
📋 TRADE PLAN — [Agent Name]
━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Signal: [DIRECTION] [Symbol]
   Entry: [price]  |  SL: [price]  |  TP: [price]
   Size: $[amount] ([X]% of portfolio)
   Risk/Reward: [ratio]

🧠 Thesis
   [LLM reasoning — 2-3 sentences max]

📈 Evidence
   SM: [direction] — Score [X]/100, [N] wallets, consensus [X]%
   TA: [key levels — RSI, MACD, support/resistance]
   Market: [funding, OI change, L/S ratio]

⚠️ Risk
   Portfolio: $[equity] | Exposure after: [X]%
   Max loss: $[amount] | Open positions: [N]

⏰ Expires: [time remaining]
Plan ID: [plan_id]

What would you like to do?
✅ Approve — Execute this trade
✏️ Edit — Modify entry/SL/TP/size then execute
📄 Paper — Simulate only
❌ Reject — Skip this signal
```

### User Interaction Flow

1. **User sees plan** → Can ask "Why this entry?", "SM breakdown?", "Show TA"
2. **Answer** → Use `agent-plan-detail`, `dashboard-asset`, `ta`, `derivatives`
3. **User decides** → Run `agent-plan-action` with their choice
4. **If edit** → Ask what to change, call with `edits: {entry, stop_loss, ...}`

Plans expire after **2 hours** by default.

---

## Telegram Setup

**Recommended for HITL agents.** Zero delay, zero LLM cost.

**Easy setup (no chat_id needed):**
1. User creates bot via @BotFather → gets `bot_token`
2. `telegram-setup-init --bot-token "<TOKEN>"`
3. Server responds: "send /start to @your_bot_name"
4. User sends /start → webhook auto-detects chat_id → done

**Advanced setup:** `telegram-setup --bot-token "<TOKEN>" --chat-id "<ID>"`

**Manage:** `telegram-config` (view) | `telegram-disable` (disable + remove webhook)

**How it works after setup:**
- HITL: trade plan → instant Telegram with ✅ Approve / ❌ Reject buttons
- Auto: trade execution → informational notification

### Telegram vs Cron

| | Telegram | Cron |
|--|---------|------|
| **Delay** | ~0s instant | 0-5 min polling |
| **LLM cost** | $0 | ~500 tokens/cycle |
| **Approve UX** | Tap button | Type in chat |
| **Offline** | Works 24/7 | Needs Gateway running |

**Cron fallback** (if no Telegram):
```bash
openclaw cron add --name "Agent Monitor" --every "5m" --session isolated \
  --message "Check for pending trading agent trade plans by running: python3 skills/zonein/scripts/zonein.py agent-check. If pending plans, present each with signal tracker format. If none, say HEARTBEAT_OK." \
  --announce --exact
```

---

## Strategy Examples (for Q4)

Show 3 random examples when asking user about their strategy.

1. **Trend Confirmation Rider** — "Enter LONG when SM long_ratio ≥50% with ≥3 wallets AND SuperTrend 'buy' on 4h AND ADX ≥15. Exit when SM short_ratio ≥55% AND SuperTrend flips."
2. **Momentum Scalper** — "Quick entries when SM wallet_count ≥5 with long_ratio ≥50%. RSI 35-65. TP 1.5%, SL 0.8%."
3. **Contrarian Funding Fader** — "SHORT when funding ≥0.04% AND RSI 4h ≥72 AND SM short_ratio ≥50%. LONG when funding ≤-0.03% AND RSI ≤28."
4. **Multi-Timeframe Sniper** — "1d SuperTrend='buy' AND 4h RSI ≤45 AND SM long_ratio ≥50%. 1-2 trades/week."
5. **OI Divergence Trader** — "LONG when oi_change_4h >2% BUT price flat AND SM wallet_count increasing."
6. **RSI Oversold Bouncer** — "RSI 4h <28 AND Stoch K <15 AND SM long_ratio ≥50%. Target RSI mean reversion."
7. **EMA Trend Surfer** — "EMA9 > EMA21 > EMA55 on 4h. Enter pullbacks to EMA21 when RSI 1h 35-45 AND SM ≥50%."
8. **L/S Ratio Contrarian** — "SHORT when market.long_ratio ≥68% AND funding positive AND SM short_ratio ≥50%."
9. **Conservative Diamond Hands** — "BTC/ETH only. SM ≥55% with ≥7 wallets AND 1d SuperTrend AND RSI 1d 35-60. Target 10%+."
10. **SM Front-Runner** — "Enter when SM 1h wallet_count jumps to ≥5 with ratio ≥55%. Speed over TA. Tight stop."
11. **HIP-3 Trend Surfer** — "Trade HIP-3 stocks following 4h SuperTrend. SM ≥50% AND ADX ≥15. SL 3%, TP 6%."
12. **HIP-3 Commodity Momentum** — "Trade GOLD/OIL on momentum. SM ≥3 wallets AND RSI 35-65 AND MACD bullish. 3x leverage."
13. **HIP-3 Diversified Portfolio** — "5+ HIP-3 assets. SM consensus ≥50% AND 1 TA confirm. Patient, wide stops."

---

## Output Presentation

**PM Signal:** `🔮 [title] — Smart money: [YES/NO] | Agreement: [X]% | [N] traders | Price: YES [x] / NO [x]`

**Perp Signal:** `📊 $[COIN] — Smart money: [LONG/SHORT] | Agreement: [X]% | [N] whales | Long: $[X] / Short: $[X]`

**Periods:** PM: DAY/WEEK/MONTH/ALL. Perp: day/week/month.
**PM Categories:** OVERALL, POLITICS, SPORTS, CRYPTO, CULTURE, ECONOMICS, TECH, FINANCE.
