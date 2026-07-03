# 数据字典 (Data Catalog)

> 用于 LLM agent 在自然语言查询时定位数据维度。按 **11 大类 → 20 scope → 5 套餐** 组织（2026-06-08 whoami 实测）。
> **档位命名（由低到高）**：`free < plus < pro < max < ultra`（plus 入门 / pro 中级 / max 高级，付费 3 档 ↔ claw LOW/MID/HIGH；ultra 为内部档不对外）。
> **2026-06-08 whoami 实测**：`stock.market` **未拆分**（仍是单一 Pro scope，计划中的 4 个子 scope 未落地）；非股票 scope（`market`/`derivative`/`fund`/`bond`/`forex`/`stock.intl-macro`/`news`）均在 **Max** tier；仅 `stock.selection` + `tmt` 是 Ultra 内部；`futures.basic`/`futures.kline` 从来不是独立 scope（已删）。**以 `/openapi/v1/whoami` 返回的 scopes 为准**。
>
> **使用流程**：`自然语言 → 定位大类 → 找到 scope → 决定调用哪个 OpenAPI 端点 / 或返回"数据存在但端点未覆盖"`。

---

## 概览

| 项 | 值 |
|----|----|
| 大类 | 11（原 5 + 新 6） |
| Scope | 20（18 对外可售：Free 3 + Plus 5 + Pro 2 + Max 8；2 Ultra 内部不对外：`stock.selection` + `tmt`）+ 1 管理员 `*` |
| 套餐 | 5（免费 / Plus / Pro / Max / Ultra，由低到高，付费 3 档 ↔ claw LOW/MID/HIGH，Ultra 内部不对外） |
| 端点路径 | `/openapi/v1/{category}/...` |
| 覆盖 PG 表数 | ~165 / 168 |

## 大类 → Scope 索引

| # | 大类 | Scope | 套餐归属 | PG 表数 |
|---|------|-------|---------|---------|
| 一 | 股票（A 股） | `stock.basic` | free | 8 |
| | | `stock.kline` | free | 9 |
| | | `stock.indicator` | free | 9 |
| | | `stock.index` | plus | 14 |
| | | `stock.minute` | plus | 4 |
| | | `stock.financial` | plus | 12 |
| | | `stock.research` | plus | 3 |
| | | `stock.shareholder` | plus | 11 |
| | | `stock.market` | pro（⚠️ 生产 whoami 2026-06-08 仍是单一 scope，未拆分；包含板块/龙虎榜/资金流/异动/涨跌停/集合竞价等） | 47 |
| | | `market` | pro（国内宏观：CPI/PPI/PMI/GDP/M2/Shibor/LPR/社融）| 10 |
| | | `stock.selection` | ultra（内部不对外） | 4 |
| 二 | 港股（新） | `stock.hk` | max | 12 |
| 三 | 美股（新） | `stock.us` | max | 9 |
| 四 | 期货期权 | `derivative` | **max** | 15 |
| 五 | 基金+ETF | `fund` | **max** | 15 |
| 六 | 新闻资讯（新） | `news` | **max** | 1 |
| 七 | 国际宏观（新） | `stock.intl-macro` | **max**（URL 前缀 `/intl-macro/...` 不含 `stock/`） | 9 |
| 八 | 外汇（新） | `forex` | **max** | 2 |
| 九 | 债券+可转债 | `bond` | **max** | 12 |
| 十 | TMT 媒体（新） | `tmt` | ultra（空数据不外卖） | 8 |

## 套餐定义速查（2026-06 与 claw-server 对齐重排）

| 套餐 ↔ claw | 含 Scope（累进） | scope 数 |
|------|---------|:-------:|
| **免费**（无套餐引流） | `stock.basic` + `stock.kline` + `stock.indicator` | 3 |
| **Plus ↔ claw LOW** | + `stock.index` + `stock.minute` + `stock.financial` + `stock.research` + `stock.shareholder` | 8 |
| **Pro ↔ claw MID** | + **`stock.market`**（个股市场行为，URL `/stock/market/...`；⚠️ 生产 whoami 2026-06-08 返回仍是 `stock.market` 单一 scope）+ **`market`**（国内宏观，URL `/market/...`） | 10 |
| **Max ↔ claw HIGH** | + `stock.hk` + `stock.us` + `derivative` + `fund` + `bond` + `stock.intl-macro` + `forex` + `news` | 18 |
| **Ultra**（内部不外卖） | + `stock.selection` + `tmt` | 20 |

> 套餐为累进式包含。**以 `/openapi/v1/whoami` 返回的 `tier`/`scopes` 为准**（2026-06-08 实测 Max token 含 18 个 scope，见上表）。`@OpenApiScope` 用前缀通配（持有 `stock.*` 包含所有 `stock.xxx`），`*` 为管理员级。`stock.intl-macro` 的 URL 前缀是 `/openapi/v1/intl-macro/...`（不带 `stock/`），但 scope 名是 `stock.intl-macro`。
>
> **2026-06-08 生产实测要点**：
> - **`stock.market` 未拆分**：生产 whoami 仍返回单一 `stock.market` scope，原计划的 4 个子 scope（stock.plate/lhb/moneyflow/sentiment）**未落地**。
> - **非股票 scope 在 Max 层**：`market`/`derivative`/`fund`/`bond`/`forex`/`stock.intl-macro`/`news` 均在 **Max** tier（非 Ultra），whoami 实测 Max token 含这些 scope。
> - **`futures.basic` / `futures.kline` 从来不是独立 scope**（期货全部数据在 `derivative`，文档历史误列已删）。
> - **仅 `stock.selection` 和 `tmt` 是 Ultra**（选股/票房确实是内部不对外，Max token 无这 2 个 scope）。

---

## 一、股票（Stocks）

### Scope: `stock.basic` — 基础信息（**免费引流**）

| 表 | 用途 | Hyper | 主键 | 列数 | 关键列 |
|----|------|-------|------|------|--------|
| `stock_basic_info` | 股票基本信息 | No | ts_code | 19 | ts_code, symbol, name, area, industry, market, list_date, exchange, list_status, is_hs |
| `stock_company_info` | 上市公司信息 | No | ts_code | 17 | ts_code, com_name, chairman, manager, secretary, reg_capital, setup_date, province, city, employees |
| `stock_managers` | 公司管理层 | No | (ts_code, name) | 13 | ts_code, name, title, gender, edu, birthday, begin_date, end_date |
| `stock_stk_surv` | 机构调研 | No | (ts_code, surv_date) | 11 | ts_code, name, surv_date, rece_mode, rece_org, fund_visitors |
| `stock_trading_calendar` | 交易日历 | No | id | 4 | exchange, cal_date, is_open, pretrade_date |
| `stock_suspend_d` | 停复牌 | No | (ts_code, trade_date) | 5 | ts_code, trade_date, suspend_timing, suspend_type |
| `stock_new_share` | IPO 新股 | No | ts_code | 13 | ts_code, name, ipo_date, issue_date, price, pe, amount, market_amount |
| `stock_bse_mapping` | BSE 与主板 ts_code 映射 | No | (bse_code, ts_code) | 4 | bse_code, ts_code, mapping_type |

### Scope: `stock.kline` — K 线行情（**免费引流**）

| 表 | 用途 | Hyper | 主键 | 列数 | 关键列 |
|----|------|-------|------|------|--------|
| `stock_candles_daily` | 股票日 K 线 | **Yes** (trade_date) | (trade_date, ts_code) | 12 | ts_code, trade_date, open, high, low, close, pre_close, chg, pct_chg, vol, amount |
| `stock_candles_week` | 股票周 K 线 | **Yes** (trade_date) | (trade_date, ts_code) | 12 | 同日 K 线 |
| `stock_candles_month` | 股票月 K 线 | **Yes** (trade_date) | (trade_date, ts_code) | 12 | 同日 K 线 |
| `stock_adj_factor` | 复权因子 | No | (ts_code, trade_date) | 4 | ts_code, trade_date, adj_factor |
| `stock_percentage_change` | 多周期涨跌幅 | No | (ts_code, trade_date) | 17 | ts_code, trade_date, pct_chg, pct_chg_3d, pct_chg_1w, pct_chg_1m, pct_chg_1q, pct_chg_1y |
| `stock_weekly_monthly` | A 股周/月线（含 freq 字段） | **Yes** (trade_date) | (trade_date, ts_code, freq) | 13 | ts_code, trade_date, freq（W/M）, OHLC, vol, amount |
| `stock_week_month_adj` | A 股周/月线（复权版） | **Yes** (trade_date) | (trade_date, ts_code, freq, adj) | 14 | ts_code, trade_date, freq, adj（hfq/qfq）, OHLC |
| `stock_bak_basic` | 备用基础列表（25 列宽） | No | ts_code | 25 | ts_code, name, area, industry, list_date, market 等 |
| `stock_bak_daily` | 备用日线（32 列宽） | No | (trade_date, ts_code) | 32 | ts_code, trade_date, OHLCV, turnover, pe/pb, total_share/float_share |

### Scope: `stock.minute` — 分钟与盘前（**Plus 套餐 ↔ claw LOW**）

| 表 | 用途 | Hyper | 主键 | 列数 | 关键列 |
|----|------|-------|------|------|--------|
| `stock_candles_minutes` | 分钟 K 线 | **Yes** (trade_time) | (trade_time, ts_code) | 9 | ts_code, trade_time, open, high, low, close, vol, amount |
| `stock_minute_vol_snapshot` | 分钟成交快照 | No | id | 10 | ts_code, trade_date, minute_time, vol, amount, price, pct_change, turnover_rate |
| `stock_premarket` | 盘前每日股本 | No | (ts_code, trade_date) | 8 | ts_code, trade_date, total_share, float_share, up_limit, down_limit |
| `stock_idx_mins` | 指数分钟 K 线（独立表） | **Yes** (trade_time) | (trade_time, ts_code) | 9 | ts_code, trade_time, OHLC, vol, amount |

### Scope: `stock.index` — 指数与行业（**Plus 档**，原 Pro）

| 表 | 用途 | Hyper | 主键 | 列数 | 关键列 |
|----|------|-------|------|------|--------|
| `stock_index_info` | 指数基本信息 | No | id | 13 | ts_code, name, fullname, market, publisher, base_date, base_point |
| `stock_index_candles_daily` | 指数日 K 线 | **Yes** (trade_date) | (trade_date, ts_code) | 12 | ts_code, trade_date, open, high, low, close, vol, amount |
| `stock_index_candles_minutes` | 指数分钟 K 线 | No | (ts_code, trade_time) | 9 | 同分钟 K 线 |
| `stock_index_daily` | 指数成分股日行情 | No | id | 19 | ts_code, trade_date, name, close, pe, pb, float_mv, total_mv, weight |
| `stock_index_dailybasic` | 指数估值数据（PE/PB/市值） | **Yes** (trade_date) | (trade_date, ts_code) | 16 | ts_code, trade_date, total_mv, float_mv, pe, pe_ttm, pb, turnover_rate |
| `stock_index_weekly` | 指数周线 | **Yes** (trade_date) | (trade_date, ts_code) | 12 | 同指数日 K |
| `stock_index_monthly` | 指数月线 | **Yes** (trade_date) | (trade_date, ts_code) | 12 | 同指数日 K |
| `stock_index_weight` | 指数权重 | No | (index_code, ts_code, trade_date) | 5 | index_code, ts_code, trade_date, weight |
| `stock_index_global` | 国际主要指数 | **Yes** (trade_date) | (trade_date, ts_code) | 12 | ts_code（SPX/DJI/IXIC/HSI 等）, OHLC, vol |
| `stock_sw_industry_classify` | 申万行业分类 | No | (ts_code, sw_code) | 6 | ts_code, sw_code, sw_name, industry |
| `stock_sw_industry_classify_detail` | 行业分类明细 | No | (ts_code, sw_code) | 7 | 扩展行业分类信息 |
| `stock_sw_industry_classify_quo_daily` | 行业日行情 | **Yes** (trade_date) | (trade_date, sw_code) | 12 | sw_code, sw_name, trade_date, close, pct_chg |
| `stock_sw_industry_classify_quo_daily_last` | 行业最新行情快照 | No | sw_code | 11 | 最新行业行情 |

### Scope: `stock.indicator` — 技术指标 + 估值（**免费引流**）

| 表 | 用途 | Hyper | 主键 | 列数 | 关键列 |
|----|------|-------|------|------|--------|
| `stock_daily_tech_factor` | 日 K 线技术因子（综合） | **Yes** (trade_date) | (trade_date, ts_code) | 36 | ts_code, trade_date, close, adj_factor, close_hfq, close_qfq, macd, kdj_k, rsi_6, boll_upper |
| `stock_tech_ma_channel` | 均线与通道（28 × 3 复权 + 时间维 = 86 列） | **Yes** (trade_date) | (trade_date, ts_code) | 86 | ma_*5/10/20/30/60/90/250 (BFQ/HFQ/QFQ), ema_*, boll_upper/mid/lower, bbi, ktn_*, taq_*, expma_12/50 |
| `stock_tech_oscillator` | 振荡与情绪（18 × 3 + 4 = 62 列） | **Yes** (trade_date) | (trade_date, ts_code) | 62 | macd_dif/dea, kdj_k/d/j, rsi_6/12/24, bias1/2/3, dmi_*, cci, wr/wr1, brar_ar/br, cr |
| `stock_tech_trend_volume` | 趋势量能动量（15 × 3 = 47 列） | **Yes** (trade_date) | (trade_date, ts_code) | 47 | atr, obv, asi/asit, trix/trma, vr, psy, mtm, roc, emv, dfma, dpo, mass, mfi, xsii_td1~4 |
| `stock_short_term_tech_indicators` | 短线技术因子（19 个） | **Yes** (trade_date) | (trade_date, ts_code) | 27 | momentum_5/10, volatility_10/20, historical_vol, volume_ma_5/20, resistance_level, support_level, market_heat, attention_score, sentiment_index |
| `stock_quo_indicator_daily` | 每日估值指标 | **Yes** (trade_date) | (trade_date, ts_code) | 20 | ts_code, trade_date, close, turnover_rate, pe, pe_ttm, pb, ps, total_share, float_share, total_mv, circ_mv |
| `stock_quo_indicator_daily_last` | 估值最新快照 | No | ts_code | 19 | 同 daily（保留最新交易日） |
| `stock_nine_turn` | 九转序列 | No | (ts_code, trade_date) | 10 | ts_code, trade_date, turn_point, signal_strength |
| `stock_idx_factor_pro` | 指数技术因子（91 列宽表） | **Yes** (trade_date) | (trade_date, ts_code) | 91 | ts_code, trade_date, OHLCV + MA/EMA/BOLL/MACD/KDJ/RSI 等全套指数级技术因子 |

> **复权说明**：技术指标列后缀 `_bfq` / `_hfq` / `_qfq` = 不复权 / 后复权 / 前复权。线性指标可由 BFQ × adj_factor 推；非线性需独立计算。

### Scope: `stock.financial` — 财务报表（**Plus 套餐 ↔ claw LOW**）

| 表 | 用途 | Hyper | 主键 | 列数 | 关键列 |
|----|------|-------|------|------|--------|
| `stock_company_financial_reports` | 利润表 | No | (ts_code, end_date) | 65 | ts_code, end_date, basic_eps, total_revenue, revenue, operate_cost, sell_exp, admin_exp, fin_exp, rd_exp, ebit, ebitda, total_profit, n_income |
| `stock_company_balance_sheet_full` | 资产负债表（**完整 321 列**） | No | (ts_code, end_date) | 321 | total_assets, total_cur_assets, total_nca, accounts_receiv, inventories, fix_assets, total_liab, total_cur_liab, st_borr, lt_borr, total_hldr_eqy_exc_min_int — **完整字段见 SQL 第 683-846 行** |
| `stock_cash_flow_statement` | 现金流量表（**完整 201 列**） | No | (ts_code, end_date) | 201 | c_fr_sale_sg, n_cashflow_act, c_paid_goods_s, n_cashflow_inv_act, c_recp_borrow, n_cashflow_fnc_act, free_cashflow — **完整字段见 SQL 第 849-951 行** |
| `stock_financial_indicator` | 财务指标（**完整 341 列**） | No | (ts_code, end_date) | 341 | eps, bps, ocfps, roe, roa, roic, grossprofitmargin, netprofitmargin, currentratio, quickratio, debttoassets, inventory_turn — **完整字段见 SQL 第 970-1114 行** |
| `stock_financial_data` | 分业务营收 | No | (ts_code, end_date, bz_item) | 8 | ts_code, end_date, bz_item, bz_sales, bz_profit, bz_cost |
| `stock_core_financials` | 核心财务摘要 | No | (ts_code, end_date) | 26 | eps, bps, roe, roa, gross_profit_margin, net_profit_margin, current_ratio, debt_to_assets, revenue_yoy, net_profit_yoy |
| `stock_dividend_data` | 分红派息 | No | (ts_code, end_date) | 14 | ts_code, end_date, stk_div, cash_div, cash_div_tax, record_date, ex_date, pay_date |
| `stock_repurchase` | 股票回购 | No | (ts_code, report_date) | 11 | ts_code, report_date, repurchase_amount, repurchase_shares, repurchase_avprice |
| `stock_pledge_stat` | 股权质押统计 | No | (ts_code, end_date) | 8 | ts_code, end_date, pledge_count, pledge_shares, pledge_ratio |
| `stock_disclosure_date` | 业绩披露日历（预约/实际） | No | (ts_code, end_date) | 6 | ts_code, end_date, ann_date, pre_date, actual_date, modify_date |
| `stock_express` | 业绩快报 | No | (ts_code, end_date) | 18 | ts_code, end_date, ann_date, revenue, n_income, total_assets, total_hldr_eqy_exc_min_int |
| `stock_forecast` | 业绩预告 | No | (ts_code, ann_date, end_date) | 13 | ts_code, ann_date, end_date, type, p_change_min, p_change_max, summary |

### Scope: **`stock.market`** — 板块 + 龙虎榜 + 资金流 + 热度（47 张表；**Pro 套餐 ↔ claw MID**；⚠️ 生产 scope 名仍是 `stock.market`，4子scope分拆未落地）

> **2026-06-08 实测**：`stock.market` 仍是单一 Pro scope，REST URL `/openapi/v1/stock/market/...`。下面的子分类（板块/资金流/龙虎榜/热度情绪/涨跌停）仅为数据逻辑分组，**不代表独立的 scope 名**——whoami 只返回 `stock.market`，判断权限时不要用 stock.plate/lhb/moneyflow/sentiment。

#### 板块（DC 东财）— 逻辑分组（实际 scope: `stock.market`）

| 表 | 用途 | Hyper | 关键列 |
|----|------|-------|--------|
| `stock_dc_plate` | 板块聚合（涨跌/资金/排名） | No | ts_code, name, trade_date, content_type, pct_change, close, net_amount |
| `stock_dc_plate_constituents` | 板块成分股 | No | ts_code, plate_ts_code, name |
| `stock_dc_plate_market_cash_flow` | 板块资金流（4 档） | No | ts_code, trade_date, net_amount, buy/sell_sm/md/lg/elg_vol |
| `stock_dc_plate_continue_net_amount` | 板块连续净流入 | No | ts_code, name, last_date, amount, avg_amount |
| `stock_dc_mainboard_market_data` | 主板市场数据 | No | trade_date, content_type, pct_change, net_amount, avg_price, pe, pb |
| `stock_ths_member` | 同花顺概念成分 | No | ts_code, concept_code, concept_name, in_date |
| `stock_ths_index` | 同花顺概念/行业指数列表 | No | ts_code, name, type, list_date |
| `stock_ths_daily` | 同花顺概念/行业指数日 K（1234 行/日） | **Yes** (trade_date) | ts_code, trade_date, OHLC, vol, turnover_rate, total_mv |
| `stock_ths_hot` | 同花顺 App 热榜（4 列 UK） | No | ts_code, trade_date, type, rank |
| `stock_tdx_index` | 通达信板块基础 | No | ts_code, name, type, list_date |
| `stock_tdx_member` | 通达信板块成分 | No | ts_code, plate_code, plate_name |
| `stock_tdx_daily` | 通达信板块日 K（~36 列宽表） | **Yes** (trade_date) | ts_code, trade_date, OHLC, return_3day/1year, ma5/10/20 |
| `stock_ci_daily` | 中信行业指数日行情 | **Yes** (trade_date) | ts_code, trade_date, OHLC, vol, amount, pct_chg |
| `stock_ci_index_member` | 中信行业指数成分（5 列 UK） | No | ts_code, ci_code, ci_name |
| `stock_kpl_concept_cons` | 开盘啦概念成分股 | No | ts_code, concept_code, description |

#### 资金流 — 逻辑分组（实际 scope: `stock.market`）

| 表 | 用途 | Hyper | 关键列 |
|----|------|-------|--------|
| `stock_money_flow` | 个股资金流向（4 档买卖量额） | **Yes** (trade_date) | ts_code, trade_date, buy/sell_sm/md/lg/elg_vol, net_mf_vol, net_mf_amount |
| `stock_moneyflow_dc` | 个股资金流（DC 来源） | No | 同 stock_money_flow |
| `stock_moneyflow_hsgt` | 沪深港通资金流 | No | ts_code, trade_date, hgt_in, sgt_in, hk_in |
| `stock_moneyflow_ths` | 同花顺个股资金流 | No | ts_code, trade_date, net_amount, total_buy_amount, total_sell_amount |
| `stock_moneyflow_cnt_ths` | 同花顺概念资金流 | No | ts_code, trade_date, net_amount, pct_change |
| `stock_moneyflow_ind_ths` | 同花顺行业资金流 | No | ts_code, trade_date, net_amount, sector_name |

#### 龙虎榜 — 逻辑分组（实际 scope: `stock.market`）

| 表 | 用途 | Hyper | 关键列 |
|----|------|-------|--------|
| `stock_lhb_day` | 龙虎榜日数据 | No | ts_code, trade_date, name, close, pct_change, l_sell, l_buy, net_amount, reason |
| `stock_lhb_institution` | 龙虎榜机构席位 | No | ts_code, trade_date, institution, volume, amount |
| `stock_institution_trading_list_records` | 机构交易列表 | No | ts_code, report_date, business_name, buy_vol, sell_vol |
| `stock_broker_trade_detail` | 券商交易明细 | No | ts_code, trade_date, broker_name, buy_amount, sell_amount, net_amount |
| `stock_hm_list` | 市场游资名录 | No | ts_code, trade_date, name, hot_rank |

#### 热度与情绪 — 逻辑分组（实际 scope: `stock.market`）

| 表 | 用途 | Hyper | 关键列 |
|----|------|-------|--------|
| `stock_hot_rank` | 热度排名 | No | ts_code, trade_date, name, hot_score, rank |
| `stock_dc_hot` | 东财热榜 | No | ts_code, trade_date, name, hot_score, rank |
| `stock_dc_guba_rank` | 股吧排名 | No | ts_code, trade_date, name, post_count, rank |
| `stock_kpl_list` | 开盘啦榜单 | No | ts_code, trade_date, name, rank, hot_score |
| `stock_news_daily_sentiment` | 全市场新闻舆情日度（ML 特征，词典法聚合，非个股） | No | trade_date, total_news_count, positive_count, negative_count, avg_sentiment_score, news_volume_ma5, news_surge_ratio, src_diversity |
| `stock_macro_monthly` | 行业层宏观月度（ML 特征） | No | date, gdp_growth, cpi, pmi, ppi, m1_growth, m2_growth |
| `stock_hsgt_top10` | 沪深股通十大成交股 | No | ts_code, trade_date, name, hgt_volume, hgt_amount, rank |
| `stock_cyq_perf` | 每日筹码胜率 | No | ts_code, trade_date, win_rate, avg_cost, profit_ratio |
| `stock_cyq_chips` | 筹码分布明细（每股 N 价位） | No | (ts_code, trade_date, price) | 8 | ts_code, trade_date, price, percent, cum_percent |

#### 涨跌停 / 集合竞价 / 大宗 / 游资 — 逻辑分组（实际 scope: `stock.market`）

| 表 | 用途 | Hyper | 关键列 |
|----|------|-------|--------|
| `stock_limits` | 涨跌停价格 | No | ts_code, trade_date, up_limit, down_limit, pre_close |
| `stock_limit_analysis` | 涨停分析（连板） | No | ts_code, trade_date, limit_status, continuous_days, open_pct |
| `stock_limit_step` | 连板天梯（连续涨停） | No | ts_code, trade_date, nums, theme, lu_desc |
| `stock_limit_cpt_list` | 最强板块（涨停统计） | No | ts_code, trade_date, name, cont_lu_nums, lu_num |
| `stock_limit_list_ths` | 同花顺涨停列表 | No | ts_code, trade_date, name, status, lu_time, last_time |
| `stock_st_daily` | A 股 ST 列表 | No | ts_code, trade_date, name, st_type |
| `stock_st_warning` | ST 警示公告 | No | (ts_code, pub_date) | 6 | ts_code, pub_date, st_type, content |
| `stock_auction_open` | 开盘集合竞价 | No | ts_code, trade_date, open_price, open_vol, open_amount, pre_close |
| `stock_auction_close` | 收盘集合竞价 | No | ts_code, trade_date, close_price, close_vol, close_amount |
| `stock_block_trade` | 大宗交易 | No | ts_code, trade_date, buyer, seller, volume, price, amount |
| `stock_hm_list` | 市场游资名录 | No | ts_code, trade_date, name, hot_rank |
| `stock_hm_detail` | 游资买卖明细 | No | (ts_code, trade_date, hm_name) | 8 | ts_code, trade_date, hm_name, buy_amount, sell_amount, net_amount |

### Scope: `stock.shareholder` — 股东数据（含港股通持股）（**Plus 套餐 ↔ claw LOW**）

| 表 | 用途 | Hyper | 主键 | 列数 | 关键列 |
|----|------|-------|------|------|--------|
| `stock_shareholder_holdings` | 股东持仓 | No | (ts_code, ann_date, end_date, holder_name) | 13 | ts_code, ann_date, end_date, holder_name, hold_amount, hold_ratio, holder_type |
| `stock_shareholder_statistics` | 股东户数统计 | No | (ts_code, end_date) | 6 | ts_code, end_date, holder_num, per_share_equity |
| `stock_shareholder_classify` | 股东分类汇总 | No | (ts_code, end_date, holder_type) | 7 | ts_code, end_date, holder_type, hold_amount, hold_ratio |
| `stock_shareholder_float` | 流通股东 | No | (ts_code, end_date, holder_name) | 9 | ts_code, end_date, holder_name, float_hold_amount, float_hold_ratio |
| `stock_holder_trade` | 股东增减持 | No | (ts_code, announce_date, holder_name) | 12 | ts_code, announce_date, holder_name, change_amount, change_ratio, trade_avg_price, total_hold_ratio |
| `stock_ccass_hold` | 中央结算系统持股统计 | No | (ts_code, trade_date) | 7 | ts_code, trade_date, name, shareholding, hold_count |
| `stock_ccass_hold_detail` | 中央结算持股明细（每股 N 行机构） | No | (ts_code, trade_date, col_participant_id) | 9 | ts_code, trade_date, participant_id, name, hold_amount |
| `stock_hk_hold` | 沪深股通持股明细 | No | (ts_code, trade_date, code) | 8 | ts_code, trade_date, code（机构）, name, vol, ratio |
| `stock_hsgt_list` | 沪深股通成分股列表 | No | (ts_code, type) | 4 | ts_code, type（HG/SG/HK）, name, in_date |
| `stock_ggt_daily` | 港股通每日成交统计 | **Yes** (trade_date) | (trade_date, name) | 5 | trade_date, name（港股通南向/北向）, buy_amount, sell_amount, net_amount |
| `stock_ggt_monthly` | 港股通月度统计（month=YYYYMM） | No | (month, type) | 6 | month, type, total_buy, total_sell, net |

### Scope: `stock.research` — 券商研报 + 评级（**Plus 套餐 ↔ claw LOW**）

| 表 | 用途 | Hyper | 主键 | 列数 | 关键列 |
|----|------|-------|------|------|--------|
| `stock_research_report` | 个股研报 | No | (ts_code, report_date, title) | 11 | ts_code, name, report_date, org_name, author, title, report_type, classify, rating |
| `stock_report_rc` | 卖方评级（report_date probe） | No | (ts_code, report_date, org_name) | 13 | ts_code, name, report_date, org_name, quarter, rating, target_price |
| `stock_broker_recommend` | 券商月度推荐组合（month=YYYYMM） | No | (month, ts_code, broker_name) | 8 | month, ts_code, name, broker_name, weight, reason |

### Scope: `stock.selection` — 选股（**Ultra 内部档**，ML 选股当前空表，仅内部）

| 表 | 用途 | Hyper | 主键 | 列数 | 关键列 |
|----|------|-------|------|------|--------|
| `stock_ml_selection_result` | ML 智能选股结果 | No | (ts_code, trade_date, model_id) | 12 | ts_code, trade_date, model_id, score, signal, confidence |
| `stock_ml_backtest_summary` | ML 选股回测摘要 | No | (model_id, start_date, end_date) | 13 | model_id, start_date, end_date, total_return, max_drawdown, sharpe_ratio, hit_rate |
| `stock_value_selection_result` | 长期价值选股 | No | (ts_code, trade_date) | 15 | ts_code, trade_date, pb, pe, value_score, signal |
| `stock_momentum_selection_result` | 中短期博弈选股 | No | (ts_code, trade_date) | 16 | ts_code, trade_date, momentum_score, trend_signal, strength |

---

## 二、港股（Hong Kong Stocks，2026-05-22 新增大类）

### Scope: `stock.hk` — 港股完整数据（**Max 套餐 ↔ claw HIGH**）

港股专属数据集，与 A 股 `stock.basic` / `stock.kline` / `stock.financial` 结构平行但 schema 独立（不同上市规则与会计准则）。

| 表 | 用途 | Hyper | 主键 | 列数 | 关键列 |
|----|------|-------|------|------|--------|
| `stock_hk_basic` | 港股基础信息 | No | ts_code | 18 | ts_code（如 00700.HK）, name, fullname, list_date, list_status, market |
| `stock_hk_tradecal` | 港股交易日历 | No | (exchange, cal_date) | 4 | exchange, cal_date, is_open |
| `stock_hk_daily` | 港股日 K | **Yes** (trade_date) | (trade_date, ts_code) | 12 | ts_code, trade_date, OHLC, vol, amount |
| `stock_hk_daily_adj` | 港股日 K（复权 + 估值）| **Yes** (trade_date) | (trade_date, ts_code) | 19 | + adj OHLC + pe/pb + 总市值/流通市值 |
| `stock_hk_adjfactor` | 港股复权因子 | No | (ts_code, trade_date) | 5 | ts_code, trade_date, adj_factor, fwd_adj_factor, bwd_adj_factor |
| `stock_hk_mins` | 港股分钟 K（实际归 stock.minute 子能力，但 hk 独立 scope 兼容）| **Yes** (trade_time) | (trade_time, ts_code) | 9 | ts_code, trade_time, OHLC, vol |
| `stock_hk_income` | 港股利润表（long format）| No | (ts_code, end_date, name) | 6 | ts_code, end_date, name（科目名）, ind_name, ind_value |
| `stock_hk_balancesheet` | 港股资产负债表（long format）| No | (ts_code, end_date, name) | 6 | 同 hk_income 结构 |
| `stock_hk_cashflow` | 港股现金流量表（long format）| No | (ts_code, end_date, name) | 6 | 同 hk_income 结构 |
| `stock_hk_fina_indicator` | 港股财务指标（~85 列宽表）| No | (ts_code, end_date) | 85 | ts_code, end_date, eps, bps, roe, roa, debt_to_assets 等 |
| `stock_ah_comparison` | A/H 股比价 | **Yes** (trade_date) | (trade_date, ts_code) | 8 | a_ts_code, h_ts_code, trade_date, a_price, h_price, premium_rate ⚠️ 无 OpenAPI 端点（已入库未暴露）|

> 港股通持股相关的 `stock_ccass_*` / `stock_hk_hold` / `stock_ggt_*` 表归在 `stock.shareholder` scope 下（数据本质是 A 股投资人对港股的持仓视角）。

---

## 三、美股（US Stocks，2026-05-22 新增大类）

### Scope: `stock.us` — 美股完整数据（**Max 套餐 ↔ claw HIGH**；⚠️ Tushare 需 VIP 权限）

| 表 | 用途 | Hyper | 主键 | 列数 | 关键列 |
|----|------|-------|------|------|--------|
| `stock_us_basic` | 美股基础信息 | No | ts_code | 17 | ts_code（如 AAPL.O，带 .O/.N 交易所后缀）, name, exchange（NAS/NYS/OTC）, list_date, sector |
| `stock_us_tradecal` | 美股交易日历 | No | (exchange, cal_date) | 4 | exchange, cal_date, is_open |
| `stock_us_daily` | 美股日 K（含 pe/pb）| **Yes** (trade_date) | (trade_date, ts_code) | 14 | ts_code, trade_date, OHLC, vol, pe, pb |
| `stock_us_daily_adj` | 美股日 K（复权 + 分类）| **Yes** (trade_date) | (trade_date, ts_code) | 18 | + adj OHLC + exchange |
| `stock_us_adjfactor` | 美股复权因子 | No | (ts_code, trade_date) | 5 | ts_code, trade_date, adj_factor, fwd_adj_factor, bwd_adj_factor |
| `stock_us_income` | 美股利润表（long format）| No | (ts_code, end_date, name) | 6 | ts_code, end_date, name, ind_name, ind_value |
| `stock_us_balancesheet` | 美股资产负债表 | No | (ts_code, end_date, name) | 6 | 同 |
| `stock_us_cashflow` | 美股现金流量表 | No | (ts_code, end_date, name) | 6 | 同 |
| `stock_us_fina_indicator` | 美股财务指标（~66 列宽表）| No | (ts_code, end_date) | 66 | ts_code, end_date, eps, bps, roe, gross_margin |

---

## 四、期货期权（Derivatives）

### Scope: `derivative` — 期货 + 期权 + SGE 上海黄金（**Max**）

> 期货全部数据（`futures_*` 表）都归在本 scope，**没有独立的 `futures.basic` / `futures.kline` scope**（文档历史误列，已删）。**不含可转债**（可转债 `cb_*` 在 `bond` scope）。

| 表 | 用途 | Hyper | 主键 | 列数 | 关键列 |
|----|------|-------|------|------|--------|
| `futures_basic_info` | 期货基础信息 | No | ts_code | 13 | ts_code, name, exchange, market_type, multiplier, min_change, min_order |
| `futures_daily` | 期货日线 | **Yes** | (trade_date, ts_code) | 12 | ts_code, trade_date, open, high, low, close, vol, amount, open_interest |
| `futures_weekly_monthly` | 期货周/月线 | **Yes** | (trade_date, ts_code, cycle) | 13 | ts_code, trade_date, cycle, close |
| `futures_weekly_detail` | 期货周度详细数据 | No | (ts_code, week_date) | 10 | ts_code, week_date, prod_name, vol, oi, week_open, week_close |
| `futures_minutes` | 期货分钟 K 线 | **Yes** (trade_time) | (trade_time, ts_code) | 9 | ts_code, trade_time, open, high, low, close, vol, amount |
| `futures_holding` | 期货持仓排名 | No | (ts_code, trade_date, rank) | 8 | ts_code, trade_date, rank, vol, vol_chg |
| `futures_limit` | 涨跌停价格 | **Yes** | (trade_date, ts_code) | 5 | ts_code, trade_date, up_limit, down_limit |
| `futures_mapping` | 主力连续合约映射 | **Yes** | (trade_date, underlying_code) | 4 | underlying_code, main_code, trade_date |
| `futures_settle` | 结算参数 | **Yes** | (trade_date, ts_code) | 8 | ts_code, trade_date, settle_price, pre_settle, delta |
| `futures_wsr` | 期货仓单日报 | No | (ts_code, date) | 9 | ts_code, date, warehouse, receipt_vol, change |
| `option_contracts` | 期权合约（**ETF/股指/商品/能源全 8 所**：SSE/SZSE/CFFEX/SHFE/DCE/CZCE/INE/GFEX，21 万+ 合约，仅元数据无价格） | No | ts_code | 18 | ts_code, opt_code(标的码=OP+标的), exchange, call_put, exercise_price, s_month, maturity_date, per_unit |
| `option_daily` | 期权日线（**带日期的期权价格筛选都查这张**：某日最低/收盘/结算/涨跌幅、跨日比价排序） | **Yes** | (trade_date, ts_code) | 18 | ts_code, trade_date, open, high, low, close, settle, pre_settle, vol, open_interest |
| `option_minutes` | 期权分钟 K 线 | **Yes** (trade_time) | (trade_time, ts_code) | 9 | 同期权分钟 |
| `sge_basic_info` | 上海黄金交易所产品 | No | ts_code | 11 | ts_code, name, market_type, min_change |
| `sge_daily` | 上海黄金日线 | **Yes** | (trade_date, ts_code) | 11 | ts_code, trade_date, open, high, low, close, vol, amount |

---

## 五、基金 + ETF（Funds & ETFs）

### Scope: `fund` — ETF + 公募基金（**Max**）

#### ETF

| 表 | 用途 | Hyper | 主键 | 列数 | 关键列 |
|----|------|-------|------|------|--------|
| `etf_basic_info` | ETF 基础信息 | No | ts_code | 15 | ts_code, name, fund_type, underlying_index, total_size, expense_ratio |
| `etf_candles_daily` | ETF 日线 | **Yes** | (trade_date, ts_code) | 12 | ts_code, trade_date, close, open, high, low, vol, amount |
| `etf_index` | ETF 跟踪指数映射 | No | ts_code | 8 | ts_code, index_code, index_name |
| `etf_share_size` | ETF 份额规模 | **Yes** | (trade_date, ts_code) | 5 | ts_code, trade_date, total_share, change_pct |
| `etf_adj_factor` | ETF 复权因子 | **Yes** | (trade_date, ts_code) | 4 | ts_code, trade_date, adj_factor |

#### 公募基金

| 表 | 用途 | Hyper | 主键 | 列数 | 关键列 |
|----|------|-------|------|------|--------|
| `fund_basic` | 公募基金列表 | No | ts_code | 24 | ts_code, name, fund_type, setup_date, status, per_fund_size, total_size, manager_code |
| `fund_company` | 基金公司 | No | id | 16 | name, short_name, established_date, total_assets, fund_count |
| `fund_nav` | 基金净值 | **Yes** (nav_date) | (nav_date, ts_code) | 6 | ts_code, nav_date, unit_nav, total_nav, daily_growth |
| `fund_div` | 基金分红 | No | (ts_code, announce_date) | 11 | ts_code, announce_date, div_per_share, record_date, pay_date |
| `fund_portfolio` | 基金持仓 | No | (ts_code, period_end, holding_code) | 7 | ts_code, period_end, holding_code, holding_name, vol, ratio |
| `fund_share` | 基金规模历史 | No | (ts_code, statistic_date) | 6 | ts_code, statistic_date, total_share, share_change |
| `fund_manager` | 基金经理 | No | (ts_code, manager_id) | 10 | ts_code, manager_id, manager_name, appointment_date, removal_date |
| `fund_factor_pro` | 基金技术因子 | No | (ts_code, factor_date) | 12 | ts_code, factor_date, momentum, volatility, value_score |
| `fund_sales_ratio` | 基金销售机构占比（年度） | No | (year, name) | 6 | year, name（机构名）, market_share, public_amount, fund_amount |
| `fund_sales_vol` | 基金销售机构规模（季度） | No | (year, quarter, name) | 8 | year, quarter, name, rank, stock_amount, mixed_amount, total_amount |

---

## 六、宏观（Macro）

### Scope: `market` — 宏观经济（**Pro**，纯国内宏观，新闻已拆到 `news`（Max））

> CPI/PPI/PMI/GDP/M0M1M2/社融 + Shibor/LPR + 政策档案 + 经济事件日历。**`news_list` 已移到 `news` scope**（见下文「七、新闻资讯」）。

| 表 | 用途 | Hyper | 主键 | 列数 | 关键列 |
|----|------|-------|------|------|--------|
| `macro_shibor` | Shibor 拆借利率 | No | trade_date | 8 | trade_date, sobibor_on, shibor_1w, shibor_1m, shibor_3m, shibor_6m, shibor_12m |
| `macro_lpr` | LPR 贷款利率 | No | trade_date | 4 | trade_date, lpr_1y, lpr_5y |
| `macro_cn_cpi` | CPI 居民物价 | No | stat_date | 5 | stat_date, cpi_index, cpi_yoy, cpi_mom |
| `macro_cn_ppi` | PPI 工业生产者价格 | No | stat_date | 5 | stat_date, ppi_index, ppi_yoy, ppi_mom |
| `macro_cn_pmi` | PMI 采购经理指数 | No | stat_date | 7 | stat_date, pmi_mfg, pmi_nms, pmi_svces |
| `macro_cn_gdp` | GDP 国内生产总值 | No | quarter | 8 | quarter, gdp, gdp_yoy, pi, si, ti |
| `macro_cn_money_supply` | M0/M1/M2 货币 | No | stat_date | 8 | stat_date, m0, m1, m2, m0_yoy, m1_yoy, m2_yoy |
| `macro_cn_social_finance` | 社会融资增量 | No | stat_date | 10 | stat_date, total_sf, sf_yoy, entrust_loan, bank_accept, corporate_bond |
| `macro_eco_cal` | 经济事件日历（5 列 UK） | No | (event_id, country, event_name, event_time, importance) | 9 | event_id, country, event_name, event_time, importance, value, forecast, prev |
| `macro_policy_npr` | 政策档案（央行/财政等） | No | pcode | 7 | pcode, ann_date, title, content_html, source, level |

---

## 七、新闻资讯（News，2026-06 从宏观大类拆出）

### Scope: `news` — 实时新闻 / 资讯（**Max**，2026-06 从 `market` 拆出）

> 2026-06 把实时新闻从 `market` scope 拆为独立的 `news` scope（tier=plus），作为高级档差异化卖点。

| 表 | 用途 | Hyper | 主键 | 列数 | 关键列 |
|----|------|-------|------|------|--------|
| `news_list` | 新闻列表（实时新闻 / 资讯，按类型/关键字/时间筛选） | No | id | 9 | title, content, publish_date, source, url |

---

## 八、国际宏观（Intl Macro，2026-05-22 新增大类）

### Scope: `stock.intl-macro` — 美国/香港/国际利率（**Max**；scope名 `stock.intl-macro`，URL前缀 `/openapi/v1/intl-macro/*` 不含 `stock/`）

| 表 | 用途 | Hyper | 主键 | 列数 | 关键列 |
|----|------|-------|------|------|--------|
| `macro_us_tycr` | 美国国债收益率曲线 | No | date | 14 | date, m1, m3, m6, y1, y2, y3, y5, y7, y10, y20, y30 |
| `macro_us_trycr` | 美国国债实际收益率曲线 | No | date | 9 | date, y5, y7, y10, y20, y30（实际利率，扣 CPI）|
| `macro_us_tbr` | 美短期国债利率 | No | date | 5 | date, w4_bd（4 周）, w13_bd（13 周）, w26_bd, w52_bd |
| `macro_us_tltr` | 美长期国债利率 | No | date | 5 | date, ltc（长期组合）, cmt（恒定到期）, e_factor |
| `macro_us_trltr` | 美长期实际利率平均值 | No | date | 4 | date, ltr_avg, ltr_avg_change |
| `macro_hibor` | 香港 HIBOR 同业拆借利率 | No | trade_date | 9 | trade_date, on（隔夜）, w1, w2, m1, m3, m6, m12 |
| `macro_libor` | 国际 LIBOR 拆借利率 | No | (trade_date, curr_type) | 8 | trade_date, curr_type（USD/EUR/JPY/GBP/CHF）, on, w1, m1, m3, m6 |
| `macro_gz_index` | 广州民间融资利率（GZ Index） | No | trade_date | 6 | trade_date, gz_index_avg, gz_index_max, gz_index_min |
| `macro_wz_index` | 温州民间融资利率（WZ Index） | No | trade_date | 6 | trade_date, wz_general_index, wz_personal_index, wz_total_amount |

---

## 九、外汇（Forex，2026-05-22 新增大类）

### Scope: `forex` — 外汇基础与日线（**Max**）

| 表 | 用途 | Hyper | 主键 | 列数 | 关键列 |
|----|------|-------|------|------|--------|
| `forex_obasic` | 外汇产品基础信息 | No | ts_code | 8 | ts_code（USDCNH/EURUSD 等）, name, classify, exchange, min_unit |
| `forex_daily` | 外汇日线 | **Yes** (trade_date) | (trade_date, ts_code) | 9 | ts_code, trade_date, bid_open, bid_close, ask_open, ask_close, tick_qty |

---

## 十、TMT 媒体（Technology, Media, Telecom，2026-05-22 新增大类）

### Scope: `tmt` — 电影/电视剧/电视/台湾电子（**Ultra 内部档**，原 Plus；票房 7/8 张空表待补齐，暂不外卖）

| 表 | 用途 | Hyper | 主键 | 列数 | 关键列 |
|----|------|-------|------|------|--------|
| `tmt_bo_cinema` | 影院票房数据 | No | (date, name) | 9 | date, name（影院名）, area, total_box, person_count, attendance_rate |
| `tmt_bo_daily` | 日票房 | No | (date, ranking) | 8 | date, ranking, name, box_office, total_box_office, week_in_box_office |
| `tmt_bo_weekly` | 周票房（周一发布） | No | (date, ranking) | 8 | 同日票房（按周聚合） |
| `tmt_bo_monthly` | 月票房（月初发布） | No | (date, ranking) | 8 | 同日票房（按月聚合） |
| `tmt_film_record` | 电影备案（年度备案制） | No | (ann_date, film_name) | 9 | ann_date, film_name, owners, dir, scr, license_no |
| `tmt_teleplay_record` | 电视剧备案 | No | license_key | 11 | license_key, ann_date, name, episodes, owners, prod_company |
| `tmt_twincome` | 台湾电子合计营收 | No | (date, item) | 8 | date, item（8001 合计 / 8002 子分类）, value, ratio_yoy |
| `tmt_twincome_detail` | 台湾电子明细营收 | No | (date, ts_code) | 11 | date, ts_code, name, monthly_income, yoy_growth |

---

## 十一、债券 + 可转债（Bond）

> 状态：12 个端点已上线（**Max**）。`bc_otcqt` / `bc_bestotcqt` 是银行间柜台报价，机构间用，**暂不开放给 OpenAPI**。

### Scope: `bond` — 可转债 + 债券（**Max**）

| 表 | 用途 | Hyper | 主键 | 列数 | 关键列 | 端点 |
|----|------|-------|------|------|--------|------|
| `cb_basic_info` | 可转债基础信息 | No | ts_code | 15 | ts_code, bond_short_name, stk_code, list_date, maturity_date, conv_price, coupon_rate, issue_rating | `/openapi/v1/bond/cb/list` |
| `cb_daily` | 可转债日行情 | **Yes** | (trade_date, ts_code) | 15 | ts_code, trade_date, open/close, bond_value/over_rate, cb_value/over_rate | `/openapi/v1/bond/cb/daily` |
| `cb_factor_pro` | 可转债技术因子 | **Yes** | (trade_date, ts_code) | 10 | ts_code, trade_date, OHLC, factor_data (JSONB) | `/openapi/v1/bond/cb/factor` |
| `cb_issue` | 可转债发行 | No | (ts_code, ann_date) | 12 | plan_issue_size, issue_size, issue_price, onl_winning_rate, lead_underwriter | `/openapi/v1/bond/cb/issue` |
| `cb_call` | 可转债赎回 | No | (ts_code, ann_date, call_type) | 11 | call_type（到期/强赎/回售）, is_call, call_price, call_date, payment_date | `/openapi/v1/bond/cb/call` |
| `cb_rate` | 可转债票面利率分档 | No | (ts_code, rate_start_date) | 5 | rate_start_date, rate_end_date, coupon_rate | `/openapi/v1/bond/cb/rate` |
| `cb_price_chg` | 可转债转股价变动 | No | (ts_code, change_date) | 7 | publish_date, change_date, convertprice_bef/aft | `/openapi/v1/bond/cb/price-chg` |
| `cb_share` | 可转债转股结果 | No | (ts_code, end_date) | 15 | end_date, convert_val/vol/ratio, acc_*, remain_size | `/openapi/v1/bond/cb/share` |
| `repo_daily` | 国债逆回购日行情 | **Yes** | (trade_date, ts_code) | 12 | ts_code（如 204001.SH=GC001）, weight_r（加权利率） | `/openapi/v1/bond/repo/daily` |
| `yc_cb` | 国债 / 中债收益率曲线 | **Yes** | (trade_date, ts_code, curve_type, curve_term) | 6 | curve_type（0 到期/1 即期）, curve_term（年）, yield | `/openapi/v1/bond/yc` |
| `bond_blk` | 债券大宗交易 | **Yes** | (trade_date, ts_code, price) | 6 | ts_code, name, price, vol, amount | `/openapi/v1/bond/blk` |
| `bond_blk_detail` | 债券大宗交易明细 | **Yes** | (trade_date, ts_code, price, buy_dp, sell_dp) | 8 | + buy_dp / sell_dp（买卖营业部） | `/openapi/v1/bond/blk-detail` |
| `bc_otcqt` | 银行间柜台报价 | No | (trade_date, qt_time, bank, ts_code) | 13 | bank, buy_price, sell_price, buy_yield, sell_yield | ⏸ 不暴露 |
| `bc_bestotcqt` | 银行间最优报价 | No | (trade_date, ts_code) | 11 | best_buy_bank, best_buy_yield, best_sell_bank | ⏸ 不暴露 |

---

## SYSTEM 表（不入 OpenAPI）

| 表 | 用途 | 关键列 |
|----|------|--------|
| `user` | 用户表 | id, username, email, password, is_active |
| `user_stock_collect_list` | 自选股 | user_id, ts_code, collect_date, remark |
| `user_stock_strategy_config` | 用户策略配置 | id, user_id, strategy_name, is_active |
| `user_stock_strategy_score_rule` | 策略评分规则 | id, config_id, field_name, rule_expression, score_value |
| `user_stock_daily_score_result` | 日评分结果 | user_id, ts_code, score_date, config_id, total_score |
| `user_stock_daily_score_rule_detail` | 评分明细 | result_id, rule_id, field_name, actual_value, score_awarded |
| `api_token` | OpenAPI Token | id, user_id, token_hash, token_name, allowed_ips, scopes, expires_at |
| `api_token_access_log` | OpenAPI 审计 | token_id, request_path, client_ip, http_status, response_time_ms |
| `data_sync_task_record` | 同步任务记录 | trade_date, task_name, status, started_at, ended_at, record_count |
| `data_polling_session` | 轮询会话记录 | trade_date, exchange, session_status, completed_tasks, failed_tasks |

---

## 数据查询速查表

| 业务需求 | 推荐表 | 时间列 | 标识列 |
|---------|--------|--------|--------|
| K 线（日/周/月） | `stock_candles_daily/week/month` | trade_date | ts_code |
| 分钟 K 线 | `stock_candles_minutes` | trade_time | ts_code |
| 综合技术指标 | `stock_daily_tech_factor` | trade_date | ts_code |
| MA/EMA/BOLL 通道 | `stock_tech_ma_channel` | trade_date | ts_code |
| MACD/KDJ/RSI 振荡 | `stock_tech_oscillator` | trade_date | ts_code |
| 趋势量能 | `stock_tech_trend_volume` | trade_date | ts_code |
| 估值（PE/PB/市值） | `stock_quo_indicator_daily(_last)` | trade_date | ts_code |
| 多周期涨跌幅 | `stock_percentage_change` | trade_date | ts_code |
| 三大财务报表 | `stock_company_financial_reports` / `stock_company_balance_sheet_full` / `stock_cash_flow_statement` | end_date | ts_code |
| 财务综合指标 | `stock_financial_indicator` | end_date | ts_code |
| 个股资金流 | `stock_money_flow` / `stock_moneyflow_dc` | trade_date | ts_code |
| 北向资金 | `stock_moneyflow_hsgt` / `stock_hsgt_top10` | trade_date | ts_code |
| 板块涨跌/资金 | `stock_dc_plate(_market_cash_flow)` | trade_date | ts_code |
| 板块连续净流入 | `stock_dc_plate_continue_net_amount` | last_date | ts_code |
| 行业（申万） | `stock_sw_industry_classify_quo_daily(_last)` | trade_date | sw_code |
| 龙虎榜 | `stock_lhb_day` / `stock_lhb_institution` | trade_date | ts_code |
| 大宗交易 | `stock_block_trade` | trade_date | ts_code |
| 集合竞价 | `stock_auction_open` / `stock_auction_close` | trade_date | ts_code |
| 涨停连板 | `stock_limit_analysis` | trade_date | ts_code |
| 股东持仓 | `stock_shareholder_holdings` | end_date | ts_code |
| 股东户数 | `stock_shareholder_statistics` | end_date | ts_code |
| 股东增减持 | `stock_holder_trade` | announce_date | ts_code |
| ML 选股 | `stock_ml_selection_result` | trade_date | ts_code |
| 价值选股 | `stock_value_selection_result` | trade_date | ts_code |
| 动量选股 | `stock_momentum_selection_result` | trade_date | ts_code |
| 期货行情 | `futures_daily` / `futures_minutes` | trade_date / trade_time | ts_code |
| 期权行情 | `option_daily` / `option_minutes` | trade_date / trade_time | ts_code |
| ETF 行情 | `etf_candles_daily` | trade_date | ts_code |
| 基金净值 | `fund_nav` | nav_date | ts_code |
| 基金持仓 | `fund_portfolio` | period_end | ts_code |
| 可转债基础/日 K | `cb_basic_info` / `cb_daily` | trade_date | ts_code |
| 可转债事件 | `cb_issue` / `cb_call` / `cb_rate` / `cb_price_chg` / `cb_share` | ann_date / change_date / end_date | ts_code |
| 国债逆回购 | `repo_daily` | trade_date | ts_code |
| 国债收益率曲线 | `yc_cb` | trade_date | — |
| 债券大宗 | `bond_blk` / `bond_blk_detail` | trade_date | ts_code |
| 新闻 | `news_list` | publish_date | — |
| 宏观（CPI/PPI/PMI/GDP/M2 等） | `macro_cn_*` / `macro_lpr` / `macro_shibor` | stat_date / quarter / trade_date | — |

---

## 字段约定

- **代码**：`ts_code` 是带交易所后缀的代码（如 `600519.SH` / `000001.SZ`）；`symbol` 是不带后缀的纯数字代码。
- **日期**：除少数 TEXT 历史字段外，主要用 `DATE`（trade_date / end_date / stat_date）和 `TIMESTAMPTZ`（trade_time / *_at）。前者格式 `YYYY-MM-DD`，后者带时区。
- **数值**：货币 / 比率 / 价格统一 `DECIMAL(18,4)` 或 `DECIMAL(20,4)`，**绝不用 FLOAT**。
- **复权**：技术指标列后缀 `_bfq` / `_hfq` / `_qfq`。线性指标 = BFQ × adj_factor；非线性必须用复权价独立计算。
- **百分比**：`pct_chg` / `pct_change` 单位都是 `%`（70.5 表示 70.5%，不是 0.705）。

## OpenAPI 端点覆盖现状

按 scope 分布的 OpenAPI 端点数（**2026-05-22 扩充版**）。端点上线状态分 3 档：
- ✅ 已上线（**Phase 1 完成**）
- 🚧 待补充（属于现有 scope，**Phase 2** 上线）
- 🆕 待新建（属于 6 个新 scope，**Phase 3** 上线）

| Scope | 当前端点 | 待补 endpoint | 总目标 | 套餐（2026-06） |
|-------|---------|--------------|--------|------|
| `stock.basic` | ✅ 5 | 🚧 + bse-mapping | 6 | free |
| `stock.kline` | ✅ 8 | 🚧 + weekly_monthly / week_month_adj / bak_basic / bak_daily | 12 | free |
| `stock.indicator` | ✅ 10 | 🚧 + idx_factor_pro | 11 | free |
| `stock.index` | ✅ 7 | 🚧 + index_dailybasic / weekly / monthly / weight / global | 12 | **plus**（原 Pro） |
| `stock.minute` | ✅ 1 | 🚧 + idx_mins | 2 | plus |
| `stock.financial` | ✅ 11 | 🚧 + disclosure_date / express / forecast | 14 | plus |
| `stock.research` | 🆕 0 | 🆕 + research_report + report_rc + broker_recommend | 3 | plus |
| `stock.shareholder` | ✅ 3 | 🚧 + ccass_hold/detail + hk_hold + hsgt_list + ggt_daily/monthly | 9 | plus |
| **`stock.market`**（未拆分单一 scope；包含原计划中的 plate/lhb/moneyflow/sentiment 全部端点，URL `/stock/market/...`） | ✅ 25 | 🚧 + ths_index/daily/hot + tdx*3 + ci*2 + kpl_concept_cons + moneyflow_ths/cnt_ths/ind_ths + limit_step/cpt_list/list_ths + hm_detail + cyq_chips + st_daily/warning | ~45 | **pro**（4 子 scope 同档） |
| `market` | ✅ 12 | 🚧 + eco_cal + policy_npr | 13 | **pro**（纯国内宏观） |
| `news` | ✅ 1 | — | 1 | **max**（2026-06 从 market 拆出） |
| `derivative` | ✅ 14 | 🚧 + futures_weekly_detail | 15 | **max**（含期货全部） |
| `fund` | ✅ 9 | 🚧 + sales_ratio + sales_vol | 11 | **max** |
| `bond` | ✅ 12 | — | 12 | **max** |
| `stock.hk` | 🆕 0 | 🆕 + 11 个港股端点 | 11 | **max** |
| `stock.us` | 🆕 0 | 🆕 + 9 个美股端点 | 9 | **max** |
| `stock.intl-macro`（URL前缀 `/intl-macro/`，scope名 `stock.intl-macro`） | 🆕 0 | 🆕 + 9 个国际利率端点 | 9 | **max** |
| `forex` | 🆕 0 | 🆕 + forex/obasic + forex/daily | 2 | **max** |
| `tmt` | 🆕 0 | 🆕 + 8 个 TMT 端点 | 8 | **🔒 ultra 内部**（空数据不外卖） |
| `stock.selection` | ✅ 5 | — | 5 | **ultra 内部**（ML选股暂空，不对外） |
| **合计** | **122** | **+ ~70** | **~190** | — |

**未覆盖（保留不开放）**：
- `stock_market_sentiment` — 无时间维快照表
- `stock_irm_qa_sh` / `stock_irm_qa_sz` — 投资者关系问答（数据敏感性 + 调用量小，暂不暴露）
- `bc_otcqt` / `bc_bestotcqt` — 银行间柜台报价（机构间数据）

## 维护规则

- 后端新增 / 删除 / 重命名数据维度时，本字典必须同步更新。
- 新数据维度分配 scope 时，参考"按现有数据原始粒度"原则，不要为了平衡套餐重新切分。
- 字段说明仅展示 8-12 个最高信号列；如需更深字段请联系后端方提供。
- 套餐归属调整请先在 `stock/docs/openapi-token.md` 商业化决议后再回写本字典。
