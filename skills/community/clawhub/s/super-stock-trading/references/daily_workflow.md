# 日常工作流（daily_workflow）

> 本文档描述超级股票操盘 Skill 的日常工作流，按 **盘前 / 盘中 / 盘后 / 周末 / 月度 / 事件驱动** 六个阶段组织。每个阶段列出步骤、调用的 Skills 与调度专家。所有交易动作在执行前必须通过 `references/risk_rules.md` 中的 7 条风控闸门。

> 时区：Asia/Shanghai。以下时间为 A 股交易日时间，非交易日跳过盘前/盘中/盘后阶段。

---

## 阶段一：盘前（07:00 – 09:15）

目标：完成隔夜信息消化、持仓体检、当日策略制定与集合竞价准备。

### 步骤 1.1 隔夜要闻与外盘复盘（07:00–07:30）
- **动作**：拉取隔夜外盘（美股/欧股/商品/汇率）、国内财经要闻与政策动态。
- **调用 Skill**：`market-overview-skill`、`market-news-hot-monitor`
- **调度专家**：宏观经济学家（主）、外汇研究员（辅）
- **产出**：隔夜要闻简报

### 步骤 1.2 公告与事件扫描（07:30–08:00）
- **动作**：扫描自选股及关注题材的公告、停复牌、业绩预告/快报。
- **调用 Skill**：`announcement-monitor-skill`、`major-announcement-parsing`、`performance-pre-announcement`
- **调度专家**：魏亚妮（主）、聂方义（辅）
- **产出**：公告事件清单与影响评级

### 步骤 1.3 持仓体检与风险扫描（08:00–08:30）
- **动作**：对当前持仓做风险体检，更新估值与风险评分，识别需止损/止盈的标的。
- **调用 Skill**：`portfolio-risk-monitor`、`valuation-multi-model-skill`、`stop-loss-take-profit-manager`
- **调度专家**：沃伦·巴菲特（主）、塔勒布（辅）
- **产出**：持仓体检报告 + 风控动作建议
- **风控闸门**：校验个股止损 5%、组合止损 8%、单只仓位 30%、行业集中度 50%

### 步骤 1.4 当日策略与重点标的（08:30–09:00）
- **动作**：结合大盘趋势、资金面与持仓风险，制定当日策略与重点观察标的。
- **调用 Skill**：`index-trend-analysis`、`capital-flow-intraday`、`trading-plan-generator`
- **调度专家**：刘高畅（主）、陶川（辅）
- **产出**：当日策略卡（进攻/防守/观望 + 重点标的）

### 步骤 1.5 集合竞价准备（09:00–09:15）
- **动作**：监控集合竞价撮合，识别高开/低开强度与异动标的。
- **调用 Skill**：`opening-auction-analysis`、`real-time-hot-plate`
- **调度专家**：王开（主）、赵哲（辅）
- **产出**：竞价观察清单
- **风控闸门**：事件前置审查（重大公告后 30 分钟内禁止新增仓位）

---

## 阶段二：盘中（09:30 – 15:00）

目标：实时跟踪盘面、识别机会与风险、执行交易动作并控制仓位。

### 步骤 2.1 开盘强度与情绪（09:30–10:30）
- **动作**：评估开盘强度、市场情绪温度、板块轮动方向。
- **调用 Skill**：`intraday-rotation-monitor`、`market-sentiment-thermometer`、`limit-up-limit-down-stats`
- **调度专家**：赵哲（主）、魏嵬猫哥（辅）
- **产出**：开盘情绪简报

### 步骤 2.2 资金面与题材轮动（10:30–11:30）
- **动作**：监控主力资金、北向资金、题材热度与龙头卡位。
- **调用 Skill**：`main-force-capital-detection`、`theme-heatmap-skill`、`dragon-stock-identification`、`northbound-flow-analysis`
- **调度专家**：Serenity白毛股神（主）、海榕君（辅）
- **产出**：资金面与题材轮动简报

### 步骤 2.3 午间复盘（11:30–13:00）
- **动作**：午间总结半日盘面，更新当日策略与重点标的。
- **调用 Skill**：`daily-market-summary`、`volume-energy-analysis`、`trading-plan-generator`
- **调度专家**：策略分析师（主）
- **产出**：午间复盘简报 + 下午计划

### 步骤 2.4 午后题材深化（13:00–14:00）
- **动作**：深化午后题材，识别题材持续性与轮动路径。
- **调用 Skill**：`dragon-stock-identification`、`concept-sector-strength`、`theme-sustainment-scoring`、`theme-rotation-forecast`
- **调度专家**：焦娟（主）、吴立（辅）
- **产出**：午后题材简报

### 步骤 2.5 尾盘决策与减仓（14:00–14:57）
- **动作**：评估尾盘风险，执行减仓/止盈/止损，准备收盘。
- **调用 Skill**：`closing-session-review`、`position-exit-strategy`、`stop-loss-take-profit-manager`、`order-routing-skill`
- **调度专家**：王开（主）、塔勒布（辅）
- **产出**：尾盘交易动作清单
- **风控闸门**：个股止损 5%、流动性约束（单笔不超 20 日均量 10%）、黑天鹅熔断

### 步骤 2.6 收盘集合竞价（14:57–15:00）
- **动作**：收盘集合竞价委托与滑点评估。
- **调用 Skill**：`order-routing-skill`、`slippage-analysis`
- **调度专家**：王开（主）
- **产出**：收盘委托记录

---

## 阶段三：盘后（15:00 – 22:00）

目标：完成收盘总结、资金复盘、公告财报解读与次日计划。

### 步骤 3.1 收盘总结与盈亏（15:00–16:00）
- **动作**：汇总当日盈亏、交易记录、持仓变化，写入交易日志。
- **调用 Skill**：`daily-market-summary`、`trade-journal-logger`、`portfolio-risk-monitor`
- **调度专家**：策略分析师（主）
- **产出**：日度交易日志

### 步骤 3.2 龙虎榜与资金复盘（16:00–18:00）
- **动作**：复盘龙虎榜、北向资金、机构席位与资金流向。
- **调用 Skill**：`dragon-tiger-list-analysis`、`northbound-flow-analysis`、`institutional-capital-tracking`、`etf-fund-flow-monitor`
- **调度专家**：海榕君（主）、基金研究员（辅）
- **产出**：资金复盘简报

### 步骤 3.3 公告与财报解读（18:00–20:00）
- **动作**：解读当日公告与财报，评估对持仓与选股池的影响。
- **调用 Skill**：`earnings-report-parsing`、`earnings-surprise-analysis`、`major-announcement-parsing`、`equity-event-tracker`
- **调度专家**：魏亚妮（主）、焦娟（辅）
- **产出**：公告/财报解读清单

### 步骤 3.4 个股深度与次日计划（20:00–22:00）
- **动作**：对重点标的做深度研究，生成次日交易计划。
- **调用 Skill**：`stock-deep-research`、`trading-plan-generator`、`watchlist-monitoring`、`after-hours-news-digest`
- **调度专家**：沃伦·巴菲特（主）、查理·芒格（辅）
- **产出**：次日交易计划 + 选股池更新
- **风控闸门**：次日计划须预设止损止盈位

---

## 阶段四：周末

目标：完成周度持仓体检、行业梳理、选股池更新与复盘归档。

### 步骤 4.1 周度持仓体检
- **动作**：对全持仓做深度估值与同业对比，识别需调整的标的。
- **调用 Skill**：`portfolio-risk-monitor`、`valuation-peer-comparison`、`financial-statement-health-check`
- **调度专家**：沃伦·巴菲特（主）、海榕君（辅）
- **产出**：周度持仓体检报告

### 步骤 4.2 行业与题材梳理
- **动作**：梳理本周行业景气与题材产业链，更新产业链图谱。
- **调用 Skill**：`industry-chain-mapping`、`theme-correlation-analysis`、`industry-capital-comparison`、`serenity-industry-chain-analysis`
- **调度专家**：Serenity白毛股神（主）、吴立（辅）
- **产出**：行业与题材梳理简报

### 步骤 4.3 选股池更新
- **动作**：多因子选股 + 估值校验，更新选股池并设置监控。
- **调用 Skill**：`multi-factor-stock-screening`、`valuation-multi-model-skill`、`fundamental-value-screening`、`watchlist-monitoring`
- **调度专家**：查理·芒格（主）、望京博格（辅）
- **产出**：更新后的选股池

### 步骤 4.4 复盘日志归档
- **动作**：归档本周交易日志与决策记录，沉淀知识库。
- **调用 Skill**：`trade-journal-logger`、`knowledge-base-assistant`
- **调度专家**：策略分析师（主）
- **产出**：周度复盘归档

---

## 阶段五：月度

目标：完成组合再平衡、资产配置审视、风险预算重设与理财保障检视。

### 步骤 5.1 月度组合再平衡
- **动作**：基于周期定位与策略观点，生成组合再平衡方案。
- **调用 Skill**：`portfolio-rebalance-skill`、`cycle-position-assessment`、`sector-rotation-tracker`
- **调度专家**：策略分析师（主）、纳瓦尔（辅）
- **产出**：月度再平衡方案
- **风控闸门**：单只仓位 30%、行业集中度 50%、权益仓位上限 80%

### 步骤 5.2 资产配置审视
- **动作**：审视权益/固收/商品的配置比例，评估估值与配置合理性。
- **调用 Skill**：`valuation-multi-model-skill`、`margin-trading-balance`、`etf-fund-flow-monitor`、`index-futures-basis-analysis`
- **调度专家**：望京博格（主）、杨业伟（辅）
- **产出**：资产配置审视报告

### 步骤 5.3 风险预算重设
- **动作**：重设下月风险预算与仓位上限，更新止损止盈参数。
- **调用 Skill**：`portfolio-risk-monitor`、`position-sizing-calculator`、`stop-loss-take-profit-manager`
- **调度专家**：塔勒布（主）、聂方义（辅）
- **产出**：下月风险预算表
- **风控闸门**：组合止损 8%、黑天鹅熔断参数

### 步骤 5.4 理财与保障检视
- **动作**：审视银行理财、固收、保险等非权益配置，完善财富规划。
- **调用 Skill**：`cash-flow-quality-analysis`、`financial-statement-health-check`、`knowledge-base-assistant`
- **调度专家**：银行理财专家（主）、保险专家（辅）、杨业伟（辅）
- **产出**：理财与保障检视报告

---

## 阶段六：事件驱动

目标：在重大事件发生时，中断或补充常规时间表，立即调度对应专家与 Skill。

### 6.1 重大政策
- **触发条件**：央行/证监会/国常会发布重大政策
- **调用 Skill**：`policy-driven-theme-analysis`、`market-overview-skill`、`theme-sustainment-scoring`
- **调度专家**：陶川（主）、陈洪斌（辅）、宏观经济学家（辅）
- **风控闸门**：事件前置审查（30 分钟内禁止新增仓位）

### 6.2 个股异动
- **触发条件**：自选股 ±7% 或量比 > 5
- **调用 Skill**：`capital-flow-stock-level`、`intraday-trade-signal`、`historical-k-line-review`
- **调度专家**：王开（主）、赵哲（辅）
- **风控闸门**：个股止损 5%、流动性约束

### 6.3 临时停复牌
- **触发条件**：交易所发布停复牌公告
- **调用 Skill**：`announcement-monitor-skill`、`regulatory-disclosure-tracker`
- **调度专家**：魏亚妮（主）

### 6.4 财报披露
- **触发条件**：业绩预告/快报/正式报告披露
- **调用 Skill**：`earnings-report-parsing`、`earnings-surprise-analysis`、`earnings-quality-redflag`、`revenue-profit-trend`
- **调度专家**：魏亚妮（主）、沃伦·巴菲特（辅）
- **风控闸门**：事件前置审查

### 6.5 重大公告（并购/增减持/分红/股权）
- **触发条件**：并购重组、大股东增减持、分红送转、股权激励等
- **调用 Skill**：`major-announcement-parsing`、`equity-event-tracker`、`merger-acquisition-monitor`、`shareholder-change-monitor`、`dividend-rights-event`
- **调度专家**：聂方义（主）、海榕君（辅）
- **风控闸门**：事件前置审查

### 6.6 龙虎榜上榜
- **触发条件**：自选股或关注题材上榜
- **调用 Skill**：`dragon-tiger-list-analysis`、`institutional-capital-tracking`
- **调度专家**：海榕君（主）

### 6.7 北向异动
- **触发条件**：单日净流入/流出超阈值
- **调用 Skill**：`northbound-flow-analysis`、`etf-fund-flow-monitor`
- **调度专家**：基金研究员（主）

### 6.8 题材爆发
- **触发条件**：新题材热度超阈值
- **调用 Skill**：`new-theme-discovery`、`theme-sustainment-scoring`、`dragon-stock-identification`
- **调度专家**：Serenity白毛股神（主）、焦娟（辅）

### 6.9 黑天鹅
- **触发条件**：千股跌停、流动性骤缩、指数单日跌幅 > 5%
- **调用 Skill**：`portfolio-risk-monitor`、`stop-loss-take-profit-manager`、`position-exit-strategy`
- **调度专家**：塔勒布（主）、策略分析师（辅）
- **风控闸门**：黑天鹅熔断（暂停新开仓 + 对冲评估，需人工确认解除）

### 6.10 社区情绪极值
- **触发条件**：看多/看空情绪偏离阈值
- **调用 Skill**：`community-sentiment-aggregator`、`market-panic-greed-index`
- **调度专家**：i小万（主）

---

## 附录：阶段-专家-Skill 速查矩阵

| 阶段 | 主专家 | 高频 Skill |
|------|-------|-----------|
| 盘前 | 宏观经济学家 / 沃伦·巴菲特 / 刘高畅 / 王开 | market-overview-skill、portfolio-risk-monitor、index-trend-analysis、opening-auction-analysis |
| 盘中 | 赵哲 / Serenity白毛股神 / 策略分析师 / 焦娟 / 王开 | intraday-rotation-monitor、main-force-capital-detection、daily-market-summary、order-routing-skill |
| 盘后 | 策略分析师 / 海榕君 / 魏亚妮 / 沃伦·巴菲特 | daily-market-summary、dragon-tiger-list-analysis、earnings-report-parsing、stock-deep-research |
| 周末 | 沃伦·巴菲特 / Serenity白毛股神 / 查理·芒格 / 策略分析师 | portfolio-risk-monitor、industry-chain-mapping、multi-factor-stock-screening、trade-journal-logger |
| 月度 | 策略分析师 / 望京博格 / 塔勒布 / 银行理财专家 | portfolio-rebalance-skill、valuation-multi-model-skill、position-sizing-calculator |
| 事件驱动 | 陶川 / 王开 / 魏亚妮 / 聂方义 / 塔勒布 / i小万 | policy-driven-theme-analysis、capital-flow-stock-level、earnings-report-parsing、portfolio-risk-monitor |
