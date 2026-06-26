# 📊 Stock Realtime Brief

> **A-Share Real-time Analysis & Actionable Recommendation Generator** — turning gut-feeling trading into rule-based discipline.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Market: A-Share](https://img.shields.io/badge/Market-A--Share-red.svg)]()

[中文](./README.md) | English

---

## ✨ What it does

For the China A-Share market, the tool **automatically switches between 3 modes** based on user input:

| Mode | Trigger | Output |
|:---:|---------|--------|
| 📦 **Portfolio** | given a portfolio file | full pre-market briefing: realtime status + key MAs + 3-level hard stop-loss + margin risk check + recent announcement alerts + prioritized action list |
| 🔍 **Single** | one stock | deep-dive: stance + technicals + 5 operational levels (entry/add/stop-loss/short-term TP/swing TP) |
| 📊 **Multi** | multiple stocks | comparison table: composite score ranking + key differences + ⭐/🟡/⚠️ tags |

**Auto mode**: picks the right mode based on input — 1 code → Single, multiple → Multi, portfolio file → Portfolio.

---

## 🚀 30-second quick start

```bash
git clone https://github.com/<your-name>/stock-realtime-brief.git
cd stock-realtime-brief
pip install -r requirements.txt

# Single
python -m stock_realtime_brief --code 300750

# Multi
python -m stock_realtime_brief --codes 600519,300750,600036

# Portfolio
cp examples/portfolio_demo.json my_portfolio.json
python -m stock_realtime_brief --portfolio my_portfolio.json
```

---

## 🎯 Key Features

### ⭐ Hard 3-Level Stop Loss

Not vague advice like "stay alert", but **specific price levels you can directly set as conditional orders**:

| Level | Logic | Action |
|:---:|---------|------|
| **Warning** | MA5 (regular) / MA10 (heavy) + profit lock | trim 1/3 |
| **Risk** | MA10 (regular) / MA20 (heavy) / max(MA20, cost-15%) | trim another 1/3 |
| **Cut** | MA20 / cost-25% (loss state) | clear all |

### ⭐ Resilient Data Source Strategy

A-share data sources are notoriously unreliable. This tool degrades in **battle-tested order**:

```
Tencent Finance (most stable) → Sina Finance batch → AKShare (with timeout)
```

> **War story**: AKShare's primary `82.push2.eastmoney.com` endpoint frequently times out during opening sessions (measured: 50+ minutes hung). This tool defaults to **Tencent first** to avoid that pit.

### ⭐ Auto Announcement Detection

Portfolio mode automatically pulls **recent 14-day important announcements** in parallel, flagging **HIGH / MED severity events**:

- 🔴 **HIGH**: shareholder reduction / regulatory investigation / earnings warning / penalty / lawsuit
- 🟡 **MED**: lockup expiration / acquisition / restructuring / shareholder meeting / earnings forecast

Announcements are pinned at the top of output, prompting "adjust your move on top of the technicals".

### ⭐ Margin Risk Health Check (A-share specific)

Margin trading risk is commonly overlooked. This tool:

- Auto-calculates **margin coverage ratio**
- 5-level alerting: ✅ safe / 🟡 manageable / ⚠️ caution / 🚨 strong warning / 🚨🚨🚨 near forced liquidation
- Provides **repayment priority recommendations**

---

## 📚 Design Philosophy

### "Rules over feelings"

Core belief: **Retail investors' biggest enemy is not the market, but their own emotions.**

- ❌ "Trade cautiously" → ✅ "Trim 1/2 on break of 500"
- ❌ "Sentiment is weak" → ✅ "Volume 479M, volume ratio 0.62 (thin morning)"
- ❌ "Target 600" → ✅ "SL 482 / TP1 539 / TP2 588"

Every recommendation comes with a **trigger condition**, so even the busy/emotional retail investor can execute consistently.

---

## ⚠️ Disclaimer

**This tool is for analysis aid only, NOT investment advice.**

See [DISCLAIMER.md](./DISCLAIMER.md).

---

## 📜 License

[MIT](./LICENSE) © 2026
