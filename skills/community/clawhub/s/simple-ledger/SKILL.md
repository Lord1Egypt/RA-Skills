---
name: simple-ledger
name_zh: 简单记账 · 个人投资管家
description: Log expenses, check balances, track budgets, set savings goals, and monitor stock/fund/ETF investments from natural language. Plain-text CSV storage, multi-account, offline-first with optional real-time quotes via opt-in network access.
description_zh: 记账工具，一句话记录日常消费。自动分类、查账单、预算管理、月度报告、攒钱目标。支持股票/基金/ETF 投资记录、持仓查询、收益分析、实时行情刷新（需显式授权联网）。CSV 本地存储，支持多账户管理。
triggerWords:
  - 记一笔
  - 帮我记账
  - 记到账本里
  - 这个月花了多少
  - 查账单
  - 月度报告
  - 消费报告
  - 收支
  - 设定预算
  - 攒钱目标
  - 查持仓
  - 买入基金
  - 买入股票
  - 卖出股票
metadata:
  openclaw:
    requires:
      bins: [python3]
      pypi: [akshare]
    tags: [ledger, budget, personal-finance, accounting, csv, natural-language, zh, 记账, 记一笔, 账本, 流水账, 消费记录, 支出管理, 个人理财, 个人财务, 资产管理, 投资, 投资记账, 持仓, 股票, 基金, ETF, 月度报告, 消费分析, 预算管理, 预算规划, 攒钱目标, 财务目标, 收支记录, 账户余额, 查账]
    permissions:
      file:
        read: ["~/.openclaw/workspace/data/ledger/**"]
        write: ["~/.openclaw/workspace/data/ledger/**"]
      network:
        domains: ["*.sina.com.cn", "*.eastmoney.com", "*.akshare.xyz"]
      exec:
        scripts: ["scripts/*.py"]
---

## Overview

A natural-language expense tracker for everyday spending, plus investment tracking for stocks/funds/ETFs. Just say "lunch cost 50 today" — the agent parses and appends a CSV row to your ledger. No database, no cloud sync, just one CSV file.

**What this skill is good at:**

- 📝 **Natural-language logging** — record an expense with one sentence
- 📊 **Spending queries** — by month, by category, by account
- 💰 **Multi-account balances** — WeChat Pay, Alipay, bank card, cash
- 📐 **Budget management** — set monthly caps per category, get overspend alerts
- 📈 **Monthly reports** — income/expense breakdown with visual ASCII chart
- 🎯 **Savings goals** — track progress toward a target (trip, emergency fund)
- 💹 **Investment tracking** — buy/sell stocks & funds, portfolio P&L, optional live quotes

**What this skill is NOT:**

- ❌ Not an investment advisor (no stock picks, no market predictions)
- ❌ Not a tax planner
- ❌ Not a bank sync tool (no automatic transaction import)

---

## Quick Start

Just tell the agent something like:

```
今天中午吃了碗面花了25
昨天打车23.5
工资到账8000
买了件外套299，支付宝付的
```

The agent will:
1. Parse date / amount / category / description / account from your sentence
2. Append a row to `~/.openclaw/workspace/data/ledger/default.csv`
3. Show you the updated balance

Default account is **WeChat Pay** if you don't specify one.

---

## Core Features

### 1. 📝 Natural-language logging

**More examples:**
- "今天中午吃饭花了50块"
- "昨天打车花了23.5"
- "工资到账8000"
- "充话费30"
- "买了一件外套299，用支付宝付的"
- "给小王转了200"

**Batch logging:**
```
今天花了：早餐15、打车30、午饭45
```

**Confirm-then-write:** the agent shows the parsed entry before appending.

**Parsed fields:**

| Field | Default | Notes |
|-------|---------|-------|
| `date` | today | supports "today", "yesterday", "last Wednesday" |
| `amount` | required | decimal allowed |
| `category` | auto-inferred | from keyword list (see references) |
| `description` | auto-extracted | brief summary |
| `account` | 微信钱包 | WeChat Pay default |

### 2. 📊 Spending queries

- "这个月花了多少" — total spending this month
- "上个月餐饮多少钱" — by category, by month
- "最近的账单" — recent transactions
- "我的余额" / "各账户余额" — account balances

Output format:
```
📊 2026年5月 餐饮支出
日期        金额      描述
2026-05-01  ¥50.00   午餐
2026-05-03  ¥128.00  火锅
...
合计        ¥238.00
```

### 3. 💰 Account balance management

- View: "微信钱包还有多少"
- Initialize: "微信钱包初始余额1000"
- Adjust: "银行卡余额修正为5000"

Balance = initial balance + sum(income) − sum(expense)

### 4. 📐 Budget management

```bash
python3 scripts/budget.py <ledger.csv> --set 餐饮 2000
python3 scripts/budget.py <ledger.csv> --progress 2026-05
python3 scripts/budget.py <ledger.csv> --alert 2026-05
python3 scripts/budget.py <ledger.csv> --template 15000   # 50/30/20 rule
python3 scripts/budget.py <ledger.csv> --list
python3 scripts/budget.py <ledger.csv> --remove 餐饮
```

See `references/budget_guide.md` for details.

### 5. 📈 Monthly report

```bash
python3 scripts/generate_report.py ./default.csv --month 2026-05
python3 scripts/generate_report.py ./default.csv --month 2026-05 --output report.txt
```

Output includes: income/expense summary, top 5 categories (ASCII bar chart), daily average, biggest single expense, vs last month delta, brief suggestions.

### 6. 🎯 Savings goals

```bash
goal.py create "旅行基金" 10000 2026-12-31
goal.py deposit "旅行基金" 2000
goal.py progress "旅行基金"
goal.py list
goal.py delete "旅行基金"    # ⚠️ requires typing "删除" to confirm
```

See `references/goal_guide.md`.

### 7. 💹 Investment tracking

⚠️ **Network:** investment features (code lookup + live quotes) require `akshare` (pip install) and explicit `--allow-network` flag. All other features are offline.

**Quick commands:**

```bash
# Buy (auto-lookup code by name, requires Y/N confirm)
invest.py --buy "有色金属ETF南方" auto 3100 2.07 2026-01-10 --allow-network

# Buy (manual code)
invest.py --buy "沪深300ETF" 510050 100 3.50 2026-01-15

# Sell
invest.py --sell "沪深300ETF" 510050 500 4.00 2026-03-01

# Portfolio (offline, uses last-set prices)
invest.py --portfolio

# Portfolio with auto-refresh quotes (needs network opt-in)
invest.py --portfolio --auto-refresh

# Total P&L
invest.py --summary

# Single quote
invest.py --quote 601138 --allow-network
```

Full command reference: `references/invest_api.md`.

**Auto-refresh mode:** create `~/.openclaw/workspace/data/ledger/.env` with `AUTO_REFRESH=1` to make portfolio queries always fetch live prices. Delete the file to disable.

---

## Trigger Conditions

Activate this skill **only when the user expresses an explicit financial intent**:

- Log an expense ("记一笔：花了XX", "帮我记账", "记到账本里")
- Query spending ("这个月花了多少", "查账", "账单")
- Account management ("我的余额", "银行卡还有多少")
- Monthly report ("月度报告", "消费分析")
- Investment action ("买入XX股", "卖了XX", "查持仓", "投资收益") — ⚠️ needs network
- Budget ("设定预算", "超支了吗", "生成预算模板")
- Savings goal ("建个攒钱目标", "旅行基金进度")

**Do NOT activate for:**

- Casual mention of money in conversation ("那顿饭花了50，味道一般")
- Asking about prices without logging intent ("这个多少钱", "iPhone 17 多少钱")
- Generic financial discussion ("最近花了不少钱" as a sigh)
- Other people's spending (only the user's own)

**Disambiguation rule:** If the user is just chatting about a recent expense, treat it as ordinary conversation. The key signal is whether the user has an **explicit intent to record, manage, or query** their finances.

---

## File Format (Original CSV)

```
# 日期,类型,金额,分类,描述,账户
余额,微信钱包,1000.00
余额,支付宝,2000.00
余额,银行卡,50000.00
余额,现金,500.00
2026-05-21,支出,50,餐饮,午餐,微信钱包
2026-05-22,收入,8000,工资,5月工资,银行卡
2026-05-23,支出,299,购物,外套,支付宝
```

**Rules:**
- 6 fields: `日期,类型,金额,分类,描述,账户`
- `类型` must be `收入` or `支出`
- `金额` is always positive (direction comes from `类型`)
- Flat account names (no hierarchy)
- Initial balance uses `余额,账户,金额` format

**Default location:** `~/.openclaw/workspace/data/ledger/default.csv`

---

## 🔒 Security & Permissions

This skill performs the following operations:

| Operation | Behavior | Scope |
|-----------|----------|-------|
| 📖 Read files | Reads ledger CSV, budget JSON, investment CSV, goals JSON | Only `data/` directory |
| ✏️ Write files | Appends/modifies ledger entries, budgets, investments, goals | Only `data/` directory |
| 🗑️ Delete data | Deletes transactions, budgets, goals (all require user Y/N confirm) | Only `data/` directory |
| 🌐 Network access | Queries stock/fund codes + real-time quotes via akshare (Sina/Eastmoney APIs) | Sends only security codes/names, no personal financial data |
| 💻 Execute scripts | Runs Python scripts in `scripts/` | Only this skill's own scripts |

**Data isolation:** `investments.csv` (investments) and `default.csv` (daily ledger) are completely independent files.

**Will NOT do:**

- ❌ Read MEMORY.md, USER.md, SOUL.md, or any non-financial file
- ❌ Access ~/.ssh, ~/.aws, ~/.config or other system directories
- ❌ Upload your financial data to any external server
- ❌ Modify system files or execute external commands

**Backup reminder:** All operations modify local CSV/JSON files directly. Back up `data/` regularly.

---

## 🌐 Network Behavior

> ⚠️ **Network summary:** Investment features (security code lookup + live quotes) require network via the `akshare` library calling Sina Finance public APIs. All other features are fully local — **your financial data is never sent to any external server**.

> 🔒 **Privacy notice:** Network queries only send security codes/names to public quote APIs (Sina, Eastmoney). **No personal financial data (balances, transactions, account info) is transmitted.** Be aware that queries themselves reveal which securities you're interested in.

**Default behavior: offline queries.**

Network access uses an **explicit opt-in** mechanism — never enabled by default. Add `--allow-network` to one-off network commands, or set `AUTO_REFRESH=1` in a local `.env` file to auto-refresh quotes on portfolio queries.

| Operation | Default | Enable network |
|-----------|---------|----------------|
| Portfolio (`--portfolio`) | offline (uses last-set prices) | add `--auto-refresh` |
| Summary (`--summary`) | offline | add `--auto-refresh` |
| Refresh quotes (`--refresh`) | blocked | add `--allow-network` |
| Single quote (`--quote`) | blocked | add `--allow-network` |
| Auto-lookup code on buy | blocked | add `--allow-network` |

**Disable auto-refresh:** delete `~/.openclaw/workspace/data/ledger/.env` or say "关闭自动联网刷新".

**Manual price update (no network):**

```
工业富联现在81.58
亨通光电价格91.43
```

Both methods (auto-refresh vs manual update) work side-by-side without conflict.

---

## First-run Setup

When the user first triggers this skill:

1. Check if ledger file exists
2. If not, create with template header
3. Ask for common payment methods and initial balances

**Template:**

```
# 日期,类型,金额,分类,描述,账户
# 个人账本 - 创建于 YYYY-MM-DD
# 格式说明见 references/ledger_format.md

# 账户初始余额
余额,微信钱包,0.00
余额,支付宝,0.00
余额,银行卡,0.00
余额,现金,0.00

# === 交易记录 ===
```

---

## Interaction Modes

### Single entry (most common)

```
用户: 今天中午吃了碗面花了25
Agent: 已记录 ✅
      📅 2026-05-21
      💰 ¥25.00
      📂 餐饮
      💳 微信钱包
      📝 午餐
      微信钱包余额：¥975.00
```

### Dialogue entry (multi-field fill-in)

```
用户: 花了200块
Agent: 买的什么？
用户: 买了本书
Agent: 已记录 ✅ ...
```

### Goal-linked entry

When the user says they saved money toward a goal, do two things:
1. Call `goal.py deposit` to update goal progress
2. Record the expense normally

### Modify / Delete

> ⚠️ All delete operations require user Y/N confirm — never auto-delete.

- "删掉刚那笔" (delete most recent, needs confirm)
- "删除5月15日那笔餐饮" (delete specific, needs confirm)
- "把刚才那笔改成30块" (modify amount, needs confirm)

---

## ⚖️ Professional Standards

This skill provides **financial recording and basic analysis tools**, not investment advisory services.

| Can do | Cannot do |
|--------|-----------|
| Record and analyze your spending data | Recommend specific financial products |
| Compare your spending vs general benchmarks | Guarantee any investment return |
| Suggest savings based on your data | Predict market movements |
| Explain financial concepts (compound interest, inflation) | Provide tax planning |
| Help you build a savings plan | Do asset allocation |

**Bottom line:** I help you understand where your money went, not where it should go.

---

## 📚 References

Load on demand:

- **`references/ledger_format.md`** — CSV format details
- **`references/budget_guide.md`** — budget management
- **`references/goal_guide.md`** — savings goals
- **`references/invest_guide.md`** — investment tracking workflow
- **`references/invest_api.md`** — investment command reference
- **`references/user_guide.md`** — user FAQ
- **`references/financial_benchmarks.md`** — financial health benchmarks
- **`references/education.md`** — financial concepts

---

## Tone & Style

| Scenario | Style |
|----------|-------|
| Successful logging | Concise confirmation + key info: "已记录 ✅ 餐饮 ¥35 余额 ¥965" |
| Monthly report | Clear data + 1-2 sentence suggestions |
| User overspending | Gentle reminder, not criticism |
| User reaching a goal | Genuine encouragement |
| User asking investment advice | Educational content + disclaimer |

**Avoid:** preachy tone, number-shaming, over-cautious language, fake intimacy.

---

## Constraints

1. **Write vs delete separation.** Deletes require explicit user request + Y/N confirm — no auto-delete.
2. **Amount required.** If amount can't be confirmed, ask.
3. **Category guessable.** When confident, auto-categorize; when uncertain, offer options.
4. **Date optional.** Defaults to today, supports relative dates.
5. **Account optional.** Defaults to WeChat Pay.
6. **Files are the database.** All data in CSV/JSON files. Users can edit any file with a text editor. Back up `data/` regularly.
7. **External deps.** Basic features (logging, queries, budgets, reports, goals) use Python stdlib only. Investment code lookup requires `akshare` (pip install akshare) + network.
