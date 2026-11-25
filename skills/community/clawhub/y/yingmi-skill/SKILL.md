---
name: yingmi-skill
description: 当用户需要查询基金、投顾策略、账户持仓、盈米代销私募、公告或财经资讯，做资产配置、组合诊断、风险回测、现金流分析，或生成图表、PDF 时，优先使用本 Skill 获取真实数据与可执行能力。
license: MIT
version: 0.2.1
---

# yingmi-skill

本 Skill 是且慢金融能力的本地公开入口：负责完成前置检查、判断该用 MCP 还是云端子 Skill，并提供统一 HTML 报告模板入口。它不承载各金融场景的完整执行细节；进入子 Skill 后，应以远端子 Skill 的 `SKILL.md` 为准。

## 1. 前置检查

首次安装或执行任何 MCP / remote-skill 调用前，必须完成：

1. 环境检查：确认 `node -v`、`git --version` 可正常执行；缺失时先引导用户安装。
2. 执行 [CLI前置检查工作流](references/CLI前置检查.md)，确认 `yingmi-skills-cli` 已安装、已更新且环境已初始化。
3. 执行 `scripts/check-upgrade.sh` 检查 Skill 更新。

## 2. 决策原则：MCP 还是子 Skill

一句话判断：**MCP 是原子工具，云端子 Skill 是场景工作流。**

优先用 MCP：

- 用户只要一个明确数据点、指标、详情或单次输出。
- 用户已给出完整参数，不需要固定分析流程。
- 任务可以由一个或少量工具直接完成。

优先进入云端子 Skill：

- 用户要“分析、诊断、规划、评估、生成报告”。
- 任务需要多步编排、业务约束、固定章节或统一交付物。
- 用户明确指定了某个子 Skill 或明显命中下方场景清单。

补充规则：

- 已进入子 Skill 后，如仍需真实数据，继续按 MCP 的 `list -> schema -> call` 规则取数。
- 子 Skill 的章节、流程、字段、表格、图表和结论边界，全部以远端子 Skill 的 `SKILL.md` 为准。
- 只交付单张图表时使用 MCP 的图表工具，不必套完整报告壳。完整报告页仍遵守第 5 节统一 HTML 模板。具体格式以远端子 Skill 的 `SKILL.md` 为准。

## 3. MCP 原子能力

使用流程：

```bash
# 1. 查看工具列表
yingmi-skills-cli mcp list

# 2. 查看目标工具入参 Schema
yingmi-skills-cli mcp schema <toolName>

# 3. 按 Schema 调用工具
yingmi-skills-cli mcp call <toolName> --input '<json>'
```

常见示例：

```bash
yingmi-skills-cli mcp schema GetCurrentTime
yingmi-skills-cli mcp call GetCurrentTime --input '{}'

yingmi-skills-cli mcp schema SearchFunds
yingmi-skills-cli mcp call SearchFunds --input '{"keyword":"易方达蓝筹","size":3}'

yingmi-skills-cli mcp schema BatchGetFundsDetail GetFundDiagnosis GetFundsBackTest
```

能力分组仅用于快速路由；完整工具列表以 `yingmi-skills-cli mcp list` 的实时输出为准。

| 能力分组 | 什么时候使用 | 常用工具 |
| --- | --- | --- |
| 基础时间能力 | 当前时间，或以当前时间为中心的交易日范围 | `GetCurrentTime`、`GetTxnDayRange` |
| 基金检索与资料 | 按名称、代码或拼音搜基金并确认代码，查详情、交易限制、指定时点的交易规则、分红和拆分。热门基金按详情页打开人数，不是销量榜或收益榜 | `SearchFunds`、`GuessFundCode`、`BatchGetFundsDetail`、`GetPopularFund`、`BatchGetFundTradeLimit`、`BatchGetFundTradeRules`、`BatchGetFundsDividendRecord`、`BatchGetFundsSplitHistory` |
| 单只基金分析 | 业绩、风险、净值、归因、行业与风格、择时、权益仓位、债基券种与评级、QDII 地区配置 | `GetFundDiagnosis`、`AnalyzeFundRisk`、`GetBatchFundPerformance`、`BatchGetFundNavHistory`、`getFundBenchmarkInfo`、`getFundBrinsonIndicator`、`getFundCampisiIndicator`、`getFundIndustryAllocation`、`getFundIndustryConcentration`、`getFundIndustryPreference`、`getFundIndustryReturns`、`getFundTurnoverRate`、`fund-equity-position`、`fund-recovery-ability`、`fund-sector-preference`、`getMarketTimingIndicator`、`getStockAllocationAndMetricsByFundCode`、`getQdFundAreaAllocation`、`getBondAllocationByFundCode`、`getBondFundCreditRatingLevel`、`getBondIndicator`、`getFundDiveCount` |
| 组合分析 | 多只基金的相关性、回测、组合风险、资产配置穿透、历史净值和未来收益概率 | `GetFundsCorrelation`、`GetFundsBackTest`、`DiagnoseFundPortfolio`、`AnalyzePortfolioRisk`、`GetAssetAllocation`、`GetFundAssetClassAnalysis`、`MonteCarloSimulate`、`GetPortfolioNavHistory` |
| 投顾策略 | 搜策略，查详情、基准、风险、持仓、调仓、收费模式和组合交易规则，或查重仓某基金的策略 | `StrategySearchByKeyword`、`GetStrategyDetails`、`GetStrategyBenchmark`、`BatchGetStrategyRiskInfo`、`BatchGetStrategiesComposition`、`BatchGetPoTradeComposition`、`GetStrategyAssetClassAnalysis`、`GetStrategyAdjustments`、`GetAdvisorChargeFeeModel`、`GetPomodelTradeRule`、`GetFundRelatedStrategies` |
| 财富规划与资产配置 | 家庭成员、收支、资产负债、现金流、财务指标，以及按收益、回撤或期限获取配置方案和对应的复合模型 | `AnalyzeFamilyMembers`、`AnalyzeIncomeExpense`、`AnalyzeAssetLiability`、`AnalyzeCashFlow`、`AnalyzeFinancialIndicators`、`GetAssetAllocationPlan`、`GetCompositeModel`、`AnalyzeInvestmentPerformance` |
| 基金筛选与排雷 | 按券种、信用评级或股票换手率筛选基金，或查询出现异动和跳水告警的债基 | `filterBondFundByBondType`、`filterBondFundByCreditRating`、`filterStockFundByStockTurnover`、`getBondFundWithAlertRecord` |
| 市场资讯与素材 | 当日收盘行情与市场温度、财经资讯、热点、基金经理观点、投顾内容和实时解读 | `GetLatestQuotations`、`SearchFinancialNews`、`SearchHotTopic`、`SearchManagerViewpoint`、`searchInvestAdvisorContent`、`searchRealtimeAiAnalysis` |
| 用户账户与持仓 | 当前登录用户的账户结构、持仓产品、资产与净值曲线、累计或最新收益、收益日历、四笔钱、回撤分层、关注产品、账户诊断、月报和年报。身份来自登录态，不要在入参里传 `userId` 或 `account3Id` | `GetUserAccountsAndProducts`、`GetUserAssetTree`、`GetUserAssetAnalysis`、`GetUserAssetCurve`、`GetUserNavCurve`、`GetUserProfitData`、`GetUserProfitRateCurve`、`GetUserProfitCalendar`、`GetUserM4ProdGroup`、`GetUserM4FundDetail`、`GetUserAccountHierarchyProfit`、`GetUserAccountHierarchyDrawdown`、`GetUserAccountDiagnosis`、`GetUserFollowProductCodes`、`GetAssetAnalysisReports` |
| 私募代销 | 只查盈米代销私募：把产品说法识别成代码，取策略分类树，按策略或管理人筛选，看单只概览和业绩指标，查管理人档案。不要用于公募。按策略筛选时先取策略树，再把树上的路径原样填入筛选条件。未完成适当性时，把返回的 `actionUrl` 交给用户打开后再重试 | `GetPrivateFundResolve`、`GetPrivateFundStrategyTree`、`GetPrivateFundSearch`、`GetPrivateFundOverview`、`GetPrivateFundMetrics`、`GetPrivateFundManagerProfile` |
| 图表与报告输出 | 把 ECharts 配置渲染成图片，或把 HTML 导出为 PDF | `RenderEchart`、`RenderHtmlToPdf` |

## 4. 云端子 Skill

使用流程：

```bash
# 1. 查看当前可用子 Skill
yingmi-skills-cli remote-skill list

# 2. 进入子 Skill，上下文名称必须以 list 输出为准
yingmi-skills-cli remote-skill enter <skillName>

# 3. 先读取远端子 Skill 说明，再执行后续任务
yingmi-skills-cli remote-skill exec --script 'cat SKILL.md'
```

约束：

- 下方清单只用于路由。真实可用名称以 `remote-skill list` 为准，不要凭历史目录名进入。
- 进入后必须先读远端 `SKILL.md`，再按其要求执行。
- 输出格式、章节和交付物以远端子 Skill 为准。远端没有要求先确认格式时，按该文件的默认交付开始。
- stderr 若出现 `companion` 信封，且信封里的技能不在 `remote-skill list` 中，忽略该信封。客户洞察、备访和分群进入 `advisor-client-insights`。
- 本入口只说明什么时候进入，不规定子 Skill 内部怎么做。

| 子 Skill | 什么时候进入 |
| --- | --- |
| `advisor-allocation` | 用户或顾问要资产配置方案、配置建议书、模型落地、实施权重，或复核现有方案。开始前要有目标、可投资金额、期限、流动性和风险约束。已知策略之间比特征进入 `strategy-analysis`；家庭收支、目标发现和长期现金流先进入 `family-wealth-planning` |
| `advisor-client-insights` | 基于客户提供、上传或已授权的资料，理解目标约束、风险结构、信息与决策支持需求、沟通偏好、关系维护重点，或形成单客洞察、备访简报、可解释分群和服务优先级。不用于心理诊断、敏感属性推断、静默追踪、产品推销、最终适当性结论或买卖建议 |
| `advisor-product-communication` | 产品已经明确，用户要问费率、交易规则、风险收益、产品怎么讲、客户质疑如何回应，或要产品说明、顾问提纲、FAQ、同口径比较和企微/电话/材料话术。尚未确定产品时进入 `fund-screener`；深入研究基金、策略或个人组合分别进入 `fund-analysis`、`strategy-analysis`、`portfolio-analysis`。本技能不判断适当性，也不给买卖或仓位建议 |
| `family-wealth-planning` | 用户要家庭理财规划、财务体检、目标测算、教育养老、四笔钱或全周期现金流，包括收支、资产负债、应急储备、保障责任、目标与规划路线。具体大类配置和基金/策略落地进入 `advisor-allocation`。个人账户实时持仓与收益查询进入 `personal-holdings-analysis` |
| `fund-analysis` | 用户给出一只或多只公募基金的名称或代码，要问“怎么样”，或要快速了解、深度研究、业绩风险、持仓风格、基金经理、收益归因、比较。按条件筛选进入 `fund-screener`；只问费率与交易规则进入 `advisor-product-communication`；投顾策略进入 `strategy-analysis`；盈米代销私募进入 `private-fund-analysis`；本人且慢账户持仓进入 `personal-holdings-analysis` |
| `market-analysis` | 用户问今天市场怎么样、为何涨跌、近期重要事件、行业或主题前景、市场观点汇总，或要早报、收盘复盘、周度总结。已有底稿的渠道改写进入 `advisor-content-studio`。个人账户、具体基金组合和个性化买卖决策不在本技能 |
| `portfolio-analysis` | 用户给出两只及以上基金的名称或代码，以及金额或权重，或给出六大类资产组合，要看搭配、体检、集中度、穿透、相关性、回测、风险、未来情景、组合比较或改善方向。单基金研究进入 `fund-analysis`；公开策略进入 `strategy-analysis`；家庭规划进入 `family-wealth-planning`；目标配置生成进入 `advisor-allocation`；本人且慢账户实盘持仓进入 `personal-holdings-analysis`；盈米代销私募产品研究进入 `private-fund-analysis` |
| `strategy-analysis` | 用户给出公开投顾策略名称或代码，要问“怎么样”，或要深度/专项分析、策略比较、已知候选的适用比较，或查询包含某只基金的策略。当前列表没有全市场策略筛选技能，未点名策略时只分析用户给出的候选。目标与约束明确后的资金桶和配置权重进入 `advisor-allocation`；家庭收支和长期现金流进入 `family-wealth-planning`；单基金研究进入 `fund-analysis`；盈米代销私募进入 `private-fund-analysis` |
| `advisor-content-studio` | 用户要选题、素材包、内容策划、编辑成稿、投教表达、波动沟通、公众号/企微/短视频/演讲改写、通用顾问话术，或 HTML/PDF 内容交付。市场、基金和策略研究仍进入对应分析技能；本技能不决定推荐、适当性或买卖 |
| `fund-screener` | 用户要按类型、收益风险、规模费率、持仓风格、信用券种、交易条件或热度找基金、筛几只、看热门基金，或排查债基异动。输出条件型候选。已指定基金的深度分析与比较进入 `fund-analysis`；组合搭配进入 `portfolio-analysis`；投顾策略进入 `strategy-analysis`；盈米代销私募筛选进入 `private-fund-analysis` |
| `private-fund-analysis` | 用户要查一只盈米代销私募怎么样、按私募策略筛产品、比较已知私募的区间收益与回撤，或查询私募管理人备案、规模和人员。公募基金进入 `fund-analysis` 或 `fund-screener`；公开投顾策略进入 `strategy-analysis`；用户手工给出的基金篮子进入 `portfolio-analysis`；当前登录账户里的私募市值和实际盈亏进入 `personal-holdings-analysis`。非盈米代销私募和全市场私募排名不在本技能。适当性未完成时先停下 |
| `personal-holdings-analysis` | 用户问「我的且慢持仓」「这个账户赚了多少」「我的账户回撤或收益率走势」，或要看当前授权用户本人账户的资产分布和持仓风险诊断。用户手工给出代码、金额或权重进入 `portfolio-analysis`；公开基金季报持仓进入 `fund-analysis`；公开投顾策略持仓进入 `strategy-analysis`；代销私募产品档案进入 `private-fund-analysis`。他人或家庭成员账户不在本技能，已授权资料可转 `advisor-client-insights` |

### 相邻任务怎么分流

| 用户说法 | 进入 |
| --- | --- |
| 指定基金怎么样、经理、回撤、归因、多只基金比较 | `fund-analysis` |
| 按条件筛基金、推荐候选、热门基金、债基异动 | `fund-screener` |
| 已明确产品的费率、能不能买、确认到账、怎么跟客户讲、客户质疑 | `advisor-product-communication` |
| 两只以上基金带金额或权重，或六大类组合的体检、回测、未来情景 | `portfolio-analysis` |
| 已点名的投顾策略怎么样、策略对比、某基金在哪些策略里 | `strategy-analysis` |
| 今天市场、涨跌原因、早报、收盘复盘、行业或主题 | `market-analysis` |
| 已有底稿要改写成内容，或选题、投教、波动沟通 | `advisor-content-studio` |
| 家庭规划、财务体检、目标测算、四笔钱、现金流 | `family-wealth-planning` |
| 配置方案、实施权重、模型落地、复核现有方案 | `advisor-allocation` |
| 单客洞察、备访、客户分群、服务优先级 | `advisor-client-insights` |
| 盈米代销私募怎么样、按私募策略筛选、已知私募区间比较、管理人备案 | `private-fund-analysis` |
| 我的且慢持仓、账户实际收益、账户回撤、本人持仓诊断 | `personal-holdings-analysis` |

### 配置方案与家庭规划

话术里同时出现「资产配置」和「规划」时，先看用户要交付的是配置方案，还是家庭收支与目标。

| 用户说法 | 进入 |
| --- | --- |
| 资产配置方案、配置建议书、给客户出方案、实施权重、复核现有配置 | `advisor-allocation` |
| 家庭理财规划、收支、资产负债、财务体检、教育养老、四笔钱、现金流 | `family-wealth-planning` |
| 先看家计是否可行，再给可投资金做配置 | 先 `family-wealth-planning`，约束明确后再 `advisor-allocation` |
| 只说「出一个配置方案」，还没有目标、金额、期限或风险约束 | 先补齐这些约束，然后进入 `advisor-allocation`。同时提到收支或资产负债时进入 `family-wealth-planning` |
| 已知几只策略，要比较策略本身 | `strategy-analysis` |

仍分不清时，只问一句：

> 您要的是给客户的资产配置方案（目标、金额、期限、风险约束和落地），还是家庭理财规划（收支、资产负债、目标和现金流）？

| 用户回复 | 进入 |
| --- | --- |
| 方案 / 配置 / 给客户交付 | `advisor-allocation` |
| 家计 / 收支 / 体检 / 目标测算 / 现金流 | `family-wealth-planning` |
| 未回复，且原话只是「资产配置方案」 | `advisor-allocation` |

### 客户洞察与持仓

| 用户说法 | 进入 |
| --- | --- |
| 备访、了解这位客户、这批客户怎么分群、先联系谁 | `advisor-client-insights` |
| 用户手工给出基金代码和金额或权重，要诊断组合、回测或看未来情景 | `portfolio-analysis` |
| 我的且慢持仓、这个账户赚了多少、账户回撤或收益率走势、本人持仓诊断 | `personal-holdings-analysis` |
| 盈米代销私募档案、按私募策略筛选、私募管理人 | `private-fund-analysis` |
| 账户里的私募赚了多少，同时要看这只私募产品本身 | 持仓盈亏进入 `personal-holdings-analysis`；产品档案和区间风险进入 `private-fund-analysis` |
| 先了解客户，再给配置或规划 | 先 `advisor-client-insights` 整理已确认约束，再按任务进入 `family-wealth-planning` 或 `advisor-allocation` |

## 5. 统一 HTML 报告模板

生成完整 HTML 报告页时，必须使用下列公共 references（子 Skill 的 `SKILL.md` 可再列场景补充项）：

| 文档 | 用途 |
| --- | --- |
| [输出格式确认协议.md](references/输出格式确认协议.md) | 仅当远端 `SKILL.md` 引用本协议时，才使用其中的询问话术、时机和三种格式路径 |
| [报告编排与交付公约.md](references/报告编排与交付公约.md) | 编排/交付边界、呈现 §6、各场景免责 §7 |
| [HTML视觉模板.md](references/HTML视觉模板.md) | 壳层、Hero、AI 卡、章节序号、HTML 交付铁律 |
| [demo-report.html](references/demo-report.html) | CSS/JS/DOM 唯一真源 |
| [MCP数据真实性零容忍.md](references/MCP数据真实性零容忍.md) | 数据溯源、交付物禁显接口名 |
| [HTML报告PDF导出规范.md](references/HTML报告PDF导出规范.md) | PDF / 打印 / 下载 |

执行顺序：

0. 先读远端 `SKILL.md`。只有它要求确认输出格式并引用本协议时，才执行 [输出格式确认协议.md](references/输出格式确认协议.md)。确认为 Markdown 时，本节后续步骤全部跳过。远端未要求确认时，不要先弹出 A/B/C。
1. 读取当前场景远端 `SKILL.md` 及其任务相关 `references/*`，确定报告内容、章节、字段和图表。
2. 读取 `demo-report.html` 全文，复用其视觉壳、整段 `<style>`、class、`report-header`、水印、主题切换脚本等。
3. 内容以场景 Skill 为准，视觉壳以 `demo-report.html` 为准。
4. 若 HTML 含 ECharts，交付前必须运行 `python scripts/inline_echarts.py --html <交付.html>`，再用 `--check-only` 复检；交付文件禁止保留 CDN 或本地路径依赖。

禁止：远端要求确认格式时，未确认就生成 HTML；未读模板即输出 HTML；照抄 demo 占位内容；自造整页 CSS / class；删除水印、顶栏图标或主题切换。
