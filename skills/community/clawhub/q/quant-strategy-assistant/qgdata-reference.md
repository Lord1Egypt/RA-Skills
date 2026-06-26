# qgdata 数据能力参考

## 初始化

```python
import qgdata as qg
qg.set_token("token")
pro = qg.pro_api(timeout=30.0)
```

调用：`pro.接口名(参数...)` → `pd.DataFrame`。接口总目录与参数详情：[SDK_USER_API.md](references/SDK_USER_API.md)，各接口单文档在 [references/apis/](references/apis/) 目录下。

## 代码格式转换

qgdata `.SZ/.SH/.BJ` ↔ vnpy `.SZSE/.SSE/.BSE`：

```python
QG2VN = {"SZ": "SZSE", "SH": "SSE", "BJ": "BSE"}
VN2QG = {v: k for k, v in QG2VN.items()}
def qg2vnpy(c): s,e = c.split("."); return f"{s}.{QG2VN[e]}"
def vnpy2qg(c): s,e = c.split("."); return f"{s}.{VN2QG[e]}"
```

---

## 数据需求→能力映射表

**收到用户需求后，对照此表判断所需数据是否可获取。能查的查，不能查的必须告知用户。**

### ✅ 支持的数据类型

| 用户需求关键词 | 数据类型 | qgdata API | 用法要点 |
|---|---|---|---|
| 日K/周K/月K/分钟线 | 行情 | `daily`/`weekly`/`monthly`/`stk_mins` | ts_code+日期，分钟线需传freq(1min/5min/15min/30min/60min) |
| PE/PB/市值/估值/换手率 | 每日指标 | `daily_basic` | ts_code+trade_date |
| 复权因子/前复权/后复权 | 复权 | `adj_factor` | ts_code+trade_date，用于长周期价格修正 |
| 涨停价/跌停价/一字板 | 涨跌停价 | `stk_limit` | ts_code+trade_date，返回up_limit/down_limit |
| 停牌/复牌/是否可交易 | 停复牌 | `suspend_d` | ts_code+trade_date，suspend_type=S停/R复 |
| 交易日历/节假日/是否交易日 | 日历 | `trade_cal` | exchange(SSE/SZSE)+start_date+end_date，返回cal_date+is_open |
| 板块/概念/行业/题材 | 板块成分 | `ths_index` + `ths_member` | 先搜板块名→取ts_code→查成分con_code |
| 东财板块 | 板块成分 | `dc_index` + `dc_member` | 需传trade_date |
| 通达信板块 | 板块成分 | `tdx_index` + `tdx_member` | 需传trade_date |
| 营收/利润/ROE/财务 | 财务指标 | `fina_indicator` | period=季度末YYYYMMDD |
| 利润表/资产负债/现金流 | 财报 | `income`/`balancesheet`/`cashflow` | period+report_type |
| 资金流入/主力/北向 | 资金流向 | `moneyflow`/`moneyflow_ths`/`moneyflow_dc` | trade_date为主过滤，moneyflow_dc需传ts_code；**主力净流入用`moneyflow_ths`的`net_amount`字段** |
| 北向/沪港通 | 北向资金 | `moneyflow_hsgt`/`hsgt_top10` | trade_date |
| 筹码/套牢盘/获利比例 | 筹码分布 | `cyq_chips`/`cyq_perf` | ts_code+trade_date |
| 龙虎榜/游资 | 龙虎榜 | `top_list`/`top_inst`/`hm_detail` | trade_date |
| 涨停/跌停/连板 | 涨跌停 | `limit_list_d`/`limit_step`/`limit_cpt_list` | trade_date |
| 融资融券/两融 | 融资融券 | `margin`/`margin_detail` | trade_date |
| 大宗交易 | 大宗 | `block_trade` | ts_code+trade_date |
| 股东/十大股东/股东人数 | 股东 | `top10_holders`/`stk_holdernumber` | ts_code+period |
| 股权质押 | 质押 | `pledge_stat`/`pledge_detail` | ts_code |
| 分红/送转 | 分红 | `dividend` | ts_code |
| 技术因子/MACD/RSI | 因子 | `stk_factor_pro` | trade_date+start_date+end_date |
| 热门股/人气排名 | 热榜 | `ths_hot`/`dc_hot` | trade_date |
| 券商金股/机构推荐 | 研报 | `broker_recommend` | month |
| 机构调研 | 调研 | `stk_surv` | trade_date+start_date+end_date |
| 业绩预告/快报 | 业绩 | `forecast`/`express` | ts_code+period |
| ST/风险警示 | 风控 | `stock_st`/`st` | - |
| ETF行情/ETF日线/ETF分钟 | ETF | `fund_daily`/`etf_stk_mins`/`etf_basic` | ts_code+trade_date，分钟线需传freq |
| ETF份额/ETF规模 | ETF规模 | `etf_share_size` | ts_code+trade_date |
| 基金净值/基金列表/基金持仓 | 公募基金 | `fund_basic`/`fund_nav`/`fund_portfolio` | fund_nav必传nav_date(或start_date+end_date) |
| 基金经理/基金公司/基金分红 | 基金基础 | `fund_manager`/`fund_company`/`fund_div` | ts_code |
| 港股行情/港股日线/港股分钟 | 港股 | `hk_daily`/`hk_mins`/`hk_basic` | ts_code+trade_date |
| 港股复权 | 港股复权 | `hk_daily_adj`/`hk_adjfactor` | ts_code+trade_date |
| 指数行情/指数日线/指数成分 | 指数 | `index_daily`/`index_weight`/`index_basic` | ts_code+trade_date |
| 指数分钟/指数周线/指数月线 | 指数周期 | `idx_mins`/`index_weekly`/`index_monthly` | ts_code+日期 |
| 申万行业/中信行业 | 行业指数 | `sw_daily`/`ci_daily`/`index_classify` | trade_date |
| GDP/经济增长 | 宏观 | `cn_gdp` | quarter |
| CPI/消费价格 | 宏观 | `cn_cpi` | month |
| PPI/出厂价格 | 宏观 | `cn_ppi` | month |
| 货币供应/M1/M2 | 宏观 | `cn_m` | month |
| PMI/采购经理 | 宏观 | `cn_pmi` | month |
| 社融/社会融资 | 宏观 | `sf_month` | month |
| Shibor/LPR/利率 | 利率 | `shibor`/`shibor_lpr` | date |
| Libor/Hibor | 海外利率 | `libor`/`hibor` | date |
| 美债/美国国债收益率 | 美国利率 | `us_tycr`/`us_tbr`/`us_tltr` | date |
| 新闻/快讯/资讯 | 资讯 | `news`/`major_news` | start_date+end_date，**news必传src**(sina/eastmoney/cls等) |
| 新闻联播 | 资讯 | `cctv_news` | date |
| 研报/券商研究报告 | 研报 | `research_report` | trade_date+start_date+end_date |
| 公告/上市公司公告 | 公告 | `anns_d` | ts_code+trade_date |
| 政策/法规 | 政策 | `npr` | - |
| 互动问答/投资者关系 | 互动 | `irm_qa_sh`/`irm_qa_sz` | ts_code |

### ❌ 不支持的数据类型

| 用户需求 | 原因 | 建议处理 |
|---|---|---|
| 实时行情/盘口/Level2 | qgdata为历史数据，实时需XT数据源 | 告知"回测可用qgdata，实盘行情由QMT提供" |
| 社交媒体情绪/微博/雪球舆情 | 无社交媒体情绪分析API | 坦诚告知，建议用技术面/资金面替代 |
| 期货/期权行情 | qgdata覆盖A股/港股/ETF/基金/指数，无期货期权 | 告知需要XT数据源 |
| 自定义另类数据 | 无接口 | 告知需要用户自行提供数据文件 |
| 实时资金流/实时筹码 | 仅盘后数据 | 告知数据为T+1 |
| 债券行情/可转债 | 当前无债券专题接口 | 告知不支持，建议关注后续版本 |

---

## 查询模板

### 板块成分查询

```python
idx = pro.ths_index(exchange='A', type='N') #N=概念 I=行业
hit = idx[idx['name'].str.contains('关键词', na=False)]
if hit.empty: print("未找到匹配板块") # → 告知用户
else:
    members = pro.ths_member(ts_code=hit.iloc[0]['ts_code'])
    codes = members[members['is_new']=='Y']['con_code'].tolist()
    vt_symbols = [qg2vnpy(c) for c in codes]
```

### 财务筛选（如"PE最低的N只"）

```python
df = pro.daily_basic(trade_date='最近交易日', fields='ts_code,trade_date,close,turnover_rate,pe,pe_ttm,volume_ratio')
df = df.dropna(subset=['pe'])
df = df[df['pe'] > 0] #排除负PE
top = df.nsmallest(20, 'pe')['ts_code'].tolist()
vt_symbols = [qg2vnpy(c) for c in top]
```

### 资金流选股（如"主力净流入最大"）

```python
df = pro.moneyflow_ths(trade_date='最近交易日')
top = df.nlargest(10, 'net_amount')['ts_code'].tolist() #主力净流入前10（net_amount字段来自moneyflow_ths文档）
vt_symbols = [qg2vnpy(c) for c in top]
```

### 涨停股/连板股

```python
df = pro.limit_list_d(trade_date='最近交易日', limit_type='U') #U=涨停
codes = df['ts_code'].tolist()
```

### 交易日历（判断交易日/取前后N个交易日）

```python
cal = pro.trade_cal(exchange='SSE', start_date='20260101', end_date='20261231', is_open='1')
trade_dates = cal['cal_date'].tolist()
```

### ETF行情查询

```python
df = pro.fund_daily(trade_date='20260320', fields='ts_code,trade_date,open,high,low,close,pre_close,change')
```

### 宏观数据查询（如GDP）

```python
df = pro.cn_gdp(fields='quarter,gdp,gdp_yoy', order_by='quarter', sort='desc', limit=20)
```

### 指数成分与权重

```python
df = pro.index_weight(index_code='399300.SZ', start_date='20260101', end_date='20260320')
```

### 成分股数量预筛

成分股超过30只时应预筛，减少回测数据下载量：

```python
basics = pro.daily_basic(trade_date='最近交易日', fields='ts_code,close,turnover_rate,pe')
filtered = basics[basics['ts_code'].isin(codes)].head(20) #取前20只，如需按市值排序请查references/apis/daily_basic.md确认可用字段
codes = filtered['ts_code'].tolist()
```

---

## 数据能力评估流程（agent必须遵守）

```
用户需求 → 提取所需数据类型 → 查映射表
    ├─ 全部支持 → 继续，记录查询方案
    ├─ 部分支持 → 告知用户：
    │    "您的需求涉及A和B两类数据，A可以通过qgdata获取，B（具体说明）当前数据源不支持。
    │     建议方案：1) 仅用A数据实现（降级） 2) 您自行提供B数据 3) 换一个思路"
    └─ 完全不支持 → 坦诚告知：
         "当前数据源不支持xxx类数据。建议：1) 换一个可实现的策略方向 2) ..."
```

**参数不确定时**：先查 [references/apis/](references/apis/) 下对应接口文档确认字段名和必填参数，不要猜测。

**核心原则：能力边界内尽力而为，能力边界外坦诚告知，绝不虚构数据。**
