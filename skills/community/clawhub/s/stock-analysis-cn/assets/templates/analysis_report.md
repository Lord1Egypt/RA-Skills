# 投资分析报告

**标的**: {{ticker}} {{name}}
**分析日期**: {{date}}
**数据截止**: {{data_date}}

---

## 一、核心指标概览

| 指标 | 数值 | 历史分位 | 行业对比 | 评价 |
|------|------|----------|----------|------|
| 当前价格 | {{current_price}} | - | - | - |
| PE (TTM) | {{pe}} | {{pe_percentile}}% | VS 行业中位数: {{industry_pe_median}} ({{pe_premium}}%)) | {{pe_zone}} |
| PB | {{pb}} | {{pb_percentile}}% | VS 行业中位数: {{industry_pb_median}} | {{pb_zone}} |
| ROE | {{roe}}% | - | - | {{roe_assessment}} |
| 股息率 | {{dividend_yield}}% | - | - | - |
| 年化波动率 | {{annualized_volatility}}% | - | - | - |
| 最大回撤 | {{max_drawdown}}% | - | - | - |
| 夏普比率 | {{sharpe_ratio}} | - | - | - |

---

## 二、基本面分析

### 盈利能力
- **ROE**: {{roe}}% → {{roe_comment}}
- **ROA**: {{roa}}%
- **毛利率**: {{gross_margin}}%
- **净利率**: {{net_margin}}%

### 成长性
- **营收3年CAGR**: {{revenue_cagr}}%
- **利润3年CAGR**: {{profit_cagr}}%

### 财务健康
- **资产负债率**: {{debt_to_equity}}× → {{debt_comment}}
- **流动比率**: {{current_ratio}}
- **经营现金流/净利润**: {{ocf_to_net_income}}×

---

## 三、技术面分析

### 趋势状态
- **当前趋势**: {{trend}} ({{trend_strength}})
- **价格位置**:
  - 相对MA20: {{above_ma20}} (当前价格: {{current_price}} vs MA20: {{ma20}})
  - MA排列: {{ma_alignment}}

### 动量指标
- **RSI(14)**: {{rsi_14}} → {{rsi_comment}}
- **MACD**:
  - 柱状图: {{macd_histogram}}
  - 信号: {{macd_signal_comment}}
- **KDJ**: K={{kdj_k}}, D={{kdj_d}}, J={{kdj_j}}

### 关键价位
- **阻力位**: {{resistance_levels}}
- **支撑位**: {{support_levels}}
- **近5日涨跌幅**: {{price_change_5d}}%
- **近20日涨跌幅**: {{price_change_20d}}%

---

## 四、估值分析

### 纵向对比（历史）
- **当前PE**: {{pe}} vs 5年 median {{pe_5y_median}}
- **当前PE百分位**: {{pe_percentile}}% ({{pe_percentile_comment}})
- **当前PB**: {{pb}} vs 5年 median {{pb_5y_median}}
- **当前PB百分位**: {{pb_percentile}}%

### 横向对比（行业）
- **行业PE中位数**: {{industry_pe_median}}
- **估值溢价**: {{pe_premium}}% ({{pe_premium_comment}})
- **行业PB中位数**: {{industry_pb_median}}
- **估值溢价**: {{pb_premium}}%

### PE Band (可选的图表)

```
PE 80  ┤                             ╱─╲
PE 70  ┤                     ╱─╲   ╱   ╲
PE 60  ┤             ╱─╲   ╱   ╲ ╱     ╲
PE 50  ┤     ╱─╲   ╱   ╲ ╱     ╲╱       ╲
PE 40  ┤ ╱─╲   ╲ ╱     ╲╱       ╲         ╲
PE 30  ┤╱   ╲   ╲╱       ╲         ╲         ╲  Current: {{pe}}
PE 20  ┤╲     ╲   ╲         ╲         ╲         ╲
PE 10  ┤ ╲     ╲   ╲         ╲         ╲         ╲
       2018    2019    2020    2021    2022    2023    2024
```

---

## 五、投资建议

### 综合评分
| 维度 | 分数 (0-10) | 权重 | 加权分 |
|------|-------------|------|--------|
| 基本面质量 | {{score_fundamental}} | 30% | {{score_fundamental_weighted}} |
| 技术趋势 | {{score_technical}} | 20% | {{score_technical_weighted}} |
| 估值吸引力 | {{score_valuation}} | 30% | {{score_valuation_weighted}} |
| 风险水平 | {{score_risk}} | 20% | {{score_risk_weighted}} |
| **总分** | - | 100% | **{{total_score}}** |

### 建议
{{recommendation}}

**理由**:
- {{reason_1}}
- {{reason_2}}
- {{reason_3}}

### 风险提示
{{risk_warnings}}

---

## 六、数据来源与免责声明

- **数据来源**: 腾讯财经、东方财富、集思录
- **数据截止**: {{data_date}}
- **分析工具**: Stock-Analysis Skill v1.0

**免责声明**: 本报告仅供研究和参考，不构成投资建议。投资有风险，决策需谨慎。历史表现不代表未来收益。

---

*报告生成时间: {{generated_at}}*
