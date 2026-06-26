# qgdata 用户接口文档

本文档基于当前服务端已注册接口（`qgdata-crawler/pipeline/config/sources.yaml`）整理，面向使用 `qgdata` 的调用方。

## 1. 安装与初始化

```bash
pip install qgdata
```

```python
import qgdata as qg

qg.set_token("your-token")
pro = qg.pro_api(timeout=30.0)
```

## 2. 通用调用方式

### 2.1 统一入口 `query`

```python
df = pro.query(
    "daily",
    ts_code="000001.SZ",
    trade_date="20260217",
    fields="ts_code,trade_date,open,high,low,close",
    order_by="trade_date",
    sort="desc",
    limit=200,
    offset=0,
)
```

### 2.2 动态方法（推荐）

```python
df = pro.daily(
    ts_code="000001.SZ",
    trade_date="20260217",
    limit=200,
)
```

动态方法与 `pro.query("daily", ...)` 完全等价，方法名即 `api_name`。

### 2.3 查询可用接口

```python
apis = pro.list_apis(enabled_only=True)
print(apis)
```

## 3. 通用参数约定

SDK 和服务端支持以下通用参数：
- `fields`: 字段白名单，支持 `"a,b,c"` 或 `["a", "b", "c"]`
- `order_by`: 排序字段，支持单字段或多字段
- `sort`: 排序方向，`asc` / `desc`（默认 `desc`）
- `limit`: 返回条数（默认 5000，最终受服务端 `max_limit` 限制，且服务端全局最大 6000）
- `offset`: 分页偏移（默认 0）

业务过滤参数（如 `ts_code`、`trade_date`、`freq`）通过 `**kwargs` 直接传入，服务端按“字段=值”或“字段 IN 列表”处理：

```python
df = pro.daily(ts_code=["000001.SZ", "000002.SZ"], trade_date="20260217")
```

分表接口（`stk_mins`/`etf_stk_mins`/`idx_mins`）的时间范围参数补充说明（按服务端规则）：
- `start_date/end_date` 支持 `YYYYMMDD` 或 `YYYY-MM-DD`
- 当接口时间字段为 `trade_time` 时，服务端自动补齐边界时间：
  - `start_date` -> `09:30:00`
  - `end_date` -> `15:00:00`
- 最终按 `trade_time >= start_date`、`trade_time <= end_date` 做区间过滤

```python
df = pro.stk_mins(
    ts_code="000001.SZ",
    freq="1min",
    start_date="2025-01-02",
    end_date="2025-01-02",
    fields="ts_code,trade_time,open,close",
    order_by="trade_time",
    sort="asc",
    limit=500,
)
```

## 4. 接口文档目录

以下接口按 `sources.yaml` 整理，部分接口已拆分为“每接口单文档”，点击可查看参数与示例。未列链接的接口可通过 `pro.接口名(...)` 直接调用，参数规则与通用约定一致。

### 4.1 基础数据

- [`stock_basic` 股票基础信息](apis/stock_basic.md)
- [`stk_premarket` 股本情况（盘前）](apis/stk_premarket.md)
- [`trade_cal` 交易日历](apis/trade_cal.md)
- [`stock_st` ST股票列表](apis/stock_st.md)
- [`st` ST风险警示板股票](apis/st.md)
- [`stock_hsgt` 沪深港通股票列表](apis/stock_hsgt.md)
- [`namechange` 股票曾用名](apis/namechange.md)
- [`stock_company` 上市公司基本信息](apis/stock_company.md)
- [`stk_managers` 上市公司管理层](apis/stk_managers.md)
- [`stk_rewards` 管理层薪酬和持股](apis/stk_rewards.md)
- [`bse_mapping` 北交所新旧代码对照表](apis/bse_mapping.md)
- [`new_share` IPO新股列表](apis/new_share.md)
- [`bak_basic` 股票历史列表](apis/bak_basic.md)

### 4.2 行情数据

- [`stk_mins` 股票分钟级行情](apis/stk_mins.md)
- [`daily` 股票日线行情](apis/daily.md)
- [`stk_weekly_monthly` 股票周/月线行情（统一接口）](apis/stk_weekly_monthly.md)
- [`stk_week_month_adj` 股票周/月线复权行情](apis/stk_week_month_adj.md)
- [`weekly` 股票周线行情](apis/weekly.md)
- [`monthly` 股票月线行情](apis/monthly.md)
- [`adj_factor` 复权因子](apis/adj_factor.md)
- [`daily_basic` 股票每日指标](apis/daily_basic.md)
- [`stk_limit` 股票涨跌停价格信息](apis/stk_limit.md)
- [`suspend_d` 股票停复牌信息](apis/suspend_d.md)
- [`stk_auction` 当日集合竞价](apis/stk_auction.md)
- [`stk_auction_o` 股票开盘集合竞价数据](apis/stk_auction_o.md)
- [`stk_auction_c` 股票收盘集合竞价数据](apis/stk_auction_c.md)

### 4.3 ETF专题

- [`etf_basic` ETF基础信息](apis/etf_basic.md)
- [`etf_stk_mins` ETF历史分钟行情](apis/etf_stk_mins.md)
- [`fund_adj` 基金复权因子](apis/fund_adj.md)
- [`fund_daily` ETF日线行情](apis/fund_daily.md)
- [`etf_index` ETF基准指数列表](apis/etf_index.md)
- [`etf_share_size` ETF份额规模](apis/etf_share_size.md)

### 4.4 公募基金

- [`fund_basic` 基金列表](apis/fund_basic.md)
- [`fund_company` 基金管理人](apis/fund_company.md)
- [`fund_manager` 基金经理](apis/fund_manager.md)
- [`fund_share` 基金规模](apis/fund_share.md)
- [`fund_nav` 基金净值](apis/fund_nav.md)
- [`fund_div` 基金分红](apis/fund_div.md)
- [`fund_portfolio` 基金持仓](apis/fund_portfolio.md)
- [`fund_factor_pro` 基金技术面因子(专业版)](apis/fund_factor_pro.md)

### 4.5 指数专题

- [`index_basic` 指数基本信息](apis/index_basic.md)
- [`index_daily` 指数日线行情](apis/index_daily.md)
- [`index_weekly` 指数周线行情](apis/index_weekly.md)
- [`index_monthly` 指数月线行情](apis/index_monthly.md)
- [`idx_mins` 指数历史分钟](apis/idx_mins.md)
- [`index_dailybasic` 大盘指数每日指标](apis/index_dailybasic.md)
- [`index_weight` 指数成分和权重](apis/index_weight.md)
- [`index_classify` 申万行业分类](apis/index_classify.md)
- [`index_member_all` 申万行业成分构成(分级)](apis/index_member_all.md)
- [`index_global` 国际指数](apis/index_global.md)
- [`idx_factor_pro` 指数技术因子(专业版)](apis/idx_factor_pro.md)
- [`sw_daily` 申万行业日线行情](apis/sw_daily.md)
- [`ci_daily` 中信行业指数行情](apis/ci_daily.md)
- [`daily_info` 市场交易统计](apis/daily_info.md)
- [`sz_daily_info` 深圳市场每日交易概况](apis/sz_daily_info.md)

### 4.6 港股数据

- [`hk_basic` 港股列表](apis/hk_basic.md)
- [`hk_tradecal` 港股日历](apis/hk_tradecal.md)
- [`hk_daily` 港股行情](apis/hk_daily.md)
- [`hk_daily_adj` 港股复权行情](apis/hk_daily_adj.md)
- [`hk_adjfactor` 港股复权因子](apis/hk_adjfactor.md)
- [`hk_mins` 港股分钟行情](apis/hk_mins.md)

### 4.7 沪深港通

- [`hsgt_top10` 沪深股通十大成交股](apis/hsgt_top10.md)
- [`ggt_top10` 港股通十大成交股](apis/ggt_top10.md)
- [`ggt_daily` 港股通每日成交统计](apis/ggt_daily.md)
- [`ggt_monthly` 港股通每月成交统计](apis/ggt_monthly.md)

### 4.8 财务数据

- [`income` 利润表](apis/income.md)
- [`balancesheet` 资产负债表](apis/balancesheet.md)
- [`cashflow` 现金流量表](apis/cashflow.md)
- [`forecast` 业绩预告](apis/forecast.md)
- [`express` 业绩快报](apis/express.md)
- [`dividend` 分红送股](apis/dividend.md)
- [`fina_indicator` 财务指标数据](apis/fina_indicator.md)
- [`fina_audit` 财务审计意见](apis/fina_audit.md)
- [`fina_mainbz` 主营业务构成](apis/fina_mainbz.md)
- [`disclosure_date` 财报披露计划](apis/disclosure_date.md)

### 4.9 股东与机构

- [`top10_holders` 前十大股东](apis/top10_holders.md)
- [`top10_floatholders` 前十大流通股东](apis/top10_floatholders.md)
- [`pledge_stat` 股权质押统计数据](apis/pledge_stat.md)
- [`pledge_detail` 股权质押明细数据](apis/pledge_detail.md)
- [`repurchase` 股票回购](apis/repurchase.md)
- [`share_float` 限售股解禁](apis/share_float.md)
- [`block_trade` 大宗交易](apis/block_trade.md)
- [`stk_holdernumber` 股东人数](apis/stk_holdernumber.md)
- [`stk_holdertrade` 股东增减持](apis/stk_holdertrade.md)
- [`report_rc` 卖方盈利预测数据](apis/report_rc.md)
- [`ccass_hold` 中央结算系统持股汇总](apis/ccass_hold.md)
- [`ccass_hold_detail` 中央结算系统持股明细](apis/ccass_hold_detail.md)
- [`hk_hold` 沪深港股通持股明细](apis/hk_hold.md)

### 4.10 技术指标与筹码

- [`cyq_perf` 每日筹码及胜率](apis/cyq_perf.md)
- [`cyq_chips` 每日筹码分布](apis/cyq_chips.md)
- [`stk_factor_pro` 股票技术面因子（专业版）](apis/stk_factor_pro.md)
- [`stk_nineturn` 神奇九转指标](apis/stk_nineturn.md)
- [`stk_ah_comparison` AH股比价](apis/stk_ah_comparison.md)

### 4.11 融资融券与资金流向

- [`margin_detail` 融资融券交易明细](apis/margin_detail.md)
- [`margin_secs` 融资融券标的（盘前更新）](apis/margin_secs.md)
- [`margin` 融资融券交易汇总](apis/margin.md)
- [`slb_len` 转融资交易汇总](apis/slb_len.md)
- [`moneyflow` 个股资金流向](apis/moneyflow.md)
- [`moneyflow_ths` 个股资金流向（THS）](apis/moneyflow_ths.md)
- [`moneyflow_dc` 个股资金流向（DC）](apis/moneyflow_dc.md)
- [`moneyflow_cnt_ths` 同花顺概念板块资金流向（THS）](apis/moneyflow_cnt_ths.md)
- [`moneyflow_ind_ths` 同花顺行业资金流向（THS）](apis/moneyflow_ind_ths.md)
- [`moneyflow_ind_dc` 东财概念及行业板块资金流向（DC）](apis/moneyflow_ind_dc.md)
- [`moneyflow_mkt_dc` 大盘资金流向（DC）](apis/moneyflow_mkt_dc.md)
- [`moneyflow_hsgt` 沪深港通资金流向](apis/moneyflow_hsgt.md)

### 4.12 龙虎榜与涨跌停

- [`top_list` 龙虎榜每日明细](apis/top_list.md)
- [`top_inst` 龙虎榜机构明细](apis/top_inst.md)
- [`limit_list_ths` 涨跌停榜单（同花顺）](apis/limit_list_ths.md)
- [`limit_list_d` 涨跌停列表（新）](apis/limit_list_d.md)
- [`limit_step` 连板天梯](apis/limit_step.md)
- [`limit_cpt_list` 最强板块统计](apis/limit_cpt_list.md)

### 4.13 板块与指数

- [`ths_index` 同花顺概念和行业指数](apis/ths_index.md)
- [`ths_daily` 同花顺板块指数行情](apis/ths_daily.md)
- [`ths_member` 同花顺概念板块成分](apis/ths_member.md)
- [`dc_index` 东方财富概念板块](apis/dc_index.md)
- [`dc_member` 东方财富概念板块成分](apis/dc_member.md)
- [`dc_daily` 东财概念板块行情](apis/dc_daily.md)
- [`tdx_index` 通达信板块信息](apis/tdx_index.md)
- [`tdx_member` 通达信板块成分](apis/tdx_member.md)
- [`tdx_daily` 通达信板块行情](apis/tdx_daily.md)

### 4.14 利率数据

- [`shibor` Shibor利率数据](apis/shibor.md)
- [`shibor_quote` Shibor报价数据](apis/shibor_quote.md)
- [`shibor_lpr` LPR贷款基础利率](apis/shibor_lpr.md)
- [`libor` Libor拆借利率](apis/libor.md)
- [`hibor` Hibor利率](apis/hibor.md)
- [`wz_index` 温州民间借贷利率](apis/wz_index.md)
- [`gz_index` 广州民间借贷利率](apis/gz_index.md)

### 4.15 美国利率

- [`us_tycr` 国债收益率曲线利率(日频)](apis/us_tycr.md)
- [`us_trycr` 国债实际收益率曲线利率](apis/us_trycr.md)
- [`us_tbr` 短期国债利率](apis/us_tbr.md)
- [`us_tltr` 国债长期利率](apis/us_tltr.md)
- [`us_trltr` 国债实际长期利率平均值](apis/us_trltr.md)

### 4.16 宏观经济

- [`cn_gdp` 中国GDP数据](apis/cn_gdp.md)
- [`cn_cpi` 居民消费价格指数(CPI)](apis/cn_cpi.md)
- [`cn_ppi` 工业品出厂价格指数(PPI)](apis/cn_ppi.md)
- [`cn_m` 货币供应量](apis/cn_m.md)
- [`sf_month` 社会融资规模数据](apis/sf_month.md)
- [`cn_pmi` 采购经理人指数(PMI)](apis/cn_pmi.md)

### 4.17 资讯与语料

- [`research_report` 券商研究报告](apis/research_report.md)
- [`news` 新闻快讯](apis/news.md)
- [`major_news` 新闻通讯](apis/major_news.md)
- [`cctv_news` 新闻联播](apis/cctv_news.md)
- [`anns_d` 上市公司全量公告](apis/anns_d.md)
- [`irm_qa_sh` 上证E互动](apis/irm_qa_sh.md)
- [`irm_qa_sz` 深证互动易](apis/irm_qa_sz.md)
- [`npr` 国家政策法规库](apis/npr.md)

### 4.18 其他

- [`stk_surv` 机构调研表](apis/stk_surv.md)
- [`broker_recommend` 券商月度金股](apis/broker_recommend.md)
- [`hm_list` 游资名录](apis/hm_list.md)
- [`hm_detail` 游资每日明细](apis/hm_detail.md)
- [`ths_hot` 同花顺热榜](apis/ths_hot.md)
- [`dc_hot` 东方财富热榜](apis/dc_hot.md)
- [`kpl_list` 开盘啦榜单数据](apis/kpl_list.md)
- [`kpl_concept_cons` 开盘啦题材成分](apis/kpl_concept_cons.md)

## 5. 接口文档使用说明

- 接口目录按功能分类，覆盖全部 127 个 source（含已禁用接口），每个接口均有独立文档
- 已有单文档的接口包含：接口简介、动态方法、默认时间字段、典型过滤参数、主要字段、调用示例
- 对于分表接口 `stk_mins`/`etf_stk_mins`/`idx_mins`/`hk_mins`，文档中已单独标注必填参数和调用注意事项
- 部分接口有频率限制或权限限制，详见各接口文档备注
- 如需确认当前环境可用接口，请先执行 `pro.list_apis(enabled_only=True)`

## 6. 异常处理

SDK 请求失败或业务失败会抛出 `PipelineSDKError`：

```python
from qgdata import PipelineSDKError

try:
    df = pro.query("daily", ts_code="000001.SZ", limit=10)
except PipelineSDKError as exc:
    print("message:", str(exc))
    print("code:", exc.code)
    print("detail:", exc.detail)
```

常见错误：
- `401 unauthorized`: token 缺失或无效
- `unknown api_name`: 接口名未注册
- `order_by field not found`: 排序字段不存在
- `invalid query response format`: 返回数据格式不符合约定

## 7. 调用建议

- 先通过 `list_apis()` 获取当前环境可用接口，再按接口调用
- 尽量显式指定 `fields`，减少传输与 DataFrame 内存占用
- 大数据量场景使用 `limit + offset` 分页拉取
- 对分表接口（`stk_mins`/`etf_stk_mins`/`idx_mins`）优先加时间范围（如 `start_date/end_date`），避免全量扫描
