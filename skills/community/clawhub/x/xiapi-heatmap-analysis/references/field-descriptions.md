# 字段说明

## 热力图数据字段（sector heatmap）

### 历史序列数据

| 字段名 | 类型 | 说明 |
|---|---|---|
| csHeatmap | string | 近5个交易日各行业 CS 值，每个数值后带 ↑↓ 标注当日相对前一日的变化方向 |
| zdfHeatmap | string | 近5个交易日各行业当日涨跌幅（%），带 ↑↓ 方向 |
| zdf5Heatmap | string | 近5个交易日各行业5日涨跌幅（%），带 ↑↓ 方向 |

### 预处理分类数据

| 字段名 | 类型 | 说明 |
|---|---|---|
| cs_gt_5_names | array | 今日 CS > 5 的行业列表，领涨候选 |
| cs_gt_ma20_names | array | 今日 CS > CS_MA20 的行业列表，均线上方 |
| yest_cs_gt_ma20Names | array | 昨日 CS > CS_MA20 的行业列表，用于热度扩散对比 |
| cs_crossover_ma20_names | array | 今日新突破 CS_MA20 的行业（昨日不在、今日在），即刚刚金叉的行业 |
| cs_crossover_5_names | array | 今日 CS 新突破 +5 的行业 |
| crossover | string | 今日板块内突破箱体股票较多的板块描述 |
| total | number | 行业总数 |

### 行业内个股字段（sector top）

| 字段名 | 类型 | 说明 |
|---|---|---|
| sector | string | 所属板块 |
| stock_name | string | 股票名称 |
| stock_code | string | 股票代码 |
| change | number | 涨跌幅（%） |

## 概念板块数据字段（sector gn）

| 字段名 | 类型 | 说明 |
|---|---|---|
| concept | string | 概念板块名称 |
| change | number | 涨跌幅（%） |
| top_stock | string | 领涨股名称 |
| top_code | string | 领涨股代码 |

## 名词解释

### CS 值（EMA20乖离率）

收盘价与 EMA20（20日指数移动平均线）的乖离率，用于衡量板块短期强度。

- CS > 0：价格在 EMA20 上方，短期偏强
- CS < 0：价格在 EMA20 下方，短期偏弱

**CS 阈值参考**：

| CS 范围 | 状态 | 操作建议 |
|---|---|---|
| > 15 | 过热 | 不追高 |
| 5–15 | 领涨 | 可考虑入场 |
| 0–5 | 正常 | 关注 |
| -5–0 | 偏弱 | 观望 |
| < -5 | 深度偏弱 | 建议离场或观望 |

### CS_MA20（CS 20日均线）

CS 值的20日移动平均线。CS 上穿 CS_MA20（即出现在 cs_crossover_ma20_names 中）是上升信号，CS 下穿 CS_MA20 是走弱信号。

### ↑↓ 方向标注

csHeatmap、zdfHeatmap、zdf5Heatmap 中每个数值后的箭头，表示该数值相对前一交易日的变化方向。连续多日 ↑ 表示持续上升趋势。

## 数据更新时间

所有数据每日收盘后更新，一般在17:00前完成。
