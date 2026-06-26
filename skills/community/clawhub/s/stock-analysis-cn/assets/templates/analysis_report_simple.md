# 投资分析报告

**标的**: {{ticker}} {{name}}
**分析日期**: {{date}}
**数据截止**: {{data_date}}

---

## 一、核心指标概览

| 指标 | 数值 | 历史分位 | 行业对比 | 评价 |
|------|------|----------|----------|------|
| 当前价格 | {{current_price}} | - | - | - |
| PE (TTM) | {{pe}} | {{pe_percentile}}% | VS 行业中位数: {{industry_pe_median}} ({{pe_premium}}%) | {{pe_zone}} |
| PB | {{pb}} | {{pb_percentile}}% | VS 行业中位数: {{industry_pb_median}} | {{pb_zone}} |
| 年化波动率 | {{annualized_volatility}}% | - | - | - |
| 最大回撤 | {{max_drawdown}}% | - | - | - |
| 夏普比率 | {{sharpe_ratio}} | - | - | - |

---

## 二、技术面分析

### 趋势状态
- **当前趋势**: {{trend}} ({{trend_strength}})
- **价格位置**: 相对MA20 {{above_ma20}} (当前价格: {{current_price}} vs MA20: {{ma20}})
- **近5日**: {{price_change_5d}}
- **近20日**: {{price_change_20d}}

### 动量指标
- **RSI(14)**: {{rsi_14}} → {{rsi_comment}}
- **支撑位**: {{support_levels}}
- **阻力位**: {{resistance_levels}}

### 技术面摘要
{{tech_summary}}

---

## 三、估值分析

### 纵向对比（历史）
- 当前PE: {{pe}}，5年 median: {{pe_5y_median}}
- 当前PE百分位: {{pe_percentile}}% → {{pe_zone}}
- 当前PB: {{pb}}，5年 median: {{pb_5y_median}}
- 当前PB百分位: {{pb_percentile}}% → {{pb_zone}}

### 横向对比（行业）
- 行业PE中位数: {{industry_pe_median}}
- 估值溢价: {{pe_premium}}% ({{pe_premium_comment}})
- 行业PB中位数: {{industry_pb_median}}

### 综合评估
**{{overall_rating}}**

---

## 四、风险指标

- 年化波动率: {{annualized_volatility}}%
- 最大回撤: {{max_drawdown}}%
- 夏普比率: {{sharpe_ratio}}
- Beta: {{beta}}

---

## 五、投资建议

### 综合评分
| 维度 | 分数 | 权重 | 加权分 |
|------|------|------|--------|
| 基本面 | {{score_fundamental}} | 30% | {{score_fundamental_weighted}} |
| 技术面 | {{score_technical}} | 20% | {{score_technical_weighted}} |
| 估值 | {{score_valuation}} | 30% | {{score_valuation_weighted}} |
| 风险 | {{score_risk}} | 20% | {{score_risk_weighted}} |
| **总分** | - | 100% | **{{total_score}}** |

### 建议
**{{recommendation}}**

**理由**:
1. {{reason_1}}
2. {{reason_2}}
3. {{reason_3}}

### 风险提示
{{risk_warnings}}

---

## 六、数据来源

- 实时行情: 腾讯财经 API
- 估值基准: 中证指数公司历史数据
- 分析工具: Stock-Analysis Skill v1.0

**免责声明**: 本报告仅供研究和参考，不构成投资建议。投资有风险，决策需谨慎。

---

*报告生成时间: {{generated_at}}*
