---
name: qveris-finance
version: 1.1.0
description: >-
  AI-powered financial data assistant for stock analysis and global market overview.
  Combines multiple QVeris data sources (TwelveData, Finnhub, Alpha Vantage, FMP)
  for company profiles, real-time quotes, fundamentals, valuation, analyst ratings,
  and news sentiment. Supports US market with extensible architecture for HK/CN.
homepage: https://github.com/QVerisAI/open-qveris-skills/tree/main/qveris-finance
env:
  - QVERIS_API_KEY
credentials:
  required:
    - QVERIS_API_KEY
  primary: QVERIS_API_KEY
  scope: read-only
  endpoint: https://qveris.ai/api/v1
runtime:
  language: nodejs
  node: ">=18"
install:
  mechanism: local-skill-execution
  external_installer: false
  package_manager_required: false
security:
  full_content_file_url:
    enabled: true
    allowed_hosts:
      - qveris.ai
    protocol: https
network:
  outbound_hosts:
    - qveris.ai
metadata:
  openclaw:
    requires:
      env: ["QVERIS_API_KEY"]
    primaryEnv: "QVERIS_API_KEY"
    homepage: https://qveris.ai
auto_invoke: true
source: https://qveris.ai
examples:
  - "分析 AAPL"
  - "Analyze NVDA with full report"
  - "今日市场速览"
  - "Global market overview"
  - "帮我看看微软的基本面和估值"
  - "Compare AAPL fundamentals to its historical valuation"
---

# QVeris Finance — AI 金融数据助手

基于 QVeris 工具生态的金融数据分析 Skill，聚合 TwelveData / Finnhub / Alpha Vantage / FMP 等专业数据源，通过一次对话获取结构化金融数据和分析摘要。

## 能力总览

| 模式 | 触发方式 | 说明 |
|------|---------|------|
| **个股分析** | `分析 AAPL` / `analyze MSFT` | 公司概况 · 行情 · 财务 · 估值 · 分析师 · 新闻情绪 |
| **市场速览** | `今日市场` / `market overview` | 美股指数 · 外汇 · 大宗商品 · 热点新闻 |

## 数据来源

所有数据通过 QVeris 工具网关获取。QVeris 聚合 1,000+ 数据供应商（含 TwelveData、Finnhub、Alpha Vantage、FMP 等），通过智能路由引擎自动选择最优供应商。本 Skill 不绑定任何特定供应商 — 每次调用由 QVeris discover 动态选择。

## 使用 QVeris 工具

本 Skill 通过 QVeris API 获取数据。检查可用调用方式并使用第一个可用的：

**Tier 1 — MCP 原生工具**（推荐）：如果环境中有 `qveris_discover` / `qveris_call` 或 `search_tools` / `execute_tool`，直接使用。

**Tier 2 — `http_request` 工具**：调用 QVeris REST API。

```
POST https://qveris.ai/api/v1/search
Headers: Authorization: Bearer ${QVERIS_API_KEY}
Body: {"query": "...", "limit": 5}

POST https://qveris.ai/api/v1/tools/execute?tool_id=<tool_id>
Headers: Authorization: Bearer ${QVERIS_API_KEY}
Body: {"search_id": "<from search>", "parameters": {...}, "max_response_size": 20480}
```

**Tier 3 — 脚本执行**（本 Skill 自带脚本）：

```bash
# 搜索工具
node {baseDir}/scripts/qveris_tool.mjs discover "stock quote real-time API" --limit 5

# 调用工具（需要先 discover 获取 discovery-id）
node {baseDir}/scripts/qveris_tool.mjs call twelvedata.quote.retrieve.v1.affbefe3 \
  --discovery-id <id> \
  --params '{"symbol": "AAPL"}'

# 查看工具详情
node {baseDir}/scripts/qveris_tool.mjs inspect twelvedata.quote.retrieve.v1.affbefe3
```

---

## 模式一：个股分析 (`analyze`)

### 触发条件

用户提到股票代码或公司名 + 分析意图：
- `"分析 AAPL"` / `"analyze NVDA"` / `"帮我看看苹果"`
- `"MSFT 基本面怎么样"` / `"英伟达估值贵不贵"`

### 工作流（5 步）

**每步先通过 QVeris discover 搜索最优工具，按 `success_rate` 和 `avg_execution_time_ms` 选择排名最高的工具，然后 call 执行。** 完整的 discover query 和预期字段定义在下方。如果 discover 无结果或首选工具失败，参考 `references/tool-routing.md` 中的已验证 tool_id 作为 fast-path。

#### Step 1: 公司概况

```
discover query: "company profile overview API"
selection: 选择 success_rate 最高、返回 name/sector/industry 等字段的工具
params: {"symbol": "<TICKER>"}
```

提取字段：`name`, `exchange`, `sector`, `industry`, `employees`, `CEO`, `description`（截取前 200 字）

#### Step 2: 实时行情

```
discover query: "stock quote real-time API"
selection: 选择支持单个 symbol 查询、返回 OHLCV + change 的工具
params: {"symbol": "<TICKER>"}
```

提取字段：`close`（当前价）, `change`, `percent_change`, `volume`, `fifty_two_week.high`, `fifty_two_week.low`, `datetime`

**重要**：输出中必须标注行情时间戳（`datetime` 字段），数据可能有 15 分钟延迟。

#### Step 3: 估值与财务指标

```
discover query: "stock valuation ratios PE PB EV EBITDA API"
selection: 选择能返回 PE/PB/PS/ROE/EPS 等综合指标的工具（优先选一次返回多指标的工具）
params: {"symbol": "<TICKER>", "metric": "all"}  (如工具支持 metric 参数)
max_response_size: 8192
```

**该类工具通常一次返回完整的估值 + 盈利 + 增长 + 效率指标**，无需单独调用财务报表。

提取字段（字段名因供应商而异，按语义匹配）：
- 估值：PE (TTM), PB, PS, EV/FCF
- 盈利：EPS (TTM), EPS 增长率, 收入增长率
- 效率：ROE, ROA
- 市值：market capitalization
- 分红：dividend yield
- 风险：beta

**注意**：响应可能因数据量大被截断（返回 `truncated_content`）。从截断内容中提取上述字段即可，无需下载完整文件。

#### Step 4: 分析师评级

```
discover query: "analyst rating recommendation price target API"
selection: 选择返回 buy/hold/sell 分布的工具
params: {"symbol": "<TICKER>"}
```

提取字段：取最新一条记录的 `buy`, `hold`, `sell`, `strongBuy`, `strongSell`, `period`

**可选加强**：如果上一步的工具不含 price target，再 discover `"analyst price target consensus API"` 补充：
提取：`price_target_high`, `price_target_low`, `price_target_average`

#### Step 5: 新闻与情绪

```
discover query: "financial news sentiment stock API"
selection: 选择支持按 ticker 过滤、返回情绪评分的工具
params: {"tickers": "<TICKER>", "sort": "LATEST", "limit": 5}  (参数名因工具而异，按描述适配)
```

提取字段：每条新闻的 `title`, `source`, `time_published`, `overall_sentiment_label`, `overall_sentiment_score`

### 输出格式

**根据用户表达方式自动选择输出风格：**

#### 口语模式（用户问"能买吗"/"怎么样"/"帮我看看"）

```
<公司名> <代码> · $<价格> (<涨跌幅>%)
数据时间: <datetime> (可能延迟 15 分钟)

一句话：<基于数据的简要结论>

收入增长 <revenueGrowthTTMYoy>%  EPS增长 <epsGrowthTTMYoy>%
PE <peTTM> 倍  PB <pbQuarterly> 倍  ROE <roeTTM>%
分析师 <strongBuy+buy> Buy / <hold> Hold / <sell+strongSell> Sell
目标价 $<price_target_average> (<vs当前价的百分比>%)
近期情绪 <overall_sentiment_label>

⚠️ 以上数据仅供参考，不构成投资建议
Data by QVeris
```

#### 专业模式（用户问"分析基本面"/"估值分析"/"详细报告"）

```
<公司名>（<代码>）分析摘要
数据时间: <datetime> UTC

| 指标 | 数值 |
|------|------|
| 价格 | $<close> (<percent_change>%) |
| 市值 | $<marketCap>B |
| PE (TTM) | <peTTM> |
| PB | <pbQuarterly> |
| PS (TTM) | <psTTM> |
| EV/FCF | <currentEv/freeCashFlowTTM> |
| EPS (TTM) | $<epsTTM> |
| ROE | <roeTTM>% |
| Beta | <beta> |
| 股息率 | <dividendYield>% |
| 52周区间 | $<low> — $<high> |

■ 概览  <sector> · <industry> · 员工 <employees>
■ 增长  收入 +<revenueGrowthTTMYoy>% YoY · EPS +<epsGrowthTTMYoy>% YoY
■ 估值  PE <peTTM> · PB <pbQuarterly> · PS <psTTM>
■ 预期  目标价 $<target_avg> (<upside>%) · <buy> Buy / <hold> Hold / <sell> Sell · 评级日期 <period>
■ 情绪  <sentiment_label> · 近期 <N> 篇报道
■ 风险  <基于数据的 2-3 个风险点>

⚠️ 数据摘要仅供参考，不构成投资建议
Powered by QVeris · Sources: TwelveData (profile/quote), Finnhub (metrics/analyst), Alpha Vantage (news)
```

### 质量要求

- **每个数字必须来自实际工具返回**，绝不编造数据
- **必须标注数据时间戳**，让用户知道数据新鲜度
- PE/PB 等指标标注口径（TTM / Annual / Quarterly）
- 分析师评级标注日期（`period` 字段）
- 如果某个工具调用失败，在输出中标注「该维度数据暂不可用」，不要跳过或编造

---

## 模式二：市场速览 (`market`)

### 触发条件

- `"今日市场"` / `"市场速览"` / `"晨间简报"`
- `"market overview"` / `"global market status"`

### 工作流（4 步）

#### Step 1: 美股指数 + VIX + 黄金

```
discover query: "stock market index quote S&P 500 NASDAQ API"
selection: 优先选择一次返回多个指数的 market summary 工具
params: {"market": "us"} 或按工具要求适配
max_response_size: 20480
```

提取：S&P 500、NASDAQ、Dow Jones 的价格和涨跌幅。如果工具同时返回 VIX 和 Gold Futures，一并提取。

**补充**：如果 market summary 工具未覆盖所有指数，再 discover `"stock quote real-time API"` 逐个查询 SPX / IXIC / DJI。

#### Step 2: 外汇汇率

```
discover query: "forex exchange rate currency pair API"
selection: 选择支持 currency pair 格式的实时汇率工具
调用 2 次：
  params: {"symbol": "USD/CNY"} 或 {"from_currency": "USD", "to_currency": "CNY"}
  params: {"symbol": "EUR/USD"}
```

#### Step 3: 大宗商品

```
discover query: "commodity price gold oil API"
selection: 选择返回黄金或原油价格的工具
```

**注意**：如果 Step 1 已返回黄金期货价格（如 GC=F），只需补充原油价格。

#### Step 4: 热点新闻

```
discover query: "financial market news sentiment API"
selection: 选择支持 topics 或 market 过滤的新闻工具
params: {"topics": "financial_markets", "sort": "LATEST", "limit": 5} (参数名因工具而异)
```

### 输出格式

```
全球市场速览 · <日期>
数据时间: <最新 datetime>

美股  标普 <SPX close> (<change>%)  纳指 <IXIC close> (<change>%)  道指 <DJI close> (<change>%)
外汇  USD/CNY <rate>  EUR/USD <rate>  USD/JPY <rate>
商品  黄金 $<price> (<change>%)  原油 $<price> (<change>%)

今日焦点
· <新闻标题 1>
· <新闻标题 2>
· <新闻标题 3>

⚠️ 数据仅供参考，不构成投资建议
Data by QVeris
```

---

## 错误处理

1. **工具调用失败**：检查参数格式，修正后重试。如果仍失败，尝试 fallback 工具
2. **数据截断**：保留 `truncated_content` 用于分析，告知用户完整数据可通过 `full_content_file_url` 获取
3. **3 次失败后**：诚实报告哪些工具和参数已尝试，标注缺失的数据维度

## 市场代码说明

| 市场 | 代码格式 | 示例 |
|------|---------|------|
| US | 直接 ticker | `AAPL`, `MSFT`, `NVDA` |
| HK | `.HK` 后缀 | `0700.HK`, `9988.HK` |
| CN | `.SH` / `.SZ` 后缀 | `600519.SH`, `000858.SZ` |

当前版本主要支持 US 市场数据。HK/CN 市场数据覆盖正在扩展中。

## 安全与合规

- 仅使用 `QVERIS_API_KEY`，不存储其他凭证
- 仅调用 `qveris.ai` API（HTTPS）
- 所有输出标注「不构成投资建议」免责声明
- 不执行任何包安装或任意命令
- 不在日志或输出中暴露 API 密钥
