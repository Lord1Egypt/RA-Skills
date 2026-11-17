# 数据获取手册

两条通道，**主用 CLI 批量取数，连接器补个人数据**。二者不可互相替代。

| 通道 | 调用方式 | 负责 | 是否需授权 |
|------|---------|------|-----------|
| **A. westockdata CLI** | `npx -y westock-data-skillhub@1.0.5 <命令>` | 行情/财报/研报/资金/板块/大盘（支持批量） | 否 |
| **B. westock-mcp 连接器** | MCP 工具 `data_*` / `portfolio_*` | 自选清单、模拟持仓、实时快照、提醒 | 是 |

组合原则：N 只股票时，**凡支持批量的命令只调 1 次**（代码逗号分隔），不要逐股拆开。
无依赖的多个命令在**同一轮并行发出**，不要串行等待。

---

## A. westockdata CLI 命令清单

代码格式：`sh600519`（沪）/ `sz000001`（深）/ `hk00700`（港）/ `usAAPL`（美）；板块 `pt01801080`。
未知代码先 `npx -y westock-data-skillhub@1.0.5 search 名称`。

### A1. 大盘研判（每次必做，5 条命令并行）

```bash
WD="npx -y westock-data-skillhub@1.0.5"
$WD market-overview                      # 市场画像总评：估值/情绪/技术/趋势/风格 14 维度得分
$WD market-overview --type trade         # 三大指数收盘 + 两市成交额多周期均值
$WD market-overview --type technical     # 大盘 MACD/KDJ/RSI/BOLL/MA
$WD market-overview --type valuation     # 中证全指 PE/PB/PS + 历史百分位
$WD changedist                           # 涨跌家数、涨跌停、上涨占比、两市成交额
```

补充（按需）：
```bash
$WD market-overview --type margin        # 两融余额变动
$WD market-overview --type rotation      # 沪深300/中证1000/成长/价值 风格轮动
$WD macro indicator cn_core              # 宏观核心指标（CPI/PMI/社融等）
$WD kline sh000300 --period day --limit 250   # 沪深300 日线，用于算 MA250 偏离
```

### A2. 个股批量取数（核心，一次拉齐）

设 `CODES="sh600519,sz000651,sz300750"`，下面 8 条**并行发出**：

```bash
WD="npx -y westock-data-skillhub@1.0.5"
$WD kline $CODES --period day --limit 1        # 最新快照：现价/成交额（没有 quote 命令）
$WD kline $CODES --period day --limit 250      # 日线（算 MA20/60/250、回撤、波动率）
$WD finance $CODES --type income --num 8       # 利润表近 8 期（算 ROE/增速/TTM 净利）
$WD finance $CODES --num 8                     # 三大报表
$WD technical $CODES --indicator macd    # MACD/KDJ/RSI/BOLL
$WD fund flow $CODES                     # 主力资金流向
$WD score $CODES                         # 官方诊股评分（综合/资金/基本面/风险/技术 + 周/月/季变动）
$WD consensus $CODES                     # 机构一致预期；仅独立参考，目标价不混入公允价值
$WD report list $CODES --limit 5         # 近期研报列表
```

> **命令名易错点（实测踩过）**：`quote` 与 `flow` 都**不是**顶层命令。
> 现价用 `kline --limit 1`；资金用 `fund flow`；北向用 `fund north-holding`；
> 分红用 `dividend list`；板块搜索用 `search <关键词> --type sector`（不是 `sector search`）。
> 拿不准就先 `$WD <命令>` 不带参数，会打印用法。

> **缺失字段先补、再派生（v2.4.0）**：取数后若仍有字段缺，按「补数据 → 派生 → 兜底」处理——能从已取原始量算出的，引擎会自己算（`np_yoy` 由 `net_profit_ttm` / `prior_net_profit` 派生，需两侧 `period_end` 相差约一年；`ocf_to_np`、股息子项、行业景气度同理），**不要因为缺一个字段就手工填 0 或干脆不报**。结构性缺失按期望分、观测项按中性 60 的兜底由引擎统一执行，取数阶段只负责"尽力补"。

补充（按需，同样批量）：
```bash
$WD risk $CODES                          # 风险事件：ST/质押/解禁/诉讼/高管减持
$WD notice list $CODES --limit 10        # 公告列表
$WD shareholder $CODES                   # 股东户数、十大股东变化
$WD fund north-holding $CODES            # 北向持股（A股）
$WD dividend list $CODES --years 3       # 分红（v2.3 股息子项必需；注意要带 list）
$WD profile <code>                       # 公司概况（单代码，按需）
```

### A3. 行业与板块（用于估值分位与景气度）

```bash
$WD search 银行 --type sector            # 先搜板块拿 code（不是 sector search）
$WD sector valuation pt01801080          # 板块 PE/PB/PS + 历史百分位
$WD sector finance pt01801780            # 申万行业财务指标（v2.3 行业景气度必需）
$WD sector ranking                       # 板块行情榜
```

**行业景气度（v2.3.0）**：`sector finance` 取行业财报后，把**行业TTM净利同比**写入
`sector_np_yoy_pct`、**行业TTM营收同比**写入 `sector_rev_yoy_pct`（都要带 `indicator_meta`）。
引擎据此派生 `industry_boom`（净利70%+营收30%）。
取不到就留空——会退回手填值，再没有才按期望分50插补；**不要为了凑分自己编一个景气分**。

### A4. 股息（v2.3.0 股息子项必需）

```bash
$WD dividend list $CODES --years 3
```

**换算口径**（引擎只收原始量，利差与覆盖倍数都自己算）：

| 写入字段 | 由什么换算 | 说明 |
|---|---|---|
| `dividend_yield_pct` | `每股现金分红TTM / 现价 × 100` | 百分数，0–100 |
| `cash_dividend_ttm` | 近12个月**现金分红总额**（元） | 与 `net_profit_ttm` 同口径，非负 |
| `market.risk_free_rate_pct` | 10年期国债收益率（%） | 市场级，90日内有效 |

要点：
- **把中期分派和年度分派都算进 TTM**。只在年报里取一次会低估算股息率。
  例：京沪高铁 2025年报 10派0.954 + 2025中报 10派0.385，TTM 每股 0.1339 元。
- 有**特殊分红**要判断是否可持续，一次性处置收益带来的高股息不宜直接当常态。
- **不要自己写 `dividend_spread_pct` / `dividend_coverage`**——引擎会丢弃并按原始量重算。
- 红利类档位（电力/公路/铁路/港口/水务/燃气）**建议每次都取**，否则同一组合里
  有的标的启用股息子项、有的不启用，横向比较口径不一致。

### A5. 市场温度原始序列（v2.3.0 可自算）

`market` 块里放序列，引擎会自算对应指标（已有现成标量则优先用标量）：

| 原始序列 | 自算出的指标 | 最少样本 | 数据来源 |
|---|---|---|---|
| `turnover_series` | `volume_ratio_5_250` | 250 | 两市成交额（`market-overview --type trade` 逐日） |
| `advance_ratio_series` | `up_ratio_20d` | 20 | 逐日上涨家数占比%（`changedist` 逐日） |
| `hs300_close_series` | `hs300_ma250_dev` | 250 | `kline sh000300 --period day --limit 250` |

- 每个序列都要配 `indicator_meta.<序列名>`，派生值继承它的来源与日期后才过证据门槛。
- `broken_net_ratio`（破净比例）**无法从序列派生**，仍需外部提供。
- **v2.4.0 起，4 项里拿到 ≥3 项就出温度分**（按可用项权重归一），缺 1 项不再直接变"数据不足"；把三条序列都补齐可拿到最稳的 4/4 温度分。

### A6. 新闻资讯

**westockdata CLI 无新闻命令**。新闻走两条路：
1. 连接器 `data_news`（`symbol=代码`，`mode=list/detail`）
2. 连接器未授权时，用 `WebSearch` 检索 `股票名 最新消息`，并**标注来源与日期**

---

## B. westock-mcp 连接器工具清单

前置：连接器需处于 connected。若 disconnected，按 SKILL.md 的降级路径处理。

### B1. 获取自选与持仓

| 工具 | 用途 | 关键参数 |
|------|------|---------|
| `portfolio_watchlist` | **自选股清单**（主入口） | `group` 分组、`market` A/HK/US、`limit` |
| `portfolio_watchlist_groups` | 自选分组列表（写操作前必调） | — |
| `portfolio_paper_positions` | **模拟交易持仓**（成本价/现价/浮盈） | — |
| `portfolio_paper_portfolio` | 模拟账户总资产/可用资金/总盈亏 | — |
| `portfolio_paper_profit` | 胜率、已实现盈亏、个股收益贡献 | — |

### B2. 补充数据

| 工具 | 用途 |
|------|------|
| `data_quote` | 实时行情快照（多只批量 `codes`） |
| `data_news` | 新闻资讯（list/detail） |
| `data_notice` | 公告 |
| `data_consensus` | 机构一致预期（目标价） |
| `data_rating` | 机构评级 |
| `data_score` | 诊股评分 |
| `data_risk` | 风险提示（质押/解禁/诉讼/ST） |
| `data_market_overview` | 市场总览（8 类型） |
| `data_changedist` | 涨跌分布 |
| `data_sector` | 板块（list/search/constituent/info/ranking） |

### B3. 写操作（需用户明确要求才执行）

`portfolio_watchlist_add` / `remove` / `batch_add` —— 调整自选清单。
`portfolio_paper_trade`（虚拟盘下单）—— **仅沪深 A 股、限价单、100 整数倍**，下单前须用户明确确认。

---

## 降级路径（连接器未连接时）

| 缺失能力 | 降级方案 |
|---------|---------|
| 自选清单 `portfolio_watchlist` | 读本地 `workspace/portfolio_ledger/watchlist.json`；无则请用户提供清单（名称或代码均可） |
| 模拟持仓 `portfolio_paper_positions` | **主路径：用户上传持仓截图**；或本地 `positions.json`；或用户口述 |
| 实时快照 `data_quote` | 用 CLI `kline --limit 1` 最新收盘价，**必须标注"非实时，数据日期 XXXX-XX-XX"** |
| 新闻 `data_news` | `WebSearch` 检索并标注来源日期 |

**禁止**：连接器未连接就编造自选/持仓数据。宁可少分析，不可虚构。

---

## 持仓截图解析规范

用户上传同花顺/券商 App 的持仓页截图时，用多模态能力直接读取图片，按以下字段提取：

| 字段 | 说明 | 缺失处理 |
|------|------|---------|
| `name` | 股票名称 | 必须提取，缺失则报错请用户重传清晰图 |
| `code` | 6 位代码 → 转 `sh/sz` 前缀 | 名称唯一时可由 `search` 补全 |
| `shares` | 持仓数量（股） | 必须 |
| `cost_price` | 成本价 | 必须 |
| `current_price` | 现价 | 可从截图读，也可后续用 `quote` 覆盖 |
| `market_value` | 市值 | 可由 `shares × current_price` 计算 |

**代码前缀规则**：`6` 开头 → `sh`；`0`/`3` 开头 → `sz`；`8`/`4` 开头 → `bj`（北交所，提示数据覆盖有限）；港股 5 位 → `hk`。

**解析后必须做两件事**：
1. 把识别结果以**表格形式回显给用户确认**，标注"请核对，尤其是数量与成本价"
2. 用户确认后写入 `workspace/portfolio_ledger/positions.json`，后续运行直接复用

**截图常见陷阱**：
- 截图可能只截到部分持仓（需滚动多张）→ 主动问"是否还有更多持仓未截到"
- 同花顺持仓页的"摊薄成本价"与"买入均价"不同 → 优先取成本价，并在报告中注明口径
- 浮动盈亏列可能是百分比而非金额 → 看表头单位
- 融资融券账户的持仓含负债 → 单独标注，不纳入常规配置权重计算

---

## 输出前的数据校验

生成报告前逐项自检。缺失或过期指标填null并注明原因；v2不会赠送中性分，关键数据不足暂停评级/估值/配置：

1. 每只股票是否有**有效代码**（`search` 校验过）
2. 财报是否为**最近一期**（超过 6 个月未更新需提示）
3. K 线**最后一根的日期**是否与当前交易日接近（滞后 >5 日需标注）
4. 是否使用适用基本面模型及完整保守/基准/乐观情景，假设与来源可追溯；券商目标价和技术压力位独立展示
5. 市值/涨跌数据单位是否为**人民币元**（港股港元、美股美元需分别标注）

6. 每项指标是否有indicator_meta，现价是否有price_meta；风险是否区分未查询与已核查无事件
7. 250日K线不能代替3–5年时点估值序列；8期财报不足时补取年度数据和完整周期样本
8. 北向/机构数据的真实披露频率与来源已核实，不能推断不可得的日度净流入
9. 配置权重分母是否为包含现金、其他资产的总资产；风险政策和可交易状态不足时暂不配置
10. **红利类档位是否取了股息数据**（`dividend list`）：没取则股息子项不启用，报告会标注"未启用"
11. **行业景气度是否取自 `sector finance`**：不能手填一个 0–100 的景气分，也不能用个股盈利增速代替行业口径
12. 市场温度若显示"数据不足"，检查四条原始序列是否给全且各带 `indicator_meta`
