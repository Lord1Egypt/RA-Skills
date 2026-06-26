---
name: qieman-mcp
description: 当用户需要查询基金、策略、公告、财经资讯，做资产配置、组合诊断、风险回测、现金流分析，或生成图表、PDF 时，优先使用本 Skill 获取真实数据与可执行能力。
license: MIT
---

# qieman-mcp

本 Skill 通过 `qieman-mcp-cli` npm 包连接且慢 MCP 服务，提供基金查询、策略分析、资产配置等金融数据与分析能力。

## 前置条件

执行任何 MCP 调用前，先执行 `qieman-mcp-cli config`，若命令不存在或输出中没有 apiKey，说明当前skill尚未初始化，必须先阅读并执行「[初始化工作流](references/初始化工作流.md)」完成环境初始化后再继续。

## 能力集合

### 调用工具

#### 调用工具的示例

调用任何工具前，必须先用 `describe` 获取完整 Schema，了解参数结构后再调用。

**示例1：无参数工具（GetCurrentTime）**

```bash
# 第一步：获取 Schema
qieman-mcp-cli describe GetCurrentTime

# 第二步：根据 Schema 调用（无需参数时传空对象）
qieman-mcp-cli call GetCurrentTime --input '{}'
```

**示例2：带参数工具（SearchFunds）**

```bash
# 第一步：获取 Schema，了解有哪些参数可用
qieman-mcp-cli describe SearchFunds

# 第二步：根据 Schema 构造参数并调用
qieman-mcp-cli call SearchFunds --input '{"keyword":"易方达蓝筹","size":3}'
```

**示例3：一次查看多个工具的 Schema**

```bash
qieman-mcp-cli describe BatchGetFundsDetail GetFundDiagnosis
```

> 也可以用 `--input-file <path>` 从文件读取 JSON 入参，适合参数较复杂的场景。

#### 工具列表

- AnalyzeAssetLiability AI专用资产负债分析接口，接收用户资产负债数据，进行全面分析并返回详细的资产负债分析结果，包含资产负债比率、净资产、各类资产和负债的详细分析报告
- AnalyzeCashFlow AI专用现金流分析接口，接收家庭现金流数据（包括当前可投资产、报酬率配置、家庭成员信息、持续性和一次性收支）作为输入，计算并返回详细的现金流分析结果，包括汇总信息、年度数据、HTML表格和数据解释提示。该接口专为大模型处理和展示现金流数据而设计。
- AnalyzeFamilyMembers AI专用家庭成员分析接口，接收家庭成员列表数据，返回详细的家庭成员分析结果。该接口可分析家庭总人数、成年人数、未成年人数及家庭所处生命周期阶段等信息，帮助进行家庭财务规划。
- AnalyzeFinancialIndicators AI专用财务指标分析接口，接收财务指标输入数据(总资产、总负债、流动性资产等)，计算7个关键财务指标(资产负债率、流动比率、融资比率等)，并提供每个指标的合理范围与状态评估
- AnalyzeFundRisk 基金风险分析接口，获取多个基金的风险评分及说明。该接口通过传入基金代码列表，返回每个基金的风险评分、R方值、残差方差、标准误差等风险指标，以及相应的风险描述文本。
- AnalyzeIncomeExpense AI专用收入支出分析接口，接收收入支出数据，返回详细的收入支出分析结果。该接口处理用户的年度收入和支出数据，计算总收入、总支出、年度结余及各收支项目的占比分析，同时提供月度必要性支出数据，用于财务规划和预算管理。
- AnalyzeInvestmentPerformance AI专用投资方案表现判断接口，接收投资方案配置数据，返回详细的投资方案表现分析结果。该接口分析投资方案的可行性，计算加权收益率，并生成配置方案权重分析，帮助用户评估投资策略是否符合预期。
- AnalyzePortfolioRisk 组合风险评估接口，计算组合的风险指标。该接口接收基金代码和权重信息，返回包含风险评分、R方、残差方差等多维度风险指标的分析结果。
- BatchGetFundNavHistory 批量返回基金历史净值，包括：单位净值、累计净值、日涨跌。
- BatchGetFundsDetail 返回基金的详细信息，包括基本概况（最新净值，规模，基准，风险等级，基金类型）、经理信息、业绩表现、持仓分析、资产配置、行业分布、净值历史、交易限制等完整数据。
- BatchGetFundsDividendRecord 提供基金代码列表，批量返回基金分红记录
- BatchGetFundsHolding 批量查询基金持仓情况。包括：十大重仓股、十大重仓债。
- BatchGetFundsSplitHistory 批量返回所有基金拆分记录，包括拆分日、拆分比例。
- BatchGetFundTradeLimit 批量获取基金交易限制信息，返回申购(allot)/认购(subscribe)/赎回/转换是否可用，以及起购金额、定投金额等；注意：认购不可用不等于申购不可用。
- BatchGetFundTradeRules 查询特定交易时间进行的基金交易操作包含的交易规则信息。支持申购、认购、赎回和转换等操作类型，返回包含最低/最高购买金额、预计确认日期、到账日期、收益产生日期、费率规则等详细交易规则数据。尽量提供精确的txnTime，无法确定可以询问用户。
- BatchGetPoTradeComposition 根据策略代码列表批量获取交易成分明细信息
- BatchGetStrategiesComposition 根据策略代码批量获取组合策略的当前持仓明细信息，包含各基金的持仓比例、净值信息、分类分组及最新调整情况等
- BatchGetStrategyRiskInfo 获取一批策略风险信息
- DiagnoseFundPortfolio 获取用户当前基金持仓的全面分析评估，包括资产配置状况、基金间相关性和历史回测表现。报告从风险分散度、资产类别分布和收益表现三个维度进行评分（1-5分）及诊断，并提供相应优化建议。
- filterBondFundByBondType 根据券种风格条件筛选符合条件的债券基金
- filterBondFundByCreditRating 根据信用评级条件筛选符合条件的基金
- filterStockFundByStockTurnover 根据股票换手率指标筛选基金
- fund-equity-position 获取基金的权益仓位数据，包括权益仓位值和权益仓位等级名称
- fund-recovery-ability 获取基金的回撤修复能力数据，根据近三年最长恢复天数排名确定修复水平
- fund-sector-preference 获取基金的板块配置偏好数据，包括基金主板块对应的行业名称和行业编号
- GetAnnouncementContent 获取特定基金公告的详细内容
- GetAssetAllocation 获取基金组合的资产配置分析结果，只需提供基金列表，只返回资产配置分析结果。该接口分析用户的资产配置情况，包括雷达图评分、诊断结果、资产大类配置详情及子账户资产配置分析
- GetAssetAllocationPlan 根据投资三性参数获取资产配置方案。提供预期年化收益率 or 预期最大回撤 or 预期投资期限，获得由盈米设计的资产配置方案，投资三性参数最少要传一个。
- GetBatchFundPerformance 批量返回基金业绩表现数据，包含业绩分析指标（收益能力、风险控制等）和阶段收益（近1月、近1年、成立以来等）的详细信息。支持一次查询多只基金的业绩对比，每次最多支持20只基金的查询。
- getBondAllocationByFundCode 获取指定债券型基金在指定时间区间下的券种配置和风格配置数据
- getBondFundCreditRatingLevel 获取指定基金在指定时间区间下的债券信用评级数据
- getBondFundWithAlertRecord 查询出现异动和跳水告警的债券型基金
- getBondIndicator 获取基金的债券相关指标数据，包括敏感性久期、杠杆水平、债券持仓集中度等
- GetCompositeModel 通过资产配置方案ID获取对应的复合模型，复合模型是资产配置方案的具体落地实现，提供每个大类资产对应的实际基金及其配置比例
- GetCurrentTime 获取当前时间。注意，模型AI你是不知道当前时间的，需要调用此工具获取当前时间。
- GetFundAnnouncements 查询基金的公告数据，包含基金代码、基金名称、基金全称、公告ID、公告日期、公告来源、公告标题、公告链接、公告类型，支持按时间范围、公告类型和标题关键词查询。
- GetFundAssetClassAnalysis 用户会提供基金代码和基金的持有金额，该工具会根据用户提供的基金持仓信息，穿透分析用户的总体持仓的资产大类分布情况
- getFundBenchmarkInfo 通过基金代码查询基金的业绩基准信息
- getFundBrinsonIndicator 获取基金股票收益归因（Brinson）数据，包括行业配置收益、选股收益和总超额收益
- getFundCampisiIndicator 获取基金债券收益归因（Campisi）数据，包括收入效应、国债效应、利差效应、券种选择效应和超额回报
- GetFundDiagnosis 获取基金的诊断信息，包括风险评价、估值、业绩指标、盈利概率、行业分布、资产配置
- getFundDiveCount 获取指定基金在指定时间段内的跳水次数和异动次数
- getFundIndustryAllocation 获取指定基金在指定时间区间下所有中信一级行业的行业配置比例、行业代码和行业名称
- getFundIndustryConcentration 获取指定基金在指定时间区间下前5大中信一级行业的独立集中度，以及前1、2、3、5大行业集中度加总的数据
- getFundIndustryPreference 获取指定基金在指定时间段内的行业偏好
- getFundIndustryReturns 获取指定基金在指定时间区间下每个一级行业的行业名称、绝对收益、相对收益、收益率、收益率得分
- GetFundRelatedStrategies 输入基金代码或基金名称，查询重仓该基金的投顾策略
- GetFundsBackTest 基于基金列表进行回测分析。只需提供基金列表，返回回测分析结果。该接口用于对给定基金组合进行回测分析，计算包括年化收益率、最大回撤、波动率、夏普比率等指标，并提供诊断结果和雷达图评分。
- GetFundsCorrelation 获取基金相关性分析结果。只需提供基金列表，只返回基金相关性分析结果。该接口分析多只基金之间的相关性系数，生成雷达图评分和诊断结果，帮助进行投资组合分析。
- getFundTurnoverRate 获取指定基金在指定时间区间下的换手率数据
- GetLatestQuotations 分析市场行情，进行行情解读，分析各市场当日收盘行情，市场温度计
- getMarketTimingIndicator 获取基金的择时相关指标数据，包括择时总胜率、择时贡献等
- GetPopularFund 返回近期访问数量前x的基金
- GetPortfolioNavHistory 组合历史净值，poManagerId、broker都不需要填。
- getQdFundAreaAllocation 获取指定QDII基金在指定时间区间下的地区配置比例数据
- getStockAllocationAndMetricsByFundCode 获取指定股票型基金的股票配置、估值盈利指标、财务指标和抱团股数据
- GetStrategyAssetClassAnalysis 获取策略持仓穿透后的资产大类分布情况
- GetStrategyBenchmark 根据策略代码获取策略的业绩基准信息
- GetStrategyDetails 组合策略详情查询，根据策略代码或名称获取组合策略的详细信息，包含策略基础信息、策略管理人信息、风险收益指标、历史业绩、资产配置情况、投资特点等。
- GetStrategyRiskInfo 获取某个策略的风险信息
- GetTxnDayRange 以某时间为中心获取一个时间段内的交易日。centerTime格式是YYYY-MM-DD HH:mm:ss，默认不填就是当前时间（建议大部分情况都不要填）
- GuessFundCode 根据基金名称匹配最相近的基金代码。
- MonteCarloSimulate 针对资产配置组合进行蒙特卡洛模拟计算（测算未来收益概率）。接收对象形式的资产权重配置，返回蒙特卡洛模拟结果。
- RenderEchart 根据提供的 ECharts 配置和尺寸参数，渲染图表并转换为图片，返回图片的 URL。
- RenderHtmlToPdf 将HTML内容转换为PDF文档，支持自定义页面格式、背景打印和页边距设置，并返回访问URL（可以使用markdown的链接语法显示这个URL供用户点击）
- SearchFinancialNews 根据关键词和时间范围搜索财经资讯内容，支持分页查询，返回符合条件的财经资讯列表，包括资讯标题、摘要、来源、链接及发布时间等信息。默认不需要提供date参数，除非用户明确要求。
- SearchFunds 搜索基金、根据基金名称匹配基金代码。通过名称（可用于确定基金代码）、代码、拼音、交易状态等信息进行搜索。同时可以按照收益、限额、费率等进行排序。
- SearchHotTopic 分析市场热点所在，聚焦大众关注、热度高的排行榜单内容。适用于：创作选题、视频脚本、营销文案创作等使用场景。当用户未指定关键词时，可不传keyword
- searchInvestAdvisorContent 搜索金融领域的文章、观点、话题和讨论内容，支持按关键词、基金组合、主理人/作者、时间范围和内容类型（文章、碎碎念、专栏、社区、策略内容等）进行筛选。
- SearchManagerViewpoint 根据时间范围和关键词搜索基金经理的行业观点及市场分析（如果用户问你对某个行业的看法，可以调用此工具进行参考）。支持按关键词匹配标题或内容，可筛选特定时间段内的观点，并提供分页功能。
- searchRealtimeAiAnalysis 根据时间范围、关键词搜索AI生成的实时资讯解读内容，支持分页查询
- StrategySearchByKeyword 根据关键词模糊搜索组合策略名称，返回匹配的组合策略信息列表。支持分页查询，可指定页码和每页记录数。工具结果里的「策略代码」可用于提供给其他工具作为入参使用。
