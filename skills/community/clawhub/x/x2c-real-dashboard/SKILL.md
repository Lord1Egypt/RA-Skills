---
name: x2c-real-dashboard
description: Query the X2C personal dashboard to get real-time KPI data, earnings trends, platform views, recent transactions, and earning projects. Use this skill whenever the user asks about their X2C income, revenue, ROI, mining status, today's/yesterday's/monthly earnings, platform performance, recent activity, or project list.
metadata: {"openclaw":{"emoji":"📊","requires":{"env":["X2C_API_KEY"]},"primaryEnv":"X2C_API_KEY"}}
---

# x2c-real-dashboard

Real-time X2C personal dashboard data via Open API.

All scripts are in `{baseDir}/scripts/`. They read `X2C_API_KEY` from the environment.

---

## Actions & Scripts

### 总览 KPI — overview
Use when the user asks: "今天赚了多少", "收益概况", "ROI", "挖矿状态", "项目总数", "播放量"

```bash
bash {baseDir}/scripts/overview.sh
```

Returns: today/yesterday/monthly/historical revenue (USD + X2C), ROI, mining status, project counts, total views, X2C price.

---

### 收益趋势 — trend
Use when the user asks: "最近 N 天趋势", "收益走势", "历史收入图"

```bash
bash {baseDir}/scripts/trend.sh [DAYS]
# DAYS: 1–90, default 7
```

Returns: daily `{ date, x2c, usd }` array sorted ascending.

---

### 各平台播放量 — platform-breakdown
Use when the user asks: "哪个平台表现最好", "各平台播放量", "TikTok / YouTube 数据"

```bash
bash {baseDir}/scripts/platform-breakdown.sh
```

Returns: total views + per-platform breakdown sorted descending.

---

### 最近动态 — recent-activity
Use when the user asks: "最近的交易", "收入记录", "挖矿记录", "最近动态"

```bash
bash {baseDir}/scripts/recent-activity.sh [LIMIT]
# LIMIT: 1–50, default 5
```

Returns: recent transactions with `tx_type`, `amount`, `currency`, `title`, `transaction_at`.

tx_type values: `mining_income` | `x2c_release` | `commission` | `referral` | `royalty` | `production` | `production_refund`

---

### 赚钱作品列表 — earning-projects
Use when the user asks: "我的作品", "哪个作品赚最多", "作品收益排名", "项目列表"

```bash
bash {baseDir}/scripts/earning-projects.sh [PAGE] [PAGE_SIZE]
# PAGE default 1, PAGE_SIZE default 10, max 50
```

Returns: paginated project list with `today_usd`, `total_usd`, `total_views`, `trend7d`, `platform_views`.

---

## Formulas (for context)

```
today_usd      = today_x2c × x2c_price + today_commission
roi_percent    = historical_usd / net_expense_usd × 100
net_expense    = max(0, spending_credits - refund_credits) / 100
vs_yesterday % = (today - yesterday) / yesterday × 100
```

All date boundaries are **UTC**. Daily payouts run at ~00:10 UTC.

## Error Handling

All scripts exit non-zero on failure and print `{"success":false,"error":"..."}`.
Always check `success: true` before presenting results.
