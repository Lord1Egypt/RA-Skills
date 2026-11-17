# 月报（Monthly Report）

> 生成时间：{{generated_at}}
> 报告月份：{{year}}-{{month}}
> 报告作者：{{author}}
> 本月交易日数：{{trading_days}}

---

## 一、月度组合绩效

### 1.1 收益概况
| 指标 | 本月 | 上月 | 今年以来 | 同期沪深 300 |
|------|------|------|----------|--------------|
| 期初净值 | {{nav_start}} | {{prev_nav_start}} | {{ytd_nav_start}} | — |
| 期末净值 | {{nav_end}} | {{prev_nav_end}} | {{ytd_nav_end}} | — |
| 月度收益率 | {{monthly_return}} | {{prev_month_return}} | {{ytd_return}} | {{benchmark_return}} |
| 超额收益 | {{monthly_alpha}} | {{prev_alpha}} | {{ytd_alpha}} | — |

### 1.2 风险指标
| 指标 | 本月 | 今年以来 | 评价 |
|------|------|----------|------|
| 最大回撤 | {{max_drawdown}} | {{ytd_max_drawdown}} | {{dd_eval}} |
| 夏普比率 | {{sharpe_ratio}} | {{ytd_sharpe}} | {{sharpe_eval}} |
| 索提诺比率 | {{sortino_ratio}} | {{ytd_sortino}} | {{sortino_eval}} |
| 卡玛比率 | {{calmar_ratio}} | {{ytd_calmar}} | {{calmar_eval}} |
| 波动率（年化） | {{volatility}} | {{ytd_volatility}} | {{vol_eval}} |
| 下行波动率 | {{downside_vol}} | {{ytd_downside_vol}} | {{downvol_eval}} |

### 1.3 月度净值曲线
```
{{nav_chart_ascii}}
```

### 1.4 月度收益分布
- 最佳单日收益：{{best_daily_return}}（{{best_daily_date}}）
- 最差单日收益：{{worst_daily_return}}（{{worst_daily_date}}）
- 盈利交易日：{{profit_days}} 天 / 亏损交易日：{{loss_days}} 天
- 日胜率：{{daily_win_rate}}

---

## 二、策略表现评估

### 2.1 策略归因分析
| 收益来源 | 贡献度 | 说明 |
|----------|--------|------|
| 选股能力（Alpha） | {{alpha_contribution}} | {{alpha_note}} |
| 行业配置 | {{sector_contribution}} | {{sector_note}} |
| 择时能力 | {{timing_contribution}} | {{timing_note}} |
| 市场贝塔 | {{beta_contribution}} | {{beta_note}} |
| **合计** | {{total_contribution}} | — |

### 2.2 各策略模块表现
| 策略模块 | 交易次数 | 胜率 | 平均收益 | 盈亏比 | 评价 |
|----------|----------|------|----------|--------|------|
| {{strategy_name}} | {{trade_count}} | {{win_rate}} | {{avg_return}} | {{pl_ratio}} | {{eval}} |

### 2.3 行业贡献分解
| 行业 | 期初仓位 | 期末仓位 | 行业涨幅 | 贡献度 |
|------|----------|----------|----------|--------|
| {{sector}} | {{start_weight}} | {{end_weight}} | {{sector_return}} | {{contribution}} |

### 2.4 策略有效性检验
- 因子有效性：{{factor_validity}}
- 信号准确率：{{signal_accuracy}}
- 滑点与成本影响：{{cost_impact}}
- 改进建议：{{improvement_suggestion}}

---

## 三、持仓全面体检

### 3.1 期末持仓明细
| 代码 | 名称 | 行业 | 持仓数量 | 成本价 | 现价 | 市值 | 仓位占比 | 浮盈/亏 |
|------|------|------|----------|--------|------|------|----------|---------|
| {{stock_code}} | {{stock_name}} | {{sector}} | {{shares}} | {{cost_price}} | {{current_price}} | {{market_value}} | {{weight}} | {{pnl_pct}} |

### 3.2 持仓结构分析
- 持仓股票数：{{holding_count}}
- 前三大重仓股集中度：{{top3_concentration}}
- 行业集中度（HHI）：{{industry_hhi}}
- 风格分布：价值 {{value_weight}} / 成长 {{growth_weight}} / 周期 {{cyclical_weight}}
- 市值分布：大盘 {{large_weight}} / 中盘 {{mid_weight}} / 小盘 {{small_weight}}

### 3.3 持仓健康度评分
| 维度 | 评分 | 状态 | 建议 |
|------|------|------|------|
| 集中度 | {{concentration_score}} | {{concentration_status}} | {{concentration_advice}} |
| 分散度 | {{diversification_score}} | {{diversification_status}} | {{diversification_advice}} |
| 行业暴露 | {{exposure_score}} | {{exposure_status}} | {{exposure_advice}} |
| 风格平衡 | {{style_score}} | {{style_status}} | {{style_advice}} |
| 流动性 | {{liquidity_score}} | {{liquidity_status}} | {{liquidity_advice}} |
| **综合评分** | {{total_score}} | {{total_status}} | — |

### 3.4 个股诊断
| 代码 | 名称 | 基本面 | 技术面 | 资金面 | 估值 | 综合诊断 | 建议操作 |
|------|------|--------|--------|--------|------|----------|----------|
| {{stock_code}} | {{stock_name}} | {{fundamental}} | {{technical}} | {{capital}} | {{valuation}} | {{diagnosis}} | {{action}} |

---

## 四、再平衡决策记录

### 4.1 再平衡触发
- 触发原因：{{rebalance_trigger}}
- 偏离阈值：{{deviation_threshold}}
- 实际偏离：{{actual_deviation}}

### 4.2 再平衡方案
| 操作类型 | 代码 | 名称 | 调整前仓位 | 调整后仓位 | 调整原因 |
|----------|------|------|-----------|-----------|----------|
| {{action_type}} | {{stock_code}} | {{stock_name}} | {{before_weight}} | {{after_weight}} | {{adjust_reason}} |

### 4.3 再平衡执行结果
- 计划调整数：{{plan_adjust_count}}
- 实际执行数：{{executed_count}}
- 执行偏差：{{execution_deviation}}
- 交易成本：{{transaction_cost}}

---

## 五、风控执行回顾

### 5.1 风控指标监控
| 风控指标 | 阈值 | 实际值 | 触发次数 | 处置措施 |
|----------|------|--------|----------|----------|
| 单股最大回撤 | {{single_stop_threshold}} | {{single_stop_actual}} | {{trigger_count}} | {{action_taken}} |
| 组合最大回撤 | {{portfolio_stop_threshold}} | {{portfolio_stop_actual}} | {{portfolio_trigger_count}} | {{portfolio_action}} |
| 单股最大仓位 | {{max_position_threshold}} | {{max_position_actual}} | {{position_trigger_count}} | {{position_action}} |
| 行业最大仓位 | {{max_industry_threshold}} | {{max_industry_actual}} | {{industry_trigger_count}} | {{industry_action}} |

### 5.2 风控事件记录
| 日期 | 事件类型 | 涉及标的 | 触发指标 | 处置措施 | 结果 |
|------|----------|----------|----------|----------|------|
| {{risk_date}} | {{risk_type}} | {{risk_stock}} | {{risk_indicator}} | {{risk_action}} | {{risk_result}} |

### 5.3 风控有效性评估
- 止损执行率：{{stop_execution_rate}}
- 止损平均损失：{{avg_stop_loss}}
- 未及时止损造成的额外损失：{{extra_loss}}
- 风控改进建议：{{risk_improvement}}

---

## 六、下月投资计划

### 6.1 市场展望
- 宏观环境：{{macro_outlook}}
- 流动性环境：{{liquidity_outlook}}
- 市场主线预判：{{theme_outlook}}
- 风险事件：{{risk_events}}

### 6.2 投资目标
- 收益目标：{{return_target}}
- 最大回撤控制：{{dd_target}}
- 夏普比率目标：{{sharpe_target}}

### 6.3 仓位规划
- 目标仓位水平：{{target_position_level}}
- 行业配置计划：
  | 行业 | 当前仓位 | 目标仓位 | 调整方向 |
  |------|----------|----------|----------|
  | {{sector}} | {{current_weight}} | {{target_weight}} | {{adjust_direction}} |

### 6.4 重点研究计划
- [ ] {{research_plan_1}}
- [ ] {{research_plan_2}}
- [ ] {{research_plan_3}}

### 6.5 关键交易日历
| 日期 | 事件 | 重要性 | 应对预案 |
|------|------|--------|----------|
| {{event_date}} | {{event_name}} | {{importance}} | {{contingency}} |

---

> 免责声明：本报告仅为个人投资决策辅助记录，不构成任何投资建议。市场有风险，投资需谨慎。
