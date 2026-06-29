# 资产配置建议报告

**报告日期**：{{REPORT_DATE}}  
**数据源**：AKShare（底层对接国家统计局 data.stats.gov.cn）  
**生成时间**：{{GENERATED_TIME}}

---

## 一、宏观经济概况

### 1.1 中国宏观环境

| 指标 | 最新值 | 时间 | 趋势 | 说明 |
|------|:------:|------|:----:|------|
| GDP同比 | {{GDP_VALUE}} | {{GDP_QUARTER}} | {{GDP_TREND}} | {{GDP_NOTE}} |
| CPI同比 | {{CPI_VALUE}} | {{CPI_MONTH}} | {{CPI_TREND}} | {{CPI_NOTE}} |
| PPI同比 | {{PPI_VALUE}} | {{PPI_MONTH}} | {{PPI_TREND}} | {{PPI_NOTE}} |
| 制造业PMI | {{PMI_VALUE}} | {{PMI_MONTH}} | {{PMI_TREND}} | {{PMI_NOTE}} |
| M2同比 | {{M2_VALUE}} | {{M2_MONTH}} | {{M2_TREND}} | {{M2_NOTE}} |
| 社融增量 | {{SH_RZGM_VALUE}} | {{SH_RZGM_MONTH}} | {{SH_RZGM_TREND}} | {{SH_RZGM_NOTE}} |
| LPR 1Y/5Y | {{LPR_1Y}}/{{LPR_5Y}} | {{LPR_DATE}} | — | — |
| USD/CNY | {{USDCNY_VALUE}} | {{USDCNY_DATE}} | {{USDCNY_TREND}} | — |

### 1.2 全球宏观环境

| 指标 | 最新值 | 说明 |
|------|:------:|------|
| 美联储基准利率 | {{FED_RATE}} | {{FED_NOTE}} |
| 美国CPI同比 | {{US_CPI}} | {{US_CPI_NOTE}} |
| 美10年期国债收益率 | {{US10Y}} | {{US10Y_NOTE}} |
| 美元指数DXY | {{DXY}} | {{DXY_NOTE}} |
| 标普500 | {{SP500}} | {{SP500_NOTE}} |
| 恒生指数 | {{HSI}} | {{HSI_NOTE}} |
| WTI原油 | {{WTI}} | {{WTI_NOTE}} |
| COMEX黄金 | {{GOLD}} | {{GOLD_NOTE}} |

### 1.3 宏观环境六维判断

| 维度 | 判断 | 置信度 | 关键指标 |
|------|:----:|:------:|---------|
| 经济增长动能 | {{ECON_GROWTH}} | {{ECON_GROWTH_CONF}} | GDP、PMI |
| 通胀压力 | {{INFLATION}} | {{INFLATION_CONF}} | CPI、PPI |
| 货币政策取向 | {{MONETARY}} | {{MONETARY_CONF}} | LPR、MLF |
| 流动性环境 | {{LIQUIDITY}} | {{LIQUIDITY_CONF}} | M2、社融 |
| 外部需求 | {{EXTERNAL}} | {{EXTERNAL_CONF}} | 出口、全球PMI |
| 风险偏好 | {{RISK_APPETITE}} | {{RISK_APPETITE_CONF}} | 汇率、外资流向 |

---

## 二、大类资产趋势

### 2.1 战略配置权重

| 资产类别 | 建议权重 | 较上期 | 趋势 | 置信度 | 核心逻辑 |
|----------|:-------:|:------:|:----:|:------:|---------|
| 债券 | {{BOND_WEIGHT}} | {{BOND_CHANGE}} | {{BOND_TREND}} | {{BOND_CONF}} | {{BOND_LOGIC}} |
| 现金及货币 | {{CASH_WEIGHT}} | {{CASH_CHANGE}} | {{CASH_TREND}} | {{CASH_CONF}} | {{CASH_LOGIC}} |
| 商品 | {{COMMODITY_WEIGHT}} | {{COMMODITY_CHANGE}} | {{COMMODITY_TREND}} | {{COMMODITY_CONF}} | {{COMMODITY_LOGIC}} |
| 股票及基金 | {{STOCK_WEIGHT}} | {{STOCK_CHANGE}} | {{STOCK_TREND}} | {{STOCK_CONF}} | {{STOCK_LOGIC}} |
| **合计** | 100% | | | | |

---

## 三、重点行业分析

### 3.1 行业筛选结果

| 行业 | 近20日涨跌 | 资金评分 | 政策评分 | 综合评分 | 趋势 |
|------|:---------:|:------:|:------:|:------:|:----:|
{{INDUSTRY_SCORES}}

### 3.2 上升行业详细分析

{{UP_INDUSTRY_DETAILS}}

### 3.3 下降行业详细分析

{{DOWN_INDUSTRY_DETAILS}}

---

## 四、品种操作建议

### 4.1 债券配置

{{BOND_DETAIL}}

### 4.2 股票及基金配置

#### A股标的

{{STOCK_A_DETAIL}}

#### 港股通标的

{{STOCK_HK_DETAIL}}

#### ETF/行业基金

{{ETF_DETAIL}}

#### QDII跨境基金

{{QDII_DETAIL}}

### 4.3 商品配置

{{COMMODITY_DETAIL}}

---

## 五、期货期权策略

### 5.1 国债期货

| 品种 | 方向 | 合约 | 建议仓位 | 止损参考 | 逻辑 |
|------|:---:|------|:------:|:------:|------|
{{BOND_FUTURES}}

### 5.2 商品期货

| 品种 | 方向 | 主力合约 | 最新价 | 建议仓位 | 止损参考 | 关联行业 |
|------|:---:|---------|:------:|:------:|:------:|---------|
{{COMMODITY_FUTURES}}

### 5.3 股指期货

| 品种 | 方向 | 合约 | 建议仓位 | 逻辑 |
|------|:---:|------|:------:|------|
{{INDEX_FUTURES}}

### 5.4 股指/ETF期权

| 标的 | 策略 | 方向 | 行权价 | 到期月 | 逻辑 |
|------|------|:---:|:------:|:------:|------|
{{ETF_OPTIONS}}

### 5.5 商品期权

| 品种 | 策略 | 方向 | 行权价 | 到期月 | 逻辑 |
|------|------|:---:|:------:|:------:|------|
{{COMMODITY_OPTIONS}}

---

## 六、风险提示与免责声明

### 宏观风险
{{MACRO_RISKS}}

### 行业特定风险
{{INDUSTRY_RISKS}}

### 衍生品杠杆风险
{{DERIVATIVES_RISKS}}

---

**免责声明**：本报告由 AI 基于公开市场数据和宏观经济指标自动生成，仅供投资研究参考，不构成任何投资建议或承诺。宏观经济数据可能存在滞后性，行业趋势分析基于历史数据，过去表现不代表未来收益。期货期权属于杠杆交易工具，存在较大亏损风险。投资者应审慎决策，自行承担投资风险。
