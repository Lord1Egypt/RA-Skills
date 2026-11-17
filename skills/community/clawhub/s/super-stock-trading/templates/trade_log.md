# 交易日志（Trade Log）

> 日志记录周期：{{log_period_start}} 至 {{log_period_end}}
> 记录人：{{author}}
> 最后更新：{{last_updated}}

---

## 一、交易记录表

### 1.1 买入记录

| 交易日期 | 交易时间 | 代码 | 名称 | 方向 | 买入价 | 数量（股） | 金额 | 手续费 | 买入原因 | 标签 |
|----------|----------|------|------|------|--------|-----------|------|--------|----------|------|
| {{trade_date}} | {{trade_time}} | {{stock_code}} | {{stock_name}} | 买入 | {{buy_price}} | {{quantity}} | {{amount}} | {{commission}} | {{buy_reason}} | {{tag}} |

### 1.2 卖出记录

| 交易日期 | 交易时间 | 代码 | 名称 | 方向 | 卖出价 | 数量（股） | 金额 | 手续费 | 卖出原因 | 盈亏 | 盈亏比例 |
|----------|----------|------|------|------|--------|-----------|------|--------|----------|------|----------|
| {{trade_date}} | {{trade_time}} | {{stock_code}} | {{stock_name}} | 卖出 | {{sell_price}} | {{quantity}} | {{amount}} | {{commission}} | {{sell_reason}} | {{pnl}} | {{pnl_pct}} |

### 1.3 完整交易明细

| 记录编号 | 日期 | 时间 | 代码 | 名称 | 方向 | 价格 | 数量 | 金额 | 费用 | 净额 | 关联批次 |
|----------|------|------|------|------|------|------|------|------|------|------|----------|
| {{trade_id}} | {{trade_date}} | {{trade_time}} | {{stock_code}} | {{stock_name}} | {{direction}} | {{price}} | {{quantity}} | {{amount}} | {{fee}} | {{net_amount}} | {{batch_id}} |

---

## 二、决策依据

### 2.1 买入决策依据

#### 交易编号：{{trade_id_buy}}

| 维度 | 内容 |
|------|------|
| 标的 | {{stock_code}} {{stock_name}} |
| 买入日期 | {{buy_date}} |
| 买入价 / 数量 | {{buy_price}} / {{quantity}} |
| **基本面依据** | {{fundamental_basis}} |
| **技术面依据** | {{technical_basis}} |
| **资金面依据** | {{capital_basis}} |
| **消息面依据** | {{news_basis}} |
| **行业逻辑** | {{industry_logic}} |
| **预期持有周期** | {{expected_holding_period}} |
| **目标价** | {{target_price}} |
| **止损价** | {{stop_loss_price}} |
| **仓位规划** | {{position_plan}} |
| **风险收益比** | {{risk_reward_ratio}} |
| **决策置信度** | {{confidence_level}} / 10 |

### 2.2 卖出决策依据

#### 交易编号：{{trade_id_sell}}

| 维度 | 内容 |
|------|------|
| 标的 | {{stock_code}} {{stock_name}} |
| 卖出日期 | {{sell_date}} |
| 卖出价 / 数量 | {{sell_price}} / {{quantity}} |
| **卖出触发条件** | {{sell_trigger}} |
| **卖出类型** | 止盈 / 止损 / 调仓 / 持有逻辑破坏（{{sell_type}}） |
| **基本面变化** | {{fundamental_change}} |
| **技术面变化** | {{technical_change}} |
| **资金面变化** | {{capital_change}} |
| **持仓盈亏情况** | {{holding_pnl}} |
| **决策置信度** | {{confidence_level}} / 10 |

---

## 三、事后复盘

### 3.1 单笔交易复盘

#### 复盘标的：{{stock_code}} {{stock_name}}

| 复盘维度 | 内容 |
|----------|------|
| 买入批次 | {{batch_id}} |
| 买入日期 / 价格 | {{buy_date}} / {{buy_price}} |
| 卖出日期 / 价格 | {{sell_date}} / {{sell_price}} |
| 持有周期 | {{holding_period}} |
| 最终盈亏 | {{final_pnl}}（{{final_pnl_pct}}） |
| **决策正确性** | {{decision_correctness}} |
| **执行及时性** | {{execution_timeliness}} |
| **止损是否到位** | {{stop_loss_eval}} |
| **仓位是否合理** | {{position_eval}} |
| **可复用的成功经验** | {{success_lesson}} |
| **需改进的不足** | {{improvement_needed}} |
| **评分（1-10）** | {{review_score}} / 10 |

### 3.2 阶段性统计

| 统计项 | 数值 |
|--------|------|
| 统计周期 | {{stats_period}} |
| 总交易笔数 | {{total_trades}} |
| 盈利笔数 / 亏损笔数 | {{profit_trades}} / {{loss_trades}} |
| 胜率 | {{win_rate}} |
| 平均盈利 | {{avg_profit}} |
| 平均亏损 | {{avg_loss}} |
| 盈亏比 | {{pl_ratio}} |
| 最大单笔盈利 | {{max_profit}} |
| 最大单笔亏损 | {{max_loss}} |
| 平均持有周期 | {{avg_holding_period}} |
| 总手续费 | {{total_commission}} |
| 净盈亏 | {{net_pnl}} |

### 3.3 经验教训沉淀

#### 3.3.1 高胜率交易模式
1. {{winning_pattern_1}}
   - 共性特征：{{common_feature_1}}
   - 复用建议：{{reuse_advice_1}}

2. {{winning_pattern_2}}
   - 共性特征：{{common_feature_2}}
   - 复用建议：{{reuse_advice_2}}

#### 3.3.2 高频错误模式
1. {{error_pattern_1}}
   - 出现频次：{{error_frequency_1}}
   - 根因分析：{{root_cause_1}}
   - 防范措施：{{prevention_1}}

2. {{error_pattern_2}}
   - 出现频次：{{error_frequency_2}}
   - 根因分析：{{root_cause_2}}
   - 防范措施：{{prevention_2}}

### 3.4 交易纪律自检

| 纪律项 | 遵守情况 | 违规次数 | 改进措施 |
|--------|----------|----------|----------|
| 严格按计划交易 | {{compliance_status}} | {{violation_count}} | {{improvement}} |
| 到止损必执行 | {{stop_compliance}} | {{stop_violation}} | {{stop_improvement}} |
| 不追涨杀跌 | {{chase_compliance}} | {{chase_violation}} | {{chase_improvement}} |
| 单股仓位上限 | {{position_compliance}} | {{position_violation}} | {{position_improvement}} |
| 行业仓位上限 | {{industry_compliance}} | {{industry_violation}} | {{industry_improvement}} |

---

> 免责声明：本日志仅为个人投资决策辅助记录，不构成任何投资建议。市场有风险，投资需谨慎。
