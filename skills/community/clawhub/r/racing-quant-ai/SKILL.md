---
name: racing-quant-ai
description: 赛马量化AI选股系统，集成量化策略选股+个股智能推荐分析。从量化策略数据库筛选符合需求的策略，获取持仓个股，再进行深度分析，最终给出投资参考。触发词：量化选股，racing quant，策略选股，数据库选股，量化分析，AI选股。
---

# Racing Quant AI 赛马量化AI选股系统

## Overview

Racing Quant AI是一套集成化的A股量化选股分析系统，其本质是一个 **「信号→资产」的智能匹配引擎**。系统在三个层面产生信号（策略信号→持仓信号→交易信号），并通过四层匹配机制（用户需求→策略→标的→交易指令）完成从策略研究到交易执行的全链路闭环。

核心功能包含两大部分：
1. **策略选股**：从远程MySQL量化策略数据库中，根据用户需求智能匹配推荐量化策略，并获取策略对应的最新持仓股票
2. **深度分析**：对筛选出的持仓个股，使用结构化分析框架进行个股深度分析，给出客观的投资参考

整个工作流闭环：用户需求 → 匹配策略 → 获取持仓 → 个股分析 → 综合推荐

> ⚠️ **路演/系统说明时的叙事规范**：不要从数据库表结构或技术架构讲起。必须围绕「信号」和「匹配」展开——每个功能点都要回答：它产生什么信号？信号怎么找到对应的资产？详见 `references/signal-asset-matching-framework.md`。

## 触发条件

当用户满足以下任意一种场景时，自动启用本skill：
1. 用户要求"量化选股"、"AI选股"、"策略选股"
2. 用户提到"racing quant"、"赛马量化"、"赛马量化AI"
3. 用户需要从数据库选股并进行深度分析
4. 用户要求根据量化策略推荐股票并分析
5. 用户要求优化策略仓位管理（如调整单仓上限、分仓规则）或回测对比优化方案
6. 用户要求修改或排查 racingai.top 网站功能（前端展示、后端API、数据库问题），包括 bug 修复、性能排查、页面异常
## 数据源（优先级：Tushare > akshare > baostock > 东方财富API）

> 🔴 **数据校验铁律**：所有行情、财务、资金数据必须来自实际数据源调用结果。数据获取失败时必须如实标注"数据获取失败"，**严禁编造任何具体数值**。违反此规则视为重大事故（参见陷阱#14）。

### 1. Tushare MCP（主数据源 - 优先使用）
- **接入方式**：MCP Server `tushareMcp`，工具前缀 `mcp_tushareMcp_*`
- **覆盖范围**：
  - 日线行情（OHLCV）：`daily` / `pro_bar`（含前复权）
  - 每日指标（PE/PB/换手率/市值）：`daily_basic`
  - 财务指标（ROE/净利率/毛利率等）：`fina_indicator`
  - 利润表/资产负债表：`income` / `balancesheet`
  - 个股资金流向：`moneyflow`
  - 龙虎榜：`top_list` / `top_inst`
  - 涨跌停价：`stk_limit`
  - 复权因子：`adj_factor`
  - 交易日历：`trade_cal`
  - 股票基本信息：`stock_basic`
- **优势**：专业金融数据接口，数据准确性和稳定性优于 akshare/baostock
- **前提条件**：Gateway 已配置 tushareMcp MCP Server 并成功发现工具

### 2. new-akshare-stock（第一备用）
- 当 Tushare MCP 不可用（token失效、MCP连接失败、工具未注册）时自动切换
- 覆盖行情、财务、资金流向、龙虎榜等A股量化数据

### 3. baostock（第二备用）
- 当 akshare 也不可用时自动切换
- 覆盖行情K线、财务、基础证券数据

### 4. 东方财富 Push API（兜底）
- 当以上所有Python/MCP接口均不可用时，通过curl调用东方财富实时行情API

### 5. cn-web-search / wechat-article-search（辅助信息源）
- 个股深度研究、行业动态、政策解读，优先返回微信公众号来源内容，自动备注文章标题

### 6. 赛马量化策略数据库
- 实时获取策略持仓、历史绩效、因子暴露数据（MySQL远程连接，独立于行情数据源）

## 核心功能

### 功能1：策略数据库查询与选股

支持多种查询方式，包括直接查询、关键词搜索和**互动偏好匹配**，满足不同用户场景：

#### 数据库配置
连接信息（远程公开量化策略库）：
- 地址：47.121.180.199
- 端口：3306
- 账号：display
- 密码：display999!
- 数据库：db_strategy
- 主表：strategy_information

#### 主策略表字段说明
| 字段 | 类型 | 说明 |
|------|------|------|
| strategy_table | text | 策略对应持仓数据表名称 |
| strategy_name | text | 策略英文名称 |
| strategy_id | text | 策略ID（唯一标识） |
| benchmark | text | 对标指数 |
| owner_name | text | 策略创建人姓名 |
| owner_id | text | 创建人ID |
| start_date | datetime | 策略开始回测时间 |
| online_date | datetime | 策略上线时间 |
| strategy_name_cn | text | 策略中文名称 |
| strategy_summ | text | 策略简介 |
| strategy_desc | text | 策略详细描述 |
| strategy_cat | text | 策略分类（量价/基本面/事件驱动/量化选股等） |
| how_to_trade | text | 交易调仓规则 |
| if_recommended | bigint | 是否推荐（1=推荐，0=不推荐） |

#### 策略持仓表字段说明
| 字段 | 类型 | 说明 |
|------|------|------|
| trade_date | text | 交易日期 |
| strategy_name | text | 策略名称 |
| strategy_id | text | 策略ID |
| trading_info | text | 交易信息（持仓信息json，主键为证券代码、值为权重，举例 {'300001.SZ':'0.1'}） |
| trade_price | text | 交易价格（open/close） |
| update_time | datetime | 更新时间 |

#### 支持的查询操作
1. **获取全部策略列表**：查询数据库中所有注册策略，展示策略基本信息
2. **关键词搜索策略**：根据关键词搜索策略名称/简介/描述，返回匹配结果
3. **分类筛选**：按策略分类（量价/基本面等）筛选策略
4. **推荐策略筛选**：只筛选标记为if_recommended=1的优质推荐策略
5. **需求智能匹配**：根据用户描述的投资需求，语义匹配最符合的策略
6. **互动偏好匹配**：通过多轮互动提问，了解用户的投资偏好和风险承受能力，从strategy_desc字段中匹配最契合的策略
7. **获取最新持仓**：根据选中的策略，查询对应持仓表获取最新一期持仓股票列表
备注：多策略命中时，仅列表展示，不自动择优，需用户确认后再获取持仓。

---

### 功能2：个股深度分析（5维度分析框架）

对策略输出的持仓股票，逐个进行结构化深度分析，遵循以下分析框架：

> 💡 **深度分析模式选择**：当用户要求使用"stock-research-sop"分析时，应加载 `quant-finance` 技能的 `templates/stock-research-sop.md` 模板，按三阶段（基本面->技术面->综合判断）执行，该SOP比本5维度框架更严格（含评分、盈亏比、投资者匹配）。本5维度框架适用于快速分析和批量持仓扫描。

#### 维度1：核心交易数据
- 最新股价、当日涨跌幅
- 日内波动区间（最高价/最低价）
- 成交量、成交额、换手率
- 总市值
- 估值指标（PE(TTM)、PB）

**数据源**：优先通过 Tushare MCP 获取；若 Tushare 不可用（token失效/MCP连接失败），切换至`new-akshare-stock`；再不可用切换至`baostock`。最终报告标注实际使用的数据源。
**数据校验要求**：所有量价、市值、估值基础字段，必须与调用数据源实时校验准确性，异常数据高亮备注。

#### 维度2：股价走势回顾
分类展示不同周期涨跌幅：
- 短期：近5日、近1个月
- 中期：近3个月
- 长期：近1年、近5年

**数据源**：优先通过 Tushare MCP 获取；若 Tushare 不可用（token失效/MCP连接失败），切换至`new-akshare-stock`；再不可用切换至`baostock`。最终报告标注实际使用的数据源。
**数据校验要求**：多周期涨跌幅历史量价数据，需匹配数据源原始口径核验计算逻辑，杜绝偏差。

#### 维度3：资金面分析
- 近期主力资金流向（净流入/净流出）
- 主力持仓成本对比当前股价
- 机构控盘度
- 关键支撑位/压力位

**数据源**：优先通过 Tushare MCP 获取；若 Tushare 不可用（token失效/MCP连接失败），切换至`new-akshare-stock`；再不可用切换至`baostock`。最终报告标注实际使用的数据源。
**数据校验要求**：主力资金流向明细，严格校验数据源原始流水数据，异常波动单独标注。

#### 维度4：基本面核心分析
- 估值对比：当前PE/PB对比行业平均，判断高估/低估
- 业绩表现：近期营收、净利润增速，增长稳定性
- 业务亮点：核心优势、新增长点
- 风险提示：客观列出潜在风险（高负债、政策风险、行业周期等）

**数据源**：优先通过 Tushare MCP（`fina_indicator` / `income` / `balancesheet`）获取财务数据；若 Tushare 不可用，切换至`new-akshare-stock`获取公开财务数据；再不可用切换至`baostock`获取。结合`cn-web-search`搜索最新公开信息和机构研报，优先返回微信公众号来源内容，自动备注文章标题
**数据校验要求**：营收、净利润、PE/PB 等财务核心指标，必须对照数据源原始财报字段精准校验，保证基本面数据真实可溯源。

#### 维度5：综合评价
- 短期趋势判断，基于资金面和技术面数据
- 长期投资价值评价，基于基本面分析和估值水平
- 不同类型投资者参考建议（保守/稳健/激进）
- **必须添加免责声明**：明确说明"分析结果仅供学习交流，不构成任何投资建议，投资有风险，入市需谨慎"
- **必须标注**：本次行情/财务/资金数据实际来源（new-akshare-stock 或 baostock）

## 完整工作流程
工作流优先级：用户有明确选股需求 / 指定策略→直接自动执行；无任何需求→触发互动提问；
补充匹配兜底规则：若关键词 / 偏好 / 分类筛选匹配出 2 条及以上策略，仅展示【策略名称 + 中文简介】列表给到用户，等待用户手动选定具体策略后，再执行拉取持仓、个股分析流程，不自动默认选中任意策略。

### 标准工作流（用户给出投资需求）
```
1. 连接数据库 → 查询所有策略
2. 根据用户需求，智能匹配最符合的1-3个策略
3. 对匹配的每个策略，获取其最新一期持仓股票（通常前10-20只）
4. 对持仓股票逐个进行个股深度分析（如用户没有指定数量，则默认前5只）
5. 整理汇总：策略信息 → 持仓列表 → 个股分析报告 → 综合总结
6. 输出完整报告，报告格式严格按照如下输出：
   - 策略信息（名称/ID/简介/描述）
   - 持仓列表（股票代码/名称/占比）
   - 个股分析（每只股票按照5维度分析框架输出）
   - 综合总结（策略优势、风险提示、投资建议）
   - 信息来源注释（公开研报、微信公众号深度报告标题）
   - 免责声明（分析结果仅供学习交流，不构成投资建议，投资有风险，入市需谨慎）
```

### 用户指定策略名称/ID工作流
```
1. 根据用户提供的策略名称/ID，从数据库查询策略详细信息，返回匹配到的策略信息包括名称/ID
2. 获取该策略最新持仓列表
3. 对持仓股票进行个股深度分析（如用户没有指定数量，则默认前5只）
4. 输出完整报告，报告格式严格按照如下输出：
   - 策略信息（名称/ID/简介/描述）
   - 持仓列表（股票代码/名称/占比）
   - 个股分析（每只股票按照5维度分析框架输出）
   - 综合总结（策略优势、风险提示、投资建议）
   - 信息来源注释（公开研报、微信公众号深度报告标题）
   - 免责声明（分析结果仅供学习交流，不构成投资建议，投资有风险，入市需谨慎）
```

### 用户只想查询策略工作流
```
1. 根据用户条件（关键词/分类）筛选策略
2. 输出策略列表和基本信息，供用户选择
3. 用户选择后再进行下一步获取持仓和分析（如用户没有指定数量，则默认前5只）
4. 输出完整报告，报告格式严格按照如下输出：
   - 策略信息（名称/ID/简介/描述）
   - 持仓列表（股票代码/名称/占比）
   - 个股分析（每只股票按照5维度分析框架输出）
   - 综合总结（策略优势、风险提示、投资建议）
   - 信息来源注释（公开研报、微信公众号深度报告标题）
   - 免责声明（分析结果仅供学习交流，不构成投资建议，投资有风险，入市需谨慎）
```

### 互动偏好匹配工作流（在不明确用户偏好时，优先使用）
```
1. 主动提问了解用户的投资偏好，包括：
   - 投资周期偏好（短期/中期/长期）
   - 风险承受能力（保守/稳健/激进）
   - 选股风格偏好（价值成长/红利低波/动量趋势/事件驱动）
   - 行业偏好（是否有特定看好或回避的行业）
   - 其他特殊需求
2. 将用户回答的偏好转化为搜索关键词，在strategy_desc字段中进行语义匹配
3. 按匹配度排序，推荐最符合的3-5个策略
4. 请用户确认选择哪个策略
5. 用户确认后，获取策略最新持仓并进行个股分析（如用户没有指定数量，则默认前5只）
6. 输出完整报告，报告格式严格按照如下输出：
   - 策略信息（名称/ID/简介/描述）
   - 持仓列表（股票代码/名称/占比）
   - 个股分析（每只股票按照5维度分析框架输出）
   - 综合总结（策略优势、风险提示、投资建议）
   - 信息来源注释（公开研报、微信公众号深度报告标题）
   - 免责声明（分析结果仅供学习交流，不构成投资建议，投资有风险，入市需谨慎）
```

### 策略持仓→交易执行（QMT下单）

当用户要求将策略持仓直接推送到交易系统（QMT）时，启用此工作流。

#### 工作流程
```text
1. 连接MySQL策略数据库 → 获取指定策略的最新持仓（代码+权重）
2. 调用东方财富批量API获取实时行情（前20只的现价/涨跌幅/昨收）
3. 加载当前持仓快照（如有）
4. 计算买卖指令：
   - 买入：按权重分配资金，考虑现存仓位，100股取整
   - 卖出：全量换仓模式下，不在目标持仓中的股票全部卖出
5. 风险检查：涨跌停偏离、最低金额、单只仓位上限
6. 输出交易指令JSON或通过xtquant实际下单
```

#### 脚本位置
- `~/.hermes/scripts/racing_to_qmt.py` — 一体化生成+执行脚本
- 详情见 `references/trading-execution-pipeline.md`

#### 关键命令
```bash
# 生成指令（Hermes端）
python3 ~/.hermes/scripts/racing_to_qmt.py --mode=generate-only \\
    --strategy="短周期机器学习时序交叉版" --capital=100000 --top-n=10

# 执行下单（QMT端，需安装xtquant）
python racing_to_qmt.py --mode=execute --account=1234567890
```
1. "你好！为了给你推荐最合适的量化策略，可以先回答几个问题吗？"
2. "你的投资周期更倾向于哪种？（短期/中期/长期）"
3. "你的风险承受能力大概是什么水平？（保守/稳健/激进）"
4. "你更喜欢哪种选股风格？比如：价值成长/红利低波/动量趋势/事件驱动..."
5. "有没有特别看好或者想要回避的行业？"
6. "还有其他特殊需求吗？"

## 工具调用规范

0. **数据校验强制要求（铁律）**：获取个股量价行情、财务估值、资金流向核心数据时，优先使用 Tushare MCP 获取专业金融数据，严格对照当前生效数据源（Tushare/new-akshare-stock/baostock）做字段核验，确保股价、市值、PE/PB、营收利润、主力资金等关键数值完整无误；异常空值、离谱极值需标注说明。**严禁编造任何具体数值，严禁沿用错误数据。数据获取失败时必须如实标注"数据获取失败"。** 违反此规则视为重大事故（参见陷阱#14）。
1. **数据库查询**：使用Node.js连接MySQL数据库，参考scripts目录下的数据库连接模板
2. **获取行情数据**：优先通过 Tushare MCP（`daily` / `daily_basic` / `pro_bar`）获取最新股价和各周期涨跌幅数据；Tushare 不可用时切换至`new-akshare-stock`；再不可用切换至`baostock`
3. **获取主力资金流向**：优先通过 Tushare MCP（`moneyflow`）获取每日主力资金数据；Tushare 不可用时切换至`new-akshare-stock`；再不可用切换至`baostock`
4. **基础信息搜索**：分析前先使用`cn-web-search`搜索股票最新公开信息、机构研报和市场数据
5. **深度报告搜索**：添加`wechat-article-search`深度搜索机制，搜索微信公众号最新发布的个股深度研究报告，获取市场最新观点和深度分析内容，并在最终报告中明确注释引用的公众号文章/深度报告标题
6. **融合分析**：整合量化策略数据库信息、行情数据、主力资金数据、公开市场数据和微信公众号深度研究报告内容，进行多维度融合分析
7. **严格框架**：严格按照5维度分析框架整理输出，不遗漏风险提示
8. **风险优先**：必须同时列出优势和风险，不做片面推荐
9. **输出格式适配**：用户可能要求不同场景的输出格式。若用户要求"雪球讨论区/评论区发帖格式"，输出应遵循：纯文本、无Markdown表格（用对齐文本替代）、用▍/▸/⚠/◆等Unicode符号增强可读性、段落短小精悍、口语化表达（"一句话：…"、"别装看不见"）、避免过度学术化措辞、风险清单用数字编号简洁列出、末尾保留免责声明。核心原则：像一篇有深度的球友帖子，不是研报。
10. **信息标注**：分析过程中引用的公开研报和公众号深度文章，需要在报告末尾注明信息来源
10. **数据源标注**：每份报告必须标注本次量化数据来源（Tushare MCP / new-akshare-stock / baostock），注明实际使用的具体接口
11. **免责声明**：所有分析结果末尾必须带有免责声明

## 陷阱与注意事项

### 环境依赖安装
- akshare 和 baostock 不一定预装在 hermes venv 中
- hermes venv python 路径：`/home/ubuntu/.hermes/hermes-agent/venv/bin/python3`
- 安装步骤：先 `python3 -m ensurepip`（venv 可能没有 pip），再 `python3 -m pip install akshare baostock`
- **必须在 venv python 下安装**，系统 python3 的 `--break-system-packages` 安装不会对 hermes 生效

### 网络限制与数据源降级
- akshare 的东方财富实时接口（`stock_zh_a_spot_em`、`stock_zh_a_hist`）可能因服务器网络限制返回 `RemoteDisconnected` 错误
- baostock 连接也可能超时（login 成功但 query 超时），但**批量K线查询通常稳定**（每次query约1秒）
- **多股票批量分析的最优数据源组合**：
  - **baostock**：批量K线+技术指标（MA/MACD/RSI）——最稳定，for循环批量查询不超时
  - **akshare**：仅用`stock_individual_fund_flow`（资金流向）和`stock_news_em`（新闻）——最稳定的两个接口
  - **akshare**：`stock_financial_abstract_ths`（财务摘要）——可用但注意indicator参数
  - **执行方式**：将Python脚本write_file到/tmp再执行，**不要用`python3 -c`传递含中文的复杂代码**——shell引号嵌套+中文字符极易SyntaxError
- **降级方案**：当 akshare/baostock Python 接口不可用时，使用 `web_fetch` 通过东方财富 Push API 获取实时行情：
  - 实时行情：`https://push2.eastmoney.com/api/qt/stock/get?secid=0.300308&fields=f43,f44,f45,f46,f47,f48,f50,f51,f52,f55,f57,f58,f60,f116,f117,f162,f167,f170,f171`
  - 字段映射：f43=最新价, f44=最高, f45=最低, f46=今开, f47=成交量, f48=成交额, f50=量比, f57=代码, f58=名称, f60=昨收, f116=总市值, f117=流通市值, f162=PE, f167=PB, f170=换手率, f171=涨跌幅
  - 沪市股票 secid 前缀用 `1.`，深市用 `0.`

### 财务数据 API 陷阱
- `stock_financial_abstract_ths(symbol, indicator="按报告期")` 默认按时间正序排列，`head(4)` 返回最早的数据而非最新的
- 应使用 `indicator="按年度"` 并 `tail(4)` 获取最近4年数据
- 或始终用 `tail()` 而非 `head()` 取最新数据

### 资金流向数据可靠性
- `stock_individual_fund_flow` 接口通常稳定可用，即使实时行情接口不通
- 可优先获取资金流向数据，作为行情数据的补充参考（含每日收盘价）

## 基本原则

1. **遵守规范**：严格按照既定流程和标准执行各项操作
2. **客观中立**：只整理公开信息和量化策略结果，不做主观判断
3. **风险提示**：风险提示清晰可见，不隐藏负面信息
4. **信息来源**：所有数据来自公开渠道和量化策略数据库
5. **责任豁免**：始终声明不构成投资建议，投资风险自负
6. **容错降级**：量化数据源支持自动降级切换（Tushare -> akshare -> baostock -> 东方财富API），保证系统稳定可用
7. **数据真实性铁律**：严禁编造数据。数据获取失败时必须如实标注，不得用任何估算值、猜测值或模型生成值替代真实数据。报告中每个数值必须可溯源至具体数据源调用

### 资源

### references/
- `signal-asset-matching-framework.md` — 信号-标的匹配框架：对外路演的核心叙事规范，三层信号体系+四层匹配机制，禁止从架构讲起
- `portfolio-analysis-workflow.md` — 全持仓深度分析的可复用工作流（数据采集→5维度分析→报告输出），含数据源可靠性、陷阱与报告模板
- `trading-execution-pipeline.md` — 策略持仓→QMT交易执行流水线，含 racing_to_qmt.py 脚本用法、模式对比、交易规则配置
- `strategy-drawdown-analysis.md` — 策略历史回撤分析方法论：月度持仓快照、换手率统计、持仓集中度追踪、ETF涨跌幅与持仓时长相关性分析
- `strategy-drawdown-analysis.md` — 策略历史回撤分析方法论：查询任意策略在指定时间段内的持仓变化、换手率、持仓集中度，并关联ETF/个股价格走势解释回撤原因

### references/
- `position-sizing-optimization.md` — 策略仓位优化回测框架：从MySQL拉取历史持仓→东方财富获取价格→模拟原始vs优化策略→对比指标。含最优参数(10%单仓上限+50%总仓位保底)回测验证结果
- `fintech-codebase-structure.md` — racingai.top网站(Go+React)代码结构、开发规范、部署流程。当用户要求修改网站功能时参考

### scripts/
### references/
- `multi-stock-analysis-workflow.md` - 多股票批量深度分析的完整工作流模板（数据源组合、技术指标计算、分析框架、Feishu导出）
- `concept-stock-analysis-workflow.md` - 概念股/主题驱动产业链分析工作流（搜索->识别标的->产业链分层->批量行情采集->综合研判->持仓交叉分析），含超节点算力产业链实战案例
- `tsauto_run-strategy-inventory.md` — 用户自研量化仓库 warwickInv/tsauto_run 的完整策略储备清单（数据ETL→因子工程→ML多因子模型20+变体→择时策略5种→行业轮动→运维辅助），私有Gitee仓库需token访问

### scripts/
包含可直接运行的数据库查询脚本：
- `check-json.js`：检查JSON格式正确性
- `desc-table.js`：输出策略描述表格
- `get-positions-correct.js`：获取策略最新正确持仓列表
- `get-positions.js`：获取策略持仓列表（原始版）
- `get-positions-json.js`：获取持仓JSON格式
- `get-position-table.js`：输出持仓表格
- `list-recommended.js`：列出所有推荐策略
- `read-strategies.js`：读取策略信息
- `strategy-history-analysis.js`：查询指定策略在任意时间段的持仓变化历史（月度快照+换手率+持仓数趋势），用法：`node strategy-history-analysis.js <strategy_id> <start_date> <end_date>`

## 依赖
- Node.js 环境
- `mysql2` 包：用于连接MySQL量化策略数据库（**必须在 scripts/ 目录下 `npm install mysql2`，旧版 `mysql` 包不可用**）
- **Tushare MCP（主数据源）**：MCP Server `tushareMcp` 已在 config.yaml 中配置，提供专业金融数据（行情/财务/资金流向/龙虎榜等）。需 Gateway 重启后自动发现工具。若 MCP 连接失败则自动降级至下方备用数据源
- `new-akshare-stock`技能：第一备用数据源（行情、财务、资金流向、龙虎榜等A股量化数据）
- `baostock`技能：第二备用数据源（行情、财务、基础证券数据，自动降级使用）
- `cn-web-search`技能：用于获取个股最新公开信息和机构研报
- `wechat-article-search` 深度搜索：搜索微信公众号最新深度研究报告
- `stock-analysis` 技能：提供结构化个股分析框架，自动适配 Tushare / new-akshare-stock / baostock 数据源

## 坑与陷阱（实战经验）

### 14. 数据幻觉事故防范（2026-07-24 重大事故修复）

**事故复盘**：每日持仓分析cron job（8c5674a53206）使用 `portfolio_report.py` 脚本采集行情。当 akshare 的 `stock_zh_a_spot_em()` 接口返回 `RemoteDisconnected` 时，脚本输出全 N/A。下游 LLM（deepseek-v4-flash）在收到全 N/A 数据后，**没有如实报告失败，而是编造了一整套虚假行情数据**（成交额、涨跌幅、换手率、大宗交易等全部捏造），推送至飞书群。

**根因**：
1. 脚本无降级方案（akshare 失败即全军覆没）
2. Prompt 无防幻觉护栏（未禁止编造数据）
3. 盘前9:00运行取实时行情（市场未开，数据无效）

**修复措施（已实施 v2.1）**：
1. **脚本降级**：`portfolio_report.py` 主数据源改为 baostock（稳定可靠），登录一次批量查询，3秒完成14只标的采集
2. **Prompt 硬护栏**：在 cron prompt 中添加 5 条数据完整性要求，明确禁止编造数据
3. **状态报告**：脚本输出开头包含采集状态摘要（成功/失败计数），失败品种标注"数据获取失败"

**铁律：任何分析报告中，行情数据只能来自脚本采集的表格。如果数据为 N/A/获取失败，必须如实标注，严禁编造任何具体数字。违反此规则视为重大事故。**

### 15. Tushare MCP 数据源使用规范（2026-07-24 新增）

**Tushare MCP 作为主数据源的调用优先级**：
1. 优先调用 `mcp_tushareMcp_*` 系列工具获取行情、财务、资金数据
2. Tushare MCP 连接失败时（工具未注册/连接超时/token失效），自动降级至 `new-akshare-stock` 技能
3. akshare 不可用时再降级至 `baostock` 技能
4. 所有 Python 接口不可用时，使用东方财富 Push API（curl方式）兜底

**Tushare 接口与原数据源的映射关系**：
| 数据需求 | Tushare 接口 | 原 akshare/baostock 接口 |
|---------|-------------|------------------------|
| 日线行情(OHLCV) | `daily` / `pro_bar`(前复权) | `stock_zh_a_hist` / `query_history_k_data_plus` |
| 每日指标(PE/PB/换手率/市值) | `daily_basic` | `stock_zh_a_spot_em` |
| 财务指标(ROE/净利率等) | `fina_indicator` | `stock_financial_abstract_ths` |
| 利润表 | `income` | 同上 |
| 资产负债表 | `balancesheet` | 同上 |
| 个股资金流向 | `moneyflow` | `stock_individual_fund_flow` |
| 龙虎榜 | `top_list` / `top_inst` | `stock_lhb_detail_em` |
| 涨跌停价 | `stk_limit` | 无直接对应 |
| 复权因子 | `adj_factor` | baostock `adjustflag`参数 |
| 交易日历 | `trade_cal` | `tool_trade_date_hist_sina` |
| 股票基本信息 | `stock_basic` | `stock_info_a_code_name` |

**注意事项**：
- Tushare MCP 工具需 Gateway 重启后才能发现注册，新会话中才能使用
- 检查 Tushare MCP 是否可用：观察是否有 `mcp_tushareMcp_*` 前缀工具
- Tushare 的日期格式为 `YYYYMMDD`（如 `20260724`），需注意与 akshare（`YYYY-MM-DD`）和 baostock（`YYYY-MM-DD`）的格式差异
- Tushare 部分高级接口需要更高积分权限，若返回权限不足错误，降级至 akshare/baostock
- **数据校验**：从 Tushare 获取数据后，与降级数据源进行关键字段交叉验证（如最新价、PE），确保数据一致性

### 1. 首次使用必须安装依赖
```bash
# Node.js 依赖（必须在 scripts/ 目录下执行）
cd ~/.hermes/skills/racing-quant-ai/scripts && npm install mysql2

# Python 依赖（hermes venv 需要先安装 pip 再装 akshare）
python3 -m ensurepip
python3 -m pip install akshare baostock
```
**如果跳过此步骤，所有数据库脚本和行情接口都会报 MODULE_NOT_FOUND。**

### 2. akshare 接口不稳定 — 必须准备降级方案

**接口可靠性矩阵（2026-05 实测）：**

| 接口 | 可用性 | 说明 |
|------|:------:|------|
| `stock_zh_a_spot_em()` | ❌ | 高频 `RemoteDisconnected`，**不可作唯一数据源** |
| `stock_zh_a_hist()` | ⚠️ | 同样受连接问题影响 |
| `fund_etf_spot_em()` | ⚠️ | 部分可用，但部分ETF返回NaN（如纳指ETF、现金流ETF），沪市ETF较稳定。**当stock_zh_a_spot_em失败时此接口仍可尝试** |
| `stock_individual_fund_flow()` | ✅ | **最可靠**的akshare接口，含每日收盘价和主力净流入 |
| `stock_financial_abstract_ths()` | ✅ | 可用，`indicator="按年度"` 取近年数据，**勿用"按报告期"**（返回2008年起旧数据） |
| `stock_news_em()` | ✅ | 个股新闻稳定可用，返回标题+时间 |
| `index_us_stock_sina()` | ⚠️ | 可用但返回全量历史数据（数万行），需 tail() 截取，否则极耗内存 |
| 黄金价格接口 | ❌ | `gold_price_history`、`fx_spot_quote` 等均不可用 |

**baostock 接口可靠性（2026-05 实测）：**

| 接口 | 可用性 | 说明 |
|------|:------:|------|
| `query_history_k_data_plus()` — **个股** | ✅ | 个股K线稳定，前复权取最新价 |
| `query_history_k_data_plus()` — **ETF** | ⚠️ | **仅返回近~120天数据**，不支持长历史回测！回测ETF需用东方财富历史K线API（见下方） |
| `query_profit_data()` | ✅ | 盈利能力数据稳定 |
| `query_growth_data()` | ✅ | 成长能力数据稳定 |
| `query_balance_data()` | ✅ | 偿债能力数据稳定 |

### 降级链路：Tushare MCP（daily/daily_basic/pro_bar）-> akshare实时行情 -> baostock K线（个股，前复权取最新价）-> 东方财富Push API
- ⚠️ 东方财富Push API（curl方式）在hermes环境下**返回空响应**，不可用！需通过akshare/baostock Python接口获取
- ⚠️ **baostock ETF K线仅返回近120天**，不支持长历史回测
- 若所有Python接口均不可用，可尝试 `web_fetch` 抓取东方财富网页版

### 东方财富历史K线API（回测/长历史数据专用）
当需要完整的历史K线数据（如策略回测、多年度涨跌幅计算）时，使用以下API：
```python
# API: https://push2his.eastmoney.com/api/qt/stock/kline/get
# 参数: secid={market}.{code}&fields1=f1,f2,f3&fields2=f51,f52,f53&klt=101&fqt=1&beg=YYYYMMDD&end=YYYYMMDD
# market: 1=沪市, 0=深市
# fields2: f51=date, f52=open, f53=close (还有f54=high, f55=low)
# klt=101=日线, fqt=1=前复权

import subprocess, json
url = f"https://push2his.eastmoney.com/api/qt/stock/kline/get?secid={market}.{code}&fields1=f1,f2,f3&fields2=f51,f52,f53&klt=101&fqt=1&beg=20230601&end=20260701"
result = subprocess.run(['curl', '-s', '--connect-timeout', '10', '--max-time', '15', url], capture_output=True, text=True, timeout=20)
data = json.loads(result.stdout)
klines = data.get('data', {}).get('klines', [])  # ["2023-06-01,1.474,1.523", ...]
```
**关键坑**：必须用 `subprocess.run(['curl', ...])` 而非 `urllib.request.urlopen` — 批量请求时urllib会大量失败（"Remote end closed connection"），curl带重试机制可靠。每个请求间隔0.15秒，3次重试。

### 3. Node.js 内联脚本在 terminal 中有转义陷阱
- 在 `terminal(command="node -e '...'")` 中写复杂 SQL 查询时，shell 引号嵌套极易出错
- **推荐做法**：先用 `write_file` 写入 `/tmp/xxx.js`，然后 `cp` 到 `scripts/` 目录再执行（因为 `scripts/` 下已有 `node_modules`）

### 4. 策略持仓扫描的正确做法
- 查询某只股票是否被策略持有时，不能仅查当前推荐策略（if_recommended=1）
- 应全库扫描所有36个策略的 `trading_info LIKE '%股票代码%'`
- 当前不持有不代表历史上没持有过 — **历史持仓回溯**能提供重要的量化信号（集体清仓时间点）

### 6. trading_info 字段在 mysql2 中返回为 Object 而非 String
- mysql2 默认会自动解析 JSON 类型的列，`trading_info` 字段返回时已经是 **JavaScript 对象**，不是字符串
- 对 Object 调用 `.substring()` 会报 `row.trading_info?.substring is not a function`
- **正确处理方式**：
```javascript
let holdings = row.trading_info;
if (typeof holdings === 'string') {
    try { holdings = JSON.parse(holdings); } catch(e) { holdings = {}; }
}
// holdings 现在是对象，直接用 Object.keys(holdings) 即可
```
- 如果用 `JSON.stringify(row.trading_info)` 反而会把已解析的对象再序列化成字符串，导致双重编码

### 7. 策略网页为 React SPA，curl 无法获取内容
- `http://racingai.top/strategy/{id}` 是 Vite + React 前端，curl 只返回空壳 HTML
- 需要直接查询策略数据库获取策略信息和持仓数据（strategy_information 表 + 对应 strategy_table）
- 策略ID映射：URL中的 `/strategy/stgetf0001` → `strategy_id = 'stgetf0001'` → 查询 `strategy_information` 表获取 `strategy_table` 名

### 8. 仓位优化代码必须放在信号生成脚本中
> ⚠️ 用户曾明确要求：撤销推送到 fintech 仓库 dev_hermes 分支的所有前后端改动，改为只改信号脚本。
- 仓位调整逻辑（如分层仓位管理）**直接写在 `stgetf0001_huaxia_pool.py` 等信号生成脚本中**
- **绝不在 fintech 前后端展示层修改**——前后端只负责读取和展示 `trading_info` 中的权重值，不参与仓位计算
- 部署到 quant-ai-4u 项目的 `dev_hermes` 分支，不要推到 fintech 仓库
- 优化完成后用户通常要求生成**非常详细**的总结报告（"不要遗漏任何点"），详见 `references/position-sizing-optimization.md` 第6-7节。报告须包含四大部分+9个分析维度+市场温度计ASCII可视化，并上传至飞书文档

### 9. 后端日志不在 journalctl 中
- fintech-backend.service 的 `StandardOutput/StandardError` 重定向到 `/var/log/fintech/backend.log`
- `journalctl -u fintech-backend` 只显示 systemd 层面的启停/崩溃日志，**看不到 Go 应用 `log.Printf` 输出**
- **正确做法**：`tail -50 /var/log/fintech/backend.log` 查看应用日志

### 10. GORM 全局 MAX(date) 反模式导致数据查不到
- 不同策略的监控数据更新日期可能不一致（如 stg000006 到 7-11，其他策略到 7-10）
- `GetLatestStrategyMonitoring` 先取全局 `MAX(calculate_date)`，再用该日期查特定策略 -> 大部分策略 `record not found` -> 500 错误 -> 净值曲线无法显示
- **正确做法**：MAX 查询加 `WHERE strategy_id = ?` 条件；批量查询用 INNER JOIN 子查询
- 详见 `references/fintech-codebase-structure.md` 的「调试指南」章节

### 12. cronjob 工具 action='update' 会覆盖 prompt（2026-07 实测）
- `cronjob(action='update')` **不是只读操作**——传入 `prompt` 参数会立即覆盖现有 prompt
- ⚠️ **绝对不要用 `cronjob(action='update', prompt='test')` 来"查看"当前 prompt**，这会直接把生产 prompt 替换为 "test"
- **查看完整 prompt 的正确方法**：直接读取 `~/.hermes/cron/jobs.json` 文件（`read_file` 工具），其中 `prompt` 字段包含完整内容
- `cronjob(action='list')` 返回的 `prompt_preview` 字段是被截断的，不足以查看全貌
- 如果已误覆盖：检查 `~/.hermes/cron/output/<job_id>/` 目录下的历史输出 .md 文件，其中 `## Prompt` 段落包含原始 prompt 全文

### 13. 融资融券/北向资金 akshare API 陷阱（2026-07 实测）
- `stock_margin_detail_szse()` **不接受 `code` 参数**，必须传 `date` 获取全量数据再过滤
- `stock_hsgt_individual_em()` 参数名是 `symbol` 不是 `stock`，且返回数据可能严重滞后（实测仅返回2024-08数据）
- 融资融券数据可用 `stock_margin_detail_szse(date="20260717")` 后过滤目标股票
- 龙虎榜用 `stock_lhb_detail_em(start_date, end_date)` 后过滤，大盘股通常不在龙虎榜
- 完整API调用示例见 `quant-finance` 技能的 `references/technical-indicators-computation.md`

### 8. 东方财富 ETF 名称/价格批量查询
- **ETF 名称**：`push2.eastmoney.com/api/qt/stock/get?secid={market}.{code}&fields=f57,f58`（f57=代码, f58=名称）
- **历史K线**：`push2his.eastmoney.com/api/qt/stock/kline/get?secid={market}.{code}&fields1=f1,f2,f3&fields2=f51,f52,f53,f54,f55,f56&klt=101&fqt=1&beg={YYYYMMDD}&end={YYYYMMDD}`
  - klines 格式：`date,open,close,high,low,volume`
- **secid 前缀**：沪市 `1.`，深市 `0.`
- 部分请求会失败（`Remote end closed connection without response`），需 retry 或间隔 `time.sleep(0.5-1)`
- 详见 `references/strategy-drawdown-analysis.md`

## 使用示例

### 示例1：列出所有推荐策略
```
cd ./scripts && node list-recommended.js
```

### 示例2：获取指定策略最新持仓并分析N只个股（N默认为5）
```
1. 获取持仓（通过策略名称，支持模糊匹配）
cd ./scripts && node get-positions-correct.js "短周期机器学习" 20
脚本执行流程：
- 先在 strategy_information 表查找匹配的策略
- 获取对应的 strategy_table 名称
- 查询该表的最新持仓数据
2. 对每只个股调用公开信息搜索
3. 调用微信文章深度搜索，获取最新公众号深度研究报告
4. 融合公开信息与深度报告内容，整理分析结果，并注释引用的公众号文章标题
5. 输出完整报告，末尾注明信息来源并添加免责声明
```

## 完整运行示例（如本文档编写过程）
1. 用户要求："现在开始对前5只重仓个股进行深度分析"
2. 执行`node list-recommended.js`获取推荐策略列表
3. 执行`node get-positions-correct.js "策略名称" 20`获取最新20只持仓（脚本会自动反查strategy_table）
4. 逐个对前5只股票调用公开搜索获取基础基本面信息
5. 逐个对前5只股票调用微信文章深度搜索，获取最新公众号深度研究报告
6. 融合整合公开信息与深度报告内容，按照结构化分析框架整理输出分析报告
7. 在报告中注释引用的公众号文章/深度报告标题，并注明信息来源，最后添加免责声明

## 上架信息
- 作者：Warwick
- 分类：金融/量化选股
- 标签：A股, 量化, 选股, 基本面分析, 深度分析, 投资
- 版本：1.10.0
- 更新日志：
  - v1.10.0 (2026-07-24): 数据源架构重构--Tushare MCP 升为主数据源（覆盖行情/财务/资金流向/龙虎榜），原 new-akshare-stock 降为第一备用，baostock 为第二备用，东方财富API为兜底。新增数据校验铁律强调（严禁编造数据，失败必标注）。降级链路更新为4级：Tushare -> akshare -> baostock -> 东方财富API。依赖列表和工具调用规范同步更新。
  - v1.9.3 (2026-07-23): 新增陷阱#12（cronjob工具action='update'会覆盖prompt，绝对不要用来"查看"prompt，正确方式是read_file读取jobs.json）；新增 `references/concept-stock-analysis-workflow.md`（概念股/主题驱动产业链分析工作流，含超节点算力产业链实战案例，覆盖搜索->分层->采集->研判->持仓交叉分析6步法）。
  - v1.9.2 (2026-07-20): 新增陷阱#11（融资融券/北向资金akshare API参数陷阱）；功能2新增stock-research-sop深度分析模式选择说明，当用户要求"stock-research-sop"分析时引导加载quant-finance技能模板。
  - v1.9.1 (2026-07-13): `fintech-codebase-structure.md` 新增「基础设施与运维」章节（nginx/systemd/双数据库/Entity表名映射/API路由总览）和「调试指南」章节（排查流程+GORM MAX(date)反模式）。SKILL.md 新增陷阱#9（后端日志不在journalctl）和#10（GORM全局MAX(date)反模式），触发条件扩展覆盖网站bug排查。
  - v1.9.0 (2026-07-02): 仓位优化报告规范——`position-sizing-optimization.md` 新增第7节：详细报告撰写规范。用户明确要求"不要遗漏任何点"，报告须包含四大部分（回撤分析/直觉验证/单仓上限对比/方案D深度回测）、9个分析维度、市场温度计ASCII可视化、飞书文档上传步骤。退回简略报告并要求补充所有数据点，是用户偏好强信号。
  - v1.8.0 (2026-07-02): 仓位优化落地生产部署——`position-sizing-optimization.md` 新增第5-6节（生产部署代码+Git流程+优化后总结报告工作流）。SKILL.md 新增陷阱#8：仓位优化代码必须放在信号生成脚本中，禁止在fintech前后端展示层修改。
  - v1.6.0：全量新增双数据源自动降级（new-akshare-stock→baostock），所有分析维度统一兜底，报告强制标注数据来源，强制校验数据准确性。
  - v1.5.0 (2026-03-31): 将直接读取akshare接口更改为调用成熟skill；集成微信文章深度搜索机制，支持搜索公众号最新发布的个股深度研究报告，并融合深度内容进行分析，自动注释引用的报告名称，提供更丰富的市场观点和深度分析内容
  - v1.4.0 (2026-03-30): `get-positions-correct.js`脚本升级，支持通过策略名称（strategy_name_cn）自动反查strategy_table，无需手动指定表名，使用更便捷
  - v1.3.0 (2026-03-30): 主力资金数据获取升级为`akshare`接口，可直接获取准确的单日/近5日/近20日/近一月主力净流入数据，资金面分析数据更精准
  - v1.2.0 (2026-03-30): 行情数据获取方式升级为`akshare`接口，自动获取准确的最新股价和各周期涨跌幅数据，数据来源更稳定可靠
  - v1.1.0 (2026-03-28): 添加微信文章深度搜索机制，支持搜索公众号最新发布的个股深度研究报告，并融合深度内容进行分析，自动注释引用的报告名称

