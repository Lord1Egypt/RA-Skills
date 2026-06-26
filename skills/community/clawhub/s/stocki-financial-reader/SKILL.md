---
name: stocki-financial-reader
version: 0.4.0
description: "Institutional-grade financial data skill for OpenClaw. Real-time quotes, financials, valuation time series, OHLCV history, industry membership, consensus forecasts, composite analysis. Covers cn/hk/us markets and stock/index/etf/futures/crypto. For structured market/financial data, use this skill."
metadata:
  openclaw:
    emoji: "📈"
    requires:
      bins: [python3]
      env: [STOCKI_GATEWAY_URL, STOCKI_API_KEY]
      os: [linux, darwin]
    primaryEnv: STOCKI_API_KEY
    envVars: [STOCKI_GATEWAY_URL, STOCKI_API_KEY]
---

# stocki-financial-reader

Institutional-grade financial data analyst skill. Aggregates 8 reference docs that teach the LLM how to retrieve structured market/financial data via HTTP. Routes user queries to the right reference, handles output discipline (no data-vendor leakage), and ships self-diagnostic scripts.

## Core Principle

**For structured market/financial data, use this skill.** Examples: real-time prices, OHLCV history, financial statements, valuation time series, industry membership, consensus forecasts, composite company analysis.

**Do NOT use this skill for**: general financial knowledge questions ("what is P/E ratio?"), news commentary without data backing, or anything requiring fabricated numbers.

**Never fabricate market data.** If a value is not in a real response, say so. Completeness and output discipline are non-negotiable.

**Stay non-advisory.** Relay numbers and the response's own context fields (percentiles / industry comparisons). Do NOT append buy/sell/hold ratings, target-price opinions, or personalized recommendations on top of the data.

## HTTP Convention

All references share these conventions. The router enforces them globally; individual references may override only with explicit justification.

- **Base URL**: `$STOCKI_GATEWAY_URL` (env var). Set to `http://localhost:9996` in dev or `https://skill.stocki.com.cn` in prod.
- **Auth**: every request carries `Authorization: Bearer $STOCKI_API_KEY`. localhost dev mode does not validate but the header MUST still be sent (no environment-conditional code paths).
- **Content-Type**: `application/json` for all POST.
- **Error code mapping** (mirrors `scripts/_http.py` exit codes):

  | HTTP | Mapped error code | Exit code |
  |---|---|---|
  | 401 | `auth_invalid` | 1 |
  | 503 / 504 / 5xx / timeout | `stocki_unavailable` | 3 |
  | 429 / quota | `rate_limited` | 4 |
  | TCP/DNS refused | `unreachable` | 2 |

## Inline Threshold (`/api/v3/datareader/read` only)

The stocki gateway v3 默认按 50 行截断 `response.data`;超过部分目前 runtime 不读取
外部存储。Body 参数 `inline_threshold`(max 1000)可把 inline 上限抬到 1000,
覆盖绝大部分时序需求。

**Scope**:仅 `/api/v3/datareader/read` 读此参数。其他 v3/v2/executor 端点静默忽略,
**禁止**给 `financial_context/*` / `quotes/*` / `market/*` / `executor/*` / v2
端点传 `inline_threshold`(会误导对响应结构的理解)。

**估算先行**:`N = unique_symbols × time_window_trading_days × unique_metrics`。
形态特化:
- `index_member` panel:`成分股数 × 时间窗交易日`
- `fundamental` / `indicator`:`symbols × 时间窗内财报期数`(年 1 / 季 4)
- `consensus` / `estimate`:`symbols × 时间窗内有发布的交易日`(稀疏)
- `revenue_breakdown`:`symbols × 期数 × 估 5-15 segments`
- `company_info`:`symbols`(静态)

**Margin 表**(中心化):

| data_type | margin |
|---|---|
| `price` / `fundamental` / `indicator` / `company_info` | ×1.2 |
| `consensus` / `estimate` / `forecast` | ×1.5 |
| `index_member` | ×1.33 |
| `revenue_breakdown` | ×2.0 |

**四档分支**:

| N | 行为 |
|---|---|
| ≤ 50 | 不设 `inline_threshold`,默认 50 已覆盖 |
| 50 < N ≤ 1000 | 设 `inline_threshold = min(ceil(N × margin), 1000)` |
| > 1000 | 先 narrow query(单日 / 单 symbol / 显式 metrics);仍 >1000 → fail-loud「当前只能返回前 1000 行预览,完整数据请联系数据团队」 |
| 未知 | 设 `inline_threshold = 1000`;响应后校验 `total_records ≤ 1000`;>1000 走 narrow / fail-loud |

**禁止**:
- ✗ 一律设 1000(token 浪费)
- ✗ N>1000 继续用截断数据回答(误导用户)
- ✗ 用户层文本出现内部存储术语(`data_path` / 内部 bucket 路径 / 文件后缀 等)

## Routing Table

8 references, organized in 3 tiers. Trigger keywords are multilingual (Chinese / English / mixed).

| Tier | Trigger keywords (CN / EN) | Reference |
|---|---|---|
| 0 (preprocessor) | metric name not in `fundamentals-panel` cheatsheet | `references/metric-resolver.md` |
| 0 (preprocessor) | NL company / ticker / concept / sector / index name (not already a bare code); default strict, LLM may bypass when very confident in the canonical identifier | `references/name-resolver.md` |
| 1 (composite-first, cn/hk only) | analyze X / 分析 / 综合 / 贵不贵 / 健康吗 / 业务结构 / 哪条业务最快 / 为什么涨/跌 / 共识修正轨迹 | `references/financial-context.md` |
| 2 (current snapshot) | now / 现价 / 实时 / intraday / "PE 现在" / "ROE 现在" | `references/realtime-quote.md` |
| 2 (price time series) | history / K 线 / OHLCV / 区间收益 / 复权 / 走势 | `references/price-history.md` |
| 2 (fundamentals panel) | "营收 8 季度" / "PE 历史时序" / "ROE 4 季趋势" / "三表 Q4" / 总市值时序 / 单季 / 累计 / TTM | `references/fundamentals-panel.md` |
| 2 (forecast snapshot) | consensus / 一致预期 / 目标价 / 分部 (when financial-context unavailable) | `references/consensus-and-target.md` |
| 2 (registry) | industry / 行业 / 成分股 / 公司简介 / 上市日期 / 股本注册表 | `references/industry-and-symbols.md` |
| 2 (calendar) | trading days / 交易日 / availability / 开盘了吗 / N 月有几个交易日 | `references/market-calendar.md` |

### Routing Decision Rules (R1–R8)

Apply in order. Later rules can override earlier ones if user intent is specific.

- **R1. Open-ended fundamentals analysis → `financial-context`** (cn/hk only). User asks generically without naming a specific metric ("分析下 X / X 基本面怎么样 / X 贵不贵 / X 健康吗 / 业务结构 / 哪条业务最快 / 为什么涨跌 / 共识修正轨迹"). Pick L1 / L2 / L3 by depth. Do NOT chain `fundamentals-panel + consensus-and-target + price-history` to recreate what one composite call returns.

- **R2. `financial-context` only ships pre-computed 5-year valuation percentile fields** (`valuation` 段里 key 后缀含 `percentile_5y` 的字段即是;具体字段名以响应实际为准,不假定固定前缀)。It does NOT compute arbitrary windows. User asks 5y percentile → use these fields directly (even when a specific metric like PE/PB is named, do NOT go to `fundamentals-panel` to recompute). User asks any other window (3y / 10y / "历史" without specifying) → upstream does NOT serve this directly. Pull raw daily series via `fundamentals-panel` `data_type=valuation` and EITHER (a) compute percentile rank from the series and label clearly as "approximation from raw series", OR (b) tell the user only 5y is directly supported.

- **R3. Full consensus time series is exclusive to `financial-context` L3** (≥132 records). When using L3, do NOT additionally call `consensus-and-target`.

- **R4. Current single value (PE/ROE/PB now)** → `realtime-quote` with `include_fundamentals=true`. Lighter than `fundamentals-panel` with `extra.daily=true` and carries an explicit freshness signal.

- **R5. Specific named metric(s), multi-period panel → `fundamentals-panel`**. User explicitly names one or more financial / derived indicator / valuation metric(s) and wants a time-series panel ("8 季度营收 / ROE 4 季 / 毛利率历史 / PE 时序 / 总市值历史 / 三表 Q4"). Pick `data_type` ∈ {financial, indicator, market_cap, valuation} by metric kind.

- **R6. us:stock fallback.** `financial-context` and most `fundamentals-panel` data_types are unavailable for us. Surface upstream `availability` warning to user; fall back to `realtime-quote` for current value, `fundamentals-panel data_type=market_cap` (only us-supported), `price-history` for OHLCV.

- **R7. Multi-call is allowed and expected.** A query like "AAPL 现价 + 一致预期 + 行业" correctly results in 3 reference calls. Do NOT collapse into a single reference at the cost of correctness.

- **R8. Two Tier 0 preprocessors, not routing targets.**
  - `metric-resolver` runs *before* `fundamentals-panel` / `financial-context` field lookup when user mentions a metric name not in the cheatsheet, returning canonical raw key + EN/CN label.
  - `name-resolver` runs *before* any reference that needs a bare code or collection symbol, when the user supplied a natural-language name (company / concept / sector / index). Default is strict (always call); LLM may bypass when very confident in the canonical identifier for mainstream names.

**R1 vs R5 litmus test**: Did user name a specific metric? No → R1; yes + single point → R4; yes + multi-period panel → R5; any + 5y percentile → R2 override.

## Output Discipline

When relaying response content to user-visible text, **never expose** any data-vendor identifiable artifacts:

| Category | Forbidden form | Required form |
|---|---|---|
| symbol | pipe-delimited (`AAPL\|ST\|USA`) | bare code (`AAPL`, `600519`) |
| metric | raw column key (e.g. `oper_rev`, `waa_roe`, `roe_deducted`, `pe_ttm`) | EN label ("Total Revenue") or CN label ("营业总收入") by user language |
| industry | source-tagged prefix (形如 `<src>-<category>`) | category itself ("食品饮料") |

**Why**: data-vendor identity is implementation detail. Leaking it locks the output format and prevents future source switches. Each reference's `Response Fields — Raw → User-Facing Label` table is the source of truth for label mappings; metric-resolver's `name` field is fallback when not in the cheatsheet.

## Doctor / Diagnose

Run before reporting any setup issue or after install:

```bash
python3 {baseDir}/scripts/doctor.py     # env / version / file integrity / workspace
python3 {baseDir}/scripts/diagnose.py   # gateway reachability + auth + read smoke test
```

Exit codes (uniform across all scripts):
- `0` ok
- `1` auth invalid
- `2` unreachable (TCP/DNS layer)
- `3` stocki unavailable (5xx / timeout)
- `4` rate limited / quota exceeded

When a script fails, **report the exit code verbatim and stop**. Do not retry.

## Cross-ref

See `INSTALL.md` for setup. See `references/<n>.md` for per-endpoint contracts.
