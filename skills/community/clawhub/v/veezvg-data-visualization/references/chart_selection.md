# 图表选择指南

根据数据类型智能选择最合适的图表类型。

## 选择规则表

| No. | 数据类型 | 关键词 | 推荐图表 | 备选图表 |
|-----|---------|--------|---------|---------|
| 1 | 趋势数据 | trend, time-series, line, growth, timeline, progress | Line Chart | Area Chart, Smooth Area |
| 2 | 类别比较 | compare, categories, bar, comparison, ranking | Bar Chart (Horizontal/Vertical) | Column Chart, Grouped Bar |
| 3 | 占比数据 | part-to-whole, pie, donut, percentage, proportion, share | Pie Chart / Donut | Stacked Bar, Treemap |
| 4 | 相关性/分布 | correlation, distribution, scatter, relationship, pattern | Scatter Plot / Bubble Chart | Heat Map, Matrix |
| 5 | 热力图/强度 | heatmap, heat-map, intensity, density, matrix | Heat Map / Choropleth | Grid Heat Map, Bubble Heat |
| 6 | 地理数据 | geographic, map, location, region, geo, spatial | Choropleth Map, Bubble Map | Geographic Heat Map |
| 7 | 漏斗/流程 | funnel, flow | Funnel Chart, Sankey | Waterfall |
| 8 | 绩效 vs 目标 | performance, target | Gauge Chart / Bullet Chart | Dial, Thermometer |
| 9 | 时序预测 | time-series, forecast | Line with Confidence Band | Ribbon Chart |
| 10 | 异常检测 | anomaly, detection | Line Chart with Highlights | Scatter with Alert |
| 11 | 层级/嵌套数据 | hierarchical, nested, data | Treemap | Sunburst, Nested Donut, Icicle |
| 12 | 流程数据 | flow, process, data | Sankey Diagram | Alluvial, Chord Diagram |
| 13 | 累计变化 | cumulative, changes | Waterfall Chart | Stacked Bar, Cascade |
| 14 | 多变量比较 | multi-variable, comparison | Radar / Spider Chart | Parallel Coordinates, Grouped Bar |
| 15 | 股票/交易 OHLC | stock, trading, ohlc | Candlestick Chart | OHLC Bar, Heikin-Ashi |
| 16 | 关系/连接数据 | relationship, connection, data | Network Graph | Hierarchical Tree, Adjacency Matrix |
| 17 | 分布/统计 | distribution, statistical | Box Plot | Violin Plot, Beeswarm |
| 18 | 绩效目标(紧凑) | performance, target, compact | Bullet Chart | Gauge, Progress Bar |
| 19 | 比例/百分比 | proportional, percentage | Waffle Chart | Pictogram, Stacked Bar 100% |
| 20 | 层级比例 | hierarchical, proportional | Sunburst Chart | Treemap, Icicle, Circle Packing |
| 21 | 根因分析 | root cause, decomposition, tree, hierarchy, drill-down, ai-split | Decomposition Tree | Decision Tree, Flow Chart |
| 22 | 3D 空间数据 | 3d, spatial, immersive, terrain, molecular, volumetric | 3D Scatter / Surface Plot | Volumetric Rendering, Point Cloud |
| 23 | 实时流数据 | streaming, real-time, ticker, live, velocity, pulse | Streaming Area Chart | Ticker Tape, Moving Gauge |
| 24 | 情感/情绪 | sentiment, emotion, nlp, opinion, feeling | Word Cloud with Sentiment | Sentiment Arc, Radar Chart |
| 25 | 流程挖掘 | process, mining, variants, path, bottleneck, log | Process Map / Graph | DAG, Petri Net |

## 使用方法

1. **识别数据类型**：根据数据特征和分析目的确定数据类型
2. **匹配关键词**：查找与需求匹配的关键词
3. **选择图表**：优先使用「推荐图表」，特殊情况可使用「备选图表」
4. **应用规范**：按 `guidelines/visualization_spec.md` 中的规范生成图表

## 常用场景速查

### 展示趋势变化
→ **Line Chart** (折线图)

### 比较不同类别
→ **Bar Chart** (柱状图)

### 展示占比分布
→ **Pie/Donut** (饼图/环形图) - 限5项以内
→ **Stacked Bar** (堆叠柱状图) - 超过5项时使用

### 展示相关性
→ **Scatter Plot** (散点图)

### 展示层级结构
→ **Treemap** (矩形树图)
