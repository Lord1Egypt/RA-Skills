# 风控规则（risk_rules）

> 本文档定义超级股票操盘 Skill 的 7 条风控规则。任何交易动作（开仓/加仓/减仓/清仓/再平衡）在执行前**必须**通过下列闸门校验；任一规则触发即阻断或调整动作。规则参数对应 `config.json` → `risk_control.rules`，可在配置中调整阈值。

> 优先级说明：`hard_limit=true` 为硬性上限，不建议突破；`hard_limit=false` 为软性提醒，触发后生成建议供人工决策。

---

## 规则 1：个股止损（stop_loss）

| 项目 | 内容 |
|------|------|
| **规则 ID** | R01-individual-stop-loss |
| **类型** | 个股级 / 软性提醒 |
| **优先级** | high |
| **触发条件** | 任一持仓标的浮亏达 −5%（`threshold_pct: -5.0`，可在 config 调整） |
| **执行动作** | 1) 触发止损评估；2) 强制生成减仓/清仓建议；3) 推送至用户人工确认；4) 记录交易日志 |
| **关联 Skill** | `stop-loss-take-profit-manager`、`portfolio-risk-monitor`、`position-exit-strategy`、`order-routing-skill` |
| **调度专家** | 塔勒布（主）、王开（辅） |
| **硬性上限** | 否（`hard_limit: false`） |

---

## 规则 2：组合止损（portfolio_stop_loss）

| 项目 | 内容 |
|------|------|
| **规则 ID** | R02-portfolio-stop-loss |
| **类型** | 组合级 / 软性提醒 |
| **优先级** | high |
| **触发条件** | 账户整体回撤达 −8%（`threshold_pct: -8.0`） |
| **执行动作** | 1) 触发组合级降仓；2) 权益仓位上限临时下调一档（如 80% → 60%）；3) 启动风险预算重设流程；4) 推送至用户人工确认 |
| **关联 Skill** | `portfolio-risk-monitor`、`portfolio-rebalance-skill`、`position-sizing-calculator`、`cycle-position-assessment` |
| **调度专家** | 塔勒布（主）、策略分析师（辅） |
| **硬性上限** | 否（`hard_limit: false`） |

---

## 规则 3：单只仓位上限（single_position_limit）

| 项目 | 内容 |
|------|------|
| **规则 ID** | R03-single-position-limit |
| **类型** | 集中度 / 硬性上限 |
| **优先级** | high |
| **触发条件** | 任一标的持仓市值占账户总市值比例 > 30%（`threshold_pct: 30.0`） |
| **执行动作** | 1) 阻止继续加仓该标的；2) 触发再平衡提醒，建议减仓至 30% 以内；3) 计算建议减仓股数；4) 推送至用户人工确认 |
| **关联 Skill** | `position-sizing-calculator`、`portfolio-rebalance-skill`、`portfolio-risk-monitor`、`order-routing-skill` |
| **调度专家** | 策略分析师（主）、聂方义（辅） |
| **硬性上限** | 是（`hard_limit: true`） |

---

## 规则 4：单行业集中度（industry_concentration_limit）

| 项目 | 内容 |
|------|------|
| **规则 ID** | R04-industry-concentration-limit |
| **类型** | 集中度 / 硬性上限 |
| **优先级** | high |
| **触发条件** | 任一行业（申万一级）合计仓位占账户总市值比例 > 50%（`threshold_pct: 50.0`） |
| **执行动作** | 1) 阻止继续加仓该行业标的；2) 触发分散化提醒，建议跨行业分散；3) 输出该行业持仓明细与减仓建议；4) 推送至用户人工确认 |
| **关联 Skill** | `portfolio-risk-monitor`、`portfolio-rebalance-skill`、`sector-rotation-tracker`、`industry-capital-comparison` |
| **调度专家** | 策略分析师（主）、刘高畅（辅） |
| **硬性上限** | 是（`hard_limit: true`） |

---

## 规则 5：黑天鹅熔断（black_swan_circuit_breaker）

| 项目 | 内容 |
|------|------|
| **规则 ID** | R05-black-swan-circuit-breaker |
| **类型** | 系统级 / 硬性上限 |
| **优先级** | high |
| **触发条件** | 检测到系统性风险信号之一：①千股跌停；②流动性骤缩；③指数单日跌幅 > 5%（`triggers: ["千股跌停","流动性骤缩","指数单日跌幅>5%"]`） |
| **执行动作** | 1) 触发风控熔断，暂停所有新开仓；2) 启动对冲评估（期权/股指期货）；3) 生成紧急降仓方案；4) **需用户人工确认后方可解除熔断** |
| **关联 Skill** | `portfolio-risk-monitor`、`stop-loss-take-profit-manager`、`position-exit-strategy`、`index-futures-basis-analysis` |
| **调度专家** | 塔勒布（主）、聂方义（辅）、策略分析师（辅） |
| **硬性上限** | 是（`hard_limit: true`） |

---

## 规则 6：事件前置审查（event_pre_check）

| 项目 | 内容 |
|------|------|
| **规则 ID** | R06-event-pre-check |
| **类型** | 事件级 / 硬性上限 |
| **优先级** | high |
| **触发条件** | 重大公告/异动发生后 30 分钟内（`cooldown_min: 30`），对应标的被标记为「事件审查中」 |
| **执行动作** | 1) 30 分钟内禁止对该标的新增仓位；2) 须先完成事件评估（公告解读 + 影响评级）；3) 评估通过后解除标记；4) 记录事件评估日志 |
| **关联 Skill** | `announcement-monitor-skill`、`major-announcement-parsing`、`equity-event-tracker`、`regulatory-disclosure-tracker` |
| **调度专家** | 聂方义（主）、魏亚妮（辅） |
| **硬性上限** | 是（`hard_limit: true`） |

---

## 规则 7：流动性约束（liquidity_constraint）

| 项目 | 内容 |
|------|------|
| **规则 ID** | R07-liquidity-constraint |
| **类型** | 执行级 / 硬性上限 |
| **优先级** | high |
| **触发条件** | 单笔委托量 > 该标的近 20 日平均成交量的 10%（`max_order_pct_of_adv20: 10.0`） |
| **执行动作** | 1) 阻止单笔超额委托；2) 自动拆分为多笔小额委托（TWAP/VWAP）；3) 评估冲击成本与滑点；4) 推送拆单方案至用户确认 |
| **关联 Skill** | `order-routing-skill`、`batch-order-execution`、`slippage-analysis`、`volume-energy-analysis` |
| **调度专家** | 聂方义（主）、王开（辅） |
| **硬性上限** | 是（`hard_limit: true`） |

---

## 闸门校验流程

任何交易动作执行前，编排层按以下顺序校验，**任一硬性规则触发即阻断动作**：

```
交易动作请求
      │
      ▼
┌─────────────────────────┐
│ R05 黑天鹅熔断？         │──是──▶ 阻断 + 对冲评估（需人工解除）
└─────────────────────────┘
      │否
      ▼
┌─────────────────────────┐
│ R06 事件前置审查？       │──是──▶ 阻断新增 + 事件评估
└─────────────────────────┘
      │否
      ▼
┌─────────────────────────┐
│ R03 单只仓位 > 30%？     │──是──▶ 阻断加仓 + 再平衡提醒
└─────────────────────────┘
      │否
      ▼
┌─────────────────────────┐
│ R04 行业集中度 > 50%？   │──是──▶ 阻断加仓 + 分散化提醒
└─────────────────────────┘
      │否
      ▼
┌─────────────────────────┐
│ R07 流动性 > 10% ADV20？ │──是──▶ 拆单 + 滑点评估
└─────────────────────────┘
      │否
      ▼
┌─────────────────────────┐
│ R01 个股浮亏 ≤ -5%？     │──是──▶ 止损评估（软性，生成建议）
└─────────────────────────┘
      │
      ▼
┌─────────────────────────┐
│ R02 组合回撤 ≤ -8%？     │──是──▶ 组合降仓（软性，生成建议）
└─────────────────────────┘
      │
      ▼
  全部通过 → 执行动作（需用户人工二次确认）
```

---

## 规则与 Skill 速查

| 规则 | 关联 Skill（核心） | 调度专家 | 硬性 |
|------|-------------------|---------|------|
| R01 个股止损 | stop-loss-take-profit-manager | 塔勒布 | 否 |
| R02 组合止损 | portfolio-risk-monitor | 塔勒布 / 策略分析师 | 否 |
| R03 单只仓位上限 | position-sizing-calculator | 策略分析师 / 聂方义 | 是 |
| R04 行业集中度 | portfolio-rebalance-skill | 策略分析师 / 刘高畅 | 是 |
| R05 黑天鹅熔断 | portfolio-risk-monitor | 塔勒布 / 聂方义 | 是 |
| R06 事件前置审查 | major-announcement-parsing | 聂方义 / 魏亚妮 | 是 |
| R07 流动性约束 | order-routing-skill | 聂方义 / 王开 | 是 |

---

## 免责声明

风控规则旨在降低风险，但无法消除所有市场风险。规则触发后的建议均需用户人工二次确认，本 Skill 不提供直接下单通道，不构成任何投资建议。所有交易决策与盈亏由用户自行承担。
