---
name: stock-summary
description: "Query stock quotes and technical analysis. Triggers on phrases like 查股价, 看股票, 帮我分析XX股票, XX走势. Input: stock code (A-share like 600519, HK like 00700, US like AAPL). Output: real-time quote, RSI/MACD indicators, buy/sell/hold signal, and a trend chart image."
---

# Stock Summary Skill

## Usage

When user provides a stock code, run `stock_summary.py` and present the results.

## Supported Markets

| Market | Input Format | Example |
|--------|-------------|---------|
| A股 | 6-digit code | `600519` (茅台) |
| 港股 | 5-digit code | `00700` (腾讯) |
| 美股 | Alphabet code | `AAPL`, `TSLA` |

## Output Format

### Text Section
```
📈 {股票名称}（{代码}）当日行情

【实时行情】
├ 现价：{价格}
├ 涨跌：{涨跌额}（{涨跌幅%}）
├ 开盘：{开盘价}
├ 最高：{最高价}
├ 最低：{最低价}
└ 成交量：{成交量}

【技术分析】
├ RSI(14)：{值} → 🟢超卖 / 🔴超买 / 🟡正常
├ MACD：DIF={值}, DEA={值}, MACD={值} → ⚔️金叉 / ⚔️死叉
└ 成交量变化：较昨日 {放量+/缩放-} {百分比}%

【综合信号】🟢买入 / 🔴卖出 / 🟡持有
理由：{分析理由}
```

### Chart Section
Generate a 1-month trend chart with MA5 and MA10 lines. Save to `stock_chart.png` and send as image.

## Technical Indicators

| Signal | Condition |
|--------|-----------|
| 🟢 买入 | RSI < 30 AND MACD 金叉 |
| 🔴 卖出 | RSI > 70 AND MACD 死叉 |
| 🟡 持有 | 其他情况 |

## Script Execution

```bash
python3 scripts/stock_summary.py <stock_code>
```

Example:
```bash
python3 scripts/stock_summary.py 600519
python3 scripts/stock_summary.py 00700
python3 scripts/stock_summary.py AAPL
```

## Data Sources

- A股: East Money API (无需API key)
- 港股/美股: Yahoo Finance (yfinance库)
