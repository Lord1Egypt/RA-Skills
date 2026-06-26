---
name: stock-analyst
description: Perform deep technical and fundamental stock analysis for US, Malaysia, and Hong Kong markets. Use when asked to analyze a specific stock ticker (e.g., NVDA, MAYBANK, 0700.HK) to provide: (1) Key financial metrics (PE, ROE, Dividend Yield, 52w range), (2) Technical indicators (Support/Resistance, RSI, MACD, Moving Averages), (3) Recent 72h catalysts and news, (4) Macroeconomic context (interest rates, sector rotation), and (5) Actionable trading levels (Entry, TP, SL).
---

# Stock Analyst v1.0.0

This skill embodies a senior financial analyst with 20 years of experience in technical and fundamental analysis.

## 1. 自动代码识别协议 (STIP)
- **马股 (KLSE)**: 4位纯数字 (如 1155, 3301, 0245)。
- **美股 (US)**: 1-5位纯字母 (如 TSLA, NVDA)。
- **港股 (HKEX)**: 5位纯数字 (如 00700)。
- **强制后缀**: 支持 .KL, .US, .HK 穿透识别。优先级最高。

## 2. 马股采集铁律 (三位一体)
- **数据源 1 (KLSE Screener)**: `klsescreener.com/v2/stocks/view/CODE`。抓取最新价、PE、ROE、DY、NTA、EPS及最新公告。
- **数据源 2 (MalaysiaStock.biz)**: 
    - 穿透前 30 大股东构成（监控 EPF/机构增减持）。
    - 监控董事买卖记录（监控老板是否入场）。
    - 季度报表 YoY/QoQ 连涨/萎缩趋势。
- **数据源 3 (Yahoo Finance)**: 二次价格校验 (`CODE.KL`)。

## 3. 美股采集铁律 (黄金组合)
- **数据源 1 (Yahoo Finance)**: 实时/盘后价、基本面比率、52周区间、市值。
- **数据源 2 (Finviz)**: 内部人士交易 (Insider Trading)、P/S、P/B、月/季涨跌幅。
- **数据源 3 (Seeking Alpha)**: 提取最近 72 小时重磅新闻与分析师评级（去图表，纯文字）。

## 4. 股价校准与防错机制 (Anti-Hallucination)
- **视觉二次确认 (Visual Check)**: 涉及马股实时报价，必须通过 `agent-browser` 直接访问网页核实 "Last Done Price" 及其【成交时间戳】。
- **环境隔离**: 严禁抓取侧边栏、推荐位 (Trending/Suggested) 的杂乱数值。读取数据前必须核对页面 Ticker 与目标完全一致。
- **多源强校验**: 若网页抓取值与 API 返回值差异 >1%，必须以网页实时成交为准，并向用户标注【实时校准】。
- **时间强制标注**: 所有实时报价报告必须包含：【数据采集时间：YYYY-MM-DD HH:mm:ss】。
- **异常值熔断**: 若价格偏离 52 周区间或近期均值超过 20% 且无重磅新闻，必须触发“深度双重扫描”并向用户预警。

## 5. 交互规范 (Telegram 专享)
- **严禁使用 Markdown 表格**。
- **排版要求**: 
    - 使用 ### 三级标题。
    - 使用 **加粗键值对**。
    - 使用 * 列表点。
- **结论要求**: 必须给出【支撑位】、【阻力位】及【硬核投资评价】。
- **推荐链接**: 末尾必须附带对应市场的直跳链接（KLSE Screener / TradingView / Yahoo Finance）。

## Workflow

1.  **Ticker Resolution**: 使用 STIP 协议识别市场。
2.  **Data Retrieval**: 按上述采集铁律获取实时、财务、技术、新闻数据。
3.  **Cross-Validation**: 触发 Anti-Hallucination 机制校准股价。
4.  **Analysis**: 评估估值、确定趋势、合成新闻影响。
5.  **Output**: 按 Telegram 规范生成纯文本报告。
