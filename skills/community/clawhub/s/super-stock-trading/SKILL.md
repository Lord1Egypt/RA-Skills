---
name: super-stock-trading
version: 1.1.0
author: super-stock-trading-team
license: MIT
language: zh-CN
market: A-Share
tags:
  - stock-trading
  - a-share
  - portfolio-management
  - risk-control
  - chinese-stock-market
  - pre-market-analysis
  - post-market-review
  - stock-picking
  - short-line-tactics
  - limit-up-sniper
  - intraday-trading
description: |
  超级股票操盘 Skill —— 面向 A 股个人投资者的全流程操盘智能体 Skill 包。整合 137 个细粒度 Skills 与 31 位数字人专家，并内置《短线金手》七册实战战法体系（私募盈利系统/经典形态/涨停狙击/急速拉升/分时图/T+0/K线精通），覆盖盘前分析、盘中决策、盘后复盘、选股、持仓体检、月度组合管理等完整投资闭环。

  何时使用本 Skill：当用户提到「股票操盘」「盘前分析」「盘后复盘」「选股」「持仓体检」「月度组合管理」「仓位管理」「止损止盈」「板块轮动」「题材挖掘」「龙头战法」「财报季」「公告解读」「资金面」「北向资金」「龙虎榜」「风险体检」「组合再平衡」「定投」「指数基金」「期权对冲」「产业链」「护城河」「估值」「黑马」「打板」「异动」等关键词，或提到「短线」「涨停」「集合竞价」「分时图」「T+0」「主力吸筹」「仙人指路」「黄金十字」「梅开二度」「大长腿」「黄金分割」「急速拉升」等短线战术关键词，或需要系统性地完成 A 股投研—交易—风控—复盘工作时，应启用本 Skill。

  能力边界：主要服务于 A 股（沪深京）及与之相关的港股通、ETF、可转债、期权等品种的研究与决策辅助；不提供直接下单通道，所有交易建议均需用户人工二次确认；不构成任何投资建议，最终决策与盈亏由用户自行承担。
---

# 超级股票操盘 Skill（super-stock-trading）

> 本文件是整个 Skill 包的入口。日常时间表、事件触发规则、专家调度映射、风控规则等核心编排逻辑均在此声明；细粒度 Skills 与数字人专家的完整注册表见 `references/` 目录，配置项见 `config.json`。

## 一、系统架构

本 Skill 采用四层架构，自下而上依次为：**数据层 → Skill 层 → 专家层 → 编排层**。每一层职责单一、可独立替换，便于数据源切换与能力扩展。

```
┌─────────────────────────────────────────────────────────────┐
│                       编排层 (Orchestrator)                  │
│   日常时间表 · 事件触发 · 专家调度 · 风控闸门 · 任务编排       │
├─────────────────────────────────────────────────────────────┤
│                       专家层 (Experts)                       │
│   31 位数字人专家：价值投资 / 技术操盘 / 产业链 / 宏观 / 量化 / 短线战术 │
├─────────────────────────────────────────────────────────────┤
│                       Skill 层 (Skills)                      │
│   137 个细粒度 Skill：市场分析 / 资金面 / 选股 / 财报 / 交易 / 短线战法 │
├─────────────────────────────────────────────────────────────┤
│                       数据层 (Data)                           │
│   akshare · wind_aifin_market · tushare · 公告/资讯/社区      │
└─────────────────────────────────────────────────────────────┘
```

### 1. 数据层（Data Layer）
- **akshare**：开源金融数据接口，覆盖行情、资金流、龙虎榜、财报、宏观等，作为默认主数据源，无需 Key。
- **wind_aifin_market**：Wind 终端行情与资讯接口，用于高质量盘口、深度资金与研报数据，需 API Key（在 `config.json` 中配置）。
- **tushare**：Pro 版接口，补充财务三大表、分红送转、指数成分等结构化数据，需 Token。
- **辅助数据**：交易所公告、财经资讯 RSS、社区情绪（雪球/东财股吧）、Serenity 产业链图谱。
- 所有数据源在 `config.json` 中统一配置，支持按字段路由与降级（主源失败自动切备源）。

### 2. Skill 层（Skill Layer）
共 137 个细粒度 Skill，按 16 大类组织（详见 `references/skills_registry.json`），其中第 16 类「短线战法」沉淀自《短线金手》七册，主攻短线/超短线决策：

| 分类 | 数量 | 说明 |
|------|------|------|
| GitHub 开源 | 18 | 社区开源操盘/选股/分析仓库，作为能力底座 |
| Serenity 产业链 | 4 | 产业链图谱与价值链分布分析 |
| 市场分析 | 11 | 大盘趋势、情绪、广度、轮动 |
| 资金面 | 6 | 主力资金、机构、北向、融资融券 |
| 题材产业链 | 12 | 题材热度、龙头、持续性、轮动 |
| 选股 | 11 | 多因子、技术、基本面、主题选股 |
| 个股研究 | 10 | 股东、业务、护城河、同业对比 |
| 估值财务 | 5 | 多模型估值、财报健康、杜邦分析 |
| 财报 | 9 | 财报日历、解析、超预期、质量 |
| 公告事件 | 8 | 公告监控、并购、增减持、分红 |
| 交易执行 | 11 | 下单、仓位、止损、再平衡、日志 |
| 日常盘面 | 8 | 集合竞价、盘中轮动、收盘、情绪 |
| 周期风控 | 2 | 周期定位、组合风险监控 |
| 社区 | 1 | 社区情绪聚合 |
| 辅助 | 1 | 知识库助手 |
| 短线战法 | 20 | 沉淀自《短线金手》七册：私募盈利系统、经典形态、涨停狙击、急速拉升、分时图、T+0、K线精通 |

每个 Skill 声明 `tier`（T1 核心 / T2 高频 / T3 按需 / T4 辅助）、`data_source`、`trigger` 触发条件，供编排层按需调用。

### 3. 专家层（Experts Layer）
31 位数字人专家（详见 `references/experts_registry.json`），每位绑定一个核心能力域与若干触发场景；其中「短线战术派」为本次升级新增，专司短线攻击决策：
- **价值派**：沃伦·巴菲特、查理·芒格、海榕君
- **技术派**：王开、赵哲、魏嵬猫哥
- **产业链派**：Serenity白毛股神、焦娟、吴立
- **宏观策略派**：刘高畅、陶川、陈洪斌、宏观经济学家
- **量化风控派**：塔勒布、聂方义、策略分析师
- **配置理财派**：纳瓦尔、望京博格、基金研究员、杨业伟、银行理财专家、保险专家
- **另类**：黄金研究专家、外汇研究员、i小万、魏亚妮
- **短线战术派**：吴国平、陈旭、王炳洁、曹芝烨、杨涛

专家之间通过编排层进行「圆桌讨论」，输出可被风控闸门校验的结论。

### 4. 编排层（Orchestrator Layer）
负责：日常时间表调度、事件触发、专家↔Skill 映射、风控闸门、任务编排与日志。核心机制：
- **时间表驱动**：按交易时段自动推进工作流（见第二节）。
- **事件驱动**：重大事件（政策/公告/异动）触发对应专家与 Skill（见第三节）。
- **风控前置**：任何交易动作在执行前必须通过 7 条风控规则校验（见第五节）。
- **日志归档**：所有决策与交易记录写入 `reports/` 并由 `knowledge-base-assistant` 归档。

---

## 二、日常时间表

### 盘前 07:00 – 09:15

| 时段 | 动作 | 调用 Skill | 调度专家 |
|------|------|-----------|---------|
| 07:00–07:30 | 隔夜要闻与外盘复盘 | market-overview-skill / market-news-hot-monitor | 宏观经济学家、外汇研究员 |
| 07:30–08:00 | 公告与事件扫描 | announcement-monitor-skill / major-announcement-parsing | 魏亚妮、聂方义 |
| 08:00–08:30 | 持仓体检与风险扫描 | portfolio-risk-monitor / valuation-multi-model-skill | 沃伦·巴菲特、塔勒布 |
| 08:30–09:00 | 当日策略与重点标的 | index-trend-analysis / capital-flow-intraday | 刘高畅、陶川 |
| 09:00–09:15 | 集合竞价准备 | opening-auction-analysis / real-time-hot-plate | 王开、赵哲 |

### 盘中 09:30 – 15:00

| 时段 | 动作 | 调用 Skill | 调度专家 |
|------|------|-----------|---------|
| 09:30–10:30 | 开盘强度与情绪 | intraday-rotation-monitor / market-sentiment-thermometer | 赵哲、魏嵬猫哥 |
| 10:30–11:30 | 资金面与题材轮动 | main-force-capital-detection / theme-heatmap-skill | Serenity白毛股神、海榕君 |
| 11:30–13:00 | 午间复盘 | daily-market-summary / volume-energy-analysis | 策略分析师 |
| 13:00–14:00 | 午后题材深化 | dragon-stock-identification / concept-sector-strength | 焦娟、吴立 |
| 14:00–14:57 | 尾盘决策与减仓 | closing-session-review / position-exit-strategy | 王开、塔勒布 |
| 14:57–15:00 | 收盘集合竞价 | order-routing-skill / slippage-analysis | 王开 |
| 09:15–09:25 | 短线战机扫描（集合竞价巨量高开/量比涨幅前排） | limit-up-collection-auction / intraday-chart-pankou | 吴国平、陈旭 |

### 盘后 15:00 – 22:00

| 时段 | 动作 | 调用 Skill | 调度专家 |
|------|------|-----------|---------|
| 15:00–16:00 | 收盘总结与盈亏 | daily-market-summary / trade-journal-logger | 策略分析师 |
| 16:00–18:00 | 龙虎榜与资金复盘 | dragon-tiger-list-analysis / northbound-flow-analysis | 海榕君、基金研究员 |
| 18:00–20:00 | 公告与财报解读 | earnings-report-parsing / major-announcement-parsing | 魏亚妮、焦娟 |
| 20:00–22:00 | 个股深度与次日计划 | stock-deep-research / trading-plan-generator | 沃伦·巴菲特、查理·芒格 |

### 周末

| 动作 | 调用 Skill | 调度专家 |
|------|-----------|---------|
| 周度持仓体检 | portfolio-risk-monitor / valuation-peer-comparison | 沃伦·巴菲特、海榕君 |
| 行业与题材梳理 | industry-chain-mapping / theme-correlation-analysis | Serenity白毛股神、吴立 |
| 选股池更新 | multi-factor-stock-screening / watchlist-monitoring | 查理·芒格、望京博格 |
| 复盘日志归档 | trade-journal-logger / knowledge-base-assistant | 策略分析师 |

### 月末

| 动作 | 调用 Skill | 调度专家 |
|------|-----------|---------|
| 月度组合再平衡 | portfolio-rebalance-skill / cycle-position-assessment | 策略分析师、纳瓦尔 |
| 资产配置审视 | valuation-multi-model-skill / fixed-income-analysis | 望京博格、杨业伟 |
| 风险预算重设 | portfolio-risk-monitor / position-sizing-calculator | 塔勒布、聂方义 |
| 理财与保障检视 | bank-wealth-advisor / insurance-advisor | 银行理财专家、保险专家 |

---

## 三、事件触发规则

以下事件将中断或补充常规时间表，立即调度对应专家与 Skill：

| 事件类型 | 触发条件 | 调用 Skill | 调度专家 | 优先级 |
|---------|---------|-----------|---------|-------|
| 重大政策 | 央行/证监会/国常会公告 | policy-driven-theme-analysis | 陶川、陈洪斌 | 高 |
| 个股异动 | 自选股 ±7% 或量比>5 | capital-flow-stock-level / intraday-trade-signal | 王开、赵哲 | 高 |
| 临时停复牌 | 交易所停复牌公告 | announcement-monitor-skill | 魏亚妮 | 高 |
| 财报披露 | 业绩预告/快报/正式报告 | earnings-report-parsing / earnings-surprise-analysis | 魏亚妮、沃伦·巴菲特 | 高 |
| 重大公告 | 并购/增减持/分红/股权 | major-announcement-parsing / equity-event-tracker | 聂方义、海榕君 | 高 |
| 龙虎榜上榜 | 自选股或关注题材上榜 | dragon-tiger-list-analysis | 海榕君 | 中 |
| 北向异动 | 单日净流入/流出超阈值 | northbound-flow-analysis | 基金研究员 | 中 |
| 题材爆发 | 新题材热度>阈值 | new-theme-discovery / theme-sustainment-scoring | Serenity白毛股神、焦娟 | 中 |
| 黑天鹅 | 系统性风险信号 | portfolio-risk-monitor | 塔勒布、策略分析师 | 高 |
| 短线战机 | 自选股出现仙人指路/黄金十字/梅开二度/巨量高开/涨停基因等形态 | limit-up-collection-auction / intraday-chart-pankou / classic-pattern-* | 吴国平、陈旭 | 中 |
| 社区情绪极值 | 看多/看空情绪偏离 | community-sentiment-aggregator | i小万 | 低 |

---

## 四、专家调度映射

编排层根据任务类型选择主专家，并可召集辅助专家进行「圆桌」讨论：

| 任务类型 | 主专家 | 辅助专家 |
|---------|-------|---------|
| 价值选股 | 沃伦·巴菲特 | 查理·芒格、海榕君 |
| 短线交易 | 王开 | 赵哲、魏嵬猫哥 |
| 产业链挖掘 | Serenity白毛股神 | 焦娟、吴立 |
| 大盘趋势 | 刘高畅 | 陶川、陈洪斌 |
| 风险控制 | 塔勒布 | 聂方义、策略分析师 |
| 组合管理 | 策略分析师 | 纳瓦尔、望京博格 |
| 个股深度 | 魏亚妮 | 沃伦·巴菲特、查理·芒格 |
| 财报解读 | 魏亚妮 | 沃伦·巴菲特、海榕君 |
| 公告事件 | 聂方义 | 魏亚妮、海榕君 |
| 资金面 | 海榕君 | 基金研究员、i小万 |
| 题材情绪 | 赵哲 | 焦娟、i小万 |
| 宏观政策 | 陶川 | 陈洪斌、宏观经济学家 |
| 固收理财 | 杨业伟 | 望京博格、银行理财专家 |
| 贵金属/外汇 | 黄金研究专家 | 外汇研究员 |
| 短线战术 | 吴国平 | 陈旭、王炳洁、曹芝烨、杨涛 |
| 保障配置 | 保险专家 | 银行理财专家 |

---

## 五、风控规则（7 条）

> 完整规则见 `references/risk_rules.md`。任何交易动作执行前必须通过下列闸门；任一规则触发即阻断或调整动作。

1. **个股止损**：单只标的浮亏达 −5%（默认，可在 `config.json` 调整）即触发止损评估，强制生成减仓/清仓建议。
2. **组合止损**：账户整体回撤达 −8% 即触发组合级降仓，权益仓位上限临时下调一档。
3. **单只仓位上限**：任一标的持仓市值占比不得超过 30%，超限触发再平衡提醒。
4. **单行业集中度**：任一行业（申万一级）合计仓位不得超过 50%，超限触发分散化提醒。
5. **黑天鹅熔断**：检测到系统性风险信号（如千股跌停、流动性骤缩）即触发风控熔断，暂停新开仓并启动对冲评估。
6. **事件前置审查**：重大公告/异动发生后 30 分钟内，对应标的禁止新增仓位，须先完成事件评估。
7. **流动性约束**：单笔委托量不得超过该标的近 20 日均量的 10%，避免冲击成本与流动性陷阱。

---

## 六、短线战法体系（短线金手丛书）

> 详细战术手册见 `references/short_line_mastery.md`（已沉淀《短线金手》七册实战战法，作者吴国平主编，企业管理出版社 2019）。本体系是 Skill 层与专家层的**短线攻击补充**，与原有价值/产业链/宏观体系并行，主攻 1~20 个交易日及日内/T+1 短线决策。

### 1. 七大战术域与映射

| 战术域 | 来源册 | 在 Skill/专家层的落点 |
|--------|--------|----------------------|
| 私募盈利系统（总纲） | 书1 | 主力追踪（龙虎榜/F10）、K线语言、分时盘口、止损体系 → 专家层"短线战术派" + Skill 层"短线战法"类 |
| 经典形态战法 | 书2 | 11 式中长线/波段形态（旭日东升/梅开二度/黄金十字/20天线/布林等）→ `short_line_mastery.md` §二 |
| 涨停狙击战法 | 书3 | 58 式涨停 → §三（六大类） |
| 急速拉升战法 | 书4 | 92 案例主升浪图谱 → §四 |
| 分时图战法 | 书5 | 盘口波形/买卖点 → §五 |
| T+0 战法 | 书6 | 日内回转降本 → §六 |
| K线从入门到精通 | 书7 | K线基础 + 实战利器（黄金分割/时间窗口/大长腿等）→ §七 |

### 2. Skill 层新增「短线战法」类

在 `references/skills_registry.json` 新增独立分类 **"短线战法"**：含私募盈利系统、经典形态(11)、涨停狙击(58)、急速拉升、分时图、T+0、K线精通等细粒度技能，tier 以 T2 高频为主，数据源以 akshare 行情/龙虎榜/资金流为主。

### 3. 专家层新增「短线战术派」

在 `references/experts_registry.json` 新增学派 **"短线战术派"**，主专家 **吴国平**（总纲/私募盈利系统导师），辅以陈旭（涨停狙击）、王炳洁（分时图）、曹芝烨（急速拉升）、杨涛（K线精通），负责短线攻击决策与盘口圆桌。

### 4. 与风控的关系

短线战法全部受 §五 七条风控闸门约束；额外叠加 `short_line_mastery.md` §八 的环境闸门（牛市/平衡市才启用攻击性战法、大盘下降斜率>60% 禁用）、个股质地闸门（排除 ST/过高市盈率/过大盘股）、涨停基因闸门。任何打板、集合竞价狙击、T+0 动作前必须过环境评估与止损校验。

### 5. 调度入口

当用户提到「短线」「打板」「涨停」「集合竞价」「分时图」「T+0」「主力吸筹」「仙人指路」「黄金十字」「梅开二度」「龙虎榜」「大长腿」「黄金分割」「急速拉升」等关键词时，编排层优先调度本体系，加载 `references/short_line_mastery.md` 并召集短线战术派专家进行圆桌。

---

## 七、与 references 的关系

- `references/skills_registry.json`：137 个 Skill 的完整注册表（含 `tier`、`data_source`、`trigger`）。
- `references/experts_registry.json`：31 位数字人专家的完整注册表（含 `role`、`research_area`、`priority`）。
- `references/daily_workflow.md`：盘前/盘中/盘后/周末/月度/事件驱动六阶段的逐步操作手册。
- `references/risk_rules.md`：7 条风控规则的触发条件、执行动作与关联 Skill 详表。
- `references/wealth_reports/`：3 份 2026 年全球权威财富报告（莱坊 / 瑞银 / BCG），作为宏观背景与资产配置参考资源。
- `references/short_line_mastery.md`：《短线金手》七册实战战法知识库——私募盈利系统总纲、经典形态(11)、涨停狙击(58)、急速拉升、分时图、T+0、K线精通，含风控纪律与战术决策速查。
- `config.json`：数据源、API Key、自选股、风控参数与发布配置。

## 八、免责声明

本 Skill 仅供学习与研究使用，不构成任何投资建议。A 股市场有风险，投资需谨慎。所有交易决策与盈亏由用户自行承担。请在合法合规的前提下使用，并遵守所在地区的证券法律法规。
