# StockToday Skill

A 股 / 港股 / 美股 / 基金 / 期货 / 期权 / 债券 / 宏观 数据 Skill，提供 **241** 个数据接口。基于 Tushare 协议，通过 StockToday 自定义后端加速。

> **⚡ 给 AI 智能体的快速规则** (最重要,先读!)
> 1. **不确定日期**: 先调 `trade_cal(is_open=1, start_date=今天-7天)` 找最近交易日
> 2. **不确定 ts_code**: 调 `stock_basic(list_status='L', limit=10)` 查股票列表
> 3. **不确定 token 状态**: 调 `token_info(token=自己)` 一次解决
> 4. **返空不一定是错**: 节假日/未发数据/不存在的股票, 都是空 []。结合 trade_cal 判断
> 5. **同一查询 60 次/分钟**: 超限会静默返 `ok:false`,不要连点
> 6. **指数代码传了 `daily/weekly/monthly` 会自动转 `index_*`** (LLM 无感, 数据照样返)

---

## 🧭 任务驱动 (从自然语言到工具)

> **核心原则**: 用户说人话时, 先**判断任务类型** → **选推荐工具** → **套默认参数**, 不要从 241 个 tool 里瞎挑。
> 下方 10 大任务路由覆盖 95% 真实请求。

### 自然语言触发 (这些说法直接进 skill)

- "看下 XX 最近怎么样" / "XX 这段时间涨了多少" / "今年表现" / "最近强不强" → **行情/趋势**
- "看 XX 财报" / "营收趋势" / "ROE 多少" / "现金流好不好" → **财务/估值**
- "对比 XX 和 YY" / "谁更强" / "排个前 10" → **多标的对/排行**
- "最近哪个板块最强" / "半导体行情" / "指数成分" → **板块/指数**
- "北向资金" / "主力流入" / "龙虎榜" → **资金流/情绪**
- "今天涨停" / "连板梯队" / "炸板率" → **打板/情绪**
- "XX 公告" / "新闻" / "最近政策" → **公告/新闻**
- "CPI / PMI / 利率" / "港股美股" → **宏观/跨市场**
- "导出 XX 行情 CSV" / "做回测数据" → **数据导出**
- "快速研究 XX" / "做份简报" → **综合研究**

### 10 大任务路由 (默认工具 + 默认参数)

#### 1. 行情/趋势 → `daily` + `pro_bar` + `daily_basic`
- 默认窗口: "最近" = 近 20 个交易日; "这段时间" = 近 3 个月
- 必传: `ts_code` (1只) 或 `trade_date` (全市场) 或 `start_date+end_date` (范围)
- 配套: 加 `daily_basic` 拿 PE/PB/换手率, 加 `adj_factor` 算复权

#### 2. 财务/估值 → `income` + `fina_indicator` + `balancesheet` + `cashflow`
- 必传: `ts_code` (StockToday 后端硬要求)
- 不传 `period` 自动取最近季度报告期
- 配套: `forecast`/`express` 看业绩预告, `disclosure_date` 看披露计划

#### 3. 多标的对/排行 → `daily_basic` + `fina_indicator` (排序打分)
- 推荐: 选 3-5 个关键指标 (PE / ROE / 营收增速), 用 `fields` 限定
- 配套: 多 ts_code 逗号分隔, 一次拉

#### 4. 板块/指数 → `index_daily` + `index_member_all` + `ths_index`/`ths_member`
- 分类口径: 行业用 `sw_daily`, 概念用 `ths_index`, 地域用 `dc_index`
- 配套: `ths_hot` / `dc_hot` 看热度榜

#### 5. 资金流/情绪 → `moneyflow` + `moneyflow_hsgt` + `top_list`/`top_inst`
- 口径区分: 北向=沪深港通 / 主力=moneyflow 大单 / 龙虎榜=top_list
- 配套: `moneyflow_ind_dc` 看板块资金, `moneyflow_mkt_dc` 看市场资金

#### 6. 打板/情绪 → `limit_list_d` + `limit_step` + `kpl_list` + `ths_hot`/`dc_hot`
- 默认窗口: 当日 `trade_date=今天`, 涨停梯队看 `limit_step` 的 `nums='2,3,4'`
- 配套: `cyq_perf` 看筹码活跃度

#### 7. 公告/新闻 → `anns_d` + `news` + `major_news` + `npr`
- 必传: `anns_d` 必传 `ts_code + start_date + end_date`
- 配套: `research_report` 看券商研报, `irm_qa_sh/sz` 看互动问答

#### 8. 宏观/跨市场 → `cn_cpi/ppi/pmi/m` + `us_tycr` + `hk_daily` + `us_daily`
- 配套: `shibor` / `shibor_lpr` 看利率

#### 9. 数据导出 → `daily` + `pro_bar` + `fina_indicator` (按 ts_code+日期范围)
- 长区间分段拉: 日线按年/季度切, 财报按年切, 分钟按月切
- 输出 CSV / parquet, 命名格式: `daily_600519.SH_20240101_20241231_20260620.csv`

#### 10. 综合研究简报 → 组合调 1+2+5+7
- 一句话结论 → 行情 → 财务 → 资金流 → 公告 → 风险点
- 配套: `token_info` 自查权限 (高级接口需要 V2+)

### ⭐ 29 个核心工具 (覆盖 80% 任务)

> 优先从这 29 个里选, 其它 200+ 工具按需翻 `## 🛠️ 工具列表` 或 schema:

| 分类 | 工具 |
|---|---|
| 基础 | `stock_basic`, `trade_cal`, `token_info` |
| 行情 | `daily`, `pro_bar`, `daily_basic`, `adj_factor` |
| 财务 | `income`, `balancesheet`, `cashflow`, `fina_indicator`, `forecast`, `express` |
| 资金/情绪 | `moneyflow`, `moneyflow_hsgt`, `hsgt_top10`, `top_list`, `top_inst` |
| 指数/板块 | `index_daily`, `index_basic`, `sw_daily`, `ths_index`, `ths_member` |
| 打板 | `limit_list_d`, `limit_step`, `ths_hot`, `dc_hot` |
| 公告/宏观 | `anns_d`, `news`, `cn_cpi`, `us_tycr` |

### 🎯 中文自然语言默认口径

| 用户说 | 解释为 |
|---|---|
| "最近 / 这段时间" | 近 20 个交易日 |
| "今年 / 今年以来" | 1 月 1 日至今 |
| "财报 / 业绩" | 最近 8 个季度 + 最近年度 |
| "强不强" | 走势 + 相对强弱 + 活跃度 |
| "资金关注" | 净流入 + 活跃成交 + 龙虎榜/北向 |
| "估值" | PE / PB / 股息率 |
| "对比 / 排前 10" | 选 3-5 个关键指标排序 |

---

## 📤 交付规范 (Output Contract)

> **核心原则**: 用户没明说只要原始表, 就要按"先结论 → 再数据 → 后风险"的方式给, 不要直接吐 JSON 表格。

### 5 段式输出 (默认结构)

每次给结果, 严格按这 5 段:

1. **一句话结论** — 用一句话回答用户的核心问题 (涨跌 / 估值高低 / 资金方向 / 风险点)
2. **数据范围与口径** — 标的代码 / 时间窗口 / 数据源 / 是否包含复权 / 是否含交易日历过滤
3. **关键指标 / 关键表格** — 3-7 个最关键数字, 或对比表 (PE/ROE/涨跌幅/净流入), 不要全字段 dump
4. **异常点 / 风险点 / 解释限制** — 数据缺失原因 / 非交易日 / 接口权限 / 单日噪声 / 字段含义
5. **本地输出 (如有)** — CSV / parquet 路径, 方便用户回看

### 4 种交付形态 (按任务复杂度选)

| 复杂度 | 形态 | 适用 |
|---|---|---|
| 小 | Markdown 摘要 + 简短表格 | 1-2 个标的关键指标查询 |
| 中 | Markdown 摘要 + CSV (5-1000 行) | 多标的对比, 区间数据, 财报趋势 |
| 大 | Markdown 摘要 + Parquet (1000+ 行) | 多年日线, 分钟数据, 全市场扫描 |
| 流程化 | 附 Python 脚本 | 客户要"可复用流程", 或要回测/二次分析 |

### 元信息 (生成文件时必带)

- 接口名 (e.g. `daily`)
- 请求参数 (e.g. `ts_code=600519.SH, start_date=20240101, end_date=20241231`)
- 拉取时间 (UTC+8)
- 数据行数
- 字段列表
- 是否存在缺失 / 失败分段

### 按任务类型的输出模板

#### 行情/趋势任务 (单只)
```
📌 结论: 茅台 2024 年累计下跌 8.5%, 跑输沪深 300 (涨 14.7%)
📊 范围: 600519.SH / 2024-01-02 ~ 2024-12-31 / 复权(qfq) / 共 243 个交易日
📈 关键:
  - 年初: 1715 元 → 年末: 1569 元 (复权后)
  - 区间最大回撤: -23.4% (5-7 月)
  - 平均换手率: 0.32%
⚠️ 注意: 6-7 月震荡下行, 9-10 月企稳反弹; 数据按 2026-06-20 拉取
```

#### 财务/估值任务 (单只)
```
📌 结论: 茅台 2025Q3 ROE 24.1% (行业头部), PE 23x (略高于近 5 年中位 20x)
📊 范围: 600519.SH / 8 季度 2023Q4-2025Q3 + 2024 年报
💰 关键 (单位: 亿元):
  | 指标       | 2024A   | 2025Q3  | 同比   |
  |------------|---------|---------|--------|
  | 营收       | 1738    | 1285    | +15%   |
  | 归母净利   | 862     | 638     | +13%   |
  | ROE        | 26.5%   | 24.1%   | -2.4pp |
  | 毛利率     | 91.8%   | 91.3%   | -0.5pp|
⚠️ 风险: 增速放缓但盈利质量仍优; PE 偏高需关注估值消化
```

#### 多标的对/排行
```
📌 结论: 3 只白酒中, 茅台综合最强 (ROE 24%, 毛利率 91%); 泸州老窖增速最快
📊 范围: 600519.SH / 000858.SZ / 000568.SZ / 2024 年报
📊 对比表:
  | 指标     | 茅台     | 五粮液   | 泸州老窖 |
  |----------|----------|----------|----------|
  | ROE      | 26.5%    | 22.1%    | 24.8%    |
  | 毛利率   | 91.8%    | 75.3%    | 87.5%    |
  | 营收增速 | 15.7%    | 8.4%     | 22.6%    |
  | PE       | 23x      | 18x      | 20x      |
```

#### 资金流任务
```
📌 结论: 茅台 6/18 主力净流出 2.3 亿 (大单), 但北向净买入 1.1 亿
📊 范围: 600519.SH / 2026-06-18
💰 关键:
  - 主力净流入: -2.3 亿 (大单 -1.8 / 特大单 -0.5)
  - 北向净买入: +1.1 亿
  - 涨跌: -0.42%
⚠️ 解读: 主力减仓但北向接盘, 信号矛盾需看后续 1-2 日确认
```

#### 板块/打板任务
```
📌 结论: 6/18 涨停 47 只 (连板 12 只), 半导体板块最热 (涨停 8 只)
📊 范围: 全市场 / 2026-06-18
🔥 板块强度: 半导体 +5.2% / 新能源车 +3.8% / AI +3.1%
📊 连板梯队: 6 板 1 只 / 5 板 2 只 / 4 板 3 只
⚠️ 风险: 涨停炸板率 18% (偏高), 明日分歧概率大
```

#### 公告/新闻任务
```
📌 结论: 寒武纪 6/18 公告 3 条, 核心是定增预案修订 (募资 50 亿)
📊 范围: 688256.SH / 近 30 日 / anns_d + news
📰 关键:
  - 6/18: 定增预案修订 (募资 50 亿, 用于 AI 芯片研发)
  - 6/15: 5 月经营数据公告
  - 6/10: 投资者关系活动记录
⚠️ 注意: 定增属利好但稀释 EPS, 关注发行价折扣
```

### ⚠️ 不要做的 5 件事

1. **不要直接吐 JSON 原始表** — 用户看不懂, 至少要前 3 行 + 摘要
2. **不要忘记标"非交易日"** — 周末/节假日返空要在异常点说明
3. **不要用绝对收益承诺** — "必涨 20%" 这种话别说, 数据只描述历史
4. **不要漏单位** — 金额"亿/万"、涨跌幅"%"、换手率"%", 必须标
5. **不要把单日信号当趋势** — 资金流单日 1 天噪声, 至少看 5 日才稳

---

## 🎯 实战工作流 (8 个最常见模式)

### 1. 查 1 只股票最近的行情
```
User: 茅台今天怎么样
Step 1: trade_cal(exchange='SSE', start_date='20260615', end_date='20260620', is_open='1')
        → 拿到最近交易日 (e.g. 20260618)
Step 2: daily(ts_code='600519.SH', trade_date='20260618')
        → 拿到 OHLCV 数据
```

### 2. 查 1 只股票一段时间的行情
```
User: 茅台 6 月行情
→ daily(ts_code='600519.SH', start_date='20260601', end_date='20260618')
  或
→ pro_bar(ts_code='600519.SH', start_date='20260601', end_date='20260618', adj='qfq', freq='D')
  (pro_bar 带复权/均线/换手率, 行情分析首选)
```

### 3. 查 1 只股票最新财务数据
```
User: 茅台去年业绩
→ income(ts_code='600519.SH', period='20251231', report_type='1')
  period: 报告期末 (年报=1231, 半年报=0630, 一季报=0331, 三季报=0930)
  report_type: 1=合并报表(默认) / 2=母公司
  不传 period: 返最近一期
```

### 4. 同时查 1 只股票的 3 张报表
```
User: 平安银行 2025 完整财务
→ 3 个并行调用:
  income(ts_code='000001.SZ', period='20251231')
  balancesheet(ts_code='000001.SZ', period='20251231')
  cashflow(ts_code='000001.SZ', period='20251231')
→ 也可以用 fina_indicator(ts_code='000001.SZ', period='20251231') 拿关键比率
```

### 5. 查龙虎榜
```
User: 6/18 上交所龙虎榜
→ top_list(trade_date='20260618')
  或加 ts_code='600519.SH' 看单只上榜详情
→ top_inst(trade_date='20260618', ts_code='600519.SH') 看机构席位
```

### 6. 查 1 只股票的资金流向
```
User: 平安银行 6/18 主力资金
→ moneyflow(ts_code='000001.SZ', trade_date='20260618')
  字段: net_mf_vol/net_mf_amount 主力净流, buy_lg/sell_lg 大单, buy_elg/sell_elg 特大单
```

### 7. 查北向资金 / 沪深港通
```
User: 6/18 北向买了多少
→ moneyflow_hsgt(trade_date='20260618')
  字段: hgt 沪股通, sgt 深股通, north_money 北向合计
→ hsgt_top10(trade_date='20260618', market_type='1') 沪市北向前 10
```

### 8. 查实时行情 (需 rt 权限)
```
User: 茅台现在多少钱 (盘中问)
→ rt_tick(ts_code='600519.SH') 最新一笔
→ rt_k(ts_code='600519.SH') 最新 K 线
```

---

## 📅 数据时间规则

| 场景 | 数据可用性 | 备注 |
|------|------------|------|
| 行情 (日线) | T+1 18:00 后 | 当天数据当晚 6 点后可用 |
| 行情 (分钟) | 实时 | 盘中每分钟更新 |
| 实时 Tick | 实时 | 盘中每 3 秒 |
| 财务 (季报) | 公告日 | 4/30 一季报, 8/30 半年报, 10/30 三季报, 4/30 年报 |
| 财务 (年报) | 4/30 前 | 1/1-4/30 是年报披露季 |
| 业绩预告 | 季报前后 | 1/15, 4/15, 7/15, 10/15 前后集中 |
| 龙虎榜 | T+1 18:00 后 | 盘后公布 |
| 限流阈值 | 100/分钟 | (perMin=100) |

**重要**: 周末/节假日调接口会返空,这是**正常**,不是接口坏。

---

## 🚨 错误排查速查

| 现象 | 原因 | 解决 |
|------|------|------|
| `TOKEN无效` | token 错/过期 | 调 `token_info(token=自己)` 看状态 |
| `参数不能为空` | 必填参数没传 | 看 schema 里的 `required: true` |
| `您的IP因异常请求已被临时封禁` | 5 分钟内 5+ 次 IP_KEY 错 | 改对 token,等 5h |
| `单次查询数据量不可超过 10000 条` | 数据范围太大 | 缩 start_date~end_date |
| 返 `{"code":0,"items":[]}` | 节假日/未发数据/股票不存在 | 调 `trade_cal` 确认日期 |
| `HTTP 400` (stock_hsgt) | 缺 ts_code | 传 ts_code 或 trade_date |
| `data: null` (fut/hk 接口) | 合约/港股代码错 | 检查后缀 (.SHF/.HK) |

---

## 🔑 Token 4 种类型

调 `token_info(token=自己)` 自动检测自己属于哪一档:

| 类型 | 适用 | 特征 |
|------|------|------|
| V0 免费 | 注册即得 | 只 6 个基础接口,需要 plugin 解锁 |
| V1 基础 | 旗舰积分 | 193 个基础接口 (无实时) |
| V2 高级 | 龙虾套餐 | 全部 193+48 = 241 个 |
| V3/V4 高级 | 大客户 | 同 V2 |

接口分 2 档:
- **基础档** (193 个): daily/income/top_list/stock_basic/...
- **实时档** (48 个): rt_k/rt_tick/rt_min/cb_price_chg/anns_d/news/...

---

## ⚙️ 配置

### 环境变量
```bash
export STOCKTODAY_TOKEN="your_token"    # 必填
export STOCKTODAY_URL="https://..."     # 可选, 默认 https://tushare.citydata.club/
```

### 调速 (默认即可, 高频可调)
- `STOCKTODAY_RATE_PER_MIN=100` (默认)
- `STOCKTODAY_MAX_CONCURRENT=10` (默认)
- `STOCKTODAY_MAX_RETRIES=3` (默认)

---

## 🛠️ 工具列表 (按分类)

> 完整 241 个工具,按 22 个分类列出。**所有 schema 含 `type` / `required` / `pattern`**,智能体可直接读 `dist/tool_schemas.js` 看详细参数。

### 股票-基础数据 (16)
| 工具 | 说明 |
|---|---|
| `stock_basic` | **查股票列表**: list_status='L' 上市 / 'D' 退市 / 'P' 暂停 |
| `stk_premarket` | 新股上市 |
| `trade_cal` | **交易日历**: is_open='1' 交易日 / '0' 休市, 节假日调这个 |
| `stock_st` | ST 股票列表 (需 trade_date) |
| `namechange` | 股票名称变更 |
| `stock_company` | 上市公司信息 (1 只: ts_code) |
| `stk_managers` | 公司管理层 |
| `stk_rewards` | 高管薪酬 |
| `new_share` | 新股发行 (需 start_date) |
| `bak_basic` | 备用基础数据 |
| `bse_mapping` | 北交所新旧代码对照 |
| `stock_hsgt` | 沪深港通股票列表 (需 ts_code 或 trade_date) |
| ... | 还有 4 个,见下方 |

### 股票-行情数据 (15)
| 工具 | 说明 | 必填 |
|---|---|---|
| `daily` | 日线行情 | ts_code + (trade_date \| start_date+end_date) |
| `weekly` | 周线行情 | 同上 |
| `monthly` | 月线行情 | 同上 |
| `pro_bar` | 行情(支持复权) | ts_code + start_date + end_date, **adj** 可选 qfq/hfq/none, **freq** D/W/M |
| `stk_weekly_monthly` | 周月线行情 (高频首选) | ts_code + freq='W' 或 'M' |
| `stk_week_month_adj` | 周月线复权 | 同上 |
| `adj_factor` | 复权因子 | ts_code + start_date + end_date |
| `daily_basic` | 每日指标 (PE/PB/换手率) | ts_code + trade_date |
| `stk_limit` | 涨跌停价格 | ts_code + trade_date |
| `suspend_d` | 停复牌 | ts_code + start_date + end_date |
| `hsgt_top10` | 沪/深股通前 10 | trade_date + market_type (1=沪/3=深) |
| `ggt_top10` | 港股通前 10 | trade_date + market_type (2=沪/4=深) |
| `ggt_daily` | 港股通每日 | trade_date |
| `ggt_monthly` | 港股通每月 | trade_date |
| `bak_daily` | 备用每日行情 | trade_date |

### 股票-财务数据 (17)
| 工具 | 说明 | 必填 |
|---|---|---|
| `income` | 利润表 | **ts_code** + 可选 period/ann_date |
| `balancesheet` | 资产负债表 | 同上 |
| `cashflow` | 现金流量表 | 同上 |
| `forecast` | 业绩预告 | ts_code 或 ann_date |
| `express` | 业绩快报 | ts_code 或 ann_date |
| `dividend` | 分红送股 | ts_code |
| `fina_indicator` | **财务指标** (ROE/EPS/PE/PB) | ts_code + 可选 period |
| `fina_audit` | 财务审计 | ts_code + period |
| `fina_mainbz` | 主营业务 | ts_code + period + type (P=产品/D=地区) |
| `disclosure_date` | 披露日期 | ts_code + end_date |
| `income_vip` | VIP 利润表 | ts_code + period |
| `balancesheet_vip` | VIP 资产负债表 | ts_code + period |
| `cashflow_vip` | VIP 现金流量表 | ts_code + period |
| `fina_indicator_vip` | VIP 财务指标 | ts_code + period |
| `express_vip` | VIP 业绩快报 | ts_code + period |
| `forecast_vip` | VIP 业绩预告 | ts_code + period |
| `fina_mainbz_vip` | VIP 主营业务 | ts_code + period + type |

### 股票-参考数据 (9)
| 工具 | 说明 |
|---|---|
| `top10_holders` | 十大股东 |
| `top10_floatholders` | 十大流通股东 |
| `pledge_stat` | 股权质押统计 |
| `pledge_detail` | 股权质押明细 |
| `repurchase` | 股份回购 |
| `share_float` | 流通股本 |
| `block_trade` | 大宗交易 |
| `stk_holdernumber` | 股东户数 |
| `stk_holdertrade` | 股东增减持 (trade_type: 1=增持/2=减持) |

### 股票-特色数据 (18)
| 工具 | 说明 |
|---|---|
| `top_list` | **龙虎榜上榜** (trade_date 必填) |
| `top_inst` | **龙虎榜机构席位** (trade_date 必填) |
| `limit_list_d` | 涨跌停和炸板数据 (trade_date) |
| `limit_list_ths` | 同花顺涨跌停榜单 (trade_date) |
| `limit_step` | 涨停连板天梯 (trade_date, 可选 nums='2,3') |
| `limit_cpt_list` | 涨停最强板块 (trade_date) |
| `stk_auction` | 集合竞价 (trade_date) |
| `stk_auction_o` | 开盘竞价成交 (trade_date) |
| `stk_auction_c` | 收盘竞价 (trade_date) |
| `cyq_perf` | 筹码活跃度 (ts_code + trade_date) |
| `cyq_chips` | 筹码分布 (ts_code + trade_date) |
| `ccass_hold` | 中央结算持股 (港股) |
| `ccass_hold_detail` | 中央结算持股明细 |
| `stk_ah_comparison` | AH 股对比 |
| `stk_factor_pro` | **股票因子库** (200+ 指标) |
| `stk_nineturn` | 九转序列 (技术指标) |
| `stk_surv` | 舆情监控 |
| `report_rc` | 研报 |

### 资金流向 (8)
| 工具 | 说明 |
|---|---|
| `moneyflow` | 股票资金流向 (ts_code + trade_date) |
| `moneyflow_hsgt` | **沪深港通北向** (trade_date) |
| `moneyflow_ths` | 同花顺资金流 (ts_code + trade_date) |
| `moneyflow_dc` | 东方财富资金流 (ts_code + trade_date) |
| `moneyflow_ind_ths` | 同花顺行业资金流 (trade_date) |
| `moneyflow_ind_dc` | 东方财富行业资金流 (trade_date) |
| `moneyflow_mkt_dc` | 东方财富市场资金流 (trade_date) |
| `moneyflow_cnt_ths` | 同花顺概念资金流 (trade_date) |

### 指数数据 (10)
| 工具 | 说明 |
|---|---|
| `index_basic` | 指数基本信息 (market='SSE'/'SZSE'/'BSE') |
| `index_daily` | 指数日线 (ts_code) |
| `index_weekly` | 指数周线 |
| `index_monthly` | 指数月线 |
| `index_weight` | 指数成分股权重 (index_code + trade_date) |
| `index_dailybasic` | 指数每日指标 (PE/PB/换手率) |
| `index_classify` | 指数分类 |
| `index_member_all` | 指数成分股 |
| `ci_daily` | 中证指数日线 |
| `sw_daily` | 申万指数日线 |
| `idx_factor_pro` | 指数因子 (PE/PB/动量) |

### 板块/热点 (8)
| 工具 | 说明 |
|---|---|
| `ths_index` | 同花顺概念/行业/地域指数 |
| `ths_daily` | 同花顺指数日线 (ts_code + trade_date) |
| `ths_member` | 同花顺成分股 (ts_code) |
| `ths_hot` | 同花顺热榜 (trade_date) |
| `dc_index` | 东财指数 (idx_type 必填) |
| `dc_daily` | 东财指数日线 |
| `dc_member` | 东财成分股 (trade_date) |
| `dc_hot` | 东财热榜 (trade_date) |
| `kpl_list` | 开盘啦榜单 (trade_date) |
| `kpl_concept` | 开盘啦概念 (trade_date) |
| `kpl_concept_cons` | 开盘啦概念成分 (trade_date) |
| `hm_list` | 游资名录 |
| `hm_detail` | 游资详情 |
| `tdx_index` | 通达信指数 |
| `tdx_daily` | 通达信日线 |
| `tdx_member` | 通达信成分股 |
| `stk_ah_comparison` | AH 股对比 |

### 港股/美股 (15)
| 工具 | 说明 |
|---|---|
| `hk_basic` | 港股基本信息 (注意: 港股代码 5 位,无 .SH/.SZ 后缀) |
| `hk_daily` | 港股日线 (ts_code='00700.HK') |
| `hk_daily_adj` | 港股复权日线 |
| `hk_mins` | 港股分钟线 |
| `hk_income` | 港股利润表 (period='20251231') |
| `hk_balancesheet` | 港股资产负债表 |
| `hk_cashflow` | 港股现金流量表 |
| `hk_fina_indicator` | 港股财务指标 |
| `hk_adjfactor` | 港股复权因子 |
| `hk_hold` | 沪深港通持股 (ts_code + trade_date) |
| `us_basic` | 美股基本信息 (代码纯 ticker, e.g. 'AAPL', 无 .US 后缀) |
| `us_daily` | 美股日线 |
| `us_daily_adj` | 美股复权日线 |
| `us_income` / `us_balancesheet` / `us_cashflow` / `us_fina_indicator` | 美股财务 (period='20251231') |
| `us_adjfactor` | 美股复权因子 |

### 基金 (10)
| 工具 | 说明 |
|---|---|
| `fund_basic` | 基金基本信息 (market='O'=场外/'E'='场内) |
| `fund_company` | 基金公司 |
| `fund_manager` | 基金经理 |
| `fund_share` | 基金份额 |
| `fund_nav` | 基金净值 |
| `fund_div` | 基金分红 |
| `fund_portfolio` | 基金持仓 |
| `fund_daily` | 基金日线 |
| `fund_adj` | 基金复权因子 |
| `fund_factor_pro` | 基金因子 |

### 期货/期权/债券 (10)
| 工具 | 说明 |
|---|---|
| `fut_basic` | 期货基本信息 (exchange='DCE'/'CZCE'/'CFFEX'/'SHFE'/'INE'/'GFEX') |
| `fut_daily` | 期货日线 (ts_code='CU2507.SHF' 铜 2507) |
| `fut_weekly_monthly` | 期货周月线 |
| `fut_wsr` | 期货持仓 (symbol='CU') |
| `fut_settle` | 期货结算 |
| `fut_holding` | 期货持仓量 (symbol + start_date + end_date) |
| `fut_mapping` | 期货映射 |
| `opt_basic` | 期权基本信息 |
| `opt_daily` | 期权日线 |
| `cb_basic` / `cb_daily` / `cb_issue` / `cb_call` / `cb_rate` / `cb_share` | 可转债 (注意: ts_code 6 位, 无后缀) |
| `cb_price_chg` | 可转债价格变化 |
| `cb_factor_pro` | 可转债因子 |

### 实时数据 (18, 需实时档 token)
| 工具 | 说明 |
|---|---|
| `realtime_list` | 实时行情列表 |
| `rt_min` | 股票实时分钟 (ts_code + freq='1MIN'/'5MIN'/'15MIN'/'30MIN'/'60MIN' **大写**) |
| `rt_k` | 股票实时日线 |
| `rt_tick` | 股票实时 Tick (只返回最后一条) |
| `rt_idx_k` / `rt_idx_min` / `rt_idx_tick` | 指数实时 |
| `rt_sw_k` / `rt_sw_tick` | 申万指数实时 |
| `rt_etf_k` / `rt_etf_min` / `rt_etf_tick` | ETF 实时 |
| `rt_fut_min` | 期货实时分钟 |
| `rt_hk_k` / `rt_hk_tick` | 港股实时 |
| `stk_mins` | 股票历史分钟 (ts_code + freq='1min' ~ '60min' **小写**) |
| `idx_mins` | 指数历史分钟 |
| `etf_mins` | ETF 历史分钟 |
| `hk_mins` | 港股历史分钟 |
| `ft_mins` | 期货历史分钟 |
| `opt_mins` | 期权历史分钟 |

### 资讯 (1)
| 工具 | 说明 |
|---|---|
| `news` | 资讯 (start_date + end_date, src='cls'/'sina'/'ths'/'eastmoney') |
| `major_news` | 重要资讯 |
| `cctv_news` | 新闻联播 |
| `npr` | 国家政策库 |
| `anns_d` | 上市公司公告 (ts_code + start_date + end_date) |
| `research_report` | 券商研报 |

### 其他 (11)
| 工具 | 说明 |
|---|---|
| `tmt_twincome` | 台湾电子产业月营收 |
| `tmt_twincomedetail` | TMT 月营收明细 |
| `film_record` / `teleplay_record` | 电影/电视剧备案 |
| `bo_daily` / `bo_weekly` / `bo_monthly` / `bo_cinema` | 票房 |
| `irm_qa_sh` / `irm_qa_sz` | e 互动问答 |
| `token_info` | **自查 token 状态** (必调用) |
| `stk_account` / `stk_account_old` | 股票账户 |
| `eco_cal` | 经济日历 |
| `shibor` / `shibor_quote` / `shibor_lpr` | Shibor 利率 |
| `libor` / `hibor` | Libor/Hibor |
| `us_tbr` / `us_tycr` / `us_trycr` / `us_tltr` / `us_trltr` | 美债 |
| `cn_gdp` / `cn_cpi` / `cn_ppi` / `cn_pmi` / `cn_m` | 中国宏观 |
| `fx_obasic` / `fx_daily` | 外汇 |
| `sge_basic` / `sge_daily` | 上海黄金 |
| `bond_blk` / `bond_blk_detail` | 债券大宗 |
| `bc_otcqt` / `bc_bestotcqt` | 银行间报价 |
| `repo_daily` | 回购 |
| `yc_cb` | 国债收益率曲线 (ts_code='1001.CB', curve_type='0'/'1') |
| `sf_month` | 上海黄金月报 |
| `gz_index` / `wz_index` | 国证/万德指数 |
| `margin` / `margin_detail` / `margin_secs` | 融资融券 |
| `slb_sec` / `slb_len` / `slb_sec_detail` / `slb_len_mm` | 转融通 |
| `pledge_stat` / `pledge_detail` | 股权质押 |
| `repurchase` | 股份回购 |
| `share_float` | 流通股本 |
| `block_trade` | 大宗交易 |
| `stk_holdernumber` | 股东户数 |
| `stk_holdertrade` | 股东增减持 (trade_type=1 增持/2 减持) |
| `report_rc` | 研报 |
| `stk_surv` | 调研 |
| `stk_nineturn` | 九转序列 |
| `stk_factor_pro` | 因子库 |

---

## 📝 版本说明 (精简)

**v1.3.10**: 全删 1.3.5-1.3.9 后重发, 11 文件, 43.8 kB (-46% 体积), 移 INTERFACE.md
**v1.3.0+**: 透明限流 (60/min, 5 并发, 3 次重试, 静默失败)
**v1.2.0+**: 全部 240+ 工具的 inputSchema 带 `type` / `required` / `enum` / `pattern` / `default`

详细 release notes 见 `RELEASE_NOTES.md`。

---

## 🔌 后端

默认 `https://tushare.citydata.club/`,可通过 `STOCKTODAY_URL` 环境变量覆盖。

---
*Published via ClawHub · slug: `stocktoday`*
